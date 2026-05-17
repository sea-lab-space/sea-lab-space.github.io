# [SEA Lab Website](https://sea-lab.space)

## Overview

This is the lab website code that can be maintained collaboratively.

Submit a pull request once you edit the website, and ping Orson to check the content in the lab.

## Coding Practice

- Directly push only if you are confident about your changes.
- Create a Pull Request whenever you are unsure about your edits. 

## <a name="add-member"></a> Add A New Lab Member

- Go to `content/authors`
- Create a new folder named `firstname-middlename-lastname` (all lowercase) that is consistent with the name that you used for paper publications. If you don't use a middle name, the folder will be simply named `firstname-lastname`.
  - E.g., "Xuhai Xu" will become `xuhai-xu`, "Anind K Dey" will become `anind-k-dey`.
  - Making the folder name consistent with your name in publications (i.e., bib file, more in [add publication](#add-pub) section) will link your page with the papers listed in the [Publication](https://sea-lab.space/publication/) page.
- Copy a template `_index.md` from `content/authors/0-author-template` to the new folder. Fill in with your personal content. Feel free to take a look at others' `md` for reference.
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

### Highlight in the [Research Page](https://sea-lab.space/research/)
- After you prepare the publication folder, now you can pick a set of papers to get highlighted on the [Research Page](https://sea-lab.space/research/) of our lab website.
- Go to the generated publication folder in `./content/publication/` that you want to highlight. You should see an `index.md`.
- Add a key called `tags`, and add the corresponding tag that you want to highlight under `tags`. Pick one tag from the following list (Don't forget the quotes `'` that wrap the tag name):
  - `'health prediction'`: Section 1 in the Research page
  - `'intelligent interaction and intervention'`: Section 2
  - `'clinical support'`: Section 3
- Add a feature image `featured.png` in the same folder. Use the template for the appropriate size if needed: `content/size_4x3_formatter.pptx`
- [Here](./content/publication/xu-globem-2023/index.md) is an example of the tag setup in the `index.md`.
- [Optional] By default, each section will highlight the top 3 publications with this tag, ranked by publication date (the latest will be on the top).
  - If you want to move up/down some papers, tweak the `date` in the `index.md` of the corresponding publication slightly.
  - Only change the month and day for visualization purposes. Never change the year.


## Credits

Our website is based on the following templates and tools:
- [Hugo Research Group Theme](https://github.com/HugoBlox/theme-research-group)
- [Hugo Blox](https://hugoblox.com)

## Local Test

- Follow [this page](https://docs.hugoblox.com/getting-started/install-hugo/) to install dependencies.
- Run `hugo server -D` locally.