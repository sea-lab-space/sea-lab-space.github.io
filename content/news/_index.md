---
title: Lab News

# A landing page, like the homepage. It reuses the homepage's Lab News block
# (`layouts/partials/blocks/news.html`) to list every item in `data/news.yaml`,
# grouped by year. Add news in that data file, not here.
type: landing

sections:
  - block: news
    id: news
    content:
      title: 'Lab News'
      count: 0
      group_by_year: true
    design:
      css_class: section-title-left-aligned
---
