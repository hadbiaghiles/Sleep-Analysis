"""Unified Sleep Health and Lifestyle Streamlit app.

English is the default. Visitors can switch to French in the sidebar; the
choice is kept in st.session_state. Category values stay in English internally.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from i18n import COLUMN_DISPLAY, LANGUAGES, label_series, label_value, t

DATA_PATH = Path(__file__).resolve().parent / "sleep_health_lifestyle_dataset.csv"

COLUMN_ALIASES = {
    "Sleep Duration (hours)": "Sleep Duration",
    "Quality of Sleep (scale: 1-10)": "Quality of Sleep",
    "Physical Activity Level (minutes/day)": "Physical Activity Level",
    "Stress Level (scale: 1-10)": "Stress Level",
    "Blood Pressure (systolic/diastolic)": "Blood Pressure",
    "Heart Rate (bpm)": "Heart Rate",
}

NUMERIC_COLS = [
    "Age",
    "Sleep Duration",
    "Quality of Sleep",
    "Physical Activity Level",
    "Stress Level",
    "Systolic BP",
    "Diastolic BP",
    "Heart Rate",
    "Daily Steps",
]

PLOTLY_TEMPLATE = "plotly_dark"
COLORWAY = ["#7dd3c7", "#8b9cff", "#f0ab73", "#f0718d", "#c4b5fd", "#67e8f9"]


def _init_lang() -> str:
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if st.session_state.lang not in LANGUAGES:
        st.session_state.lang = "en"
    return st.session_state.lang


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH.name}. "
            "Add sleep_health_lifestyle_dataset.csv next to app.py."
        )
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns={k: v for k, v in COLUMN_ALIASES.items() if k in df.columns})

    if "Sleep Disorder" in df.columns:
        df["Sleep Disorder"] = (
            df["Sleep Disorder"].fillna("None").replace({"": "None", "No sleep disorder": "None"})
        )

    bp_col = "Blood Pressure"
    if bp_col in df.columns:
        split = df[bp_col].astype(str).str.split("/", expand=True)
        df["Systolic BP"] = pd.to_numeric(split[0], errors="coerce")
        df["Diastolic BP"] = pd.to_numeric(split[1], errors="coerce")
        df = df.drop(columns=[bp_col])

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def display_frame(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    out = df.copy()
    for col in ("Gender", "BMI Category", "Occupation", "Sleep Disorder"):
        if col in out.columns:
            out[col] = label_series(lang, col, out[col])
    rename = {c: t(lang, COLUMN_DISPLAY[c]) for c in out.columns if c in COLUMN_DISPLAY}
    return out.rename(columns=rename)


def apply_filters(df: pd.DataFrame, genders, bmis, occupations, age_range) -> pd.DataFrame:
    out = df
    if genders:
        out = out[out["Gender"].isin(genders)]
    if bmis:
        out = out[out["BMI Category"].isin(bmis)]
    if occupations:
        out = out[out["Occupation"].isin(occupations)]
    if age_range:
        out = out[(out["Age"] >= age_range[0]) & (out["Age"] <= age_range[1])]
    return out


def style_fig(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        colorway=COLORWAY,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,18,32,0.35)",
        font=dict(color="#e8eefc", size=13),
        margin=dict(l=16, r=16, t=48, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zeroline=False)
    return fig


def kpis(df: pd.DataFrame, total: int, lang: str) -> None:
    n = len(df)
    c1, c2, c3, c4 = st.columns(4)
    sleep = df["Sleep Duration"].mean() if n else float("nan")
    quality = df["Quality of Sleep"].mean() if n else float("nan")
    disorder = (
        (df["Sleep Disorder"] != "None").mean() * 100 if n else float("nan")
    )
    c1.metric(t(lang, "kpi_n"), f"{n:,}", t(lang, "kpi_of_total", n=total))
    c2.metric(t(lang, "kpi_sleep"), f"{sleep:.2f}" if n else "—")
    c3.metric(t(lang, "kpi_quality"), f"{quality:.2f}" if n else "—")
    c4.metric(t(lang, "kpi_disorder"), f"{disorder:.1f}%" if n else "—")
    st.caption(t(lang, "filtered_note", n=n, total=total))


def insights(df: pd.DataFrame, lang: str) -> None:
    if df.empty:
        return
    disorder_rate = (df["Sleep Disorder"] != "None").mean() * 100
    by_bmi = df.groupby("BMI Category")["Quality of Sleep"].mean().sort_values()
    by_occ = df.groupby("Occupation")["Stress Level"].mean().sort_values(ascending=False)
    sleep_stress = df[["Sleep Duration", "Stress Level"]].corr().iloc[0, 1]
    top_bmi = by_bmi.index[0] if len(by_bmi) else None
    top_occ = by_occ.index[0] if len(by_occ) else None
    if lang == "fr":
        bullets = [
            f"Taux de trouble du sommeil dans la vue actuelle : **{disorder_rate:.1f}%**.",
            (
                f"Qualité de sommeil la plus basse : **{label_value(lang, 'BMI Category', top_bmi)}** "
                f"({by_bmi.iloc[0]:.2f}/10)."
                if top_bmi is not None
                else ""
            ),
            (
                f"Stress moyen le plus élevé : **{label_value(lang, 'Occupation', top_occ)}** "
                f"({by_occ.iloc[0]:.2f}/10)."
                if top_occ is not None
                else ""
            ),
            f"Corrélation durée de sommeil ↔ stress : **{sleep_stress:.2f}**.",
        ]
    else:
        bullets = [
            f"Sleep-disorder rate in the current view: **{disorder_rate:.1f}%**.",
            (
                f"Lowest average sleep quality: **{label_value(lang, 'BMI Category', top_bmi)}** "
                f"({by_bmi.iloc[0]:.2f}/10)."
                if top_bmi is not None
                else ""
            ),
            (
                f"Highest average stress: **{label_value(lang, 'Occupation', top_occ)}** "
                f"({by_occ.iloc[0]:.2f}/10)."
                if top_occ is not None
                else ""
            ),
            f"Correlation of sleep duration vs stress: **{sleep_stress:.2f}**.",
        ]
    st.markdown("**" + t(lang, "insight_title") + "**")
    for item in bullets:
        if item:
            st.markdown(f"- {item}")


def section_overview(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "preview"))
    st.dataframe(display_frame(df.head(12), lang), use_container_width=True, hide_index=True)
    left, right = st.columns(2)
    with left:
        st.subheader(t(lang, "columns_types"))
        types = pd.DataFrame(
            {
                t(lang, "columns_types"): [t(lang, COLUMN_DISPLAY.get(c, c),) if c in COLUMN_DISPLAY else c for c in df.columns],
                "dtype": df.dtypes.astype(str).values,
            }
        )
        st.dataframe(types, use_container_width=True, hide_index=True)
    with right:
        st.subheader(t(lang, "categorical_counts"))
        for col in ("Gender", "BMI Category", "Sleep Disorder", "Occupation"):
            counts = df[col].value_counts().rename_axis(col).reset_index(name="n")
            counts[col] = label_series(lang, col, counts[col])
            counts = counts.rename(columns={col: t(lang, COLUMN_DISPLAY[col])})
            st.markdown(f"**{t(lang, COLUMN_DISPLAY[col])}**")
            st.dataframe(counts, use_container_width=True, hide_index=True)


def section_cleaning(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "cleaning_title"))
    st.write(t(lang, "cleaning_intro"))
    st.markdown(t(lang, "cleaning_steps"))
    left, right = st.columns(2)
    with left:
        st.markdown("**" + t(lang, "missing_after") + "**")
        st.dataframe(
            df.isnull().sum().rename("n").to_frame(),
            use_container_width=True,
        )
    with right:
        st.markdown("**" + t(lang, "types_after") + "**")
        st.dataframe(df.dtypes.astype(str).rename("dtype").to_frame(), use_container_width=True)


def section_eda(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "describe"))
    st.dataframe(df[NUMERIC_COLS].describe().T.round(2), use_container_width=True)
    st.subheader(t(lang, "corr_table"))
    corr = df[NUMERIC_COLS].corr().round(2)
    st.dataframe(corr, use_container_width=True)
    insights(df, lang)


def section_visualizations(df: pd.DataFrame, lang: str) -> None:
    if df.empty:
        st.warning(t(lang, "empty_filter"))
        return

    plot_df = df.copy()
    plot_df["_gender"] = label_series(lang, "Gender", plot_df["Gender"])
    plot_df["_bmi"] = label_series(lang, "BMI Category", plot_df["BMI Category"])
    plot_df["_occ"] = label_series(lang, "Occupation", plot_df["Occupation"])
    plot_df["_dis"] = label_series(lang, "Sleep Disorder", plot_df["Sleep Disorder"])

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.subheader(t(lang, "chart_age"))
        fig = px.histogram(plot_df, x="Age", nbins=12, color_discrete_sequence=[COLORWAY[0]])
        fig.update_layout(title=t(lang, "chart_age"), bargap=0.08)
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(t(lang, "chart_age_caption"))
    with r1c2:
        st.subheader(t(lang, "chart_sleep_gender"))
        fig = px.box(
            plot_df,
            x="_gender",
            y="Sleep Duration",
            color="_gender",
            points="all",
        )
        fig.update_layout(
            title=t(lang, "chart_sleep_gender"),
            xaxis_title=t(lang, "col_gender"),
            yaxis_title=t(lang, "col_sleep_duration"),
            showlegend=False,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(t(lang, "chart_sleep_gender_caption"))

    st.subheader(t(lang, "chart_corr"))
    corr = plot_df[NUMERIC_COLS].corr()
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Tealrose",
            zmid=0,
            text=corr.round(2).values,
            texttemplate="%{text}",
            hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(title=t(lang, "chart_corr"), height=560)
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.caption(t(lang, "chart_corr_caption"))

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.subheader(t(lang, "chart_disorder"))
        counts = plot_df["_dis"].value_counts().reset_index()
        counts.columns = ["disorder", "n"]
        fig = px.bar(counts, x="disorder", y="n", color="disorder")
        fig.update_layout(
            title=t(lang, "chart_disorder"),
            xaxis_title=t(lang, "col_disorder"),
            yaxis_title="",
            showlegend=False,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(t(lang, "chart_disorder_caption"))
    with r2c2:
        st.subheader(t(lang, "chart_quality_bmi"))
        fig = px.box(plot_df, x="_bmi", y="Quality of Sleep", color="_bmi", points="all")
        fig.update_layout(
            title=t(lang, "chart_quality_bmi"),
            xaxis_title=t(lang, "col_bmi"),
            yaxis_title=t(lang, "col_quality"),
            showlegend=False,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(t(lang, "chart_quality_bmi_caption"))

    st.subheader(t(lang, "chart_stress_occ"))
    stress = (
        plot_df.groupby("_occ", as_index=False)["Stress Level"]
        .mean()
        .sort_values("Stress Level", ascending=False)
    )
    fig = px.bar(stress, x="_occ", y="Stress Level", color="Stress Level", color_continuous_scale="Tealgrn")
    fig.update_layout(
        title=t(lang, "chart_stress_occ"),
        xaxis_title=t(lang, "col_occupation"),
        yaxis_title=t(lang, "col_stress"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.caption(t(lang, "chart_stress_occ_caption"))

    st.subheader(t(lang, "chart_sleep_stress"))
    fig = px.scatter(
        plot_df,
        x="Stress Level",
        y="Sleep Duration",
        color="_dis",
        hover_data=["Age", "_gender", "_occ"],
        opacity=0.85,
    )
    fig.update_layout(
        title=t(lang, "chart_sleep_stress"),
        xaxis_title=t(lang, "col_stress"),
        yaxis_title=t(lang, "col_sleep_duration"),
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.caption(t(lang, "chart_sleep_stress_caption"))

    insights(df, lang)


def inject_css() -> None:
    st.markdown(
        """
        <style>
          .block-container {padding-top: 1.4rem; max-width: 1280px;}
          h1 {letter-spacing: -0.03em;}
          div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(21,29,50,0.9), rgba(11,18,32,0.9));
            border: 1px solid rgba(125,211,199,0.18);
            border-radius: 16px;
            padding: 12px 16px;
          }
          [data-testid="stSidebar"] {background: #0e1628;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    import os

    st.set_page_config(
        page_title="Sleep Health & Lifestyle",
        page_icon="💤",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "lang" not in st.session_state:
        preset = os.environ.get("SLEEP_APP_LANG", "en").lower()
        st.session_state.lang = preset if preset in LANGUAGES else "en"

    lang = _init_lang()
    inject_css()

    df = load_data()
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())

    with st.sidebar:
        st.markdown("### 💤")
        st.radio(
            t(lang, "language") + " / Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda code: LANGUAGES[code],
            key="lang",
            horizontal=True,
        )
        lang = st.session_state.lang

        st.header(t(lang, "nav"))
        section = st.radio(
            t(lang, "nav"),
            options=["overview", "cleaning", "eda", "viz"],
            format_func=lambda s: {
                "overview": t(lang, "section_overview"),
                "cleaning": t(lang, "section_cleaning"),
                "eda": t(lang, "section_eda"),
                "viz": t(lang, "section_viz"),
            }[s],
            label_visibility="collapsed",
        )

        st.header(t(lang, "filters"))
        gender_opts = sorted(df["Gender"].unique().tolist())
        bmi_opts = sorted(df["BMI Category"].unique().tolist())
        occ_opts = sorted(df["Occupation"].unique().tolist())

        genders = st.multiselect(
            t(lang, "gender"),
            options=gender_opts,
            format_func=lambda v: label_value(lang, "Gender", v),
        )
        bmis = st.multiselect(
            t(lang, "bmi"),
            options=bmi_opts,
            format_func=lambda v: label_value(lang, "BMI Category", v),
        )
        occupations = st.multiselect(
            t(lang, "occupation"),
            options=occ_opts,
            format_func=lambda v: label_value(lang, "Occupation", v),
        )
        age_range = st.slider(
            t(lang, "age_range"),
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max),
        )

        st.caption(t(lang, "dataset_source"))

    view = apply_filters(df, genders, bmis, occupations, age_range)

    st.title(t(lang, "app_title"))
    st.write(t(lang, "tagline"))
    kpis(view, total=len(df), lang=lang)
    st.divider()

    if view.empty:
        st.warning(t(lang, "empty_filter"))
    elif section == "overview":
        section_overview(view, lang)
    elif section == "cleaning":
        section_cleaning(df, lang)
    elif section == "eda":
        section_eda(view, lang)
    else:
        section_visualizations(view, lang)

    st.divider()
    st.caption(t(lang, "footer", author=t(lang, "author")))


if __name__ == "__main__":
    main()
