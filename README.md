# Sleep Health and Lifestyle..

[![Live demo](https://img.shields.io/badge/Live_demo-open-6366f1?style=for-the-badge)](https://hadbiaghiles.github.io/Sleep-Analysis/)

Public analysis of the [Sleep Health and Lifestyle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) dataset, rebuilt as a single bilingual product.

- **Default language: English**
- French is available through an in-app language switch (visitor choice, not a second URL)
- Author: **Hadbi Aghiles**

Live static dashboard (GitHub Pages):

**https://hadbiaghiles.github.io/Sleep-Analysis/**

The Streamlit app is the Python experience (`app.py`). The Pages site presents the same KPIs, filters, charts and EN/FR switch without a server.

---

## What you get

- Unified Streamlit app (`app.py`) with EN/FR UI strings and translated category labels (gender, BMI, occupation, sleep disorder) that do not change the underlying analysis values
- Dataset shipped in the repo: `sleep_health_lifestyle_dataset.csv` (Kaggle `uom190346a` schema, 374 rows)
- KPI strip: sample size, average sleep hours, average sleep quality, disorder rate
- Filters: gender, BMI category, occupation, age range
- Plotly charts with captions and computed highlights
- Static bilingual dashboard in `docs/` for GitHub Pages

---

## Language behaviour

| Surface | Default | How to switch |
|---|---|---|
| Streamlit (`app.py`) | English | Sidebar **Language / Langue** radio. Choice is stored in `st.session_state`. |
| GitHub Pages (`docs/index.html`) | English | Header **English / Français** toggle. Choice is stored in `localStorage`. |
| `app_en.py` | English | Thin wrapper around `app.py`. |
| `app_fr.py` | French pre-selected | Same app; still switchable back to English. |

There is one app, not two deployments.

---

## Dataset

File: [`sleep_health_lifestyle_dataset.csv`](sleep_health_lifestyle_dataset.csv)

Source: [Kaggle — Sleep Health and Lifestyle Dataset (uom190346a)](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) by Laksika Tharmalingam. The copy in this repo is the public CSV with columns:

`Person ID, Gender, Age, Occupation, Sleep Duration, Quality of Sleep, Physical Activity Level, Stress Level, BMI Category, Blood Pressure, Heart Rate, Daily Steps, Sleep Disorder`

The publisher notes that the dataset is synthetic and intended for illustration.

Cleaning applied in the app (not in the CSV):

1. Missing `Sleep Disorder` values are treated as `None`
2. `Blood Pressure` is split into `Systolic BP` and `Diastolic BP`
3. Column-name aliases from the original Streamlit scripts are normalised to the Kaggle schema

---

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Legacy launchers (same unified app):

```bash
streamlit run app_en.py
streamlit run app_fr.py
```

---

## Deploy

### GitHub Pages (live)

The interactive dashboard lives in `docs/index.html` (regenerate with `python generate_site.py`). GitHub Pages is enabled on this repository and serves `/docs`.

After this branch is merged to `main`, point Pages at **main / docs** so the site keeps working if the feature branch is deleted:

Settings → Pages → Source branch `main`, folder `/docs`.

### Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. **New app** → repository `hadbiaghiles/Sleep-Analysis`
3. Branch: `main` (or this feature branch)
4. **Main file path: `app.py`**
5. Deploy

`requirements.txt` and `.streamlit/config.toml` are already in the repo.

---

## Project layout

```
app.py                              # unified Streamlit entry (use this)
i18n.py                             # EN/FR strings and category labels
app_en.py / app_fr.py               # thin wrappers
sleep_health_lifestyle_dataset.csv  # public dataset
requirements.txt
.streamlit/config.toml
docs/index.html                     # GitHub Pages dashboard
generate_site.py                    # rebuilds docs/index.html
```

Notebooks `notebook.ipynb` and `botebook_fr.ipynb` are unchanged exploratory work.

---

## License / credit

Analysis and product by **Hadbi Aghiles**. Dataset credit: Laksika Tharmalingam via Kaggle (`uom190346a`).
