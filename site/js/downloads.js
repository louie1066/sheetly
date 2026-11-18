/* Download counts and the Most Downloaded page.
 * Loaded with <script src="..." defer>. The data-root attribute is set by the page's
 * position in the site: "../" for pages in subfolders, "" for root pages (see the script tag). */
(function () {
  var script = document.currentScript;
  var root = (script && script.getAttribute("data-root")) || "";
  var status = document.getElementById("countsStatus");

  function fetchJSON(path) {
    return fetch(root + path, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(path + " returned " + r.status);
      return r.json();
    });
  }

  function countText(n) {
    return "Downloads: " + n.toLocaleString() + (n === 1 ? " time" : " times");
  }

  function fillCategoryCounts(counts) {
    document.querySelectorAll(".dl-count[data-count-slug]").forEach(function (el) {
      var n = counts[el.getAttribute("data-count-slug")] || 0;
      el.textContent = countText(n);
    });
  }

  function setStatus(text) {
    if (status) status.textContent = text;
  }

  function pageFromURL(totalPages) {
    var p = parseInt(new URLSearchParams(window.location.search).get("page"), 10);
    if (isNaN(p) || p < 1) return 1;
    return Math.min(p, totalPages);
  }

  function renderPopular(templates, counts, pageSize) {
    var list = document.getElementById("rankList");
    var pager = document.getElementById("pager");
    if (!list) return;

    var ranked = templates.map(function (t) {
      return { t: t, n: counts[t.slug] || 0 };
    }).sort(function (a, b) {
      return b.n - a.n || a.t.name.localeCompare(b.t.name);
    });

    var totalPages = Math.max(1, Math.ceil(ranked.length / pageSize));
    var current = pageFromURL(totalPages);
    var start = (current - 1) * pageSize;

    list.innerHTML = "";
    ranked.slice(start, start + pageSize).forEach(function (item, i) {
      var li = document.createElement("li");
      li.className = "rank-item";

      var rank = document.createElement("span");
      rank.className = "rank-no";
      rank.textContent = "#" + (start + i + 1);

      var info = document.createElement("div");
      info.className = "rank-info";
      var name = document.createElement("strong");
      name.textContent = item.t.name;
      var meta = document.createElement("span");
      meta.className = "rank-meta";
      meta.textContent = item.t.categoryName + " · " + countText(item.n);
      info.appendChild(name);
      info.appendChild(meta);

      var a = document.createElement("a");
      a.className = "dl";
      a.href = root + item.t.file;
      a.textContent = "Download .xlsx";
      a.setAttribute("aria-label", "Download " + item.t.name + " (Excel file)");

      li.appendChild(rank);
      li.appendChild(info);
      li.appendChild(a);
      list.appendChild(li);
    });

    if (pager) {
      pager.innerHTML = "";
      if (totalPages > 1) {
        pager.appendChild(pagerLink("Previous", current - 1, current > 1));
        for (var p = 1; p <= totalPages; p++) {
          var num = pagerLink(String(p), p, true);
          if (p === current) {
            num.setAttribute("aria-current", "page");
            num.classList.add("is-current");
          }
          pager.appendChild(num);
        }
        pager.appendChild(pagerLink("Next", current + 1, current < totalPages));
      }
    }
  }

  function pagerLink(label, page, enabled) {
    var el;
    if (enabled) {
      el = document.createElement("a");
      el.href = "?page=" + page;
    } else {
      el = document.createElement("span");
      el.setAttribute("aria-disabled", "true");
    }
    el.className = "pager-link";
    el.textContent = label;
    return el;
  }

  var hasCategoryCounts = document.querySelector(".dl-count[data-count-slug]");
  var hasPopularList = document.getElementById("rankList");

  if (hasCategoryCounts || hasPopularList) {
    var countsReady = fetchJSON("api/counts").catch(function () { return null; });

    countsReady.then(function (counts) {
      if (hasCategoryCounts) {
        if (counts) {
          fillCategoryCounts(counts);
        } else {
          document.querySelectorAll(".dl-count[data-count-slug]").forEach(function (el) {
            el.textContent = "Download count unavailable";
          });
        }
      }

      if (hasPopularList) {
        fetchJSON("data/templates.json").then(function (data) {
          if (!counts) {
            setStatus("Download counts are unavailable right now. Showing the list without counts.");
            counts = {};
          }
          renderPopular(data.templates, counts, data.pageSize);
        }).catch(function () {
          setStatus("The template list could not be loaded.");
        });
      }
    });
  }
})();
