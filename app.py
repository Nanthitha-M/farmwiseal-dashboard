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
.stApp {background:#f3f6fb;}
section[data-testid="stSidebar"] {background:#10213e;}
section[data-testid="stSidebar"] * {color:white;}
.hero {
  padding:24px; border-radius:16px; color:white;
  background:linear-gradient(120deg,#10213e,#1d5b83);
}
div[data-testid="stMetric"] {
  background:white; padding:14px; border-radius:12px;
  border:1px solid #dce5ef;
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
    d.metric(
        "Possible Matches",
        int(df[match_col].astype(str).str.lower().isin(
            ["true", "yes", "matched", "match"]
        ).sum()) if match_col and not df.empty else "Review"
    )

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
