# [SEA Lab Website](https://sea-lab.space)

## Overview

This is the lab website code that can be maintained collaboratively.

Submit a pull request once you edit the website, and ping Orson to check the content in the lab.

## Coding Practice

- Directly push only if you are confident about your changes.
- Create a Pull Request whenever you are unsure about your edits. 
- Always use a Pull Request for changes to `data/research_directions.yaml`. Orson reviews every change to the research directions (see [Categorize a publication](#categorize-pub)).

## <a name="add-member"></a> Add A New Lab Member

- Go to `content/authors`
- Create a new folder named `firstname-middlename-lastname` (all lowercase) that is consistent with the name that you used for paper publications. If you don't use a middle name, the folder will be simply named `firstname-lastname`.
  - E.g., "Xuhai Xu" will become `xuhai-xu`, "Anind K Dey" will become `anind-k-dey`.
  - Making the folder name consistent with your name in publications (i.e., bib file, more in [add publication](#add-pub) section) will link your page with the papers listed in the [Publication](https://sea-lab.space/publication/) page.
- Copy a template `_index.md` from `content/authors/0-author-template` to the new folder. Fill in with your personal content. Feel free to take a look at others' `md` for reference.
- Set both `authors:` and `slug:` in `_index.md` to the folder name. `slug` controls your page address (`/author/<slug>/`). `authors` is what papers link to. If either differs from the folder, your page and your papers end up in different places.
  - Your display `title` can be anything, e.g. a nickname in quotes or parentheses. It no longer affects the address.
  - On papers and in the bib, always write your name exactly as the folder name with spaces (`millie-mengyuan-wu` becomes `Millie Mengyuan Wu`). Other spellings you publish under go in the `Alias` column of `processing/Lab Collaboration Track Record - Person-Pub.csv`.
  - `scripts/check_author_links.py` checks all of this on every pull request and before every deploy, and tells you exactly which line to fix.
- Add a personal headshot to the new folder. Name it as `avatar`, with the original file extension `[png/jpg/jpeg]`. Please make the photo to be square for the best visualization on the page.

## <a name="add-pub"></a> Add A New Publication

### List in the [Publication Page](https://sea-lab.space/publication/)
- We use `./sea-lab-publication.bib` to maintain the group bib file. Update the bib file by adding new publications.
- [Rarely needed] If some of the co-authors in the new publications have multiple names in the record:
  - Update the collaboration sheet in `./processing/Lab Collaboration Track Record - Person-Pub.csv`.
  - Add all name aliases to the `Alias` column.
  - Run `python ./processing/bib_post_processing.py`. This will update the name in the `./sea-lab-publication.bib` to ensure the next step of processing.
- After ensuring the name is consistent, run the corresponding command in `./process.sh`. Make sure you have installed the [HUGO academic tool](https://github.com/girtel/hugo-academic-cli-girtel).
- The command should automatically populate folders in `./content/publication/`. The folder should follow this naming format: `[last name of the first author]-[first word of the paper title]-[publication year]`.
- **Required:** open the `index.md` in each new folder and add its research directions under `directions:`, as described in [Categorize a publication](#categorize-pub) below. Then run `python scripts/check_publication_directions.py` to confirm.
- If you only push the bib change to `main`, the import Action opens a pull request with the new folders instead. Add the `directions` to those folders in that pull request before it is merged.

### <a name="categorize-pub"></a> Categorize a publication (required)
Every publication belongs to one or more research directions. The [Research Page](https://sea-lab.space/research/) and the direction filters on the [Publication Page](https://sea-lab.space/publication/) are built from them.

- The directions are defined in `data/research_directions.yaml`. Read each direction's `definition` there and pick every direction that fits the paper.
- In the paper's `index.md`, list the direction ids under `directions:`, main direction first. Use the `id` values from the YAML, not the titles.
  ```yaml
  directions:
    - adaptive-interventions
    - personal-health-agents
  ```
- Work outside health goes under `beyond-health`. That direction is hidden from the Research page, but its papers still show on the Publication page.
- `selected`, `highlight`, and `highlight_rank` decide what the Research page shows. They are Orson's decisions, so only add them when he asks you to.
  - `selected: true` lists the paper on the Research page when a visitor opens one of its directions.
  - `highlight: <direction id>` also makes the paper a top card in that direction's overview. It must be one of the paper's own `directions`, and a paper can be highlighted in only one direction. A highlighted paper counts as selected.
  - `highlight_rank: <number>` orders the highlight cards, with 1 first. Two papers in the same direction can't share a rank.
- **The 4-card rule:** each direction's overview shows at most 4 highlight cards. If more than 4 papers are highlighted in one direction, only the 4 most recent by `date` show, ordered by `highlight_rank`. Unranked cards come last, newest first. The check below warns when this happens. Never edit a paper's `date` to change the order. Use `highlight_rank` instead.
- [Optional] `authors_display: "First Author et al."` shortens a very long author list in the list and card views. The paper's own page still shows every author, so keep the full list in the bib.
- Research cards show the paper's `featured.png`, and a plain placeholder when there is none. Use a figure from the paper itself, such as its teaser or Figure 1. Make it exactly 4:3 and at least 1500px wide when the source allows, padding with white rather than cutting off content. The template `content/size_4x3_formatter.pptx` helps with the size.
- `scripts/check_publication_directions.py` checks all of this on every pull request and again before every deploy. It fails, naming the file and the field, when `directions` is missing or has an unknown id, when a legacy research tag is still present, when `highlight` is not one of the paper's directions, when `highlight_rank` is set without `highlight` or is shared by two papers, or when a field has the wrong type. It only warns about the 4-card rule, a direction without highlights, and a highlighted paper without a featured image.
- New folders from the bib-import pull request have no `directions` yet, so they fail the check until someone adds them. This is intended, because every paper needs a direction before it goes live. GitHub does not start checks on a pull request that a workflow opened, so the check first runs there when someone pushes the directions to that pull request's branch. If it is merged without them, the deploy stops at the same check and the live site stays as it was.

#### Propose a new direction
- Don't add, rename, or remove a direction on your own, and never push such a change straight to `main`.
- Open a pull request that changes `data/research_directions.yaml`, together with the papers that should move to the new direction. `.github/CODEOWNERS` requests Orson's review, and only he approves a new direction.
- Each direction needs an `id` (lowercase words joined by dashes, used in page addresses), a `title`, a `short_title` for the filter chips, a `description` for the Research page, and a `definition` that tells others which papers belong to it. A visible direction also has a `number`, shown in its Research page heading and chip. Directions appear in the order they are listed in the file.

## <a name="add-news"></a> Add Lab News
- Lab News lives in `data/news.yaml`. The homepage shows the ten newest items, and the [News page](https://sea-lab.space/news/) shows all of them, grouped by year.
- Copy an existing entry to the top of the list, below the header comment, and fill in its fields:
  ```yaml
  - date: "2026-11"   # quoted string, "YYYY-MM" or "YYYY-MM-DD"
    type: award       # paper | award | grant | people | teaching | service | talk | press
    text: "Congratulations to [Zhihan](/author/zhihan-jiang/) on being selected as a [UW Rising Star in EECS](https://risingstars.cs.washington.edu/)!"
  ```
- Put links inside `text`, on the words they belong to. The optional `link:` field adds a separate "More" link and is rarely needed.
- New papers follow one pattern so the list is quick to skim: "Excited to share that our paper [Title](/publication/<folder>/) is published in *Venue*!" and then one plain sentence on what it found or built.
- `text` is Markdown, one or two sentences. Link people to their profile (`/author/<folder>/`) and papers to their page (`/publication/<folder>/`), using the folder names.
- `type` picks the small icon next to the item. Leave `link` empty or out when there is no external page.
- Items are sorted newest first. Items from the same month keep their order in the file, so put the one that should show first higher up. The comment at the top of `data/news.yaml` has the details.


## Credits

Our website is based on the following templates and tools:
- [Hugo Research Group Theme](https://github.com/HugoBlox/theme-research-group)
- [Hugo Blox](https://hugoblox.com)

## Local Test

- Follow [this page](https://hugoblox.com/docs/start/cli) to install dependencies. The live site builds with Hugo 0.126.3 extended, the version pinned in `.github/workflows/publish.yaml`.
- Run `hugo server -D` locally.
- Before you push, run `python scripts/check_author_links.py` and `python scripts/check_publication_directions.py`. Both run in CI and must pass.
