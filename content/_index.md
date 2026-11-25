---
# Leave the homepage title empty to use the site title
title:
date: 2025-09-01
type: landing

sections:

  # Hero: the mission line, the three Sense, Empower, and Augment cards, and the
  # funder sentence. Each card links to its directions' views on the Research
  # page. `direction_link` reads the label from `data/research_directions.yaml`
  # and fails the build on an unknown or hidden id, so a renamed direction can't
  # leave a dead link here. Keep the card markup free of blank lines, because a
  # blank line ends a raw HTML block in markdown. Styles: `.sea-hero` and
  # `.sea-pillars` in `assets/scss/custom.scss`.
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
            <p class="sea-pillar__links">{{< direction_link "human-centered-health-foundation-models" >}}</p>
          </div>
          <div class="sea-pillar">
            {{<figure src="empower.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Empower</h2>
            <p class="sea-pillar__text">Creating AI agents and tools that turn health data into actionable insight and informed decisions.</p>
            <p class="sea-pillar__links">{{< direction_link "personal-health-agents" >}} {{< direction_link "clinician-ai-collaboration" >}}</p>
          </div>
          <div class="sea-pillar">
            {{<figure src="augment.png" alt="" lightbox="false">}}
            <h2 class="sea-pillar__title">Augment</h2>
            <p class="sea-pillar__text">Developing human-centered systems that promote healthy behaviors, enhance capabilities, and improve well-being.</p>
            <p class="sea-pillar__links">{{< direction_link "adaptive-interventions" >}}</p>
          </div>
        </div>

        Across all three, we hold health AI to a high bar through [human-centered benchmarks and real-world evaluation](/research/?direction=human-centered-evaluation).

        SEA Lab is grateful for support from the National Science Foundation (NSF), the National Institutes of Health (NIH), Google, OpenAI, NVIDIA, and Meta.

        For more details, please visit our <u>[Research Direction](/research/)</u> and <u>[Publication](/publication/)</u> pages.
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

  - block: markdown
    content:
      title: 'Join Us'
      subtitle: 
      text: |
        We are excited to welcome passionate and self-motivated researchers to join our team!

        **Postdoc**: We have 0-1 talented postdoc position that start in Fall 2026 or later.

        **PhD**: We are looking for 1-2 talented PhD students to begin in Fall 2027.

        **General Opportunities**: We always welcome enthusiastic students and research interns who want to make an impact with us.

        More details can be found in the <u>[JOIN US](/joinus/)</u> page.

    design:
      columns: '1'
      # css_style: 'text-align: justify'
      css_class: justify-text, section-title-left-aligned

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="**Meet the Team →**" %}}
    design:
      columns: '1'
      background:
        image: 
          filename: cuimc-cs.jpeg
          filters:
            brightness: 0.7
          parallax: false
          position: center
          size: cover
          text_color_light: true
      spacing:
        padding: ['280px', '0', '20px', '0']
      css_class: "intro-image-banner"

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
