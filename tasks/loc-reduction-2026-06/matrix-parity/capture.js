// Black-box DOM-parity harness for Infra Atlas matrix pages.
// Loads a page in jsdom, runs its real scripts, then fingerprints the rendered
// matrix + a fixed sequence of interactions. Same input page -> deterministic
// fingerprint. Used to prove a refactor preserves behaviour (old hash == new hash).
const fs = require("fs");
const path = require("path");
const { JSDOM, ResourceLoader } = require("jsdom");

const REPO = "/Users/ineslino/Documents/Repos/Personal-Repos/infraatlas";

function djb2(str) {
  let h = 5381;
  for (let i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) >>> 0;
  return h.toString(16);
}

class Loader extends ResourceLoader {
  fetch(url) {
    let u;
    try { u = new URL(url); } catch { return Promise.resolve(Buffer.from("")); }
    if (u.hostname !== "localhost") return Promise.resolve(Buffer.from("")); // skip external (fonts)
    let p = decodeURIComponent(u.pathname);
    if (p.endsWith("/")) p += "index.html";
    if (p.endsWith(".css")) return Promise.resolve(Buffer.from("")); // CSS irrelevant to DOM/JS
    try { return Promise.resolve(fs.readFileSync(path.join(REPO, p))); }
    catch { return Promise.resolve(Buffer.from("")); }
  }
}

function findTable(doc) {
  // the rendered matrix is the table that contains .feature-row rows
  const t = doc.querySelector("table");
  if (t) return t;
  const fr = doc.querySelector(".feature-row");
  return fr ? fr.closest("table") : null;
}

function visibleFeatureIds(doc) {
  return [...doc.querySelectorAll("tr.feature-row")]
    .filter((r) => !r.classList.contains("is-hidden"))
    .map((r) => r.dataset.feature)
    .join(",");
}

async function load(page, hash) {
  const file = path.join(REPO, page, "index.html");
  const html = fs.readFileSync(file, "utf8");
  const dom = new JSDOM(html, {
    runScripts: "dangerously",
    resources: new Loader(),
    pretendToBeVisual: true,
    url: "http://localhost/" + page + "/" + (hash || ""),
  });
  await new Promise((res) => {
    if (dom.window.document.readyState === "complete") return res();
    dom.window.addEventListener("load", res);
    setTimeout(res, 1500); // safety
  });
  await new Promise((r) => setTimeout(r, 50)); // let bootstrap settle
  return dom;
}

async function fingerprint(page) {
  const fp = { page };
  const dom = await load(page, "");
  const { document: doc, window: win } = dom.window;

  const table = findTable(doc);
  fp.tableFound = !!table;
  if (!table) { dom.window.close(); return fp; }

  fp.featureRows = doc.querySelectorAll("tr.feature-row").length;
  fp.categoryRows = doc.querySelectorAll("tr.category-row").length;
  fp.headerCols = doc.querySelectorAll("thead th").length;
  fp.cellButtons = doc.querySelectorAll("button.cell__btn").length;
  fp.tableHash = djb2(table.innerHTML);
  fp.visibleInitial = visibleFeatureIds(doc);

  // chips: click each once in order, capturing the resulting visible set + hash.
  const chips = [...doc.querySelectorAll(".filter-chips .chip, .filters .chip, .chip")];
  fp.chipCount = chips.length;
  fp.chipSeq = [];
  chips.forEach((c, i) => {
    c.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
    fp.chipSeq.push({ i, txt: (c.textContent || "").trim().slice(0, 24), vis: djb2(visibleFeatureIds(doc)), hash: win.location.hash });
  });

  // search box, if any
  const search = doc.querySelector('input[type="search"], .filter-search input, input.filter-search, input[placeholder*="earch"]');
  fp.hasSearch = !!search;
  if (search) {
    fp.searchSeq = [];
    ["a", "az", ""].forEach((term) => {
      search.value = term;
      search.dispatchEvent(new win.Event("input", { bubbles: true }));
      fp.searchSeq.push({ term, vis: djb2(visibleFeatureIds(doc)) });
    });
  }

  // drawer: open via first + last cell button, capture drawer head/body
  const cells = [...doc.querySelectorAll("button.cell__btn")];
  fp.drawerSeq = [];
  [cells[0], cells[Math.floor(cells.length / 2)], cells[cells.length - 1]].forEach((b, k) => {
    if (!b) return;
    b.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
    const head = doc.querySelector(".drawer__head");
    const body = doc.querySelector(".drawer__body");
    fp.drawerSeq.push({ k, head: djb2(head ? head.innerHTML : ""), body: djb2(body ? body.innerHTML : ""), bodyLen: body ? body.innerHTML.length : 0 });
  });
  // feature-row header button drawer
  const fbtn = doc.querySelector("button.feature-col__btn");
  if (fbtn) {
    fbtn.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
    const body = doc.querySelector(".drawer__body");
    fp.featureDrawer = djb2(body ? body.innerHTML : "");
  }

  dom.window.close();
  return fp;
}

(async () => {
  const pages = process.argv.slice(2);
  const out = {};
  for (const p of pages) {
    try { out[p] = await fingerprint(p); }
    catch (e) { out[p] = { page: p, error: String(e && e.message || e) }; }
  }
  console.log(JSON.stringify(out, null, 2));
})();
