/*
 * Publications page filters (T4).
 *
 * Loaded only on /publication/ by layouts/partials/hooks/body-end/publication-filters.html.
 * The page itself (layouts/section/publication.html) renders every paper,
 * grouped by year, so it reads fine with JS off. This script adds:
 *
 *   - Direction chips: "All" plus the visible research directions. Single-select.
 *   - Type chips: "All", Journal, Conference, Workshop & Poster, Preprint.
 *   - A search box. Every word you type must appear somewhere in the paper's
 *     title, authors, venue, or year. Case and accents are ignored.
 *
 * The three combine with AND. Year headings hide when a filter empties them,
 * and the "Showing N of M papers" line keeps count.
 *
 * URL state: ?direction=<id>&type=<id>&q=<text>. Query params, never the hash,
 * because the theme's scroll script reads every hash as an element id.
 *   - Chip clicks use pushState, so Back and Forward step through filters.
 *   - Typing uses replaceState, so a search does not add one history entry per
 *     keystroke.
 *   - Unknown values (including the hidden Beyond Health direction) fall back
 *     to "All" and are dropped from the URL.
 *   - Legacy links: paper pages link to /publication/#<CSL type>, e.g.
 *     #article-journal. Those hashes are turned into the matching ?type= on
 *     load, so old links still land on a filtered list. When the reader came
 *     from a paper page, that paper's own type wins, so the list they land on
 *     always contains the paper they came from.
 *
 * Plain ES2017, no libraries. Every lookup is guarded, so the script does
 * nothing on a page without #pub-browser.
 */
(function () {
  'use strict';

  var root = document.getElementById('pub-browser');
  if (!root) return;

  var items = Array.prototype.slice.call(root.querySelectorAll('.pub-item'));
  if (!items.length) return;

  var groups = Array.prototype.slice.call(root.querySelectorAll('.pub-year'));
  var chips = Array.prototype.slice.call(root.querySelectorAll('.pub-chip[data-filter]'));
  var searchInput = root.querySelector('#pub-search-input');
  var shownCount = root.querySelector('[data-pub-shown]');
  var emptyState = root.querySelector('.pub-empty');
  var resetButtons = Array.prototype.slice.call(root.querySelectorAll('[data-pub-reset]'));

  // The hash values the theme's paper pages link to (the first CSL type,
  // anchorized), mapped to this page's type chips. CSL types without a chip
  // map to "all", which simply clears the type filter.
  var LEGACY_HASH_TYPES = {
    'article-journal': 'journal',
    'paper-conference': 'conference',
    'manuscript': 'preprint',
    'article': 'preprint',
    'book': 'all',
    'chapter': 'all',
    'thesis': 'all',
    'report': 'all',
    'patent': 'all',
    '0': 'all'
  };

  // Lowercase, strip accents, and fold typographic dashes and quotes, so that
  // "simao" finds "Simão" and "clinician-ai" finds "Clinician–AI".
  function normalize(text) {
    return String(text || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[\u2010-\u2015]/g, '-')
      .replace(/[\u2018\u2019]/g, "'")
      .replace(/[\u201c\u201d]/g, '"')
      .toLowerCase();
  }

  // Read every paper's filter data once.
  var papers = items.map(function (el) {
    return {
      el: el,
      group: el.closest('.pub-year'),
      type: el.getAttribute('data-type') || '',
      directions: (el.getAttribute('data-directions') || '').split(/\s+/).filter(Boolean),
      text: normalize(el.getAttribute('data-search') || el.textContent)
    };
  });

  // The values each chip row accepts, taken from the chips themselves so the
  // template (and data/research_directions.yaml) stays the only list.
  var allowed = { direction: {}, type: {} };
  chips.forEach(function (chip) {
    var group = chip.getAttribute('data-filter');
    if (allowed[group]) allowed[group][chip.getAttribute('data-value')] = true;
  });

  function pick(group, value) {
    return value && allowed[group][value] ? value : 'all';
  }

  function stateFromUrl() {
    var params = new URLSearchParams(window.location.search);
    return {
      direction: pick('direction', params.get('direction')),
      type: pick('type', params.get('type')),
      q: (params.get('q') || '').trim()
    };
  }

  // Build this page's URL for a state, keeping any unrelated query params
  // (e.g. analytics tags) and dropping a hash only when asked to.
  function urlFor(state, keepHash) {
    var params = new URLSearchParams(window.location.search);
    ['direction', 'type', 'q'].forEach(function (key) {
      var value = state[key];
      if (value && value !== 'all') params.set(key, value);
      else params.delete(key);
    });
    var query = params.toString();
    return window.location.pathname + (query ? '?' + query : '') + (keepHash ? window.location.hash : '');
  }

  function sameState(a, b) {
    return a.direction === b.direction && a.type === b.type && a.q === b.q;
  }

  function isDefault(state) {
    return state.direction === 'all' && state.type === 'all' && !state.q;
  }

  var current = stateFromUrl();

  // Show the papers that match the state, then sync the chips, the year
  // headings, the counts, and the empty message.
  function render(state) {
    var terms = normalize(state.q).split(/\s+/).filter(Boolean);
    var perGroup = new Map();
    var shown = 0;

    papers.forEach(function (paper) {
      var match =
        (state.direction === 'all' || paper.directions.indexOf(state.direction) !== -1) &&
        (state.type === 'all' || paper.type === state.type) &&
        terms.every(function (term) { return paper.text.indexOf(term) !== -1; });
      paper.el.hidden = !match;
      if (match) {
        shown += 1;
        perGroup.set(paper.group, (perGroup.get(paper.group) || 0) + 1);
      }
    });

    groups.forEach(function (group) {
      var n = perGroup.get(group) || 0;
      group.hidden = n === 0;
      var count = group.querySelector('[data-pub-year-count]');
      if (count) count.textContent = n + (n === 1 ? ' paper' : ' papers');
    });

    chips.forEach(function (chip) {
      var active = state[chip.getAttribute('data-filter')] === chip.getAttribute('data-value');
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    if (shownCount) shownCount.textContent = String(shown);
    if (emptyState) emptyState.hidden = shown !== 0;
    resetButtons.forEach(function (button) {
      // The empty-state button is always visible inside its (hidden) box. The
      // one next to the count only appears once something is filtered.
      if (!button.closest('.pub-empty')) button.hidden = isDefault(state);
    });
    if (searchInput && normalize(searchInput.value).trim() !== normalize(state.q)) {
      searchInput.value = state.q;
    }
  }

  // On phones the chip rows scroll sideways. Bring the active chip into view
  // without moving the page (scrollIntoView would also scroll vertically).
  function revealActiveChips() {
    chips.forEach(function (chip) {
      if (chip.getAttribute('aria-pressed') !== 'true') return;
      var row = chip.parentElement;
      if (!row || row.scrollWidth <= row.clientWidth) return;
      var left = chip.offsetLeft - row.offsetLeft;
      var right = left + chip.offsetWidth;
      if (left < row.scrollLeft || right > row.scrollLeft + row.clientWidth) {
        row.scrollLeft = Math.max(0, left - 16);
      }
    });
  }

  // Typing waits 150ms before it filters. A chip clicked inside that window
  // must still see what was typed, or render() would put the old query back
  // in the box and the typed text would be lost.
  var searchTimer = null;

  function typedQuery() {
    window.clearTimeout(searchTimer);
    return searchInput ? searchInput.value.trim() : current.q;
  }

  // Paper pages link to /publication/#<CSL type>, so the four Workshop & Poster
  // papers (CSL `paper-conference`) send readers to the Conference list, which
  // does not include them. When the reader came from a paper on this list, use
  // that paper's own bucket instead. Returns null when that cannot be told.
  // Each row names its paper page in `data-page`. The title link can't be used
  // for this, because it opens the paper itself, off this site.
  function referrerType() {
    try {
      var from = new URL(document.referrer);
      if (from.origin !== window.location.origin) return null;
      for (var i = 0; i < items.length; i++) {
        var page = items[i].getAttribute('data-page');
        if (page && new URL(page, window.location.href).pathname === from.pathname) {
          return items[i].getAttribute('data-type');
        }
      }
    } catch (e) {
      // No referrer, or not a URL. Fall back to the CSL mapping.
    }
    return null;
  }

  function commit(next, mode) {
    if (sameState(next, current)) return;
    current = next;
    render(current);
    if (mode === 'push') window.history.pushState(null, '', urlFor(current, false));
    else window.history.replaceState(window.history.state, '', urlFor(current, true));
  }

  // ---- Initial state -------------------------------------------------------

  // A legacy hash such as #paper-conference becomes ?type=conference (or the
  // referring paper's own type), unless the URL already names a type. Other
  // hashes are real anchors and stay.
  var hash = window.location.hash.replace(/^#/, '');
  try {
    hash = decodeURIComponent(hash);
  } catch (e) {
    // A malformed %-escape is not one of ours. Leave the hash alone.
  }
  var legacyType = Object.prototype.hasOwnProperty.call(LEGACY_HASH_TYPES, hash) ? LEGACY_HASH_TYPES[hash] : null;
  var hadType = new URLSearchParams(window.location.search).has('type');
  if (legacyType !== null && !hadType) current.type = pick('type', referrerType() || legacyType);

  render(current);
  revealActiveChips();

  // Rewrite the address bar to the canonical form: invalid values dropped, a
  // legacy hash turned into ?type=. replaceState adds no history entry.
  var canonical = urlFor(current, legacyType === null);
  if (canonical !== window.location.pathname + window.location.search + window.location.hash) {
    window.history.replaceState(window.history.state, '', canonical);
  }

  // ---- Events --------------------------------------------------------------

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var next = { direction: current.direction, type: current.type, q: typedQuery() };
      next[chip.getAttribute('data-filter')] = chip.getAttribute('data-value');
      commit(next, 'push');
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(function () {
        commit({ direction: current.direction, type: current.type, q: typedQuery() }, 'replace');
      }, 150);
    });
    // Enter would otherwise do nothing useful. Apply the search at once.
    searchInput.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        commit({ direction: current.direction, type: current.type, q: typedQuery() }, 'replace');
      }
    });
  }

  resetButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      window.clearTimeout(searchTimer);
      if (searchInput) searchInput.value = '';
      commit({ direction: 'all', type: 'all', q: '' }, 'push');
      var first = root.querySelector('.pub-chip[data-filter="direction"]');
      if (first) first.focus();
    });
  });

  // Back and Forward: the URL is the source of truth.
  window.addEventListener('popstate', function () {
    window.clearTimeout(searchTimer);
    current = stateFromUrl();
    render(current);
    revealActiveChips();
  });
})();
