"""UI and category translations for the Sleep Health dashboard.

English is the default. French labels are applied only for display; the
underlying dataframe keeps original English category values so filters and
aggregations stay stable.
"""

from __future__ import annotations

LANGUAGES = {
    "en": "English",
    "fr": "Français",
}

# Display-only maps. Keys are the original dataset values.
CATEGORY_LABELS = {
    "en": {
        "Gender": {"Male": "Male", "Female": "Female"},
        "BMI Category": {
            "Normal": "Normal",
            "Normal Weight": "Normal Weight",
            "Overweight": "Overweight",
            "Obese": "Obese",
        },
        "Sleep Disorder": {
            "None": "None",
            "No sleep disorder": "None",
            "Insomnia": "Insomnia",
            "Sleep Apnea": "Sleep Apnea",
        },
        "Occupation": {
            "Software Engineer": "Software Engineer",
            "Doctor": "Doctor",
            "Sales Representative": "Sales Representative",
            "Teacher": "Teacher",
            "Nurse": "Nurse",
            "Engineer": "Engineer",
            "Accountant": "Accountant",
            "Scientist": "Scientist",
            "Lawyer": "Lawyer",
            "Salesperson": "Salesperson",
            "Manager": "Manager",
        },
    },
    "fr": {
        "Gender": {"Male": "Homme", "Female": "Femme"},
        "BMI Category": {
            "Normal": "Normal",
            "Normal Weight": "Poids normal",
            "Overweight": "Surpoids",
            "Obese": "Obèse",
        },
        "Sleep Disorder": {
            "None": "Aucun",
            "No sleep disorder": "Aucun",
            "Insomnia": "Insomnie",
            "Sleep Apnea": "Apnée du sommeil",
        },
        "Occupation": {
            "Software Engineer": "Ingénieur logiciel",
            "Doctor": "Médecin",
            "Sales Representative": "Représentant commercial",
            "Teacher": "Enseignant",
            "Nurse": "Infirmier",
            "Engineer": "Ingénieur",
            "Accountant": "Comptable",
            "Scientist": "Scientifique",
            "Lawyer": "Avocat",
            "Salesperson": "Vendeur",
            "Manager": "Cadre",
        },
    },
}

UI = {
    "en": {
        "page_title": "Sleep Health & Lifestyle",
        "page_icon": "💤",
        "app_title": "Sleep Health and Lifestyle",
        "tagline": "Explore how sleep, stress, activity and body composition relate in a public health dataset.",
        "author": "Hadbi Aghiles",
        "language": "Language",
        "filters": "Filters",
        "gender": "Gender",
        "bmi": "BMI category",
        "occupation": "Occupation",
        "age_range": "Age range",
        "reset_filters": "Reset filters",
        "all": "All",
        "nav": "Navigate",
        "section_overview": "Overview",
        "section_cleaning": "Cleaning",
        "section_eda": "Exploratory analysis",
        "section_viz": "Visualizations",
        "kpi_n": "People",
        "kpi_sleep": "Avg. sleep (h)",
        "kpi_quality": "Avg. quality",
        "kpi_disorder": "Disorder rate",
        "kpi_of_total": "of {n} in the dataset",
        "filtered_note": "Showing {n} of {total} records after filters.",
        "dataset_source": "Dataset: Sleep Health and Lifestyle (Kaggle, uom190346a). Synthetic public data.",
        "preview": "Data preview",
        "columns_types": "Columns and types",
        "categorical_counts": "Categorical value counts",
        "cleaning_title": "How the data is prepared",
        "cleaning_intro": "The published CSV is loaded as-is. A few derived fields make blood pressure and missing disorders easier to analyse.",
        "cleaning_steps": (
            "1. Missing `Sleep Disorder` values are treated as **None** (no diagnosed disorder).\n"
            "2. `Blood Pressure` (`systolic/diastolic`) is split into **Systolic BP** and **Diastolic BP**.\n"
            "3. Column names are normalised so both the Kaggle schema and the original app aliases work.\n"
            "4. Filters never mutate the source file; they only subset the in-memory frame."
        ),
        "missing_after": "Missing values after cleaning",
        "types_after": "Types after cleaning",
        "describe": "Descriptive statistics (filtered view)",
        "corr_table": "Correlation matrix",
        "chart_age": "Age distribution",
        "chart_age_caption": "Most people in this sample are between 30 and 50. Age is a useful control when comparing sleep quality.",
        "chart_sleep_gender": "Sleep duration by gender",
        "chart_sleep_gender_caption": "Compare typical sleep hours and spread for men and women in the current filter.",
        "chart_corr": "Correlation heatmap",
        "chart_corr_caption": "Sleep duration and quality usually move together; stress tends to move the other way.",
        "chart_disorder": "Sleep disorders",
        "chart_disorder_caption": "None means no recorded disorder. Insomnia and sleep apnea are the two coded conditions.",
        "chart_quality_bmi": "Sleep quality by BMI category",
        "chart_quality_bmi_caption": "Higher BMI categories often sit with slightly lower subjective sleep quality in this sample.",
        "chart_stress_occ": "Average stress by occupation",
        "chart_stress_occ_caption": "Occupation is a lifestyle proxy: some roles cluster at higher reported stress.",
        "chart_sleep_stress": "Sleep duration vs stress",
        "chart_sleep_stress_caption": "Each point is a person. Colour shows sleep disorder status.",
        "empty_filter": "No rows match the current filters. Reset them in the sidebar.",
        "footer": "Built by {author} · English is the default language · Switch to French anytime in the sidebar.",
        "live_site": "Public dashboard",
        "col_person_id": "Person ID",
        "col_gender": "Gender",
        "col_age": "Age",
        "col_occupation": "Occupation",
        "col_sleep_duration": "Sleep Duration (hours)",
        "col_quality": "Quality of Sleep (1–10)",
        "col_activity": "Physical Activity Level",
        "col_stress": "Stress Level (1–10)",
        "col_bmi": "BMI Category",
        "col_systolic": "Systolic BP",
        "col_diastolic": "Diastolic BP",
        "col_heart": "Heart Rate (bpm)",
        "col_steps": "Daily Steps",
        "col_disorder": "Sleep Disorder",
        "insight_title": "Highlights",
    },
    "fr": {
        "page_title": "Santé du sommeil et mode de vie",
        "page_icon": "💤",
        "app_title": "Santé du sommeil et mode de vie",
        "tagline": "Explorer les liens entre sommeil, stress, activité et composition corporelle dans un jeu de données public.",
        "author": "Hadbi Aghiles",
        "language": "Langue",
        "filters": "Filtres",
        "gender": "Genre",
        "bmi": "Catégorie IMC",
        "occupation": "Profession",
        "age_range": "Tranche d'âge",
        "reset_filters": "Réinitialiser les filtres",
        "all": "Tous",
        "nav": "Naviguer",
        "section_overview": "Aperçu",
        "section_cleaning": "Nettoyage",
        "section_eda": "Analyse exploratoire",
        "section_viz": "Visualisations",
        "kpi_n": "Personnes",
        "kpi_sleep": "Sommeil moy. (h)",
        "kpi_quality": "Qualité moy.",
        "kpi_disorder": "Taux de troubles",
        "kpi_of_total": "sur {n} dans le jeu",
        "filtered_note": "Affichage de {n} enregistrements sur {total} après filtres.",
        "dataset_source": "Jeu de données : Sleep Health and Lifestyle (Kaggle, uom190346a). Données publiques synthétiques.",
        "preview": "Aperçu des données",
        "columns_types": "Colonnes et types",
        "categorical_counts": "Effectifs des variables catégorielles",
        "cleaning_title": "Préparation des données",
        "cleaning_intro": "Le CSV publié est chargé tel quel. Quelques champs dérivés facilitent l'analyse de la tension et des troubles manquants.",
        "cleaning_steps": (
            "1. Les valeurs manquantes de `Sleep Disorder` sont traitées comme **Aucun** (pas de trouble diagnostiqué).\n"
            "2. `Blood Pressure` (`systolique/diastolique`) est séparé en **Systolic BP** et **Diastolic BP**.\n"
            "3. Les noms de colonnes sont normalisés pour le schéma Kaggle et les alias de l'ancienne app.\n"
            "4. Les filtres ne modifient pas le fichier source ; ils sous-ensemblent le tableau en mémoire."
        ),
        "missing_after": "Valeurs manquantes après nettoyage",
        "types_after": "Types après nettoyage",
        "describe": "Statistiques descriptives (vue filtrée)",
        "corr_table": "Matrice de corrélation",
        "chart_age": "Répartition des âges",
        "chart_age_caption": "La plupart des personnes de l'échantillon ont entre 30 et 50 ans. L'âge est un contrôle utile.",
        "chart_sleep_gender": "Durée de sommeil par genre",
        "chart_sleep_gender_caption": "Comparer les heures de sommeil typiques et la dispersion pour les hommes et les femmes.",
        "chart_corr": "Carte de chaleur des corrélations",
        "chart_corr_caption": "Durée et qualité du sommeil évoluent souvent ensemble ; le stress va généralement en sens inverse.",
        "chart_disorder": "Troubles du sommeil",
        "chart_disorder_caption": "Aucun signifie aucun trouble enregistré. Insomnie et apnée sont les deux affections codées.",
        "chart_quality_bmi": "Qualité du sommeil par IMC",
        "chart_quality_bmi_caption": "Les catégories d'IMC plus élevées s'accompagnent souvent d'une qualité de sommeil un peu plus basse.",
        "chart_stress_occ": "Stress moyen par profession",
        "chart_stress_occ_caption": "La profession est un proxy de mode de vie : certains métiers se regroupent à un stress plus élevé.",
        "chart_sleep_stress": "Durée de sommeil vs stress",
        "chart_sleep_stress_caption": "Chaque point est une personne. La couleur indique le trouble du sommeil.",
        "empty_filter": "Aucun enregistrement ne correspond aux filtres. Réinitialisez-les dans la barre latérale.",
        "footer": "Réalisé par {author} · L'anglais est la langue par défaut · Passez au français quand vous le souhaitez.",
        "live_site": "Tableau de bord public",
        "col_person_id": "Identifiant",
        "col_gender": "Genre",
        "col_age": "Âge",
        "col_occupation": "Profession",
        "col_sleep_duration": "Durée de sommeil (h)",
        "col_quality": "Qualité du sommeil (1–10)",
        "col_activity": "Niveau d'activité physique",
        "col_stress": "Niveau de stress (1–10)",
        "col_bmi": "Catégorie IMC",
        "col_systolic": "Tension systolique",
        "col_diastolic": "Tension diastolique",
        "col_heart": "Fréquence cardiaque (bpm)",
        "col_steps": "Pas quotidiens",
        "col_disorder": "Trouble du sommeil",
        "insight_title": "Points clés",
    },
}

COLUMN_DISPLAY = {
    "Person ID": "col_person_id",
    "Gender": "col_gender",
    "Age": "col_age",
    "Occupation": "col_occupation",
    "Sleep Duration": "col_sleep_duration",
    "Quality of Sleep": "col_quality",
    "Physical Activity Level": "col_activity",
    "Stress Level": "col_stress",
    "BMI Category": "col_bmi",
    "Systolic BP": "col_systolic",
    "Diastolic BP": "col_diastolic",
    "Heart Rate": "col_heart",
    "Daily Steps": "col_steps",
    "Sleep Disorder": "col_disorder",
}


def t(lang: str, key: str, **kwargs) -> str:
    bundle = UI.get(lang, UI["en"])
    text = bundle.get(key, UI["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def label_value(lang: str, column: str, value) -> str:
    if value is None:
        return ""
    raw = str(value)
    table = CATEGORY_LABELS.get(lang, CATEGORY_LABELS["en"]).get(column, {})
    return table.get(raw, raw)


def label_series(lang: str, column: str, series):
    return series.map(lambda v: label_value(lang, column, v))
