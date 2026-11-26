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
        At the intersection of human–computer interaction (HCI) and artificial intelligence (AI), SEA Lab explores how intelligent systems can sense, understand, and respond to the complexities of human life. We develop computational methods to interpret rich, longitudinal data and design novel human–AI interactions that translate this understanding into meaningful insights and actions.<br/><br/>
        Our research serves two complementary goals: (i) empowering individuals and patients to better understand their health and navigate their everyday lives, and (ii) augmenting the expertise of physicians, nurses, and other health professionals to enable more informed and personalized care. Through these efforts, we seek to establish the scientific and technological foundations for a future in which humans and AI work together to advance human health and well-being.
    design:
      columns: '1'
      css_class: section-title-left-aligned

  - block: research_directions
    id: research-directions
---
