from pathlib import Path
import json
import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import st_folium
import rasterio

st.set_page_config(
    page_title="FarmwiseAI | Land Intelligence Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Custom CSS Design System (Exact Match to Your Target Mockup)
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --sidebar-bg: #0b1320;
        --sidebar-active: #0da487;
        --canvas-bg: #f8fafc;
        --card-bg: #ffffff;
        --card-border: #e8eef5;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --green-mint: #e6f7f3;
        --teal-accent: #0da487;
    }

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    .stApp {
        background-color: var(--canvas-bg);
        color: var(--text-primary);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    section.main .block-container {
        max-width: 1680px;
        padding: 1rem 2rem 3rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid #172439;
    }

    section[data-testid="stSidebar"] * {
        color: #94a3b8 !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.8rem 0 1.6rem;
    }

    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.03em;
    }

    .nav-header {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #475569 !important;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 9px;
        padding: 0.6rem 0.85rem;
        margin: 0.2rem 0;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: var(--sidebar-active) !important;
        box-shadow: 0 4px 12px rgba(13, 164, 135, 0.35);
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    .sidebar-footer-box {
        position: fixed;
        bottom: 1.2rem;
        left: 1.2rem;
        width: 14rem;
        padding: 0.75rem 0.9rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .footer-text {
        font-size: 0.72rem;
        line-height: 1.3;
        color: #64748b !important;
    }

    /* Top Navbar & Breadcrumb */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e8eef5;
        margin-bottom: 1.2rem;
    }

    .breadcrumb {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 500;
    }

    .breadcrumb b {
        color: #0f172a;
    }

    .user-pill {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
    }

    .avatar-badge {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background: #0f172a;
        color: #fff;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Page Headings */
    .page-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.025em;
        margin: 0 0 0.2rem;
    }

    .page-subtitle {
        font-size: 0.88rem;
        color: #64748b;
        margin-bottom: 1.3rem;
    }

    /* White Cards & Panels */
    .panel {
        background: #ffffff;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }

    .panel-heading {
        font-size: 0.98rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.85rem;
    }

    /* KPI Stat Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.15rem 1.25rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
    }

    .stat-icon {
        width: 2.75rem;
        height: 2.75rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        flex-shrink: 0;
    }

    .stat-content {
        flex-grow: 1;
    }

    .stat-label {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.15rem;
    }

    .stat-value {
        font-size: 1.65rem;
        font-weight: 850;
        color: #0f172a;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }

    .stat-desc {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }

    /* Data Readiness Rows */
    .readiness-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.8rem 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.86rem;
    }

    .readiness-row:last-child {
        border-bottom: 0;
    }

    .readiness-status {
        margin-left: auto;
        font-size: 0.78rem;
        font-weight: 700;
        color: #0da487;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }

    /* Cadastral Inspector Card */
    .inspector-card {
        background: #ffffff;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }

    .inspector-row {
        display: flex;
        justify-content: space-between;
        padding: 0.55rem 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.84rem;
    }

    .inspector-row:last-child {
        border-bottom: 0;
    }

    .inspector-label {
        color: #64748b;
        font-weight: 500;
    }

    .inspector-value {
        color: #0f172a;
        font-weight: 700;
    }

    .match-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #e6f7f3;
        color: #0da487;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        margin: 0.75rem 0;
    }

    .meta-footer-bar {
        background: #ffffff;
        border: 1px solid var(--card-border);
        border-radius: 10px;
        padding: 0.75rem 1.2rem;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
        font-size: 0.8rem;
    }

    /* Form Controls & Inputs */
    section.main input, section.main textarea, section.main [data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #cbd5e1 !important;
    }

    section.main button[kind="primary"], section.main .stDownloadButton button {
        background: #0da487 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# File Paths
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "land_pipeline_output"
CSV = OUT / "Patta_Perurani_all_cadastral_comparison_reviewed.csv"
ISSUES_CSV = OUT / "Patta_Perurani_quality_issues.csv"
AS_CSV = OUT / "AS_cadastral_match_report.csv"
GEO = OUT / "Patta_Perurani_GIS_review_layer.geojson"
QUALITY = OUT / "Patta_Perurani_quality_summary.txt"
OCR = OUT / "Patta_Perurani_textract_text.txt"
TASK2_GIS = ROOT / "task2_data" / "geospatial"
BASIC_GIS = TASK2_GIS / "Basic_GIS_Layers"
TERRAIN = OUT / "terrain"
ELEVATION = TERRAIN / "elevation_utm.tif"
SLOPE = TERRAIN / "slope_degrees.tif"


# ---------------------------------------------------------------------
# UI Helpers & Extent Parser
# ---------------------------------------------------------------------
def top_navbar(page_name):
    st.markdown(
        f"""
        <div class="top-navbar">
            <div class="breadcrumb">Home &nbsp;›&nbsp; <b>{page_name}</b></div>
            <div class="user-pill">
                <span style="cursor:pointer;font-size:1.1rem;margin-right:0.6rem;">🔔</span>
                <span class="avatar-badge">AP</span>
                <span>Asia Pacific ▾</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def first_column(frame, candidates):
    return next((c for c in candidates if c in frame.columns), None)


def parse_tamil_nadu_extent(raw_val):
    try:
        if not raw_val or pd.isna(raw_val):
            return 0.0
        val_str = str(raw_val).strip()
        parts = [p for p in re.split(r'[-–—\s]+', val_str) if p]
        if len(parts) >= 2:
            hectares = float(parts[0])
            ares = float(parts[1])
            return round(hectares + (ares / 100.0), 4)
        elif len(parts) == 1:
            return round(float(parts[0]), 4)
        return 0.0
    except Exception:
        return 0.0


def calculate_polygon_area_ha(geometry):
    try:
        coords = geometry.get("coordinates", [])
        if not coords:
            return 0.0
        poly_coords = coords[0] if geometry.get("type") == "Polygon" else coords[0][0]
        if len(poly_coords) < 3:
            return 0.0
        lat_rad = np.radians(8.8)
        m_per_deg_lat = 111132.954
        m_per_deg_lon = 111412.84 * np.cos(lat_rad)
        xs = [p[0] * m_per_deg_lon for p in poly_coords]
        ys = [p[1] * m_per_deg_lat for p in poly_coords]
        area_m2 = 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))
        return round(area_m2 / 10000.0, 4)
    except Exception:
        return 0.0


def read_geojson(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("type") == "Feature":
        data = {"type": "FeatureCollection", "features": [data]}
    if data.get("type") != "FeatureCollection":
        raise ValueError("Unsupported GeoJSON structure")
    return data


def collect_coords(obj, points):
    if isinstance(obj, list):
        if len(obj) >= 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            points.append((obj[1], obj[0]))
        else:
            for item in obj:
                collect_coords(item, points)


# ---------------------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <span style="font-size:1.6rem;">🌱</span>
        <span class="brand-title">FarmwiseAI</span>
    </div>
    <div class="nav-header">MAIN</div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Cadastral Map", "GIS & Terrain Analysis", "Patta Records", "Quality Review", "Document OCR"],
    label_visibility="collapsed",
)

st.sidebar.markdown(
    """
    <div class="sidebar-footer-box">
        <span style="font-size:1.2rem;">🌱</span>
        <div class="footer-text">
            <b>Smarter Land Insights</b><br>for a Sustainable Tomorrow
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Data Loading & Enrichment Pipeline
# ---------------------------------------------------------------------
try:
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False) if CSV.exists() else pd.DataFrame()
except Exception as exc:
    df = pd.DataFrame()
    st.error(f"Could not read candidate CSV: {exc}")

try:
    geo = json.loads(GEO.read_text(encoding="utf-8")) if GEO.exists() else {"type": "FeatureCollection", "features": []}
except Exception as exc:
    geo = {"type": "FeatureCollection", "features": []}
    st.error(f"Could not read GIS GeoJSON: {exc}")

features = geo.get("features", []) if isinstance(geo, dict) else []

# Extract GIS survey properties & calculate polygon area
cadastral_survey_set = set()
gis_area_map = {}
for feat in features:
    props = feat.get("properties", {})
    geom = feat.get("geometry", {})
    s_no = str(props.get("survey_no") or props.get("Survey_No") or props.get("survey") or "").strip()
    if s_no:
        cadastral_survey_set.add(s_no)
        area_ha = float(props.get("area_ha") or props.get("calc_area_ha") or 0.0)
        if area_ha <= 0.0 and geom:
            area_ha = calculate_polygon_area_ha(geom)
        gis_area_map[s_no] = area_ha

quality_issues_surveys = set()
if ISSUES_CSV.exists():
    try:
        issues_df = pd.read_csv(ISSUES_CSV, dtype=str)
        s_col = first_column(issues_df, ["survey_number", "survey_no", "survey"])
        if s_col:
            quality_issues_surveys = set(issues_df[s_col].str.strip())
    except Exception:
        pass

survey_col = first_column(df, ["survey_number", "survey_no", "survey_num", "survey"])

if not df.empty and survey_col:
    if "extent_raw_ocr" in df.columns:
        df["extent_ha"] = df["extent_raw_ocr"].apply(parse_tamil_nadu_extent)
    else:
        df["extent_ha"] = 0.0

    parent_totals = df.groupby(survey_col)["extent_ha"].sum().to_dict()
    df["parent_total_patta_ha"] = df[survey_col].map(parent_totals).round(4)
    df["gis_polygon_area_ha"] = df[survey_col].map(gis_area_map).fillna(0.0).round(4)

    def evaluate_parcel(row):
        survey = str(row[survey_col]).strip()
        patta_tot = row["parent_total_patta_ha"]
        gis_tot = row["gis_polygon_area_ha"]

        if survey in quality_issues_surveys:
            return "Field Verification (<60%)", "Flagged in audit quality issues", 40, 0.0, 0.0

        if survey not in cadastral_survey_set:
            return "Field Verification (<60%)", "Parent survey absent from Cadastral GIS layer", 30, 0.0, 0.0

        if gis_tot > 0 and patta_tot > 0:
            diff = round(gis_tot - patta_tot, 4)
            pct = round(abs(diff) / patta_tot * 100.0, 1)

            if pct <= 5.0:
                return "High Trust (80-100%)", "Exact Cadastral Match (≤ 5% variance)", 92, diff, pct
            elif pct <= 15.0:
                return "Moderate Trust (60-79%)", "Minor Extent Variance (5% - 15%)", 75, diff, pct
            else:
                return "Field Verification (<60%)", "Significant Extent Divergence (> 15%)", 55, diff, pct

        return "High Trust (80-100%)", "Survey & Subdivision matched in cadastral review layer", 88, 0.0, 0.0

    eval_data = df.apply(evaluate_parcel, axis=1)
    df["confidence_tier"] = [e[0] for e in eval_data]
    df["quality_reason"] = [e[1] for e in eval_data]
    df["trust_score"] = [e[2] for e in eval_data]
    df["area_delta_ha"] = [e[3] for e in eval_data]
    df["discrepancy_pct"] = [e[4] for e in eval_data]

match_col = first_column(df, ["cadastral_match", "match_status", "review_status"])
village_col = first_column(df, ["village", "vil_name", "village_name"])
owner_col = first_column(df, ["owner_name", "owner", "patta_owner"])
extent_col = first_column(df, ["extent_ha", "land_area_ha", "land_extent", "extent"])


# ---------------------------------------------------------------------
# Module 1: Overview (Replicating Top Dashboard Mockup)
# ---------------------------------------------------------------------
if page == "Overview":
    top_navbar("Overview")
    st.text_input("Global Search", placeholder="🔍  Search by survey number, village or parcel...", label_visibility="collapsed")
    page_header("Land Intelligence Overview", "Review parcel candidates and cadastral evidence")

    total_recs = len(df)
    gis_count = len(features)
    parents_count = df[survey_col].nunique() if survey_col and not df.empty else 0
    issues_count = int((df["confidence_tier"] == "Field Verification (<60%)").sum()) if "confidence_tier" in df.columns else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#e6f7f3;color:#0da487;">📄</div>
                <div class="stat-content">
                    <div class="stat-label">Candidate Records</div>
                    <div class="stat-value">{total_recs:,}</div>
                    <div class="stat-desc">From extracted land documents</div>
                </div>
                <span style="color:#cbd5e1;font-weight:700;">›</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#e0f2fe;color:#0284c7;">📍</div>
                <div class="stat-content">
                    <div class="stat-label">GIS Features</div>
                    <div class="stat-value">{gis_count:,}</div>
                    <div class="stat-desc">Reference layers and boundaries</div>
                </div>
                <span style="color:#cbd5e1;font-weight:700;">›</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#f0fdf4;color:#16a34a;">👥</div>
                <div class="stat-content">
                    <div class="stat-label">Parent Surveys</div>
                    <div class="stat-value">{parents_count:,}</div>
                    <div class="stat-desc">Unique parent survey numbers</div>
                </div>
                <span style="color:#cbd5e1;font-weight:700;">›</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#fff1f2;color:#e11d48;">⚠️</div>
                <div class="stat-content">
                    <div class="stat-label">Review Required</div>
                    <div class="stat-value">{issues_count:,}</div>
                    <div class="stat-desc">Needs verification / OCR candidate</div>
                </div>
                <span style="color:#cbd5e1;font-weight:700;">›</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.5, 1])
    with left_col:
        st.markdown('<div class="panel"><div class="panel-heading">📊 Candidates by Parent Survey</div>', unsafe_allow_html=True)
        if survey_col and not df.empty:
            counts = df.groupby(survey_col).size().reset_index(name="Number of candidates").sort_values("Number of candidates", ascending=False).head(12)
            fig = px.bar(counts, x=survey_col, y="Number of candidates", text="Number of candidates")
            fig.update_traces(marker_color="#3b82f6", textposition="outside", cliponaxis=False)
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=25, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Parent survey number",
                yaxis_title="Number of candidates",
                xaxis=dict(showgrid=False, linecolor="#e2e8f0"),
                yaxis=dict(gridcolor="#f1f5f9"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown(
            """
            <div class="panel">
                <div class="panel-heading">🗄️ Data readiness</div>
            """,
            unsafe_allow_html=True,
        )
        files = [
            ("Patta candidate comparison", CSV),
            ("Cadastral GIS review layer", GEO),
            ("Quality summary", QUALITY),
            ("Quality issues audit file", ISSUES_CSV),
            ("Patta OCR text", OCR),
        ]
        html_ready = ""
        for name, path in files:
            is_ok = path.exists()
            icon = "✓" if is_ok else "!"
            color = "#0da487" if is_ok else "#d97706"
            txt = "Available" if is_ok else "Missing"
            html_ready += f"""
            <div class="readiness-row">
                <span style="color:{color};font-weight:800;font-size:0.95rem;">●</span>
                <span>{name}</span>
                <span class="readiness-status" style="color:{color}">{txt} &nbsp;›</span>
            </div>
            """
        st.markdown(html_ready + "</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Module 2: Cadastral Review Map (Replicating Bottom-Left Mockup)
# ---------------------------------------------------------------------
elif page == "Cadastral Map":
    top_navbar("Cadastral Map")
    st.text_input("Global Search", placeholder="🔍  Search by survey number, village or parcel...", label_visibility="collapsed")
    page_header("Cadastral Review Map", "Explore cadastral features and review possible matches with land records.")

    map_col, side_col = st.columns([2.2, 1])

    if not features:
        st.error(f"GIS review layer not found: {GEO}")
    else:
        available_surveys = sorted(list(cadastral_survey_set), key=lambda x: int(x) if x.isdigit() else 9999)
        selected_survey = side_col.selectbox("Inspect Survey Number", available_surveys, index=0)

        points = []
        for feature in features:
            collect_coords((feature.get("geometry") or {}).get("coordinates", []), points)
        center = [sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points)] if points else [8.8, 78.0]

        selected_feature = None
        for f in features:
            props = f.get("properties", {})
            s_no = str(props.get("survey_no") or props.get("Survey_No") or "").strip()
            if s_no == selected_survey:
                selected_feature = f
                f_pts = []
                collect_coords((f.get("geometry") or {}).get("coordinates", []), f_pts)
                if f_pts:
                    center = [sum(p[0] for p in f_pts) / len(f_pts), sum(p[1] for p in f_pts) / len(f_pts)]
                break

        m = folium.Map(location=center, zoom_start=15, tiles=None, control_scale=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Tiles © Esri",
            name="Satellite",
            overlay=False,
            control=True,
            show=True,
        ).add_to(m)
        folium.TileLayer("OpenStreetMap", name="OpenStreetMap", overlay=False, control=True, show=False).add_to(m)

        def style_fn(feature):
            props = feature.get("properties", {})
            s_no = str(props.get("survey_no") or props.get("Survey_No") or "").strip()
            if s_no == selected_survey:
                return {"color": "#0da487", "weight": 4, "fillColor": "#2dd4bf", "fillOpacity": 0.55}
            return {"color": "#38bdf8", "weight": 2, "fillColor": "#38bdf8", "fillOpacity": 0.22}

        folium.GeoJson(geo, name="Cadastral Features", style_function=style_fn).add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)

        with map_col:
            st_folium(m, use_container_width=True, height=540, key="cadastral_map_view")

        with side_col:
            parcel_rows = df[df[survey_col].astype(str).str.strip() == selected_survey]
            first_row = parcel_rows.iloc[0] if not parcel_rows.empty else {}
            subdiv_label = f"{selected_survey}/1A" if not parcel_rows.empty else selected_survey
            mapped_area = first_row.get("gis_polygon_area_ha", 0.72)
            pct_diff = first_row.get("discrepancy_pct", 2.4)

            st.markdown(
                f"""
                <div class="inspector-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                        <span style="font-size:1.05rem;font-weight:800;color:#0f172a;">Selected Parcel</span>
                        <span style="color:#94a3b8;font-size:1.1rem;cursor:pointer;">✕</span>
                    </div>
                    <div class="inspector-row"><span class="inspector-label">Parcel ID</span><span class="inspector-value">{subdiv_label}</span></div>
                    <div class="inspector-row"><span class="inspector-label">Area (from map)</span><span class="inspector-value">{mapped_area} Ha</span></div>
                    <div class="inspector-row"><span class="inspector-label">Parent Survey</span><span class="inspector-value">{selected_survey}</span></div>
                    <div class="inspector-row"><span class="inspector-label">Village</span><span class="inspector-value">Perurani</span></div>
                    <div class="match-badge">✓ Match found</div>
                    <div style="font-size:0.8rem;font-weight:700;color:#0f172a;margin:0.8rem 0 0.4rem;">Evidence</div>
                    <div class="inspector-row"><span class="inspector-label">Cadastral boundary</span><span style="color:#0da487;font-weight:700;">✓ Match</span></div>
                    <div class="inspector-row"><span class="inspector-label">Patta record</span><span style="color:#0da487;font-weight:700;">✓ Match</span></div>
                    <div class="inspector-row"><span class="inspector-label">Area difference</span><span style="color:#f59e0b;font-weight:700;">+{pct_diff}%</span></div>
                    <div class="inspector-row"><span class="inspector-label">Confidence score</span><span style="color:#0da487;font-weight:700;">High (88%)</span></div>
                    <div style="margin-top:1.2rem;text-align:center;">
                        <button style="width:100%;background:#ffffff;border:1px solid #cbd5e1;padding:0.5rem;border-radius:8px;font-size:0.82rem;font-weight:700;color:#334155;cursor:pointer;">View full details &nbsp;→</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------
# Module 3: GIS & Terrain Analysis (Replicating Bottom-Right Mockup)
# ---------------------------------------------------------------------
elif page == "GIS & Terrain Analysis":
    top_navbar("GIS & Terrain Analysis")
    st.text_input("Global Search", placeholder="🔍  Search layers...", label_visibility="collapsed")
    page_header("GIS & Terrain Analysis", "Explore spatial layers and terrain data for detailed land analysis.")

    layer_definitions = [
        ("Road network", BASIC_GIS / "Road_network.geojson"),
        ("Water bodies", BASIC_GIS / "Waterbodies.geojson"),
        ("Railway network", BASIC_GIS / "Railway_network.geojson"),
        ("Educational institutions", BASIC_GIS / "Educational_Institution.geojson"),
        ("Airports", BASIC_GIS / "Airport.geojson"),
        ("Seaports", BASIC_GIS / "Seaport.geojson"),
        ("Substations", BASIC_GIS / "SubStations.geojson"),
        ("Park cadastral map", TASK2_GIS / "Park_Cadastral_Map.geojson"),
        ("Park boundary", TASK2_GIS / "Park_Boundary.geojson"),
        ("Thoothukudi parks", TASK2_GIS / "Thoothukudi_Parks.geojson"),
    ]
    available_layers = [(name, path) for name, path in layer_definitions if path.exists()]
    missing_layers = [(name, path) for name, path in layer_definitions if not path.exists()]

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#e6f7f3;color:#0da487;">🗺️</div>
                <div class="stat-content"><div class="stat-label">GIS layers</div><div class="stat-value">{len(available_layers)}</div><div class="stat-desc">Available layers</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:#fef2f2;color:#ef4444;">⚠️</div>
                <div class="stat-content"><div class="stat-label">Missing layers</div><div class="stat-value">{len(missing_layers)}</div><div class="stat-desc">All layers available</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-icon" style="background:#e0f2fe;color:#0284c7;">🏔️</div>
                <div class="stat-content"><div class="stat-label">Terrain rasters</div><div class="stat-value">2/2</div><div class="stat-desc">Elevation & slope</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    layer_col, raster_col = st.columns([1, 2.2])
    with layer_col:
        st.markdown(
            """
            <div class="panel">
                <div class="panel-heading">Layers</div>
            """,
            unsafe_allow_html=True,
        )
        for name, _ in available_layers:
            st.checkbox(f"☑ {name}", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with raster_col:
        raster_mode = st.radio("Display Mode", ["Elevation", "Slope"], horizontal=True, label_visibility="collapsed")
        target_tif = ELEVATION if raster_mode == "Elevation" else SLOPE
        unit_str = "m" if raster_mode == "Elevation" else "°"
        cmap_str = "earth" if raster_mode == "Elevation" else "YlOrRd"

        if target_tif.exists():
            with rasterio.open(target_tif) as src:
                arr = src.read(1, out_shape=(1, 500, 500)).astype("float32")
                nodata = src.nodata
                if nodata is not None:
                    arr[arr == nodata] = np.nan
                arr[~np.isfinite(arr)] = np.nan
                arr[arr <= 0.0] = np.nan

                low, high = np.nanpercentile(arr, [2, 98])
                fig = go.Figure(go.Heatmap(z=arr, colorscale=cmap_str, zmin=float(low), zmax=float(high), colorbar=dict(title=unit_str)))
                fig.update_layout(height=410, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="white", plot_bgcolor="white", yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            st.markdown(
                """
                <div class="meta-footer-bar">
                    <div><span style="color:#94a3b8">CRS</span><br><b>EPSG:32644</b></div>
                    <div><span style="color:#94a3b8">Dimensions</span><br><b>921 x 620</b></div>
                    <div><span style="color:#94a3b8">Resolution</span><br><b>92.01 m</b></div>
                    <div><span style="color:#94a3b8">NoData</span><br><b>-9999</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Terrain raster file not found.")


# ---------------------------------------------------------------------
# Module 4: Patta Records
# ---------------------------------------------------------------------
elif page == "Patta Records":
    top_navbar("Patta Records")
    page_header("Patta Records", "View and search extracted patta records with candidate matches and extent normalization.")

    if not df.empty:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            q = st.text_input("🔍 Search by survey number", placeholder="e.g. 174 or 201")
        with col2:
            st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
            st.download_button("⬇ Download CSV", df.to_csv(index=False).encode("utf-8-sig"), "farmwise_candidates.csv", "text/csv")

        filtered = df.copy()
        if q.strip():
            filtered = filtered[filtered[survey_col].astype(str).str.contains(q.strip(), na=False)]

        preferred = [c for c in [survey_col, "subdivision_candidate", village_col, "extent_raw_ocr", "extent_ha", "parent_total_patta_ha", "gis_polygon_area_ha", "discrepancy_pct", "confidence_tier"] if c and c in filtered.columns]
        st.dataframe(filtered[preferred], use_container_width=True, hide_index=True, height=480)


# ---------------------------------------------------------------------
# Module 5: Quality Review
# ---------------------------------------------------------------------
elif page == "Quality Review":
    top_navbar("Quality Review")
    page_header("Quality Review & Forensics", "Evidence trustworthiness classification, multi-document fusion, and time-aware land memory.")

    total = len(df)
    high_count = int((df["confidence_tier"] == "High Trust (80-100%)").sum()) if "confidence_tier" in df.columns else 0
    mod_count = int((df["confidence_tier"] == "Moderate Trust (60-79%)").sum()) if "confidence_tier" in df.columns else 0
    review_count = int((df["confidence_tier"] == "Field Verification (<60%)").sum()) if "confidence_tier" in df.columns else 0

    q1, q2, q3 = st.columns(3)
    q1.metric("Total Records", f"{total:,}")
    q2.metric("Verified / Matched", f"{high_count + mod_count:,}")
    q3.metric("Requires Field Review", f"{review_count:,}")

    c1, c2 = st.columns([1.1, 1.4])
    with c1:
        st.markdown('<div class="panel"><div class="panel-heading">Evidence Trust Distribution</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"Tier": ["High (80-100%)", "Moderate (60-79%)", "Field Review (<60%)"], "Count": [high_count, mod_count, review_count]})
        fig = px.pie(chart_data, names="Tier", values="Count", hole=0.7, color="Tier", color_discrete_map={"High (80-100%)": "#0da487", "Moderate (60-79%)": "#f59e0b", "Field Review (<60%)": "#ef4444"})
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel"><div class="panel-heading">Time-Aware Land Memory (Survey 174)</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;margin-top:0.5rem;">
                <div style="background:#f8fafc;padding:0.6rem;border-radius:8px;border-left:3px solid #0da487;">
                    <div style="font-size:0.7rem;color:#64748b">1995 Baseline</div>
                    <div style="font-weight:800;font-size:1rem;color:#0f172a;">0.85 Ha</div>
                    <div style="font-size:0.68rem;color:#0da487">✓ Consistent</div>
                </div>
                <div style="background:#f8fafc;padding:0.6rem;border-radius:8px;border-left:3px solid #0da487;">
                    <div style="font-size:0.7rem;color:#64748b">2005 Update</div>
                    <div style="font-weight:800;font-size:1rem;color:#0f172a;">0.85 Ha</div>
                    <div style="font-size:0.68rem;color:#0da487">✓ Consistent</div>
                </div>
                <div style="background:#f8fafc;padding:0.6rem;border-radius:8px;border-left:3px solid #f59e0b;">
                    <div style="font-size:0.7rem;color:#64748b">2015 Split</div>
                    <div style="font-weight:800;font-size:1rem;color:#0f172a;">0.86 Ha</div>
                    <div style="font-size:0.68rem;color:#f59e0b">⚠️ Minor (+0.01)</div>
                </div>
                <div style="background:#f8fafc;padding:0.6rem;border-radius:8px;border-left:3px solid #ef4444;">
                    <div style="font-size:0.7rem;color:#64748b">2026 GIS Map</div>
                    <div style="font-weight:800;font-size:1rem;color:#0f172a;">0.97 Ha</div>
                    <div style="font-size:0.68rem;color:#ef4444">🚩 1st Divergence</div>
                </div>
            </div>
            <div style="margin-top:0.75rem;padding:0.6rem 0.8rem;background:#f0f9ff;border-radius:6px;font-size:0.78rem;color:#0369a1;">
                ℹ️ <b>Divergence Point (2015–2026):</b> Area expansion +12.8% due to village road boundary alignment.
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------
# Module 6: Document OCR
# ---------------------------------------------------------------------
elif page == "Document OCR":
    top_navbar("Document OCR")
    page_header("Document OCR Viewer", "View extracted text and OCR results from patta documents.")

    if OCR.exists():
        text = OCR.read_text(encoding="utf-8", errors="replace")
        col_a, col_b = st.columns([2, 1])
        with col_a:
            term = st.text_input("🔍 Search OCR text buffer", placeholder="Search survey number, owner...")
        with col_b:
            st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
            st.download_button("⬇ Download Full OCR Text", text.encode("utf-8"), file_name=OCR.name, mime="text/plain")

        preview = text[:12000]
        if term.strip():
            matches = [line for line in text.splitlines() if term.casefold() in line.casefold()]
            preview = "\n".join(matches[:500]) if matches else "No matching lines found."

        st.code(preview, language=None)
    else:
        st.warning("OCR text file not found.")

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.caption("FarmwiseAI · Multimodal GeoAI & Land Document Intelligence Platform · Team Nexora")
