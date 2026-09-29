#!/usr/bin/env python3
"""Fail the build when a lab member's name would not link to their profile.

How the site decides "who is who":
  * A profile lives in content/authors/<folder>/_index.md.
  * A paper attaches to that profile only if the author string on the paper,
    lowercased with spaces turned into dashes, is exactly <folder>.
  * The profile's page address is /author/<slug>/, so slug must be <folder>
    too, or the page and the paper links point at different places.

Checks:
  1. Every profile has `authors: [<folder>]` and `slug: <folder>`.
  2. No two profiles claim the same address (slug or redirect alias).
  3. Every author string on a publication that is clearly meant to be a lab
     member is written in the exact form that links:
       - it would match a folder if punctuation were ignored, but does not
         match as written (e.g. "Millie (Mengyuan) Wu"), or
       - it is a known alias of a member in the name sheet
         (e.g. "Millie Wu" for millie-mengyuan-wu).

Run from the repo root:  python scripts/check_author_links.py
"""

import csv
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
AUTHORS = ROOT / "content" / "authors"
PUBS = ROOT / "content" / "publication"
SHEET = ROOT / "processing" / "Lab Collaboration Track Record - Person-Pub.csv"
SKIP = {"0-author-template"}


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def strict_key(name):
    """What the site actually compares: lowercase, spaces to dashes."""
    return re.sub(r"\s+", "-", name.strip().lower())


def loose_key(name):
    """Same, but ignoring punctuation. Used to spot near-misses."""
    s = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[\s_]+", "-", s.strip()).strip("-")


def flip(name):
    """'Wu, Mengyuan' -> 'Mengyuan Wu'."""
    if "," in name:
        last, first = [p.strip() for p in name.split(",", 1)]
        return f"{first} {last}"
    return name.strip()


def main():
    errors = []

    # 1 and 2: profiles
    folders = {}
    claimed = {}
    for d in sorted(p for p in AUTHORS.iterdir() if p.is_dir()):
        if d.name in SKIP:
            continue
        fm = front_matter(d / "_index.md")
        folders[d.name] = fm
        where = f"content/authors/{d.name}/_index.md"

        if fm.get("authors") != [d.name]:
            errors.append(
                f"{where}: 'authors' must be a one-item list containing "
                f"'{d.name}', found {fm.get('authors')!r}."
            )
        if fm.get("slug") != d.name:
            errors.append(
                f"{where}: 'slug' must be '{d.name}' (the folder name), "
                f"found {fm.get('slug')!r}."
            )

        addresses = [f"/author/{fm.get('slug') or d.name}/"]
        addresses += [str(a) for a in fm.get("aliases") or []]
        for a in addresses:
            a = "/" + a.strip("/") + "/"
            if a in claimed:
                errors.append(
                    f"{where}: address {a} is also claimed by "
                    f"content/authors/{claimed[a]}/."
                )
            claimed[a] = d.name

    # alias sheet: alias -> member folder
    alias_to_folder = {}
    if SHEET.exists():
        with SHEET.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                folder = strict_key(row.get("Full Name", ""))
                if folder not in folders:
                    continue
                for alias in (row.get("Alias") or "").split(";"):
                    alias = alias.strip()
                    if alias:
                        alias_to_folder[flip(alias).lower()] = folder

    near_miss = {loose_key(f.replace("-", " ")): f for f in folders}

    # 3: publications
    for page in sorted(PUBS.glob("*/index.md")):
        fm = front_matter(page)
        where = f"content/publication/{page.parent.name}/index.md"
        for name in fm.get("authors") or []:
            name = str(name)
            if strict_key(name) in folders:
                continue
            target = alias_to_folder.get(flip(name).lower()) or near_miss.get(
                loose_key(name)
            )
            if target:
                good = " ".join(w.capitalize() for w in target.split("-"))
                errors.append(
                    f"{where}: author '{name}' will not link to "
                    f"content/authors/{target}/. Write it as '{good}' "
                    f"(and use the same form in sea-lab-publication.bib)."
                )

    if errors:
        print("Author link check failed:\n")
        for e in errors:
            print("  - " + e)
        print(
            "\nRule: a member's folder name, their profile 'slug', and the "
            "author string on every paper must all be the same name. "
            "See 'Add A New Lab Member' in README.md."
        )
        return 1

    print(f"Author link check passed: {len(folders)} profiles, "
          f"{len(list(PUBS.glob('*/index.md')))} publications.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
