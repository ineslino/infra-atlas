/* ════════════════════════════════════════════════════════════════════
   Toolbox · filter chips
   AND-mode across the active tag chips. A `.tbx-row` is kept when every
   active tag appears in its `data-tags`. No dependencies, no framework.
   Used by every /toolbox/<department>/ page.

   Filter state is deep-linkable: active tags are written to ?tags=TUI,Go
   and restored on load so shared URLs preserve the filter.
   ════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";
  var chips = Array.from(document.querySelectorAll(".tbx-chip"));
  var rows  = Array.from(document.querySelectorAll(".tbx-row"));
  var empty = document.getElementById("tbx-empty");
  if (!chips.length || !rows.length) return;

  function activeTags() {
    return chips
      .filter(function (c) { return c.classList.contains("is-active"); })
      .map(function (c) { return c.dataset.tag; });
  }

  function apply() {
    var tags = activeTags();
    var anyMatch = false;
    rows.forEach(function (r) {
      var rowTags = (r.dataset.tags || "").split(/\s+/);
      var match = tags.every(function (t) { return rowTags.indexOf(t) !== -1; });
      r.classList.toggle("is-hidden", !match);
      if (match) anyMatch = true;
    });
    if (empty) empty.hidden = anyMatch || tags.length === 0;
    // Sync filter state to URL so it is shareable / bookmarkable.
    var p = new URLSearchParams();
    if (tags.length) p.set("tags", tags.join(","));
    var q = p.toString();
    history.replaceState(null, "", q ? "?" + q : location.pathname);
  }

  // Restore filter state from URL on page load.
  (function () {
    var p = new URLSearchParams(location.search);
    var tagStr = p.get("tags");
    if (!tagStr) return;
    var urlTags = tagStr.split(",");
    var activated = 0;
    chips.forEach(function (c) {
      if (urlTags.indexOf(c.dataset.tag) !== -1) {
        c.classList.add("is-active");
        activated++;
      }
    });
    if (activated) apply();
  })();

  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      c.classList.toggle("is-active");
      apply();
    });
  });

  var clear = document.getElementById("tbx-clear");
  if (clear) {
    clear.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("is-active"); });
      apply();
    });
  }
})();
