---
# Leave the homepage title empty to use the site title
title:
date: 2025-09-01
type: landing

sections:

  - block: markdown
    content:
      title: 'Overview'
      text: | 
        The **SEA** (<u>**S**</u>ense, <u>**E**</u>mpower, and <u>**A**</u>ugment) Lab at Columbia University, led by <u>[Dr. Xuhai "Orson" Xu](https://orsonxu.com)</u>, focuses on designing, developing, and deploying innovative and practical human-computer interaction (HCI) and applied artificial intelligent and machine learning (AI/ML) techniques to advance human health and well-being.

        With everyday sensors and intelligent systems rapidly evolving, we adopt interdisciplinary approaches across computer science and health informatics to tackle real-world challenges.
        Our vision is to establish a set of human-centered methods, devices, and systems to **sense, empower, and augment** our everyday behavior, thereby enhancing daily experience and health outcomes.<br/> <br/>

        SEA lab is fortunate to be funded by National Science Foundation (NSF), National Institutes of Health (NIH), Google, OpenAI, NVIDIA.<br/> <br/>

        <div class="container-fluid", style="text-align: justify">
          <div class="row">
              <div class="col-md-4" style="text-align: center;">
                  {{<figure src="sense.png" alt="Sense">}}
                  <h5>Sense</h5>
              </div>
              <div class="col-md-4" style="text-align: center;">
                  {{<figure src="empower.png" alt="Sense">}}
                  <h5>Empower</h5>
              </div>
              <div class="col-md-4" style="text-align: center;">
                  {{<figure src="augment.png" alt="Sense">}}
                  <h5>Augment</h5>
              </div>
              <div class="col-md-4">
                  Collecting and integrating data from daily devices & medical systems to obtain a comprehensive picture of personal health.
              </div>
              <div class="col-md-4">
                  Creating AI methods and tools to derive actionable health insights and enable informed decisions.
              </div>
              <div class="col-md-4">
                  Developing human-centered systems to promote healthy behaviors, enhance capabilities, and improve well-being.
              </div>
          </div>
        </div> <br>

        For more details, please visit our <u>[Research Direction](/research/)</u> and <u>[Publication](/publication/)</u> pages.
    design:
      columns: '1'
      # css_style: 'text-align: justify'
      css_class: justify-text, section-title-left-aligned

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

  # - block: collection
  #   content:
  #     title: News
  #     subtitle:
  #     text:
  #     count: 5
  #     filters:
  #       author: ''
  #       category: ''
  #       exclude_featured: false
  #       publication_type: ''
  #       tag: ''
  #     offset: 0
  #     order: desc
  #     page_type: post
  #   design:
  #     view: card
  #     columns: '1'

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
        </div>
    design:
      columns: '1'
      css_class: section-title-left-aligned

---
