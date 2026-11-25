#!/usr/bin/env python3
"""Fail the build when a publication is not filed under a research direction.

How the site decides "which paper goes where":
  * data/research_directions.yaml lists the lab's research directions. It is
    the single source of truth for the Research page, the Publications page
    filters, and this check. A direction with `hidden: true` never shows on
    the Research page or as a filter chip, but its papers still appear on the
    Publications page under "All".
  * Every content/publication/<folder>/index.md picks one or more of those
    directions in its front matter:

      directions:                   # required, one or more ids from the YAML
        - personal-health-agents
      selected: true                # optional, show it on the Research page
      highlight: personal-health-agents   # optional, a top card there
      highlight_rank: 1             # optional, order among those cards
      authors_display: "Rui Yang et al."  # optional, short author line

  * `selected`, `highlight` and `highlight_rank` are Orson's decisions. Each
    visible direction shows at most 4 highlight cards. When more papers than
    that name the same highlight, the 4 most recent by `date` show, ordered by
    `highlight_rank` (unranked cards last, newest first).

Fails (exit 1) when:
  1. data/research_directions.yaml is broken: a direction without `id`,
     `title`, `short_title`, `description` or `definition`, a repeated id, an
     id that is not a lowercase-dash slug, or a field of the wrong type.
  2. A publication has no `directions`, or an empty list.
  3. A publication names a direction id that is not in the YAML.
  4. A publication still carries one of the legacy research tags
     ('health prediction', 'intelligent interaction and intervention',
     'clinical support').
  5. `highlight` is not one of the paper's own `directions`.
  6. `highlight_rank` is set without `highlight`.
  7. Two papers share a `highlight_rank` within the same direction.
  8. A field has the wrong type: `directions` must be a list of strings,
     `selected` true or false, `highlight` and `authors_display` strings, and
     `highlight_rank` a whole number from 1 up.

Warns (printed, but the check still passes) when:
  * a visible direction has more than 4 highlights (it names the 4 that show),
  * a visible direction has no highlights at all,
  * a highlighted paper has no featured image (featured.png or similar) in
    its folder, so its Research card shows a plain placeholder.

New folders from the bib-import pull request have no `directions` yet, so
they fail this check until someone adds them. That is intended: the lab
decides where every paper belongs before it goes live.

Run from the repo root:  python scripts/check_publication_directions.py
"""

import difflib
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DIRECTIONS_FILE = ROOT / "data" / "research_directions.yaml"
PUBS = ROOT / "content" / "publication"
MEDIA = ROOT / "assets" / "media"

REQUIRED_DIRECTION_FIELDS = ("id", "title", "short_title", "description", "definition")
LEGACY_TAGS = {"health prediction", "intelligent interaction and intervention", "clinical support"}
MAX_HIGHLIGHTS = 4
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff", ".bmp"}
README_SECTION = "'Categorize a publication (required)' in README.md"


class Report:
    """Collects failures and warnings, each tied to the file it is about."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append((where, message))

    def warn(self, where, message):
        self.warnings.append((where, message))


def rel(path):
    return path.relative_to(ROOT).as_posix()


def front_matter(path):
    """The YAML between the leading '---' lines, or None if there is none."""
    # utf-8-sig drops a byte-order mark, which some Windows editors add and
    # Hugo ignores. An empty block ('---' twice) counts as front matter.
    text = path.read_text(encoding="utf-8-sig")
    m = re.match(r"---[ \t]*\r?\n(?:(.*?)\r?\n)?---[ \t]*(?:\r?\n|$)", text, re.S)
    if not m:
        return None
    return yaml.safe_load(m.group(1) or "") or {}


def type_name(value):
    if isinstance(value, bool):
        return "true/false"
    return {
        str: "text", int: "a number", float: "a decimal number", list: "a list",
        dict: "a mapping", type(None): "an empty value",
    }.get(type(value), type(value).__name__)


def is_int(value):
    # YAML reads `true` as a bool, and Python treats bools as ints. Rule them out.
    return isinstance(value, int) and not isinstance(value, bool)


def date_key(value):
    """Front-matter dates come in as text ('2024-05-01') or as date objects."""
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def has_featured_image(folder, fm):
    """Same lookup as the theme: a bundle file named *featured*, else image.filename."""
    for f in folder.iterdir():
        if f.is_file() and "featured" in f.name.lower() and f.suffix.lower() in IMAGE_SUFFIXES:
            return True
    image = fm.get("image")
    if isinstance(image, dict) and image.get("filename"):
        name = str(image["filename"])
        return (folder / name).is_file() or (MEDIA / name).is_file()
    return False


# ---- data/research_directions.yaml ---------------------------------------

def load_directions(report):
    """Validate the directions file. Returns {id: entry} in file order, or None."""
    where = rel(DIRECTIONS_FILE)
    if not DIRECTIONS_FILE.exists():
        report.error(where, "file not found. It must list the research directions.")
        return None
    try:
        data = yaml.safe_load(DIRECTIONS_FILE.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        report.error(where, f"is not valid YAML ({exc}).")
        return None
    if not isinstance(data, dict):
        report.error(where, "must be a mapping with a top-level 'directions:' list.")
        return None
    if "intro" in data and not isinstance(data["intro"], str):
        report.error(where, f"'intro' must be text, found {type_name(data['intro'])}.")

    entries = data.get("directions")
    if not isinstance(entries, list) or not entries:
        report.error(where, "'directions' must be a non-empty list of directions.")
        return None

    directions = {}
    numbers = {}
    for i, entry in enumerate(entries, 1):
        label = f"direction #{i}"
        if not isinstance(entry, dict):
            report.error(where, f"{label} must be a mapping of fields, found {type_name(entry)}.")
            continue
        if isinstance(entry.get("id"), str) and entry["id"].strip():
            label = f"direction '{entry['id']}'"

        for field in REQUIRED_DIRECTION_FIELDS:
            value = entry.get(field)
            if value is None:
                report.error(where, f"{label} is missing '{field}'.")
            elif not isinstance(value, str) or not value.strip():
                report.error(where, f"{label}: '{field}' must be non-empty text, "
                                    f"found {type_name(value)}.")
        if "hidden" in entry and not isinstance(entry["hidden"], bool):
            report.error(where, f"{label}: 'hidden' must be true or false, "
                                f"found {type_name(entry['hidden'])}.")
        if "number" in entry and not is_int(entry["number"]):
            report.error(where, f"{label}: 'number' must be a whole number, "
                                f"found {type_name(entry['number'])}.")

        did = entry.get("id")
        if not isinstance(did, str) or not did.strip():
            continue
        if not SLUG.match(did):
            report.error(where, f"{label}: the id must use only lowercase letters, digits "
                                f"and single dashes (it appears in page addresses such "
                                f"as /research/?direction=<id>).")
        if did in directions:
            report.error(where, f"{label}: the id is used by more than one direction.")
            continue
        directions[did] = entry

        if not entry.get("hidden") and is_int(entry.get("number")):
            numbers.setdefault(entry["number"], []).append(did)
        elif not entry.get("hidden"):
            report.warn(where, f"{label} is visible but has no 'number', so the Research "
                               f"page heading has no number.")

    for number, ids in sorted(numbers.items()):
        if len(ids) > 1:
            report.warn(where, f"visible directions {', '.join(ids)} share number {number}.")

    if directions and all(d.get("hidden") for d in directions.values()):
        report.error(where, "every direction is hidden, so the Research page would be empty.")
    return directions


# ---- content/publication/*/index.md --------------------------------------

def suggest(value, directions):
    """A 'did you mean' hint for a mistyped direction id."""
    lowered = value.strip().lower()
    for did, entry in directions.items():
        names = {str(entry.get("title", "")).lower(), str(entry.get("short_title", "")).lower()}
        if lowered in names or lowered.replace(" ", "-") == did:
            return f" Did you mean '{did}'?"
    close = difflib.get_close_matches(lowered, list(directions), n=1, cutoff=0.6)
    return f" Did you mean '{close[0]}'?" if close else ""


def check_publication(page, directions, report):
    """Check one paper. Returns its parsed fields for the cross-paper checks."""
    where = rel(page)
    try:
        fm = front_matter(page)
    except yaml.YAMLError as exc:
        report.error(where, f"the front matter is not valid YAML ({exc}).")
        return None
    if fm is None:
        report.error(where, "has no front matter (the '---' block at the top).")
        return None
    if not isinstance(fm, dict):
        report.error(where, "the front matter must be a set of 'key: value' fields.")
        return None

    paper = {"where": where, "folder": page.parent, "fm": fm, "date": date_key(fm.get("date")),
             "directions": [], "highlight": None, "rank": None}

    # 2, 3 and 8: directions
    dirs = fm.get("directions")
    if dirs is None or dirs == [] or dirs == "":
        report.error(where, "'directions' is missing or empty. Add a list of one or more "
                            "direction ids from data/research_directions.yaml, e.g.\n"
                            "        directions:\n"
                            "          - personal-health-agents")
    elif not isinstance(dirs, list):
        hint = ""
        if isinstance(dirs, str):
            hint = f" Write it as a list:\n        directions:\n          - {dirs.strip()}"
        report.error(where, f"'directions' must be a list of direction ids, "
                            f"found {type_name(dirs)}.{hint}")
    else:
        seen = set()
        for item in dirs:
            if not isinstance(item, str) or not item.strip():
                report.error(where, f"'directions' entries must be direction ids (text), "
                                    f"found {type_name(item)} ({item!r}).")
                continue
            if item not in directions:
                report.error(where, f"'directions' has '{item}', which is not an id in "
                                    f"data/research_directions.yaml.{suggest(item, directions)}")
                continue
            if item in seen:
                report.warn(where, f"'directions' lists '{item}' more than once.")
                continue
            seen.add(item)
            paper["directions"].append(item)

    # 4: legacy tags
    tags = fm.get("tags")
    tag_list = tags if isinstance(tags, list) else [tags] if isinstance(tags, str) else []
    for tag in tag_list:
        if isinstance(tag, str) and tag.strip().lower() in LEGACY_TAGS:
            report.error(where, f"'tags' still has the legacy research tag '{tag}'. The "
                                f"Research page no longer reads tags. Remove it (and the "
                                f"'tags:' key if nothing is left) and use 'directions'.")

    # 8: selected
    selected = fm.get("selected")
    if selected is not None and not isinstance(selected, bool):
        report.error(where, f"'selected' must be true or false, found {type_name(selected)} "
                            f"({selected!r}). Write it without quotes.")

    # 5 and 8: highlight
    highlight = fm.get("highlight")
    if highlight is not None:
        if not isinstance(highlight, str) or not highlight.strip():
            report.error(where, f"'highlight' must be one direction id (text), "
                                f"found {type_name(highlight)} ({highlight!r}).")
        elif highlight not in paper["directions"]:
            listed = ", ".join(paper["directions"]) or "none"
            report.error(where, f"'highlight' is '{highlight}', which is not one of this "
                                f"paper's 'directions' ({listed}). A paper can only be "
                                f"highlighted in a direction it belongs to.")
        else:
            paper["highlight"] = highlight
            if directions[highlight].get("hidden"):
                report.warn(where, f"'highlight' is '{highlight}', a hidden direction, so "
                                   f"the card never shows on the Research page.")
            if selected is False:
                report.warn(where, "'selected' is false but 'highlight' is set. A highlight "
                                   "is always treated as selected, so drop one of the two.")

    # 6 and 8: highlight_rank
    rank = fm.get("highlight_rank")
    if rank is not None:
        if not is_int(rank) or rank < 1:
            report.error(where, f"'highlight_rank' must be a whole number from 1 up, "
                                f"found {type_name(rank)} ({rank!r}). Write it without quotes.")
        elif highlight is None:
            report.error(where, "'highlight_rank' is set but 'highlight' is not. Add "
                                "'highlight: <direction id>' or remove the rank.")
        else:
            paper["rank"] = rank

    # 8: authors_display
    display = fm.get("authors_display")
    if display is not None and (not isinstance(display, str) or not display.strip()):
        report.error(where, f"'authors_display' must be non-empty text, e.g. "
                            f"\"Rui Yang et al.\", found {type_name(display)} ({display!r}).")

    return paper


def check_highlights(papers, directions, report):
    """Cross-paper rules: shared ranks (fail), and the 4-card overview (warn)."""
    by_direction = {did: [] for did in directions}
    for p in papers:
        if p["highlight"]:
            by_direction[p["highlight"]].append(p)

    for did, entry in directions.items():
        cards = by_direction[did]

        # 7: two papers with the same rank in one direction
        ranks = {}
        for p in cards:
            if p["rank"] is not None:
                ranks.setdefault(p["rank"], []).append(p)
        for rank, same in sorted(ranks.items()):
            if len(same) > 1:
                files = " and ".join(p["where"] for p in same)
                report.error(files, f"these papers share highlight_rank {rank} in '{did}'. "
                                    f"Give each highlight in a direction its own rank.")

        if entry.get("hidden"):
            continue
        where = rel(DIRECTIONS_FILE)
        if not cards:
            report.warn(where, f"visible direction '{did}' has no highlighted papers, so its "
                               f"Research overview shows no cards.")
            continue
        if len(cards) > MAX_HIGHLIGHTS:
            newest = sorted(cards, key=lambda p: (p["date"], p["folder"].name), reverse=True)
            hidden = newest[MAX_HIGHLIGHTS:]
            # Display order: ranked cards by rank, then unranked ones newest first.
            shown = sorted((p for p in newest[:MAX_HIGHLIGHTS] if p["rank"] is not None),
                           key=lambda p: p["rank"])
            shown += [p for p in newest[:MAX_HIGHLIGHTS] if p["rank"] is None]
            names = ", ".join(f"{p['folder'].name} ({'rank ' + str(p['rank']) if p['rank'] else 'unranked'})"
                              for p in shown)
            tie = ""
            if shown and hidden and min(p["date"] for p in shown) == hidden[0]["date"]:
                tie = " Some papers at the cut-off share a date, so which of them shows may vary."
            report.warn(where, f"visible direction '{did}' has {len(cards)} highlights, but "
                               f"only the {MAX_HIGHLIGHTS} most recent show: {names}. Not shown: "
                               f"{', '.join(p['folder'].name for p in hidden)}.{tie}")

        for p in cards:
            if not has_featured_image(p["folder"], p["fm"]):
                report.warn(p["where"], f"highlighted in '{did}' but has no featured image "
                                        f"(featured.png) in its folder, so its Research card "
                                        f"shows a placeholder.")


# ---- output --------------------------------------------------------------

def annotate(level, where, message):
    """On GitHub Actions, also pin the message to the file in the pull request."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    flat = " ".join(message.split())
    flat = flat.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    first = where.split(" and ")[0]
    if (ROOT / first).is_file():
        # The annotation already names the file, so only repeat it for pairs.
        text = flat if first == where else f"{where}: {flat}"
        print(f"::{level} file={first}::{text}")
    else:
        print(f"::{level}::{where}: {flat}")


def main():
    report = Report()
    directions = load_directions(report)

    pages = sorted(PUBS.glob("*/index.md"))
    papers = []
    if directions:
        for page in pages:
            paper = check_publication(page, directions, report)
            if paper:
                papers.append(paper)
        check_highlights(papers, directions, report)

    if report.warnings:
        print("Warnings (these do not fail the check):\n")
        for where, message in report.warnings:
            print(f"  - {where}: {message}")
        print()

    for where, message in report.warnings:
        annotate("warning", where, message)
    for where, message in report.errors:
        annotate("error", where, message)

    if report.errors:
        print("Publication directions check failed:\n")
        for where, message in report.errors:
            print(f"  - {where}: {message}")
        if directions:
            print("\nDirection ids you can use (read each 'definition' in "
                  "data/research_directions.yaml to choose):")
            for did, entry in directions.items():
                note = "   (hidden, for work outside health)" if entry.get("hidden") else ""
                print(f"    {did:<42} {entry.get('title', '')}{note}")
        print(
            "\nRule: every publication lists one or more direction ids under "
            "'directions:'. Only Orson adds or renames a direction, through a "
            f"pull request that changes data/research_directions.yaml. See {README_SECTION}."
        )
        return 1

    visible = sum(1 for d in directions.values() if not d.get("hidden"))
    selected = sum(1 for p in papers if p["fm"].get("selected") is True or p["highlight"])
    highlights = sum(1 for p in papers if p["highlight"])
    print(f"Publication directions check passed: {len(directions)} directions "
          f"({visible} visible), {len(papers)} publications, {selected} selected, "
          f"{highlights} highlights, {len(report.warnings)} warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
