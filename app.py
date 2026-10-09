from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="FarmwiseAl | Land Intelligence",
    page_icon="🌱",
    layout="wide"
)

OUT = Path(__file__).resolve().parent / "land_pipeline_output"
CSV = OUT / "Patta_Perurani_all_cadastral_comparison_reviewed.csv"
GEO = OUT / "Patta_Perurani_GIS_review_layer.geojson"
QUALITY = OUT / "Patta_Perurani_quality_summary.txt"
OCR = OUT / "Patta_Perurani_textract_text.txt"

st.markdown("""
<style>
/* Overall page */
.stApp {
    background: #f3f7fc;
    color: #172b4d;
}
section.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main headings and text */
section.main h1, section.main h2, section.main h3,
section.main h4, section.main p, section.main li,
section.main label,
section.main [data-testid="stCaptionContainer"],
section.main [data-testid="stMetricLabel"],
section.main [data-testid="stMetricValue"] {
    color: #172b4d !important;
}
section.main h1 {
    font-weight: 750;
    letter-spacing: -0.5px;
}
section.main h2, section.main h3 {
    font-weight: 650;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10213e;
    border-right: 1px solid #233b60;
}
section[data-testid="stSidebar"] * {
    color: #f8fbff;
}
section[data-testid="stSidebar"] input {
    color: #172b4d !important;
    background: #ffffff !important;
}

/* Hero banner */
.hero {
    padding: 26px;
    border-radius: 16px;
    color: #ffffff;
    background: linear-gradient(120deg, #10213e, #1d5b83);
    box-shadow: 0 8px 24px rgba(16, 33, 62, 0.12);
}
.hero h1, .hero h2, .hero h3, .hero p {
    color: #ffffff !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #ffffff;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #d8e3f0;
    box-shadow: 0 3px 12px rgba(23, 43, 77, 0.05);
}
div[data-testid="stMetricLabel"] {
    color: #526783 !important;
}
div[data-testid="stMetricValue"] {
    color: #10213e !important;
    font-weight: 750;
}

/* Text fields, search boxes, and OCR preview */
section.main input,
section.main textarea,
section.main [data-baseweb="input"] input,
section.main [data-baseweb="textarea"] textarea {
    background: #ffffff !important;
    color: #172b4d !important;
    -webkit-text-fill-color: #172b4d !important;
    border-color: #c7d6e8 !important;
    border-radius: 9px !important;
    opacity: 1 !important;
}
section.main input::placeholder,
section.main textarea::placeholder {
    color: #647892 !important;
    -webkit-text-fill-color: #647892 !important;
    opacity: 1 !important;
}
section.main [data-baseweb="input"],
section.main [data-baseweb="textarea"] {
    background: #ffffff !important;
}

/* Buttons and download controls */
section.main button[kind="primary"],
section.main .stDownloadButton button {
    background: #0878e8 !important;
    color: #ffffff !important;
    border: 1px solid #0878e8 !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
}
section.main button[kind="primary"] *,
section.main .stDownloadButton button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
section.main button[kind="secondary"] {
    color: #17365f !important;
    border-color: #b9cce2 !important;
}

/* Tables and code blocks */
section.main [data-testid="stDataFrame"],
section.main [data-testid="stTable"] {
    border: 1px solid #d8e3f0;
    border-radius: 10px;
    overflow: hidden;
}
section.main pre,
section.main code {
    color: #e7efff !important;
}

/* Warnings remain readable */
section.main [data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🌱 FarmwiseAl</h1>
<h3>Multimodal GeoAI & Land Document Intelligence</h3>
<p>Document OCR · Cadastral Mapping · Discrepancy Review</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("FARMWISEAL")
page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Cadastral Map", "Patta Records",
     "Quality Review", "Document OCR"]
)
st.sidebar.caption("Task 2 | Review prototype")

# Load existing pipeline outputs without modifying them.
df = pd.read_csv(CSV, dtype=str, keep_default_na=False) if CSV.exists() else pd.DataFrame()
geo = json.loads(GEO.read_text(encoding="utf-8")) if GEO.exists() else {
    "type": "FeatureCollection", "features": []
}
features = geo.get("features", [])

if page == "Overview":
    st.header("Project Overview")
    st.write("Review extracted land-record candidates and their possible cadastral links.")

    a, b, c, d = st.columns(4)
    a.metric("Candidate Rows", len(df) if not df.empty else 0)
    b.metric("GIS Features", len(features))

    survey_col = next(
        (x for x in ["survey_number", "survey_no"] if x in df.columns), None
    )
    match_col = next(
        (x for x in ["cadastral_match"] if x in df.columns), None
    )

    c.metric(
        "Parent Surveys",
        df[survey_col].nunique() if survey_col and not df.empty else 0
    )
    possible_matches = 0
    if match_col and not df.empty:
        possible_matches = int(
            df[match_col].astype(str).str.contains(
                r"possible|matched|match",
                case=False,
                na=False,
                regex=True
            ).sum()
        )

    d.metric("Possible Matches", possible_matches)

    st.subheader("Pipeline Files")
    for name, path in [
        ("Patta candidate comparison", CSV),
        ("Cadastral GIS review layer", GEO),
        ("Quality summary", QUALITY),
        ("Patta OCR text", OCR),
    ]:
        st.write(("✅" if path.exists() else "⚠️"), name,
                 "— Available" if path.exists() else "— Not found")

    if survey_col and not df.empty:
        counts = df.groupby(survey_col).size().reset_index(name="Candidate rows")
        fig = px.bar(
            counts, x=survey_col, y="Candidate rows",
            title="Extracted candidates by parent survey"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "Matches are preliminary parent-survey links. They do not verify "
        "subdivision boundaries, land extent, or legal ownership."
    )

elif page == "Cadastral Map":
    st.header("Cadastral Review Map")

    if not features:
        st.error(f"GIS review layer not found: {GEO}")
    else:
        # Compute an approximate map center from GeoJSON coordinates.
        points = []

        def collect(obj):
            if isinstance(obj, list):
                if (len(obj) >= 2
                    and isinstance(obj[0], (int, float))
                    and isinstance(obj[1], (int, float))):
                    points.append((obj[1], obj[0]))
                else:
                    for item in obj:
                        collect(item)

        for feature in features:
            geom = feature.get("geometry") or {}
            collect(geom.get("coordinates", []))

        center = (
            [sum(p[0] for p in points) / len(points),
             sum(p[1] for p in points) / len(points)]
            if points else [8.8, 78.0]
        )

        m = folium.Map(location=center, zoom_start=14, tiles="OpenStreetMap")

        folium.GeoJson(
            geo,
            name="Cadastral Features",
            style_function=lambda f: {
                "color": "#1672a5",
                "weight": 2,
                "fillColor": "#48a9d6",
                "fillOpacity": 0.25,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    key for key in [
                        "vil_name", "survey_no", "unit_id", "block_id",
                        "patta_candidate_count", "review_status"
                    ]
                    if key in (features[0].get("properties") or {})
                ],
                sticky=False
            )
        ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, use_container_width=True, height=580)

        st.caption(f"Displaying {len(features)} GIS review features.")
        st.warning(
            "The map shows supplied cadastral geometries. Candidate records "
            "are linked at parent-survey level only; ownership and subdivision "
            "boundaries have not been independently verified."
        )

elif page == "Patta Records":
    st.header("Patta Survey Candidates")

    if df.empty:
        st.error(f"Candidate CSV not found or empty: {CSV}")
    else:
        query = st.text_input("Search survey number, subdivision, extent, or status")
        filtered = df.copy()

        if query.strip():
            search_rows = filtered.astype(str).agg(" | ".join, axis=1)
            filtered = filtered[
                search_rows.str.contains(query.strip(), case=False, na=False)
            ]

        st.caption(f"Showing {len(filtered)} of {len(df)} records.")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

        st.download_button(
            "Download filtered CSV",
            filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="farmwiseal_filtered_candidates.csv",
            mime="text/csv"
        )
        st.download_button(
            "Download complete CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            file_name="farmwiseal_all_candidates.csv",
            mime="text/csv"
        )

elif page == "Quality Review":
    st.header("Quality & Discrepancy Review")

    if QUALITY.exists():
        st.subheader("Extraction Quality Summary")
        st.code(QUALITY.read_text(encoding="utf-8"))
    else:
        st.warning(f"Quality summary not found: {QUALITY}")

    if not df.empty:
        review_cols = [
            col for col in df.columns
            if "review_status" in col.lower() or col.lower() == "review_status"
        ]
        if review_cols:
            status_col = review_cols[0]
            needs_review = df[
                df[status_col].astype(str).str.contains(
                    "review|verify|candidate|possible|unusual|manual",
                    case=False, na=False
                )
            ]
        else:
            needs_review = df

        st.subheader("Review Queue")
        st.caption(f"{len(needs_review)} records selected for attention.")
        st.dataframe(needs_review, use_container_width=True, hide_index=True)

        st.download_button(
            "Download review queue",
            needs_review.to_csv(index=False).encode("utf-8-sig"),
            file_name="farmwiseal_review_queue.csv",
            mime="text/csv"
        )

    st.warning(
        "Compare flagged candidates and raw extent values against the original "
        "document and authoritative records before making decisions."
    )

elif page == "Document OCR":
    st.header("Document OCR Viewer")

    if not OCR.exists():
        st.warning(f"Patta OCR text not found: {OCR}")
    else:
        text = OCR.read_text(encoding="utf-8", errors="replace")

        st.download_button(
            "Download full OCR text",
            text.encode("utf-8"),
            file_name="Patta_Perurani_textract_text.txt",
            mime="text/plain"
        )

        term = st.text_input("Search OCR text")
        if term.strip():
            matches = [
                line for line in text.splitlines()
                if term.casefold() in line.casefold()
            ]
            st.write(f"Matching lines: {len(matches)}")
            st.text("\n".join(matches[:500]) if matches else "No matches found.")
        else:
            st.text_area("OCR Preview", text[:5000], height=300)

st.divider()
st.caption(
    "FarmwiseAl Task 2 prototype | Human verification is required "
    "before treating matches as authoritative."
)
