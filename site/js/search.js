/* Search all templates on search.html.
 * Reads ?q= from the address bar, filters data/templates.json and updates the list as you type.
 *
 * Matching:
 * - Case does not matter, and punctuation is ignored.
 * - Whole words are matched, so "pay" does not match "repayment".
 * - Simple endings are ignored, so "budgets" finds "budget" and "invoices" finds "invoice".
 * - Words you are still typing match the start of a word, so "bud" finds "budget".
 * - Synonyms are included, so "grades" also finds gradebooks and mark sheets.
 * - Name matches count more than description matches. A template matching every word ranks first.
 */
(function () {
  var input = document.getElementById("searchPageInput");
  var list = document.getElementById("searchResults");
  var status = document.getElementById("searchStatus");
  var TINTS = ["tint-lavender", "tint-mint", "tint-blue", "tint-peach", "tint-cream"];
  var all = [];
  var indexed = [];

  if (!input || !list || !status) return;

  /* Words that mean the same thing in a classroom, office or home setting */
  var SYNONYMS = {
    grade: ["mark", "result"], mark: ["grade"], score: ["grade", "mark"],
    gradebook: ["grade", "mark"], result: ["grade"],
    pay: ["payroll", "salary", "wage"], payroll: ["pay", "salary", "wage"], salary: ["pay", "payroll"],
    wage: ["pay", "payroll"], payslip: ["payroll", "pay"],
    timesheet: ["hours", "overtime"], hours: ["timesheet"], overtime: ["timesheet", "hours"],
    timetable: ["schedule", "rota"], schedule: ["timetable", "rota"],
    rota: ["schedule", "roster", "timetable"], roster: ["rota"],
    invoice: ["bill", "billing"], bill: ["invoice"],
    expense: ["spending", "cost"], spending: ["expense"], cost: ["expense"],
    attendance: ["register"], register: ["attendance"],
    homework: ["assignment"], assignment: ["homework"],
    lesson: ["scheme"], scheme: ["lesson"],
    student: ["pupil", "learner"], pupil: ["student"], learner: ["student"],
    tax: ["vat"], vat: ["tax"],
    mileage: ["journey"],
    recipe: ["cooking", "baking"],
    workout: ["exercise", "fitness"], exercise: ["workout", "fitness"],
    holiday: ["vacation", "trip", "travel"],
    stock: ["inventory"], inventory: ["stock"],
    customer: ["client"], client: ["customer"],
    debt: ["loan"], loan: ["debt"]
  };

  /* Simple word endings: budgets -> budget, invoices -> invoice, entries -> entry */
  function stem(w) {
    if (w.length > 4 && /ies$/.test(w)) return w.slice(0, -3) + "y";
    if (w.length > 3 && /s$/.test(w) && !/(ss|us|is)$/.test(w)) w = w.slice(0, -1);
    if (w.length > 3 && /e$/.test(w)) w = w.slice(0, -1);
    return w;
  }

  function tokens(text) {
    return text.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean).map(stem);
  }

  var SYN = {};
  Object.keys(SYNONYMS).forEach(function (k) {
    SYN[stem(k)] = SYNONYMS[k].map(stem);
  });

  /* Each typed word becomes a list of variants: the word itself (weight 1) and its synonyms (weight 0.6) */
  function buildTerms(q) {
    return tokens(q).map(function (s) {
      var variants = [{ v: s, w: 1, exact: false }];
      (SYN[s] || []).forEach(function (x) { variants.push({ v: x, w: 0.6, exact: true }); });
      return variants;
    });
  }

  /* A word matches a whole word. Typed words (not synonyms) also match the start of a longer word,
     so "bud" finds "budget". Synonyms need the whole word, so "mark" does not find "marketing". */
  function wordMatches(variant, word) {
    return word === variant.v || (!variant.exact && variant.v.length >= 3 && word.indexOf(variant.v) === 0);
  }

  function scoreTemplate(entry, terms) {
    var score = 0, matched = 0;
    for (var i = 0; i < terms.length; i++) {
      var best = 0;
      for (var j = 0; j < terms[i].length; j++) {
        var variant = terms[i][j];
        var inName = entry.name.some(function (x) { return wordMatches(variant, x); });
        var inRest = !inName && entry.rest.some(function (x) { return wordMatches(variant, x); });
        var s = inName ? 3 * variant.w : (inRest ? 1 * variant.w : 0);
        if (s > best) best = s;
      }
      if (best > 0) { matched++; score += best; }
    }
    if (matched === 0) return null;
    var every = matched === terms.length;
    return { score: score + (every ? 10 : 0), every: every };
  }

  /* Templates matching every word come first. Templates matching only some words follow, so a
     search for several words still shows useful results when no template matches them all. */
  function search(q) {
    var terms = buildTerms(q);
    if (terms.length === 0) return [];
    var hits = [];
    indexed.forEach(function (entry) {
      var r = scoreTemplate(entry, terms);
      if (r) hits.push({ t: entry.t, score: r.score, every: r.every });
    });
    hits.sort(function (a, b) {
      return b.score - a.score || a.t.name.localeCompare(b.t.name);
    });
    return hits;
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  }

  function card(t, i) {
    var li = el("li", "tpl-card " + TINTS[i % TINTS.length]);
    li.appendChild(el("span", "search-cat", t.categoryName));
    li.appendChild(el("h3", "", t.name));
    li.appendChild(el("p", "", t.description));
    var a = el("a", "dl", "Download .xlsx");
    a.href = t.file;
    a.setAttribute("aria-label", "Download " + t.name + " (Excel file)");
    li.appendChild(a);
    return li;
  }

  function render(q) {
    list.innerHTML = "";
    if (q === "") {
      status.textContent = "Type a word to search " + all.length + " templates.";
      return;
    }
    var hits = search(q);
    if (hits.length === 0) {
      status.textContent = "No templates match “" + q + "”. Try a shorter word or a related one.";
      return;
    }
    if (hits[0].every) {
      status.textContent = hits.length + (hits.length === 1 ? " template" : " templates") + " found";
    } else {
      status.textContent = "No template matches every word. Showing " + hits.length +
        (hits.length === 1 ? " closest match" : " closest matches");
    }
    hits.forEach(function (h, i) { list.appendChild(card(h.t, i)); });
  }

  function update() {
    var q = input.value.trim();
    render(q);
    var url = new URL(window.location.href);
    if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
    history.replaceState(null, "", url.pathname + url.search);
  }

  input.value = new URLSearchParams(window.location.search).get("q") || "";
  input.addEventListener("input", update);

  fetch("data/templates.json", { cache: "no-store" })
    .then(function (r) {
      if (!r.ok) throw new Error("status " + r.status);
      return r.json();
    })
    .then(function (data) {
      all = data.templates;
      indexed = all.map(function (t) {
        return { t: t, name: tokens(t.name), rest: tokens(t.description + " " + t.categoryName) };
      });
      update();
    })
    .catch(function () {
      status.textContent = "The templates could not be loaded. Please try again later.";
    });
})();
