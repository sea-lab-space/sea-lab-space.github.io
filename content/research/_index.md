---
# Page title
title: Research Focus
# Page type - we want a landing page (such as a homepage)
type: landing

# The page has two blocks.
#   1. The intro below (plain markdown).
#   2. The research directions block. It builds the chip bar, the overview cards
#      and the per-direction views from data/research_directions.yaml and from
#      each publication's `directions`, `selected`, `highlight` and
#      `highlight_rank` front matter. Nothing on this page needs editing when a
#      paper is added. See "Categorize a publication" in the README.
sections:
  - block: markdown
    id: research-intro
    content:
      title: Research Directions
      text: >-
        SEA Lab is an HCI lab at heart. We design, build, and deploy human-centered AI
        that turns the data of everyday life into insight and action. Our work serves
        two groups of people: (i) **the general population**, including end-users and
        patients, whom we help live healthier lives every day, and (ii) **health
        experts**, including physicians, nurses, and other care providers, whom we help
        make better-informed decisions. Our research spans five directions, from AI
        agents that partner with people over months to benchmarks that test whether
        health AI holds up in the real world.
    design:
      columns: '1'
      css_class: section-title-left-aligned

  - block: research_directions
    id: research-directions
---
