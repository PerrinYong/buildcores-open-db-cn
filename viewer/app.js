/* global fetch */

const INDEX_URL = "../dist/product_facts/index.json";

const qEl = document.getElementById("q");
const catEl = document.getElementById("cat");
const rowsEl = document.getElementById("rows");
const metaEl = document.getElementById("meta");

let all = [];
let filtered = [];

function esc(s) {
  return (s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function norm(s) {
  return (s || "").toString().toLowerCase();
}

function renderTable(list) {
  const maxRows = 2000;
  const slice = list.slice(0, maxRows);

  rowsEl.innerHTML = slice
    .map((r) => {
      const fileHref = `../${r.path}`;
      return `
        <tr>
          <td>${esc(r.category)}</td>
          <td>${esc(r.name)}</td>
          <td>${esc(r.manufacturer)}</td>
          <td><code>${esc(r.opendb_id)}</code></td>
          <td><a href="${esc(fileHref)}" target="_blank" rel="noreferrer">${esc(r.path)}</a></td>
        </tr>
      `;
    })
    .join("");

  metaEl.textContent = `Showing ${slice.length} / ${list.length} (cap ${maxRows}).`;
}

function applyFilters() {
  const q = norm(qEl.value);
  const cat = catEl.value;

  filtered = all.filter((r) => {
    if (cat && r.category !== cat) return false;
    if (!q) return true;
    const blob = `${r.category} ${r.name} ${r.manufacturer} ${r.opendb_id}`;
    return norm(blob).includes(q);
  });

  renderTable(filtered);
}

function initCategories() {
  const cats = Array.from(new Set(all.map((r) => r.category))).sort();
  for (const c of cats) {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    catEl.appendChild(opt);
  }
}

async function main() {
  metaEl.textContent = "Loading index.json...";
  const res = await fetch(INDEX_URL, { cache: "no-store" });
  if (!res.ok) {
    metaEl.textContent = `Failed to load ${INDEX_URL} (${res.status})`;
    return;
  }
  all = await res.json();
  initCategories();
  applyFilters();

  qEl.addEventListener("input", () => applyFilters());
  catEl.addEventListener("change", () => applyFilters());
}

main().catch((e) => {
  metaEl.textContent = `Error: ${e && e.message ? e.message : String(e)}`;
});
