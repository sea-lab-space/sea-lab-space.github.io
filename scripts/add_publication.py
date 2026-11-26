#!/usr/bin/env python3
"""Add one publication to the site, the way README.md describes doing by hand.

Given one BibTeX entry (or a DOI or arXiv link to look the entry up), it:
  1. checks the entry (title, author, year, and a doi or url),
  2. sets the citation key to lastname_firstword_year,
  3. stops if the paper is already in sea-lab-publication.bib,
  4. rewrites lab members' names to the spelling that links to their profile,
  5. creates content/publication/<folder>/ with the same import tool the
     import Action uses (academic 0.10.0, never with --overwrite),
  6. writes the research directions into the new index.md,
  7. appends the entry to sea-lab-publication.bib.

Nothing is written until every check has passed. It does not commit.

The Slack bot's workflow (.github/workflows/slack-add-publication.yml) runs
this script. You can run it yourself too, from the repo root, with the Python
environment from "Local Test" in README.md:

    python3 scripts/add_publication.py paper.bib -d personal-health-agents
    echo 10.1145/3613904.3642000 | python3 scripts/add_publication.py - -d beyond-health

`--merge-bib` is a separate mode for the bot's approval workflow. See
merge_bib() below.
"""

import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_author_links import flip, loose_key, strict_key  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "sea-lab-publication.bib"
PUBS = ROOT / "content" / "publication"
AUTHORS = ROOT / "content" / "authors"
DIRECTIONS_FILE = ROOT / "data" / "research_directions.yaml"
SHEET = ROOT / "processing" / "Lab Collaboration Track Record - Person-Pub.csv"

# Left out of the group bib: `file` holds a path on someone's computer, and
# `keywords` would become `tags`, which no paper on the site uses.
DROPPED_FIELDS = ("file", "keywords")
ARTICLES = {"a", "an", "the"}
DOI = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)", re.I)
ARXIV = re.compile(r"arxiv(?:\.org/(?:abs|pdf)/|:)\s*(\d{4}\.\d{4,5})", re.I)
BARE_MONTH = re.compile(r"(\bmonth\s*=\s*)([A-Za-z]+)(\s*[,}])", re.I)
# Where an entry starts in a .bib file: "@type{key," at the start of a line.
ENTRY_START = re.compile(r"^@\w+\s*\{\s*([^,\s]+)\s*,", re.M)


class UserError(Exception):
    """A problem the person who asked for the paper can fix. Shown to them."""


# ---------------------------------------------------------------- reading

def bib_parser(to_unicode=False):
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    if to_unicode:
        parser.customization = convert_to_unicode
    return parser


def fetch_bibtex(doi):
    request = urllib.request.Request(
        "https://doi.org/" + doi,
        headers={"Accept": "application/x-bibtex", "User-Agent": "sea-lab-website-bot"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as error:
        raise UserError(
            f"I could not look up the DOI {doi} ({error}). Check it, or paste "
            "the paper's BibTeX instead."
        ) from error


def read_entry(text):
    """Return (entry, doi_it_was_looked_up_by). `entry` keeps LaTeX as typed."""
    import bibtexparser

    # People paste from Slack code blocks.
    text = text.strip().strip("`").strip()
    if not text:
        raise UserError("The request was empty. Paste one BibTeX entry or a DOI.")

    looked_up = None
    if not text.startswith("@"):
        arxiv = ARXIV.search(text)
        doi = DOI.search(text)
        if arxiv:
            looked_up = "10.48550/arXiv." + arxiv.group(1)
        elif doi:
            looked_up = doi.group(1).rstrip(".,;)")
        else:
            raise UserError(
                "That is neither a BibTeX entry (it should start with @) nor a "
                "DOI such as 10.1145/3613904.3642000."
            )
        text = fetch_bibtex(looked_up)

    # doi.org writes months as bare words (month=June, month=Sept), which the
    # parser takes for undefined abbreviations and stops on.
    text = BARE_MONTH.sub(r"\1{\2}\3", text)
    try:
        entries = bibtexparser.loads(text, parser=bib_parser()).entries
    except Exception as error:  # bibtexparser raises several kinds
        raise UserError(f"I could not read that BibTeX: {error}") from error
    if len(entries) != 1:
        raise UserError(
            f"I found {len(entries)} BibTeX entries. Send exactly one paper per "
            "request. If you sent one, check its braces and commas."
        )
    return entries[0], looked_up


def plain(value):
    """A BibTeX value as plain text: no braces, LaTeX accents or line breaks."""
    from bibtexparser.latexenc import latex_to_unicode

    return re.sub(r"\s+", " ", latex_to_unicode(value).replace("{", "").replace("}", "")).strip()


def split_authors(value):
    return [a.strip() for a in re.split(r"\s+and\s+", value.replace("\n", " ")) if a.strip()]


# ----------------------------------------------------------- checks, key

def check_fields(entry):
    for field in ("title", "author"):
        if not entry.get(field, "").strip():
            raise UserError(f"The BibTeX entry has no `{field}`.")
    if not entry.get("year") and re.match(r"\d{4}", entry.get("date", "")):
        entry["year"] = entry["date"][:4]
    if not re.fullmatch(r"\d{4}", entry.get("year", "").strip()):
        raise UserError("The BibTeX entry needs a four-digit `year`.")
    entry["year"] = entry["year"].strip()
    arxiv = entry.get("archiveprefix", "").lower() == "arxiv" and entry.get("eprint")
    if not (entry.get("doi") or entry.get("url") or arxiv):
        raise UserError(
            "The BibTeX entry needs a `doi` or a `url`, so that a click on the "
            "paper opens it."
        )


def ascii_slug(text, keep=""):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return "".join(c for c in text.lower() if (c.isascii() and c.isalnum()) or c in keep)


def make_key(entry):
    """lastname_firstword_year, as README.md asks for ('zou_mind_2026')."""
    first_author = plain(split_authors(entry["author"])[0])
    if "," in first_author:
        last_name = first_author.split(",", 1)[0]
    else:
        last_name = first_author.split()[-1]
    words = [ascii_slug(w, keep="-").strip("-") for w in plain(entry["title"]).split()]
    words = [w for w in words if w]
    while len(words) > 1 and words[0] in ARTICLES:
        words.pop(0)
    last_name = ascii_slug(last_name)
    if not last_name or not words:
        raise UserError("I could not build a citation key from the first author and title.")
    return f"{last_name}_{words[0]}_{entry['year']}"


def title_key(title):
    return ascii_slug(plain(title))


def check_not_duplicate(entry, folder):
    import bibtexparser

    with BIB.open(encoding="utf-8") as fh:
        existing = bibtexparser.load(fh, parser=bib_parser()).entries
    doi = entry.get("doi", "").strip().lower()
    for other in existing:
        same_doi = doi and other.get("doi", "").strip().lower() == doi
        same_title = title_key(other.get("title", "")) == title_key(entry["title"])
        if same_doi or same_title or other["ID"] == entry["ID"]:
            raise UserError(
                f"This paper looks like one already on the site: `{other['ID']}` "
                f"({plain(other.get('title', ''))}). To change a paper that is "
                "already listed, ask a website admin."
            )
    if (PUBS / folder).exists():
        raise UserError(
            f"content/publication/{folder}/ already exists, so this paper may "
            "already be on the site. Ask a website admin."
        )


def check_directions(directions):
    data = yaml.safe_load(DIRECTIONS_FILE.read_text(encoding="utf-8"))
    known = [d["id"] for d in data["directions"]]
    if not directions:
        raise UserError("Pick at least one research direction.")
    unknown = [d for d in directions if d not in known]
    if unknown:
        raise UserError(
            f"Unknown research direction: {', '.join(unknown)}. "
            f"Use ids from data/research_directions.yaml: {', '.join(known)}."
        )
    return list(dict.fromkeys(directions))


# ---------------------------------------------------------- author names

def canonical_names():
    """Other spellings of a name -> the spelling the site links.

    The same rules as scripts/check_author_links.py, plus the collaborator
    aliases that processing/bib_post_processing.py applies.
    """
    folders = [d.name for d in AUTHORS.iterdir() if d.is_dir() and d.name != "0-author-template"]
    by_alias, by_loose = {}, {}
    for folder in folders:
        by_loose[loose_key(folder.replace("-", " "))] = " ".join(
            w.capitalize() for w in folder.split("-")
        )
    if SHEET.exists():
        with SHEET.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                full_name = (row.get("Full Name") or "").strip()
                if not full_name:
                    continue
                if strict_key(full_name) in folders:
                    full_name = by_loose[loose_key(full_name)]
                for alias in (row.get("Alias") or "").split(";"):
                    if alias.strip():
                        by_alias[flip(alias).lower()] = full_name
    return set(folders), by_alias, by_loose


def fix_author_names(entry):
    folders, by_alias, by_loose = canonical_names()
    fixed = []
    for author in split_authors(entry["author"]):
        name = flip(plain(author))
        if strict_key(name) in folders:
            fixed.append(author)
            continue
        target = by_alias.get(name.lower()) or by_loose.get(loose_key(name))
        if target and target != name:
            first, last = target.rsplit(" ", 1)
            fixed.append(f"{last}, {first}")
        else:
            fixed.append(author)
    entry["author"] = " and ".join(fixed)


# ---------------------------------------------------------------- writing

def format_entry(entry):
    """One entry in the layout the group bib already uses."""
    from bibtexparser.bibdatabase import BibDatabase
    from bibtexparser.bwriter import BibTexWriter

    database = BibDatabase()
    database.entries = [entry]
    writer = BibTexWriter()
    writer.indent = " "
    return writer.write(database).strip() + "\n"


def import_entry(entry_text, folder):
    """Create content/publication/<folder>/ with the import tool."""
    with tempfile.TemporaryDirectory() as tmp:
        one_entry = Path(tmp) / "new.bib"
        one_entry.write_text(entry_text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-m", "academic.cli", "import", str(one_entry), str(PUBS), "--compact"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    page = PUBS / folder / "index.md"
    if result.returncode != 0 or not page.exists():
        raise RuntimeError(
            f"The import tool did not create {page}.\n{result.stdout}\n{result.stderr}"
        )
    return page


def add_directions(page, directions):
    text = page.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?\n)---[ \t]*\n?", text, re.S)
    if not match:
        raise RuntimeError(f"{page} has no front matter.")
    block = "directions:\n" + "".join(f"  - {d}\n" for d in directions)
    page.write_text(
        "---\n" + match.group(1) + block + "---\n" + text[match.end():], encoding="utf-8"
    )


def append_to_bib(entry_text):
    text = BIB.read_text(encoding="utf-8")
    BIB.write_text(text.rstrip("\n") + "\n\n" + entry_text, encoding="utf-8")


def summarize(page, key, directions, looked_up):
    front = yaml.safe_load(page.read_text(encoding="utf-8").split("---")[1])
    data = yaml.safe_load(DIRECTIONS_FILE.read_text(encoding="utf-8"))
    titles = {d["id"]: d["title"] for d in data["directions"]}
    link = ""
    for item in front.get("links") or []:
        if item.get("name") == "URL":
            link = item.get("url", "")
    if not link and front.get("doi"):
        link = "https://doi.org/" + front["doi"]
    if not link:
        link = front.get("url_pdf") or next(
            (i.get("url", "") for i in front.get("links") or []), ""
        )
    return {
        "ok": True,
        "key": key,
        "folder": page.parent.name,
        "title": front.get("title", ""),
        "authors": front.get("authors") or [],
        "venue": (front.get("publication") or "").strip("*"),
        "date": str(front.get("date", "")),
        "type": (front.get("publication_types") or [""])[0],
        "link": link,
        "has_abstract": bool(front.get("abstract")),
        "directions": directions,
        "direction_titles": [titles[d] for d in directions],
        "looked_up_doi": looked_up,
    }


def add_publication(text, directions, abstract=""):
    from academic.import_bibtex import slugify

    directions = check_directions(directions)
    entry, looked_up = read_entry(text)
    check_fields(entry)
    for field in DROPPED_FIELDS:
        entry.pop(field, None)
    abstract = " ".join(abstract.split())
    if abstract and not entry.get("abstract", "").strip():
        entry["abstract"] = abstract.replace("{", "").replace("}", "")
    entry["ID"] = make_key(entry)
    folder = slugify(entry["ID"])
    check_not_duplicate(entry, folder)
    fix_author_names(entry)

    entry_text = format_entry(entry)
    page = import_entry(entry_text, folder)
    add_directions(page, directions)
    append_to_bib(entry_text)
    return summarize(page, entry["ID"], directions, looked_up)


# ------------------------------------------------- merging two bib files

def split_entries(text):
    """{key: entry text} for a .bib file, in file order."""
    starts = [(m.start(), m.group(1)) for m in ENTRY_START.finditer(text)]
    entries = {}
    for (start, key), (end, _) in zip(starts, starts[1:] + [(len(text), None)]):
        entries[key] = text[start:end].strip() + "\n"
    return entries


def merge_bib(main_text, branch_text):
    """The group bib after merging a bot branch: main's file plus the entries
    only the branch has.

    Every bot branch appends its paper at the end of the bib, so two papers
    waiting for approval at the same time always conflict there. git cannot
    settle that on its own, and the answer is always "keep both".
    """
    merged = main_text.rstrip("\n") + "\n"
    present = split_entries(main_text)
    for key, entry in split_entries(branch_text).items():
        if key not in present:
            merged += "\n" + entry
    return merged


# -------------------------------------------------------------------- cli

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("source", nargs="?", help="file with one BibTeX entry or a DOI, or - for stdin")
    parser.add_argument("-d", "--directions", default="", help="direction ids, comma-separated, main one first")
    parser.add_argument("--abstract-file", help="file with the abstract, used when the entry has none")
    parser.add_argument("--summary", help="write the result here as JSON")
    parser.add_argument(
        "--merge-bib",
        nargs=2,
        metavar=("MAIN", "BRANCH"),
        help="print MAIN's bib plus the entries only BRANCH has, and stop",
    )
    args = parser.parse_args()

    if args.merge_bib:
        main_file, branch_file = (Path(p).read_text(encoding="utf-8") for p in args.merge_bib)
        sys.stdout.write(merge_bib(main_file, branch_file))
        return 0
    if not args.source:
        parser.error("source is required")

    text = sys.stdin.read() if args.source == "-" else Path(args.source).read_text(encoding="utf-8")
    abstract = Path(args.abstract_file).read_text(encoding="utf-8") if args.abstract_file else ""
    directions = [d.strip() for d in args.directions.split(",") if d.strip()]
    try:
        summary = add_publication(text, directions, abstract)
        code = 0
        print(f"Added {summary['key']} as content/publication/{summary['folder']}/")
        print(f"  {summary['title']}")
        print("Review the new folder and the end of sea-lab-publication.bib, then commit.")
    except UserError as error:
        summary = {"ok": False, "error": str(error)}
        code = 2
        print(f"Not added: {error}", file=sys.stderr)
    if args.summary:
        Path(args.summary).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
