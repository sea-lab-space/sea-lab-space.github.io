---
# Leave the homepage title empty to use the site title
title:
date: 2025-09-01
type: landing

sections:

  # Hero: the mission line, the three Sense, Empower, and Augment cards, one
  # sentence pointing to the Research and Publication pages, and the funder
  # sentence. Kept deliberately plain: no buttons, so it reads as a short
  # overview. Keep the card markup free of blank lines, because a blank line
  # ends a raw HTML block in markdown. Styles: `.sea-hero` and `.sea-pillars`
  # in `assets/scss/custom.scss`.
  - block: markdown
    id: overview
    content:
      title: 'Overview'
      text: |
        <div class="sea-hero__mission">

        The **SEA Lab** (**S**ense, **E**mpower, **A**ugment) at Columbia University, led by [Dr. Xuhai "Orson" Xu](https://orsonxu.com), is an HCI lab building human-centered AI that helps people live healthier lives and helps health experts make better decisions.

        </div>
        <div class="sea-pillars">
          <div class="sea-pillar">
            {{<figure src="sense.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Sense</h2>
            <p class="sea-pillar__text">Collecting and integrating data from everyday devices and medical systems to build a complete picture of personal health.</p>
          </div>
          <div class="sea-pillar">
            {{<figure src="empower.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Empower</h2>
            <p class="sea-pillar__text">Creating AI agents and tools that turn health data into actionable insight and informed decisions.</p>
          </div>
          <div class="sea-pillar">
            {{<figure src="augment.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Augment</h2>
            <p class="sea-pillar__text">Developing human-centered systems that promote healthy behaviors, enhance capabilities, and improve well-being.</p>
          </div>
        </div>

        Learn more about our five research directions on the [Research](/research/) page, and browse all our papers on the [Publication](/publication/) page.

        SEA Lab is grateful for support from the National Science Foundation (NSF), the National Institutes of Health (NIH), Google, OpenAI, NVIDIA, and Meta.
    design:
      columns: '1'
      css_class: sea-hero section-title-left-aligned

  # Lab News: the six newest items from `data/news.yaml`, drawn by
  # `layouts/partials/blocks/news.html`. The "All news" link to /news/ appears
  # only when there are more than `count` items.
  - block: news
    id: news
    content:
      title: 'Lab News'
      count: 6
      archive_link: /news/
    design:
      css_class: section-title-left-aligned

  # Join Us, set on the campus photo (CUIMC and Columbia CS) that used to be a
  # separate "Meet the Team" banner. The photo is the block background, and the
  # text sits on a white, mostly opaque panel so it stays easy to read. The two
  # buttons sit to the right of the text on wide screens and below it on
  # phones. Styles: `.sea-join` in `assets/scss/custom.scss`. Keep the panel
  # markup free of blank lines, except around the markdown text, because a
  # blank line ends a raw HTML block in markdown.
  - block: markdown
    id: join-us
    content:
      title:
      text: |
        <div class="sea-join">
        <div class="sea-join__text">
        <h1 class="sea-join__title">Join Us</h1>

        We are excited to welcome passionate and self-motivated researchers to join our team!

        **Postdoc**: We have 0-1 talented postdoc position with a flexible start date.

        **PhD**: We are looking for 1-2 talented PhD students to begin in Fall 2027.

        **General Opportunities**: We always welcome enthusiastic students and research interns who want to make an impact with us.

        </div>
        <div class="sea-join__actions">
          <a class="btn btn-primary sea-join__btn" href="/joinus/">Open Positions <span aria-hidden="true">→</span></a>
          <a class="btn btn-outline-primary sea-join__btn" href="/people/">Meet the Team <span aria-hidden="true">→</span></a>
        </div>
        </div>
    design:
      columns: '1'
      background:
        image:
          filename: cuimc-cs.jpeg
          filters:
            brightness: 1
          parallax: false
          position: center
          size: cover
          text_color_light: false
      css_class: sea-join-section

  # Funder logos. Images live in `static/uploads/funders/` (published verbatim, no
  # Hugo image processing needed for SVG); the row is styled by `.funder-logos`
  # in `assets/scss/custom.scss`, which normalises the mixed logo aspect ratios.
  #
  # Each <img> carries its source SVG's intrinsic width/height. CSS overrides the
  # rendered size, but the attributes give the browser an aspect ratio to reserve
  # space with, so the lazy-loaded marks don't reflow the row as they arrive.
  - block: markdown
    content:
      title: 'Our Funders'
      subtitle:
      text: |
        <div class="funder-logos">
          <a class="funder-logo funder-logo--emblem" href="https://www.nsf.gov/" target="_blank" rel="noopener">
            <img src="/uploads/funders/nsf.svg" alt="National Science Foundation" width="169" height="171" loading="lazy">
          </a>
          <a class="funder-logo funder-logo--emblem" href="https://www.nih.gov/" target="_blank" rel="noopener">
            <img src="/uploads/funders/nih.svg" alt="National Institutes of Health" width="374" height="329" loading="lazy">
          </a>
          <a class="funder-logo" href="https://research.google/" target="_blank" rel="noopener">
            <img src="/uploads/funders/google.svg" alt="Google" width="272" height="92" loading="lazy">
          </a>
          <a class="funder-logo" href="https://openai.com/" target="_blank" rel="noopener">
            <img src="/uploads/funders/openai.svg" alt="OpenAI" width="270" height="73" loading="lazy">
          </a>
          <a class="funder-logo" href="https://www.nvidia.com/" target="_blank" rel="noopener">
            <img src="/uploads/funders/nvidia.svg" alt="NVIDIA" width="656" height="120" loading="lazy">
          </a>
          <a class="funder-logo funder-logo--meta" href="https://ai.meta.com/" target="_blank" rel="noopener">
            <img src="/uploads/funders/meta.svg" alt="Meta" width="4972" height="1010" loading="lazy">
          </a>
        </div>
    design:
      columns: '1'
      css_class: section-title-left-aligned

---
