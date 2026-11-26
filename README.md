# [SEA Lab Website](https://sea-lab.space)

## Overview

This is the lab website code that can be maintained collaboratively.

Submit a pull request once you edit the website, and ping Orson to check the content in the lab.

- Get the code with `git clone git@github.com:sea-lab-space/sea-lab-space.github.io.git`. Ask Orson for access if that fails.
- Run every command in this README from the folder that `git clone` creates. `process.sh`, the check scripts, and `hugo` all use paths relative to it.
- Before you push, look at your change in a local build and run the two checks (see [Local Test](#local-test)).

## Coding Practice

- Directly push only if you are confident about your changes.
- Create a Pull Request whenever you are unsure about your edits.
- Always use a Pull Request for changes to `data/research_directions.yaml`. Orson reviews every change to the research directions (see [Categorize a publication](#categorize-pub)).
- Every push to `main` updates the live site a few minutes later (see [Checks and Deploys](#ci)).

## <a name="add-member"></a> Add A New Lab Member

- Go to `content/authors`
- Create a new folder named `firstname-middlename-lastname` (all lowercase) that is consistent with the name that you used for paper publications. If you don't use a middle name, the folder will be simply named `firstname-lastname`.
  - E.g., "Xuhai Xu" will become `xuhai-xu`, "Anind K Dey" will become `anind-k-dey`.
  - Making the folder name consistent with your name in publications (i.e., bib file, more in [add publication](#add-pub) section) will link your page with the papers listed in the [Publication](https://sea-lab.space/publication/) page.
- Copy a template `_index.md` from `content/authors/0-author-template` to the new folder. Fill in with your personal content. Feel free to take a look at others' `md` for reference.
- Set both `authors:` and `slug:` in `_index.md` to the folder name. `slug` controls your page address (`/author/<slug>/`). `authors` is what papers link to. If either differs from the folder, your page and your papers end up in different places.
  - Your display `title` can be anything, e.g. a nickname in quotes or parentheses. It does not affect the address.
  - On papers and in the bib, always write your name exactly as the folder name with spaces (`millie-mengyuan-wu` becomes `Millie Mengyuan Wu`). Other spellings you publish under go in the `Alias` column of `processing/Lab Collaboration Track Record - Person-Pub.csv`, on the row whose `Full Name` is your name written that way. Add a row if there is none. Separate several spellings with a semicolon, as in the row for Xuhai Xu. Spellings separated by commas are ignored without any warning.
  - `scripts/check_author_links.py` checks all of this on pull requests and before every deploy. When it fails, it names the file and the spelling to use.
- Set `user_groups` to `Researchers`. The People page shows only two groups, `Researchers` and `Alumni`. With the template's empty `user_groups`, you get an author page but no card on the People page, and no check warns you.
  ```yaml
  user_groups:
    - Researchers
  ```
- Set `role` to the position shown under your name, e.g. `PhD Student`, `Postdoc Researcher`, `Research Intern`, or `Undergraduate Research Intern`. The People page shuffles each group on every visit, so there is no order to set.
- Delete the `social:` entries you don't use. The template's placeholder links (`https://your-personal-website-link`, `mailto:test@example.org`) show on the People page if you leave them in.
- Add a personal headshot to the new folder. Name it as `avatar`, with the original file extension `[png/jpg/jpeg]`. Please make the photo square for the best visualization on the page. About 800 x 800 pixels is plenty. The site makes the small versions it shows, so a larger file only makes the repository heavier.
- If a folder ever has to be renamed, keep the old address working by listing it under `aliases:` in `_index.md`, as `content/authors/xuhai-xu/_index.md` does:
  ```yaml
  aliases:
    - /author/xuhai-orson-xu/
  ```

## <a name="move-alumni"></a> Move A Member To Alumni

- Open the member's `content/authors/<folder>/_index.md`. Keep the folder name, `slug`, and `authors` as they are, because their papers link to them.
- Change `user_groups` from `Researchers` to `Alumni`.
- Add a `now_at:` line saying where they went, e.g. `now_at: 'Harvard PhD'` or `now_at: "[nuri](https://nurihealth.ai/) (Co-founder)"`. The People page shows it under their role as "Now at ...", so don't write "Now at" yourself. It can include a Markdown link, in quotes.
- Keep `role` as the role they had in the lab.
- If you like, announce it with a Lab News item of `type: people` (see [Add Lab News](#add-news)).

## <a name="add-pub"></a> Add A New Publication

### List in the [Publication Page](https://sea-lab.space/publication/)
- We use `./sea-lab-publication.bib` to maintain the group bib file. Update the bib file by adding new publications.
- Set each new entry's citation key (the text right after `@inproceedings{` or `@article{`) to `lastname_firstword_year` in lowercase: the last name of the first author, the first word of the title, and the year, e.g. `zou_mind_2026`. The import names the paper's folder after this key, with underscores turned into dashes (`content/publication/zou-mind-2026/`). Capital letters and numbers inside a key are split off with dashes too, so a Zotero key like `kimMDAgentsAdaptiveCollaboration2024` becomes the long folder `kim-md-agents-adaptive-collaboration-2024`. The folder name is the paper's address and what Lab News links to, so don't rename a folder or change a key once the paper is live.
- [Rarely needed] If some of the co-authors in the new publications have multiple names in the record:
  - Update the collaboration sheet in `./processing/Lab Collaboration Track Record - Person-Pub.csv`.
  - Add all name aliases to the `Alias` column, separated by semicolons.
  - It needs the Python environment from [Local Test](#local-test), which has the right libraries (version 2 of bibtexparser does not work with it).
  - Copy the bib to `bak/` first, as the commented lines in `./process.sh` do. Then run `python3 ./processing/bib_post_processing.py`. It rewrites each alias in the bib to the `Full Name`. It also rewrites the whole bib, sorted by citation key, so `git diff` shows changes to almost every entry. Check that the author names you meant to fix are the only real changes. Its long "Names not found in df_author" list is normal.
- Import the new entries:
  - It needs the import tool, `academic` 0.10.0, the same version the import Action uses. Set it up once as described under [Local Test](#local-test), and activate that Python environment first.
  - Run `bash process.sh`. It runs `academic import ./sea-lab-publication.bib ./content/publication/ --compact`.
  - It prints `WARNING: Skipping creation of ... as it already exists` for every paper already on the site. That is normal. Never add `--overwrite`, even though the message suggests it. It rewrites every existing paper from the bib and deletes `directions`, awards, and everything else added by hand.
  - Run `git status` to see which folders are new.
- **Required:** open the `index.md` in each new folder and add its research directions under `directions:`, as described in [Categorize a publication](#categorize-pub) below. Then run `python3 scripts/check_publication_directions.py` to confirm.
- If you only push the bib change to `main`, the import Action opens a pull request with the new folders instead, on the branch `hugoblox-import-publications`. Add the `directions` to those folders on that branch and merge it soon. If the Action runs again while that pull request is open, because the bib changed on `main` again or someone started it by hand, it rebuilds the branch and the directions pushed there are lost.
- A click on a paper anywhere on the site (Research cards, the Publication page, Lab News, and author pages) opens the paper itself in a new tab. The site uses the first of these it finds in the paper's `index.md`: `external_link`, the `links` entry named `URL`, `doi`, a `links` entry named `arXiv`, `PDF`, or `Preprint`, and last `url_pdf`. A paper with none of them opens its page on this site instead.
  - The import fills these in from the bib. The bib `doi` becomes `doi:`, and the bib `url` becomes the `links` entry named `URL` (or `url_pdf` when the address ends in `.pdf`). So give every paper a `url` or `doi` in the bib.
  - To add a button such as a project website, add another entry under `links:` with its own name. Don't rename the `URL` entry, because that changes where the title goes.
    ```yaml
    links:
      - name: URL
        url: https://doi.org/10.1145/3772318.3790529
      - name: Project Website
        url: https://sea-lab.space/MIND/
    ```
- The type filters on the Publication page come from each entry's type and venue. `@article` shows under Journal and `@inproceedings` under Conference. A conference paper whose venue says Extended Abstracts, Adjunct, Workshop, Poster, Late-Breaking, or Doctoral Consortium shows under Workshop & Poster instead. `@misc`, `@unpublished`, and any paper whose venue names arXiv show under Preprint. Anything else shows only under All. To move a paper, fix its entry type or venue (see [Fix a paper that is already on the site](#fix-pub)).

### <a name="categorize-pub"></a> Categorize a publication (required)
Every publication belongs to one or more research directions. The [Research Page](https://sea-lab.space/research/), the direction filters on the [Publication Page](https://sea-lab.space/publication/), and the direction links under Sense, Empower, and Augment on the homepage are built from them.

- The directions are defined in `data/research_directions.yaml`. Read each direction's `definition` there and pick every direction that fits the paper.
- In the paper's `index.md`, list the direction ids under `directions:`, main direction first. Use the `id` values from the YAML, not the titles. A paper can list several, and it shows under each of them.
  ```yaml
  directions:
    - adaptive-interventions
    - personal-health-agents
  ```
- A paper whose main contribution is a new interaction or input technique (a new input modality, gesture, on-body, voice, or gaze interaction) also lists `interaction-techniques`. That direction is a filter on the Publication page only, with no section on the Research page, because it is no longer a focus of the lab.
- Work outside health goes under `beyond-health`. That direction is hidden from the Research page and the filters, but its papers still show on the Publication page under All.
- `selected`, `highlight`, and `highlight_rank` decide what the Research page shows. They are Orson's decisions, so only add them when he asks you to.
  - `selected: true` lists the paper on the Research page when a visitor opens one of its directions.
  - `highlight: <direction id>` also makes the paper a top card in that direction's overview. It must be one of the paper's own `directions`, and a paper can be highlighted in only one direction. A highlighted paper counts as selected.
  - `highlight_rank: <number>` orders the highlight cards, with 1 first. Two papers in the same direction can't share a rank.
- **The 4-card rule:** each direction's overview shows at most 4 highlight cards. If more than 4 papers are highlighted in one direction, only the 4 most recent by `date` show, ordered by `highlight_rank`. Unranked cards come last, newest first. The check below warns when this happens. Never edit a paper's `date` to change the order. Use `highlight_rank` instead.
- [Optional] `authors_display: "First Author et al."` shortens a very long author list in the list and card views. The paper's own page still shows every author, so keep the full list in the bib.
- [Optional] `publication_short: '*CHI*'` gives the short venue name that Research cards show, so a long proceedings name doesn't wrap across the card. The Publication page always shows the full `publication`. The import doesn't add it, so add it by hand to papers on the Research page.
- Research cards show the paper's `featured.png`, and a plain placeholder when there is none. Use a figure from the paper itself, such as its teaser or Figure 1. Make it exactly 4:3 and 1500 to 2000px wide when the source allows, padding with white rather than cutting off content. The site shows it at most 1000px wide, so a larger file only slows the build. The template `content/size_4x3_formatter.pptx` helps with the size.
- `scripts/check_publication_directions.py` checks all of this on every pull request and again before every deploy. It fails, naming the file and the field, when `directions` is missing or has an unknown id, when a legacy research tag is still present, when `highlight` is not one of the paper's directions, when `highlight_rank` is set without `highlight` or is shared by two papers, or when a field has the wrong type. It only warns about the 4-card rule, a direction without highlights, a Research page direction without a `number` or `pillars`, and a highlighted paper without a featured image.
- New folders from the bib-import pull request have no `directions` yet, so they fail the check until someone adds them. This is intended, because every paper needs a direction before it goes live. GitHub does not start checks on a pull request that a workflow opened, so the check first runs there when someone pushes the directions to that pull request's branch. If it is merged without them, the deploy stops at the same check and the live site stays as it was.

#### <a name="propose-direction"></a> Propose a new direction
- Don't add, rename, or remove a direction on your own, and never push such a change straight to `main`.
- Open a pull request that changes `data/research_directions.yaml`, together with the papers that should move to the new direction. `.github/CODEOWNERS` asks Orson to review it. `main` is not protected, so GitHub does not block the merge without his review. Don't merge until he approves.
- Each direction needs an `id` (lowercase words joined by dashes, used in page addresses), a `title`, a `short_title` for the filter chips, a `description` for the Research page, and a `definition` that tells others which papers belong to it. Directions appear in the order they are listed in the file.
- A direction on the Research page also has a `number`, shown in its heading and chips, and `pillars`, the homepage pillars (`sense`, `empower`, `augment`) that list it. A direction can sit under several pillars.
- `research_page: false` makes a direction a Publication page filter only, like `interaction-techniques`. `hidden: true` keeps it off both pages, like `beyond-health`, and its papers still show under All.
- The check fails when a direction is missing one of the five required fields, when two directions share an id, when an id is not lowercase words joined by dashes, or when `pillars` names something other than sense, empower, or augment.
- Some pages repeat the directions in their own words. When a direction is added, renamed, or removed, also update the Research page intro (`content/research/_index.md`, which says "five directions") and the topic lists on the Join Us page (`content/joinus/index.md`), which use the full titles.

### <a name="add-award"></a> Add an award badge
- Awards are not in the bib. Add them to the paper's `index.md`:
  ```yaml
  awards:
    - "honorable mention award"
  ```
- Use one of the names in `data/awards.yaml`: best paper award, distinguished paper award, best artifact award, honorable mention award, best paper nominee, editor's pick, oral presentation, spotlight. Capital letters don't matter. A name that isn't in that file shows no badge, and nothing warns you, so check the Publication page in a local build.
- For a new kind of award, add an entry to `data/awards.yaml` with a lowercase name, an `icon`, and the `display` text. Use 🏆 for an outright win and 🏅 for an honorable mention or a nomination, as the comment at the top of that file explains.
- The badge shows on the Publication page and on the paper's Research card. To announce the award, also add a Lab News item with `type: award`.

### <a name="fix-pub"></a> Fix a paper that is already on the site
- The import only creates folders for new bib entries. Editing an existing entry in `sea-lab-publication.bib` does not change the site by itself.
- To fix a paper, make the same change in three places: its bib entry, its `index.md` (for example `publication`, `doi`, `date`, or the `URL` entry under `links:`), and its `cite.bib`, which is what the Cite button shows.
- The most common case is a preprint that has been published. In `index.md`, update `publication`, `doi`, and `publication_types` (`paper-conference` for a conference paper, `article-journal` for a journal paper). Also change the `URL` entry under `links:` to the published version (for example `https://doi.org/<new doi>`), or delete it so the new `doi` is used. Otherwise every click on the paper still opens the preprint. Then replace the entry in `cite.bib` with the new bib entry.
- Don't delete the folder and re-import it. You would lose its `directions`, awards, `featured.png`, and everything else added by hand.
- To remove a paper, delete its bib entry and its folder in the same change. If you delete only the folder, the next import puts it back.

## <a name="add-news"></a> Add Lab News
- Lab News lives in `data/news.yaml`. The homepage shows the ten newest items, and the [News page](https://sea-lab.space/news/) shows all of them, grouped by year.
- Copy an existing entry to the top of the list, below the header comment, and fill in its fields:
  ```yaml
  - date: "2026-11"   # quoted string, "YYYY-MM" or "YYYY-MM-DD"
    type: award       # paper | award | grant | people | teaching | service | talk | press
    text: "Congratulations to [Zhihan](/author/zhihan-jiang/) on being selected as a [UW Rising Star in EECS](https://risingstars.cs.washington.edu/)!"
  ```
- Put links inside `text`, on the words they belong to. The optional `link:` field adds a separate "More" link and is rarely needed.
- New papers follow one pattern so the list is quick to skim: "Excited to share that our paper [Title](/publication/<folder>/) is published in *Venue*!" and then, if you like, one plain sentence on what it found or built.
- `text` is Markdown, one or two sentences. Link people to their profile (`/author/<folder>/`) and papers by their folder (`/publication/<folder>/`), using the folder names. The site turns a paper link into a link to the paper itself, the same place its title goes on the Publication page, and a link to a folder that doesn't exist prints a warning in the build.
- `type` picks the small icon next to the item. Leave `link` empty or out when there is no external page.
- Items are sorted newest first. Items from the same month keep their order in the file, so put the one that should show first higher up. The comment at the top of `data/news.yaml` has the details.
- No pull request check looks at `data/news.yaml`, and none builds the site. A misspelled `type` or a malformed date (such as a bare year like 2026, or a month like 2026-13) stops the deploy after the change reaches `main`. So build the site locally (see [Local Test](#local-test)) before you push a Lab News change.

## <a name="edit-pages"></a> Edit Other Pages
- **Homepage** (`content/_index.md`): the mission statement on the photo, the Sense, Empower, and Augment pillars on one white card, the Join Us panel, and the "Our Funders" logos. The direction links under each pillar come from `pillars` in `data/research_directions.yaml`, not from this file. Parts of this file are raw HTML. Don't add or remove blank lines inside them, because a blank line ends a raw HTML block in Markdown.
- **Open positions** are written in two places that must say the same thing: the Join Us panel on the homepage (the block with `id: join-us` in `content/_index.md`) and the [Join Us page](https://sea-lab.space/joinus/) (`content/joinus/index.md`). When the number of positions or the PhD start term changes, update both in the same change.
- **Funder logos** are SVG files in `static/uploads/funders/`, shown in the "Our Funders" block of `content/_index.md`. The row's CSS (`.funder-logos` in `assets/scss/custom.scss`) is sized for exactly these seven logos, three institutions and then four companies, so no logo sits alone on a line at any screen width. Adding or removing a logo needs that CSS changed too. Open a pull request and check the row at phone, tablet, and desktop widths.
- **Research page**: the intro is the first block of `content/research/_index.md`. The rest is built from `data/research_directions.yaml` and each paper's `directions`.
- **People page**: the groups are set in `content/people/index.md`.

## Site-wide Look (rarely changed)
- Tab icon: `assets/media/icon.png`, a square PNG at least 512 x 512. The theme makes the small icon sizes from it.
- Link preview image: `assets/media/sharing.png` (1200 x 630). It is shown when a page without its own featured image is shared on social media.
- Top bar logo: `assets/media/logo.png`.
- Font: `appearance.font` in `config/_default/params.yaml` names a font pack in `data/fonts/`. `Instrument Sans` loads `data/fonts/instrument_sans.toml`. To change the font, add a pack there and change that name.
- Footer: the address and links are in `layouts/partials/site_footer.html`. The copyright year and the "Latest Update" date fill in by themselves on every deploy, so don't edit them by hand.

## <a name="ci"></a> Checks and Deploys
- **Deploy website to GitHub Pages** (`.github/workflows/publish.yaml`) runs on every push to `main`. It runs both check scripts, builds the site with Hugo 0.126.3, and publishes it. If any step fails, the live site stays as it was. After you push or merge, open the Actions tab on GitHub and make sure the run is green.
- **Check author links** (`.github/workflows/check-author-links.yml`) runs on a pull request that changes `content/authors/`, `content/publication/`, `data/research_directions.yaml`, `sea-lab-publication.bib`, `processing/`, or the two check scripts. It runs the two check scripts but does not build the site.
- **Import Publications From Bibtex** (`.github/workflows/import-publications.yml`) runs when `sea-lab-publication.bib` changes on `main`, or by hand from the Actions tab. It opens a pull request with folders for the new entries.
- None of them needs a secret. In the repository settings, Pages must stay set to deploy from GitHub Actions, and Actions must stay allowed to create pull requests.

## Credits

The photo behind the homepage overview (`assets/media/hero-grand-central.webp`) is [Busy Grand Central Terminal by Branden Skeli on Unsplash](https://unsplash.com/photos/busy-grand-central-terminal-with-people-walking-around-KAT0Qy8LmiI), free to use under the [Unsplash License](https://unsplash.com/license). Its top 11% is cropped off and it is toned to the lab's blues. To swap it, put the new file in `assets/media/` and change `filename` under `background` in `content/_index.md`. The navy wash over it, the white statement, the card, and how the photo sits on phones are set under `.sea-hero` in `assets/scss/custom.scss`.

Our website is based on the following templates and tools:
- [Hugo Research Group template](https://github.com/HugoBlox/theme-research-group), which this site started from.
- [Hugo Blox Builder](https://github.com/HugoBlox/hugo-blox-builder/tree/41bd113535e815487ba69ad3c10aa8c03df91508/modules/blox-bootstrap), the Bootstrap 5 theme module. `go.mod` pins it to this May 2024 commit, and the site replaces many of its templates. Don't update it (for example with `hugo mod get -u`). The docs on [hugoblox.com](https://hugoblox.com) now describe a newer Hugo Blox, so some of their steps don't apply here.

## <a name="local-test"></a> Local Test

- Install Git and Go. On a Mac: `brew install git go`. Hugo uses Go to download the site theme the first time you build.
- Install Hugo **0.126.3 extended**, the exact version the live site uses (pinned in `.github/workflows/publish.yaml`). Newer Hugo, such as the one `brew install hugo` or the Hugo Blox install page gives you, cannot build this site. It stops with an error that ends in `can't evaluate field GoogleAnalytics`. You don't need Node or the `hugoblox` command.
  - On a Mac, in Terminal:
    ```bash
    curl -LO https://github.com/gohugoio/hugo/releases/download/v0.126.3/hugo_extended_0.126.3_darwin-universal.tar.gz
    tar -xzf hugo_extended_0.126.3_darwin-universal.tar.gz hugo
    sudo mkdir -p /usr/local/bin
    sudo mv hugo /usr/local/bin/
    ```
    Downloading with `curl` avoids the macOS message that "hugo" could not be verified. If you downloaded the file in a browser instead, run `xattr -d com.apple.quarantine hugo` before moving it.
  - On Windows or Linux, download `hugo_extended_0.126.3_windows-amd64.zip` or `hugo_extended_0.126.3_linux-amd64.tar.gz` from the [Hugo 0.126.3 release page](https://github.com/gohugoio/hugo/releases/tag/v0.126.3), unpack it, and put `hugo` (or `hugo.exe`) in a folder on your PATH.
  - Run `hugo version`. It must start with `hugo v0.126.3` and include `extended`. If it shows another version, a second Hugo comes first on your PATH. Remove it (on a Mac, `brew uninstall hugo`) or run this one by its full path, `/usr/local/bin/hugo`.
- Run `hugo server -D` and open http://localhost:1313/ to check your change. It rebuilds each time you save a file. Stop it with Ctrl+C.
- Read the terminal after each save. An ERROR line stops the build, and the same error stops the deploy, so fix it before you push. A WARN line about a `/publication/...` link means a link points to a paper folder that doesn't exist.
- Set up Python once, for the checks and the publication import. Use Python 3.11.5 or newer in a virtual environment. The Python that comes with macOS (3.9) is too old for the import tool, and Homebrew's Python refuses `pip install` outside a virtual environment.
  ```bash
  brew install python    # on a Mac, if you don't have Python 3.11.5 or newer
  python3 -m venv ~/.venvs/sea-lab
  source ~/.venvs/sea-lab/bin/activate
  python3 -m pip install pyyaml academic==0.10.0 pandas "bibtexparser<2"
  ```
  In each new terminal, run `source ~/.venvs/sea-lab/bin/activate` again before the commands in this README. The environment lives outside the repository, so it never shows up in `git status`.
- Before you push, run `python3 scripts/check_author_links.py` and `python3 scripts/check_publication_directions.py` with that environment active. Both must pass. They run again on pull requests and before every deploy.
