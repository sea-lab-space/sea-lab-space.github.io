---
# Leave the homepage title empty to use the site title
title:
date: 2025-09-01
type: landing

sections:

  # Hero: the mission line, the three Sense, Empower, and Augment cards, and
  # one sentence pointing to the Research and Publication pages. Under each
  # card, `pillar-directions` lists the research directions that belong to it,
  # as links to the Research page. Which direction goes under which card is set
  # by `pillars` in data/research_directions.yaml, and a direction can sit
  # under several cards. Keep the card markup free of blank lines, because a
  # blank line ends a raw HTML block in markdown. Styles: `.sea-hero` and
  # `.sea-pillars` in `assets/scss/custom.scss`.
  - block: markdown
    id: overview
    content:
      title: 'Overview'
      text: |
        <div class="sea-hero__mission">

        The **SEA Lab** (**S**ense, **E**mpower, **A**ugment) at Columbia University, led by [Dr. Xuhai "Orson" Xu](https://orsonxu.com), designs and builds human-centered and AI-powered methods that help people live healthier lives and empower health experts to make better decisions.

        </div>
        <div class="sea-pillars">
          <div class="sea-pillar">
            {{<figure src="sense.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Sense</h2>
            <p class="sea-pillar__text">Integrating data from everyday devices and health systems to build a holistic picture of personal health.</p>
            {{< pillar-directions sense >}}
          </div>
          <div class="sea-pillar">
            {{<figure src="empower.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Empower</h2>
            <p class="sea-pillar__text">Creating AI agents and tools that turn health data into actionable insight and informed decisions.</p>
            {{< pillar-directions empower >}}
          </div>
          <div class="sea-pillar">
            {{<figure src="augment.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Augment</h2>
            <p class="sea-pillar__text">Developing human-centered methods to promote healthy behaviors, enhance capabilities, and improve well-being.</p>
            {{< pillar-directions augment >}}
          </div>
        </div>

        Learn more about our research directions on the [Research](/research/) page, and browse all our papers on the [Publication](/publication/) page.

    design:
      columns: '1'
      css_class: sea-hero section-title-left-aligned
      # A faint photo of people crossing a street, behind the overview. The file
      # is already grey and softened. How strong it is and where it fades out
      # are set under `.sea-hero .home-section-bg` in assets/scss/custom.scss.
      # Photo: Ryoji Iwata on Unsplash (Unsplash License), see README Credits.
      background:
        image:
          filename: hero-crowd.webp

  # Lab News: the ten newest items from `data/news.yaml`, drawn by
  # `layouts/partials/blocks/news.html`. The "All news" link to /news/ appears
  # only when there are more than `count` items.
  - block: news
    id: news
    content:
      title: 'Lab News'
      count: 10
      archive_link: /news/
    design:
      css_class: section-title-left-aligned

  # Join Us, set on the campus photo (CUIMC and Columbia CS) that used to be a
  # separate "Meet the Team" banner. The photo is the block background, and the
  # text sits on a white, mostly opaque panel so it stays easy to read. The two
  # buttons sit to the right of the text on wide screens and below it on
  # tablets and phones. Styles: `.sea-join` in `assets/scss/custom.scss`. Keep the panel
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
          <a class="btn btn-primary sea-join__btn" href="/joinus/" aria-label="Read more about joining SEA Lab">Read more <span aria-hidden="true">→</span></a>
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
  #
  # Order: the three institutions (NSF, NIH, Columbia), then the companies. The
  # empty `funder-logos__break` span after Columbia is where tablets start the
  # second line. It is hidden at every other width.
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
          <a class="funder-logo funder-logo--emblem funder-logo--crown" href="https://www.columbia.edu/" target="_blank" rel="noopener">
            <img src="/uploads/funders/columbia.svg" alt="Columbia University" width="164" height="124" loading="lazy">
          </a>
          <span class="funder-logos__break" aria-hidden="true"></span>
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
