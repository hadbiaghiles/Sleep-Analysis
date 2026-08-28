#!/usr/bin/env python3
"""Build docs/index.html — a static bilingual dashboard for GitHub Pages."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "sleep_health_lifestyle_dataset.csv"
OUT = ROOT / "docs" / "index.html"


def load_rows():
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        for raw in csv.DictReader(fh):
            sys_, dia = raw["Blood Pressure"].split("/")
            disorder = raw["Sleep Disorder"] or "None"
            if disorder in ("", "No sleep disorder"):
                disorder = "None"
            rows.append(
                {
                    "id": int(raw["Person ID"]),
                    "gender": raw["Gender"],
                    "age": int(raw["Age"]),
                    "occupation": raw["Occupation"],
                    "sleep": float(raw["Sleep Duration"]),
                    "quality": int(raw["Quality of Sleep"]),
                    "activity": int(raw["Physical Activity Level"]),
                    "stress": int(raw["Stress Level"]),
                    "bmi": raw["BMI Category"],
                    "systolic": int(sys_),
                    "diastolic": int(dia),
                    "heart": int(raw["Heart Rate"]),
                    "steps": int(raw["Daily Steps"]),
                    "disorder": disorder,
                }
            )
    return rows


def main() -> None:
    rows = load_rows()
    payload = json.dumps(rows, separators=(",", ":"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.replace("__DATA__", payload)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(rows)} rows)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sleep Health and Lifestyle</title>
  <meta name="description" content="Public dashboard for the Sleep Health and Lifestyle dataset. English by default, French on demand." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,520;9..144,640&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
  <style>
    :root {
      --bg: #08111f;
      --bg-2: #101a2e;
      --card: #141e33;
      --line: rgba(125, 211, 199, 0.16);
      --text: #eaf0ff;
      --muted: #9aa8c7;
      --teal: #7dd3c7;
      --indigo: #9aa7ff;
      --sand: #f0ab73;
      --rose: #f0718d;
      --shadow: 0 18px 50px rgba(0,0,0,.35);
      --radius: 18px;
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: radial-gradient(1200px 700px at 10% -10%, #1a2744 0%, var(--bg) 55%); color: var(--text); font-family: "Source Sans 3", system-ui, sans-serif; }
    body { min-height: 100vh; }
    a { color: var(--teal); }
    header {
      position: sticky; top: 0; z-index: 20;
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
      padding: 16px 28px;
      background: rgba(8,17,31,.78);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--line);
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .mark {
      width: 42px; height: 42px; border-radius: 14px;
      display: grid; place-items: center;
      background: linear-gradient(145deg, #1d3a45, #14233a);
      border: 1px solid var(--line); font-size: 22px;
    }
    .brand h1 { font-family: Fraunces, Georgia, serif; font-size: 1.25rem; margin: 0; letter-spacing: -0.02em; }
    .brand p { margin: 0; color: var(--muted); font-size: .85rem; }
    .lang {
      display: inline-flex; padding: 4px; border-radius: 999px;
      border: 1px solid var(--line); background: var(--bg-2);
    }
    .lang button {
      appearance: none; border: 0; background: transparent; color: var(--muted);
      padding: 8px 14px; border-radius: 999px; cursor: pointer; font: inherit; font-weight: 600;
    }
    .lang button[aria-pressed="true"] { background: var(--teal); color: #06201c; }
    main { width: min(1180px, calc(100% - 32px)); margin: 24px auto 64px; }
    .hero { margin-bottom: 22px; }
    .hero h2 { font-family: Fraunces, Georgia, serif; font-weight: 640; font-size: clamp(1.8rem, 3vw, 2.6rem); margin: 0 0 8px; letter-spacing: -0.03em; }
    .hero p { margin: 0; color: var(--muted); max-width: 62ch; font-size: 1.05rem; }
    .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 22px 0; }
    .kpi {
      background: linear-gradient(180deg, rgba(20,30,51,.95), rgba(12,20,36,.95));
      border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 18px; box-shadow: var(--shadow);
    }
    .kpi span { display: block; color: var(--muted); font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; }
    .kpi strong { display: block; font-family: Fraunces, Georgia, serif; font-size: 1.8rem; margin-top: 6px; }
    .filters {
      display: grid; grid-template-columns: 1fr 1fr 1.3fr 1fr auto;
      gap: 12px; align-items: end;
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      padding: 16px; margin-bottom: 22px;
    }
    label { display: flex; flex-direction: column; gap: 6px; font-size: .82rem; color: var(--muted); }
    select, input[type="range"] { width: 100%; }
    select {
      background: #0d1730; color: var(--text); border: 1px solid var(--line);
      border-radius: 10px; padding: 8px; min-height: 42px; font: inherit;
    }
    button.reset {
      height: 42px; border-radius: 10px; border: 1px solid var(--line);
      background: transparent; color: var(--text); cursor: pointer; font: inherit; font-weight: 600; padding: 0 14px;
    }
    button.reset:hover { border-color: var(--teal); color: var(--teal); }
    .note { color: var(--muted); margin: -8px 0 18px; font-size: .92rem; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card {
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      padding: 8px 8px 14px; box-shadow: var(--shadow);
    }
    .card.wide { grid-column: 1 / -1; }
    .caption { color: var(--muted); padding: 0 12px; font-size: .9rem; margin: 0; }
    .insights {
      background: linear-gradient(135deg, rgba(125,211,199,.08), rgba(154,167,255,.08));
      border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 22px; margin: 18px 0;
    }
    .insights h3 { margin: 0 0 8px; font-family: Fraunces, Georgia, serif; }
    .insights ul { margin: 0; padding-left: 18px; color: var(--text); }
    .insights li { margin: 6px 0; }
    footer { color: var(--muted); font-size: .88rem; margin-top: 28px; border-top: 1px solid var(--line); padding-top: 16px; }
    .empty { padding: 28px; text-align: center; color: var(--muted); }
    @media (max-width: 900px) {
      .kpis, .filters, .grid { grid-template-columns: 1fr 1fr; }
      .filters { grid-template-columns: 1fr 1fr; }
      header { flex-wrap: wrap; }
    }
    @media (max-width: 560px) {
      .kpis, .filters, .grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="mark" aria-hidden="true">💤</div>
      <div>
        <h1 id="brandTitle">Sleep Health and Lifestyle</h1>
        <p id="brandBy">Hadbi Aghiles</p>
      </div>
    </div>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" id="btn-en" aria-pressed="true">English</button>
      <button type="button" id="btn-fr" aria-pressed="false">Français</button>
    </div>
  </header>
  <main>
    <section class="hero">
      <h2 id="heroTitle"></h2>
      <p id="heroTag"></p>
    </section>
    <section class="kpis">
      <article class="kpi"><span id="k1l"></span><strong id="k1v">—</strong></article>
      <article class="kpi"><span id="k2l"></span><strong id="k2v">—</strong></article>
      <article class="kpi"><span id="k3l"></span><strong id="k3v">—</strong></article>
      <article class="kpi"><span id="k4l"></span><strong id="k4v">—</strong></article>
    </section>
    <section class="filters">
      <label><span id="lGender"></span><select id="fGender" multiple size="3"></select></label>
      <label><span id="lBmi"></span><select id="fBmi" multiple size="3"></select></label>
      <label><span id="lOcc"></span><select id="fOcc" multiple size="3"></select></label>
      <label>
        <span id="lAge"></span>
        <div style="display:flex;gap:8px;align-items:center">
          <input id="ageMin" type="range" min="27" max="59" value="27" />
          <input id="ageMax" type="range" min="27" max="59" value="59" />
        </div>
        <span id="ageVal" style="color:var(--text)"></span>
      </label>
      <button class="reset" id="btnReset" type="button"></button>
    </section>
    <p class="note" id="filterNote"></p>
    <section class="insights">
      <h3 id="insightTitle"></h3>
      <ul id="insightList"></ul>
    </section>
    <section class="grid">
      <article class="card"><div id="cAge"></div><p class="caption" id="capAge"></p></article>
      <article class="card"><div id="cGender"></div><p class="caption" id="capGender"></p></article>
      <article class="card wide"><div id="cCorr"></div><p class="caption" id="capCorr"></p></article>
      <article class="card"><div id="cDis"></div><p class="caption" id="capDis"></p></article>
      <article class="card"><div id="cBmi"></div><p class="caption" id="capBmi"></p></article>
      <article class="card wide"><div id="cOcc"></div><p class="caption" id="capOcc"></p></article>
      <article class="card wide"><div id="cScatter"></div><p class="caption" id="capScatter"></p></article>
    </section>
    <div id="empty" class="empty" hidden></div>
    <footer id="footer"></footer>
  </main>
  <script>
    const DATA = __DATA__;
    const LABELS = {
      Gender: { en: {Male:"Male", Female:"Female"}, fr: {Male:"Homme", Female:"Femme"} },
      BMI: { en: {Normal:"Normal", "Normal Weight":"Normal Weight", Overweight:"Overweight", Obese:"Obese"},
             fr: {Normal:"Normal", "Normal Weight":"Poids normal", Overweight:"Surpoids", Obese:"Obèse"} },
      Disorder: { en: {None:"None", Insomnia:"Insomnia", "Sleep Apnea":"Sleep Apnea"},
                  fr: {None:"Aucun", Insomnia:"Insomnie", "Sleep Apnea":"Apnée du sommeil"} },
      Occupation: {
        en: {"Software Engineer":"Software Engineer", Doctor:"Doctor", "Sales Representative":"Sales Representative", Teacher:"Teacher", Nurse:"Nurse", Engineer:"Engineer", Accountant:"Accountant", Scientist:"Scientist", Lawyer:"Lawyer", Salesperson:"Salesperson", Manager:"Manager"},
        fr: {"Software Engineer":"Ingénieur logiciel", Doctor:"Médecin", "Sales Representative":"Représentant commercial", Teacher:"Enseignant", Nurse:"Infirmier", Engineer:"Ingénieur", Accountant:"Comptable", Scientist:"Scientifique", Lawyer:"Avocat", Salesperson:"Vendeur", Manager:"Cadre"}
      }
    };
    const UI = {
      en: {
        brand: "Sleep Health and Lifestyle",
        by: "Hadbi Aghiles",
        hero: "How sleep, stress and lifestyle fit together",
        tag: "A public dashboard on the Sleep Health and Lifestyle dataset (Kaggle uom190346a). English is the default; switch to French whenever you like — same app, not a second site.",
        k1: "People", k2: "Avg. sleep (h)", k3: "Avg. quality", k4: "Disorder rate",
        gender: "Gender", bmi: "BMI category", occ: "Occupation", age: "Age range", reset: "Reset",
        note: (n, t) => `Showing ${n} of ${t} records after filters.`,
        empty: "No rows match the current filters.",
        insight: "Highlights",
        capAge: "Most people in this sample are between 30 and 50.",
        capGender: "Typical sleep hours and spread for men and women.",
        capCorr: "Sleep duration and quality usually move together; stress tends to move the other way.",
        capDis: "None means no recorded disorder. Insomnia and sleep apnea are the two coded conditions.",
        capBmi: "Higher BMI categories often sit with slightly lower subjective sleep quality.",
        capOcc: "Occupation is a lifestyle proxy: some roles cluster at higher reported stress.",
        capScatter: "Each point is a person. Colour shows sleep disorder status.",
        titles: {age:"Age distribution", gender:"Sleep duration by gender", corr:"Correlation heatmap", dis:"Sleep disorders", bmi:"Sleep quality by BMI", occ:"Average stress by occupation", scatter:"Sleep duration vs stress"},
        axes: {age:"Age", hours:"Sleep duration (h)", quality:"Quality of sleep", stress:"Stress level", occ:"Occupation", disorder:"Sleep disorder", gender:"Gender", bmi:"BMI"},
        footer: "Built by Hadbi Aghiles · Dataset: Sleep Health and Lifestyle (Kaggle). Source is included in the repository. Streamlit app: run app.py locally or on Streamlit Community Cloud.",
        iDis: (v) => `Sleep-disorder rate in the current view: ${v}.`,
        iBmi: (lab, v) => `Lowest average sleep quality: ${lab} (${v}/10).`,
        iOcc: (lab, v) => `Highest average stress: ${lab} (${v}/10).`,
        iCorr: (v) => `Correlation of sleep duration vs stress: ${v}.`
      },
      fr: {
        brand: "Santé du sommeil et mode de vie",
        by: "Hadbi Aghiles",
        hero: "Comment le sommeil, le stress et le mode de vie s'articulent",
        tag: "Tableau de bord public du jeu Sleep Health and Lifestyle (Kaggle uom190346a). L'anglais est la langue par défaut ; passez au français quand vous le souhaitez — une seule application.",
        k1: "Personnes", k2: "Sommeil moy. (h)", k3: "Qualité moy.", k4: "Taux de troubles",
        gender: "Genre", bmi: "Catégorie IMC", occ: "Profession", age: "Tranche d'âge", reset: "Réinitialiser",
        note: (n, t) => `Affichage de ${n} enregistrements sur ${t} après filtres.`,
        empty: "Aucun enregistrement ne correspond aux filtres.",
        insight: "Points clés",
        capAge: "La plupart des personnes de l'échantillon ont entre 30 et 50 ans.",
        capGender: "Heures de sommeil typiques et dispersion pour les hommes et les femmes.",
        capCorr: "Durée et qualité du sommeil évoluent souvent ensemble ; le stress va généralement en sens inverse.",
        capDis: "Aucun signifie aucun trouble enregistré. Insomnie et apnée sont les deux affections codées.",
        capBmi: "Les catégories d'IMC plus élevées s'accompagnent souvent d'une qualité un peu plus basse.",
        capOcc: "La profession est un proxy de mode de vie : certains métiers se regroupent à un stress plus élevé.",
        capScatter: "Chaque point est une personne. La couleur indique le trouble du sommeil.",
        titles: {age:"Répartition des âges", gender:"Durée de sommeil par genre", corr:"Carte de chaleur des corrélations", dis:"Troubles du sommeil", bmi:"Qualité du sommeil par IMC", occ:"Stress moyen par profession", scatter:"Durée de sommeil vs stress"},
        axes: {age:"Âge", hours:"Durée de sommeil (h)", quality:"Qualité du sommeil", stress:"Niveau de stress", occ:"Profession", disorder:"Trouble du sommeil", gender:"Genre", bmi:"IMC"},
        footer: "Réalisé par Hadbi Aghiles · Jeu de données : Sleep Health and Lifestyle (Kaggle). Le fichier source est dans le dépôt. Application Streamlit : lancer app.py en local ou sur Streamlit Community Cloud.",
        iDis: (v) => `Taux de trouble du sommeil dans la vue actuelle : ${v}.`,
        iBmi: (lab, v) => `Qualité de sommeil la plus basse : ${lab} (${v}/10).`,
        iOcc: (lab, v) => `Stress moyen le plus élevé : ${lab} (${v}/10).`,
        iCorr: (v) => `Corrélation durée de sommeil ↔ stress : ${v}.`
      }
    };

    const layoutBase = {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(8,17,31,0.2)",
      font: { color: "#eaf0ff", family: "Source Sans 3, sans-serif", size: 12 },
      margin: { l: 48, r: 18, t: 48, b: 48 },
      colorway: ["#7dd3c7", "#9aa7ff", "#f0ab73", "#f0718d", "#c4b5fd", "#67e8f9"],
      legend: { orientation: "h", y: 1.08 }
    };
    const cfg = { responsive: true, displaylogo: false, modeBarButtonsToRemove: ["lasso2d", "select2d"] };

    let lang = localStorage.getItem("sleep-lang") === "fr" ? "fr" : "en";

    function uniq(key) {
      return [...new Set(DATA.map(d => d[key]))].sort();
    }
    function fillSelect(el, values, map) {
      el.innerHTML = "";
      values.forEach(v => {
        const o = document.createElement("option");
        o.value = v; o.textContent = map[v] || v; el.appendChild(o);
      });
    }
    function selected(el) {
      return [...el.selectedOptions].map(o => o.value);
    }
    function mean(arr) {
      return arr.length ? arr.reduce((a,b)=>a+b,0) / arr.length : NaN;
    }
    function corr(xs, ys) {
      const n = xs.length;
      if (n < 3) return NaN;
      const mx = mean(xs), my = mean(ys);
      let num = 0, dx = 0, dy = 0;
      for (let i = 0; i < n; i++) {
        const a = xs[i] - mx, b = ys[i] - my;
        num += a * b; dx += a * a; dy += b * b;
      }
      return num / Math.sqrt(dx * dy);
    }
    function filtered() {
      const g = selected(document.getElementById("fGender"));
      const b = selected(document.getElementById("fBmi"));
      const o = selected(document.getElementById("fOcc"));
      let amin = Number(document.getElementById("ageMin").value);
      let amax = Number(document.getElementById("ageMax").value);
      if (amin > amax) [amin, amax] = [amax, amin];
      return DATA.filter(d =>
        (g.length === 0 || g.includes(d.gender)) &&
        (b.length === 0 || b.includes(d.bmi)) &&
        (o.length === 0 || o.includes(d.occupation)) &&
        d.age >= amin && d.age <= amax
      );
    }

    function applyLang() {
      const ui = UI[lang];
      document.documentElement.lang = lang;
      document.title = ui.brand;
      document.getElementById("brandTitle").textContent = ui.brand;
      document.getElementById("brandBy").textContent = ui.by;
      document.getElementById("heroTitle").textContent = ui.hero;
      document.getElementById("heroTag").textContent = ui.tag;
      document.getElementById("k1l").textContent = ui.k1;
      document.getElementById("k2l").textContent = ui.k2;
      document.getElementById("k3l").textContent = ui.k3;
      document.getElementById("k4l").textContent = ui.k4;
      document.getElementById("lGender").textContent = ui.gender;
      document.getElementById("lBmi").textContent = ui.bmi;
      document.getElementById("lOcc").textContent = ui.occ;
      document.getElementById("lAge").textContent = ui.age;
      document.getElementById("btnReset").textContent = ui.reset;
      document.getElementById("insightTitle").textContent = ui.insight;
      document.getElementById("capAge").textContent = ui.capAge;
      document.getElementById("capGender").textContent = ui.capGender;
      document.getElementById("capCorr").textContent = ui.capCorr;
      document.getElementById("capDis").textContent = ui.capDis;
      document.getElementById("capBmi").textContent = ui.capBmi;
      document.getElementById("capOcc").textContent = ui.capOcc;
      document.getElementById("capScatter").textContent = ui.capScatter;
      document.getElementById("footer").innerHTML = ui.footer;
      document.getElementById("empty").textContent = ui.empty;
      document.getElementById("btn-en").setAttribute("aria-pressed", lang === "en" ? "true" : "false");
      document.getElementById("btn-fr").setAttribute("aria-pressed", lang === "fr" ? "true" : "false");
      fillSelect(document.getElementById("fGender"), uniq("gender"), LABELS.Gender[lang]);
      fillSelect(document.getElementById("fBmi"), uniq("bmi"), LABELS.BMI[lang]);
      fillSelect(document.getElementById("fOcc"), uniq("occupation"), LABELS.Occupation[lang]);
    }

    function render() {
      const ui = UI[lang];
      const rows = filtered();
      const amin = Math.min(document.getElementById("ageMin").value, document.getElementById("ageMax").value);
      const amax = Math.max(document.getElementById("ageMin").value, document.getElementById("ageMax").value);
      document.getElementById("ageVal").textContent = `${amin} – ${amax}`;
      document.getElementById("filterNote").textContent = ui.note(rows.length, DATA.length);

      const empty = document.getElementById("empty");
      const grid = document.querySelector(".grid");
      if (!rows.length) {
        empty.hidden = false; grid.style.opacity = 0.25;
      } else {
        empty.hidden = true; grid.style.opacity = 1;
      }

      const n = rows.length;
      const sleep = mean(rows.map(r => r.sleep));
      const quality = mean(rows.map(r => r.quality));
      const disRate = n ? 100 * rows.filter(r => r.disorder !== "None").length / n : 0;
      document.getElementById("k1v").textContent = n.toLocaleString(lang === "fr" ? "fr" : "en");
      document.getElementById("k2v").textContent = n ? sleep.toFixed(2) : "—";
      document.getElementById("k3v").textContent = n ? quality.toFixed(2) : "—";
      document.getElementById("k4v").textContent = n ? disRate.toFixed(1) + "%" : "—";

      const insight = document.getElementById("insightList");
      insight.innerHTML = "";
      if (n) {
        const byBmi = {};
        const byOcc = {};
        rows.forEach(r => {
          (byBmi[r.bmi] ||= []).push(r.quality);
          (byOcc[r.occupation] ||= []).push(r.stress);
        });
        const bmiAvg = Object.entries(byBmi).map(([k,v]) => [k, mean(v)]).sort((a,b)=>a[1]-b[1]);
        const occAvg = Object.entries(byOcc).map(([k,v]) => [k, mean(v)]).sort((a,b)=>b[1]-a[1]);
        const cs = corr(rows.map(r=>r.sleep), rows.map(r=>r.stress));
        const items = [
          ui.iDis(disRate.toFixed(1) + "%"),
          bmiAvg[0] ? ui.iBmi(LABELS.BMI[lang][bmiAvg[0][0]] || bmiAvg[0][0], bmiAvg[0][1].toFixed(2)) : "",
          occAvg[0] ? ui.iOcc(LABELS.Occupation[lang][occAvg[0][0]] || occAvg[0][0], occAvg[0][1].toFixed(2)) : "",
          ui.iCorr(Number.isFinite(cs) ? cs.toFixed(2) : "—")
        ];
        items.filter(Boolean).forEach(text => {
          const li = document.createElement("li"); li.textContent = text; insight.appendChild(li);
        });
      }

      if (!n) return;

      Plotly.react("cAge", [{
        x: rows.map(r => r.age), type: "histogram", nbinsx: 12, marker: { color: "#7dd3c7" }
      }], Object.assign({}, layoutBase, { title: ui.titles.age, xaxis: { title: ui.axes.age }, height: 340 }), cfg);

      const genders = uniq("gender");
      Plotly.react("cGender", genders.map(g => ({
        y: rows.filter(r => r.gender === g).map(r => r.sleep),
        name: LABELS.Gender[lang][g], type: "box", boxpoints: "all", jitter: 0.3
      })), Object.assign({}, layoutBase, { title: ui.titles.gender, yaxis: { title: ui.axes.hours }, height: 340 }), cfg);

      const keys = ["age","sleep","quality","activity","stress","systolic","diastolic","heart","steps"];
      const labels = lang === "fr"
        ? ["Âge","Sommeil","Qualité","Activité","Stress","Systolique","Diastolique","FC","Pas"]
        : ["Age","Sleep","Quality","Activity","Stress","Systolic","Diastolic","HR","Steps"];
      const z = keys.map(a => keys.map(b => {
        const c = corr(rows.map(r => r[a]), rows.map(r => r[b]));
        return Number.isFinite(c) ? +c.toFixed(2) : 0;
      }));
      Plotly.react("cCorr", [{
        z, x: labels, y: labels, type: "heatmap", colorscale: "Tealrose", zmid: 0,
        text: z, texttemplate: "%{text}", hovertemplate: "%{y} × %{x}: %{z}<extra></extra>"
      }], Object.assign({}, layoutBase, { title: ui.titles.corr, height: 520 }), cfg);

      const disOrder = ["None", "Insomnia", "Sleep Apnea"];
      Plotly.react("cDis", [{
        x: disOrder.map(d => LABELS.Disorder[lang][d]),
        y: disOrder.map(d => rows.filter(r => r.disorder === d).length),
        type: "bar", marker: { color: ["#7dd3c7", "#f0ab73", "#f0718d"] }
      }], Object.assign({}, layoutBase, { title: ui.titles.dis, xaxis: { title: ui.axes.disorder }, height: 340, showlegend: false }), cfg);

      const bmis = uniq("bmi");
      Plotly.react("cBmi", bmis.map(b => ({
        y: rows.filter(r => r.bmi === b).map(r => r.quality),
        name: LABELS.BMI[lang][b], type: "box", boxpoints: "all", jitter: 0.3
      })), Object.assign({}, layoutBase, { title: ui.titles.bmi, yaxis: { title: ui.axes.quality }, height: 340 }), cfg);

      const occAvg = uniq("occupation").map(o => ({
        o, v: mean(rows.filter(r => r.occupation === o).map(r => r.stress))
      })).filter(x => Number.isFinite(x.v)).sort((a,b) => b.v - a.v);
      Plotly.react("cOcc", [{
        x: occAvg.map(x => LABELS.Occupation[lang][x.o] || x.o),
        y: occAvg.map(x => +x.v.toFixed(2)),
        type: "bar", marker: { color: occAvg.map(x => x.v), colorscale: "Tealgrn" }
      }], Object.assign({}, layoutBase, { title: ui.titles.occ, yaxis: { title: ui.axes.stress }, height: 380, showlegend: false }), cfg);

      Plotly.react("cScatter", ["None","Insomnia","Sleep Apnea"].map(d => ({
        x: rows.filter(r => r.disorder === d).map(r => r.stress),
        y: rows.filter(r => r.disorder === d).map(r => r.sleep),
        name: LABELS.Disorder[lang][d],
        mode: "markers", type: "scatter",
        marker: { size: 9, opacity: 0.8 }
      })), Object.assign({}, layoutBase, { title: ui.titles.scatter, xaxis: { title: ui.axes.stress }, yaxis: { title: ui.axes.hours }, height: 400 }), cfg);
    }

    function setLang(next) {
      lang = next;
      localStorage.setItem("sleep-lang", next);
      applyLang();
      render();
    }

    document.getElementById("btn-en").addEventListener("click", () => setLang("en"));
    document.getElementById("btn-fr").addEventListener("click", () => setLang("fr"));
    ["fGender","fBmi","fOcc","ageMin","ageMax"].forEach(id => {
      document.getElementById(id).addEventListener("change", render);
      document.getElementById(id).addEventListener("input", render);
    });
    document.getElementById("btnReset").addEventListener("click", () => {
      ["fGender","fBmi","fOcc"].forEach(id => {
        [...document.getElementById(id).options].forEach(o => o.selected = false);
      });
      document.getElementById("ageMin").value = 27;
      document.getElementById("ageMax").value = 59;
      render();
    });

    applyLang();
    render();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
