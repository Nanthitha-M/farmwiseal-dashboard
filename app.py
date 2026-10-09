from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="FarmwiseAI | Land Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Theme: navy navigation, pale blue canvas, white cards, accessible text.
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --navy: #08264f;
        --navy-2: #103866;
        --blue: #0878e8;
        --blue-2: #e8f3ff;
        --canvas: #f2f7fd;
        --ink: #102b53;
        --muted: #58708f;
        --border: #dce8f5;
        --green: #0caa70;
        --red: #e94b62;
        --amber: #f5a623;
    }
    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: rgba(242, 247, 253, .94);
    }
    section.main .block-container {
        max-width: 1600px;
        padding: 1.45rem 1.7rem 2.5rem;
    }
    section.main h1, section.main h2, section.main h3,
    section.main h4, section.main p, section.main li,
    section.main label, section.main [data-testid="stCaptionContainer"],
    section.main [data-testid="stMetricLabel"],
    section.main [data-testid="stMetricValue"] {
        color: var(--ink);
    }
    section.main h1 {
        font-size: clamp(1.65rem, 2.2vw, 2.25rem);
        font-weight: 800;
        letter-spacing: -.035em;
    }
    section.main h2, section.main h3 {
        font-weight: 750;
        letter-spacing: -.02em;
    }
    section.main [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #09264e 0%, #061d3d 100%);
        border-right: 1px solid #1c3b64;
    }
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    section[data-testid="stSidebar"] * {
        color: #f5f9ff;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 9px;
        padding: .38rem .55rem;
        margin: .08rem 0;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #f5f9ff !important;
        font-weight: 550;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #0878e8;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] input {
        accent-color: #45a4ff;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #b8c9df !important;
    }
    .brand {
        font-size: 1.28rem;
        font-weight: 850;
        letter-spacing: -.03em;
        padding: .3rem 0 1.4rem;
        color: #fff;
    }
    .brand span { color: #52dc8b; }
    .side-kicker {
        font-size: .68rem;
        letter-spacing: .12em;
        font-weight: 800;
        color: #a9c2e2;
        margin-bottom: .25rem;
    }
    .side-footer {
        margin-top: 1.25rem;
        padding-top: .9rem;
        border-top: 1px solid #29466a;
        color: #b8c9df;
        font-size: .78rem;
    }

    /* Hero and common cards */
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        padding: 1.55rem 1.7rem;
        margin-bottom: 1.05rem;
        color: #fff;
        background: linear-gradient(112deg, #08264f 0%, #075b91 72%, #0a7b8d 100%);
        box-shadow: 0 8px 24px rgba(8, 38, 79, .13);
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 15rem;
        height: 15rem;
        right: -3rem;
        top: -8rem;
        border-radius: 50%;
        background: rgba(255,255,255,.08);
    }
    .hero .eyebrow {
        color: #a8e4ff;
        font-size: .73rem;
        letter-spacing: .12em;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: .35rem;
    }
    .hero h1 {
        color: #fff !important;
        margin: 0 0 .35rem;
        font-size: 1.8rem;
    }
    .hero p {
        color: #e5f3ff !important;
        margin: 0;
        max-width: 48rem;
        font-size: .92rem;
    }
    .section-heading {
        font-size: 1.02rem;
        font-weight: 800;
        color: var(--ink);
        margin: .55rem 0 .8rem;
    }
    .panel {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 1rem 1.05rem;
        box-shadow: 0 4px 14px rgba(16, 43, 83, .045);
    }
    .panel-title {
        color: var(--ink);
        font-weight: 800;
        font-size: .92rem;
        margin-bottom: .7rem;
    }
    .file-row {
        display: flex;
        align-items: center;
        gap: .65rem;
        padding: .62rem 0;
        border-bottom: 1px solid #edf2f8;
        color: var(--ink);
        font-size: .84rem;
    }
    .file-row:last-child { border-bottom: 0; }
    .file-icon {
        width: 1.8rem;
        height: 1.8rem;
        border-radius: 8px;
        background: var(--blue-2);
        color: var(--blue);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }
    .file-status {
        margin-left: auto;
        font-size: .75rem;
        color: #078c61;
        font-weight: 750;
        white-space: nowrap;
    }
    .info-banner {
        border: 1px solid #d7eaff;
        background: #e5f2ff;
        color: #174b83;
        padding: .75rem .9rem;
        border-radius: 10px;
        font-size: .82rem;
        margin: .8rem 0 .2rem;
    }
    .small-muted { color: var(--muted); font-size: .8rem; }
    .status-pill {
        display: inline-block;
        padding: .18rem .5rem;
        border-radius: 5px;
        font-size: .72rem;
        font-weight: 750;
        background: #d9f8e9;
        color: #08774f;
    }

    /* Streamlit metric cards */
    div[data-testid="stMetric"] {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 1rem 1.05rem;
        box-shadow: 0 4px 14px rgba(16, 43, 83, .045);
        min-height: 105px;
    }
    div[data-testid="stMetricLabel"] { color: var(--muted) !important; }
    div[data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-weight: 850;
    }
    div[data-testid="stMetricDelta"] { font-size: .75rem; }

    /* Inputs/selects/buttons */
    section.main input, section.main textarea,
    section.main [data-baseweb="input"] input,
    section.main [data-baseweb="textarea"] textarea {
        background: #fff !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        border-color: #cbdced !important;
        border-radius: 8px !important;
        opacity: 1 !important;
    }
    section.main input::placeholder, section.main textarea::placeholder {
        color: #7186a0 !important;
        -webkit-text-fill-color: #7186a0 !important;
        opacity: 1 !important;
    }
    section.main [data-baseweb="select"] > div {
        background: #fff;
        border-color: #cbdced;
        border-radius: 8px;
    }
    section.main [data-baseweb="select"] * { color: var(--ink); }
    section.main button[kind="primary"],
    section.main .stDownloadButton button {
        background: var(--blue) !important;
        color: #fff !important;
        border: 1px solid var(--blue) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    section.main button[kind="primary"] *,
    section.main .stDownloadButton button * {
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
    }
    section.main button[kind="secondary"] {
        color: #174b83 !important;
        border-color: #c6d8eb !important;
        border-radius: 8px !important;
        background: #fff !important;
    }
    section.main [data-testid="stDataFrame"],
    section.main [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
        background: #fff;
    }
    section.main pre, section.main code {
        background: #08264f !important;
        color: #eaf3ff !important;
        border-radius: 10px;
    }
    section.main [data-testid="stAlert"] { border-radius: 10px; }
    section.main hr { border-color: var(--border); }
    div[data-testid="stPlotlyChart"] {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: .4rem .45rem .05rem;
        box-shadow: 0 4px 14px rgba(16, 43, 83, .035);
    }
    @media (max-width: 800px) {
        section.main .block-container { padding: 1rem .8rem 2rem; }
        .hero { padding: 1.15rem; }
        .hero h1 { font-size: 1.45rem; }
    }
    </style>
    """,
    
    unsafe_allow_html=True,
)

OUT = Path(__file__).resolve().parent / "land_pipeline_output"
CSV = OUT / "Patta_Perurani_all_cadastral_comparison_reviewed.csv"
GEO = OUT / "Patta_Perurani_GIS_review_layer.geojson"
QUALITY = OUT / "Patta_Perurani_quality_summary.txt"
OCR = OUT / "Patta_Perurani_textract_text.txt"

TASK2_GIS = Path(__file__).resolve().parent / "task2_data" / "geospatial"
BASIC_GIS = TASK2_GIS / "Basic_GIS_Layers"

def hero(title, subtitle, eyebrow="LAND INTELLIGENCE"):
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)


def info_banner(message):
    st.markdown(f'<div class="info-banner">ℹ️&nbsp; {message}</div>', unsafe_allow_html=True)


def first_column(frame, candidates):
    return next((c for c in candidates if c in frame.columns), None)


def safe_text(value):
    return str(value).strip() if value is not None else ""


def status_series(frame):
    col = first_column(frame, ["review_status", "quality_status", "cadastral_match", "match_status"])
    if col is None or frame.empty:
        return pd.Series(["Needs Review"] * len(frame), index=frame.index)
    return frame[col].astype(str)


def plot_layout(fig, height=300):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=45, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color="#102b53", size=11),
        title=dict(font=dict(size=14, color="#102b53"), x=0.02, xanchor="left"),
        legend=dict(font=dict(color="#365575")),
        xaxis=dict(showgrid=False, zeroline=False, linecolor="#e4edf7"),
        yaxis=dict(gridcolor="#edf2f8", zeroline=False),
    )
    return fig


# Sidebar brand + navigation
st.sidebar.markdown('<div class="brand"><span>🌱</span> FarmwiseAI</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-kicker">NAVIGATION</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Cadastral Map",
        "GIS & Terrain Analysis",
        "Patta Records",
        "Quality Review",
        "Document OCR",
    ]
)
st.sidebar.markdown(
    '<div class="side-footer">Task 2 | Review prototype</div>',
    unsafe_allow_html=True,
)

# Load data without changing the source files.
try:
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False) if CSV.exists() else pd.DataFrame()
except Exception as exc:
    df = pd.DataFrame()
    st.error(f"Could not read candidate CSV: {exc}")

try:
    geo = json.loads(GEO.read_text(encoding="utf-8")) if GEO.exists() else {
        "type": "FeatureCollection", "features": []
    }
except Exception as exc:
    geo = {"type": "FeatureCollection", "features": []}
    st.error(f"Could not read GIS GeoJSON: {exc}")

features = geo.get("features", []) if isinstance(geo, dict) else []
survey_col = first_column(df, ["survey_number", "survey_no", "survey_num", "survey"])
match_col = first_column(df, ["cadastral_match", "match_status", "review_status"])
village_col = first_column(df, ["village", "vil_name", "village_name"])
owner_col = first_column(df, ["owner_name", "owner", "patta_owner"])
extent_col = first_column(df, ["land_area_ha", "land_extent", "extent", "area_ha", "area"])
status_col = first_column(df, ["review_status", "quality_status", "cadastral_match", "match_status"])

if page == "Overview":
    hero("Project Overview", "Review extracted land-record candidates and their possible cadastral links.")
    possible_matches = 0
    if match_col and not df.empty:
        possible_matches = int(
            df[match_col].astype(str).str.contains(r"possible|matched|match", case=False, na=False, regex=True).sum()
        )
    metrics = st.columns(4)
    metrics[0].metric("Candidate Rows", f"{len(df):,}")
    metrics[1].metric("GIS Features", f"{len(features):,}")
    metrics[2].metric("Parent Surveys", f"{df[survey_col].nunique():,}" if survey_col and not df.empty else "0")
    metrics[3].metric("Possible Matches", f"{possible_matches:,}")

    left, right = st.columns([1.15, 1])
    with left:
        section_title("Extracted candidates by parent survey")
        if survey_col and not df.empty:
            counts = df.groupby(survey_col).size().reset_index(name="Candidate rows")
            counts = counts.sort_values("Candidate rows", ascending=False).head(12)
            fig = px.bar(counts, x=survey_col, y="Candidate rows", text="Candidate rows")
            fig.update_traces(marker_color="#3f9bff", textposition="outside", cliponaxis=False)
            fig.update_layout(title=None, xaxis_title=None, yaxis_title=None, showlegend=False)
            st.plotly_chart(plot_layout(fig, 300), use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Survey-number data is not available for a chart.")
    with right:
        section_title("Pipeline Files")
        rows = [
            ("Patta candidate comparison", CSV),
            ("Cadastral GIS review layer", GEO),
            ("Quality summary", QUALITY),
            ("Patta OCR text", OCR),
        ]
        html = '<div class="panel">'
        for label, path in rows:
            available = path.exists()
            icon = "✓" if available else "!"
            state = "Available" if available else "Not found"
            color = "#0caa70" if available else "#d97706"
            html += (
                f'<div class="file-row"><span class="file-icon">{icon}</span>'
                f'<span>{label}</span><span class="file-status" style="color:{color}">{state}</span></div>'
            )
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    info_banner("Matches are preliminary parent-survey links. They do not verify subdivision boundaries, land extent, or legal ownership.")

elif page == "Cadastral Map":
    hero("Cadastral Review Map", "Explore cadastral features and review possible matches with land records.", "GIS EXPLORER")
    map_col, side_col = st.columns([2.25, 1])
    if not features:
        st.error(f"GIS review layer not found or contains no features: {GEO}")
    else:
        # Derive map center from GeoJSON coordinate arrays.
        points = []

        def collect_coordinates(obj):
            if isinstance(obj, list):
                if len(obj) >= 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
                    points.append((obj[1], obj[0]))
                else:
                    for item in obj:
                        collect_coordinates(item)

        for feature in features:
            geometry = feature.get("geometry") or {}
            collect_coordinates(geometry.get("coordinates", []))

        center = (
            [sum(point[0] for point in points) / len(points), sum(point[1] for point in points) / len(points)]
            if points else [8.8, 78.0]
        )
        m = folium.Map(location=center, zoom_start=14, tiles="OpenStreetMap", control_scale=True)
        props0 = features[0].get("properties") or {}
        tooltip_fields = [key for key in [
            "vil_name", "survey_no", "unit_id", "block_id", "patta_candidate_count", "review_status"
        ] if key in props0]
        folium.GeoJson(
            geo,
            name="Cadastral Features",
            style_function=lambda feature: {
                "color": "#1678d4",
                "weight": 2,
                "fillColor": "#4da3ff",
                "fillOpacity": 0.24,
            },
            highlight_function=lambda feature: {
                "color": "#f5a623", "weight": 3, "fillOpacity": 0.4
            },
            tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, sticky=False) if tooltip_fields else None,
        ).add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
        with map_col:
            st.markdown('<div class="panel-title">Cadastral feature map</div>', unsafe_allow_html=True)
            map_state = st_folium(m, use_container_width=True, height=540, returned_objects=["last_object_clicked", "last_active_drawing"])
        with side_col:
            section_title("Map Legend")
            st.markdown("""
            <div class="panel">
              <div class="file-row"><span style="color:#1678d4">▰</span><span>Cadastral boundary</span></div>
              <div class="file-row"><span style="color:#f5a623">▰</span><span>Highlighted feature</span></div>
              <div class="file-row"><span style="color:#e94b62">▰</span><span>Unmatched candidate</span></div>
              <div class="file-row"><span style="color:#0caa70">●</span><span>Selected feature</span></div>
            </div>
            """, unsafe_allow_html=True)
            section_title("Layer Details")
            st.markdown(
                f'<div class="panel"><div class="small-muted">GIS features</div>'
                f'<div style="font-size:1.6rem;font-weight:850;color:#102b53">{len(features):,}</div>'
                f'<div class="small-muted">Source: GIS review GeoJSON</div></div>',
                unsafe_allow_html=True,
            )
    info_banner("Click a feature to inspect its attributes. The supplied geometries and candidate links require independent verification.")


elif page == "GIS & Terrain Analysis":
    hero(
        "GIS & Terrain Analysis",
        "Explore supplied cadastral maps and geographic reference layers.",
        "GIS EXPLORER",
    )
    st.caption(
        "Toggle the supplied layers below. Layers may cover different areas; "
        "verify geographic alignment before drawing parcel-level conclusions."
    )

    layer_definitions = [
        ("Park boundary", TASK2_GIS / "Park_Boundary.geojson"),
        ("Park cadastral map", TASK2_GIS / "Park_Cadastral_Map.geojson"),
        ("Park FMB map", TASK2_GIS / "Park_fmb_Map.geojson"),
        ("Thoothukudi parks", TASK2_GIS / "Thoothukudi_Parks.geojson"),
        ("Airports", BASIC_GIS / "Airport.geojson"),
        ("Educational institutions", BASIC_GIS / "Educational_Institution.geojson"),
        ("Railway stations", BASIC_GIS / "Railway_Stations.geojson"),
        ("Railway network", BASIC_GIS / "Railway_network.geojson"),
        ("Road network", BASIC_GIS / "Road_network.geojson"),
        ("Seaports", BASIC_GIS / "Seaport.geojson"),
        ("Substations", BASIC_GIS / "SubStations.geojson"),
        ("Waterbodies", BASIC_GIS / "Waterbodies.geojson"),
    ]
    available = [(name, path) for name, path in layer_definitions if path.exists()]
    missing = [(name, path) for name, path in layer_definitions if not path.exists()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Available GIS layers", len(available))
    c2.metric("Missing GIS layers", len(missing))
    c3.metric("DEM raster", "Not added")

    if missing:
        with st.expander("Missing layer files"):
            for name, path in missing:
                st.write(f"**{name}:** `{path}`")

    if not available:
        st.warning("No Task 2 GeoJSON files found. Check task2_data/geospatial.")
    else:
        default_names = {"Park boundary", "Park cadastral map"}
        selected = st.multiselect(
            "Layers to display",
            options=[name for name, _ in available],
            default=[name for name, _ in available if name in default_names],
        )

        # Calculate an initial center from the first selected layer with coordinates.
        center = [8.79, 78.01]
        for name, path in available:
            if name not in selected:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                coords = []

                def collect_coordinates(obj):
                    if isinstance(obj, list):
                        if (
                            len(obj) >= 2
                            and isinstance(obj[0], (int, float))
                            and isinstance(obj[1], (int, float))
                        ):
                            coords.append((obj[1], obj[0]))
                        else:
                            for child in obj:
                                collect_coordinates(child)

                features_for_center = data.get("features", [])
                if data.get("type") == "Feature":
                    features_for_center = [data]
                for feature in features_for_center:
                    geometry = feature.get("geometry") or {}
                    collect_coordinates(geometry.get("coordinates", []))
                if coords:
                    center = [
                        sum(p[0] for p in coords) / len(coords),
                        sum(p[1] for p in coords) / len(coords),
                    ]
                    break
            except Exception:
                continue

        gis_map = folium.Map(
            location=center, zoom_start=12, tiles="OpenStreetMap", control_scale=True
        )
        loaded = 0
        for name, path in available:
            if name not in selected:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if data.get("type") not in ("FeatureCollection", "Feature"):
                    st.warning(f"{name}: unsupported GeoJSON structure; skipped.")
                    continue
                props = {}
                if data.get("type") == "FeatureCollection" and data.get("features"):
                    props = data["features"][0].get("properties") or {}
                elif data.get("type") == "Feature":
                    props = data.get("properties") or {}
                fields = list(props.keys())[:4]
                tooltip = folium.GeoJsonTooltip(fields=fields) if fields else name
                folium.GeoJson(data, name=name, tooltip=tooltip).add_to(gis_map)
                loaded += 1
            except Exception as exc:
                st.error(f"Could not load {name} ({path.name}): {exc}")

        folium.LayerControl(collapsed=False).add_to(gis_map)
        st.caption(f"Displaying {loaded} selected layer(s).")
        st_folium(gis_map, use_container_width=True, height=620, key="task2_gis_map")

        with st.expander("GIS layer inventory"):
            inventory = pd.DataFrame([
                {
                    "Layer": name,
                    "File": path.name,
                    "Status": "Available" if path.exists() else "Missing",
                    "Size (KB)": round(path.stat().st_size / 1024, 1) if path.exists() else None,
                }
                for name, path in layer_definitions
            ])
            st.dataframe(inventory, use_container_width=True, hide_index=True)

    st.subheader("Terrain and elevation analysis")
    st.info(
        "A DEM/elevation raster has not been integrated yet. Terrain, slope, and "
        "elevation analysis will be added after a suitable public raster is sourced "
        "and validated. No terrain results are claimed at this stage."
    )
    info_banner(
        "GIS layers are reference data. Their presence on the map does not confirm "
        "ownership, legal boundaries, or a match to a patta record."
    )

elif page == "Patta Records":
    hero("Patta Records", "View and search extracted patta records with candidate matches.", "LAND RECORDS")
    if df.empty:
        st.error(f"Candidate CSV not found or empty: {CSV}")
    else:
        filter1, filter2, filter3 = st.columns([1, 1, 1])
        with filter1:
            query = st.text_input("Search by survey no.", placeholder="e.g. 21/5")
        with filter2:
            villages = sorted(df[village_col].astype(str).replace("", pd.NA).dropna().unique()) if village_col else []
            village_choice = st.selectbox("Village", ["All Villages"] + villages)
        with filter3:
            statuses = sorted(status_series(df).replace("", pd.NA).dropna().unique())
            status_choice = st.selectbox("Status", ["All Statuses"] + statuses)

        filtered = df.copy()
        if query.strip():
            search_rows = filtered.astype(str).agg(" | ".join, axis=1)
            filtered = filtered[search_rows.str.contains(query.strip(), case=False, na=False, regex=False)]
        if village_col and village_choice != "All Villages":
            filtered = filtered[filtered[village_col].astype(str) == village_choice]
        if status_choice != "All Statuses" and status_col:
            filtered = filtered[filtered[status_col].astype(str) == status_choice]

        top_left, top_right = st.columns([1.4, 1])
        with top_left:
            st.caption(f"Showing {len(filtered):,} of {len(df):,} records")
        with top_right:
            st.download_button(
                "⬇ Download CSV",
                filtered.to_csv(index=False).encode("utf-8-sig"),
                file_name="farmwiseal_filtered_candidates.csv",
                mime="text/csv",
                use_container_width=True,
            )
        preferred = [c for c in [
            survey_col, village_col, owner_col, extent_col, status_col, match_col
        ] if c and c in filtered.columns]
        display_cols = list(dict.fromkeys(preferred + [c for c in filtered.columns if c not in preferred]))
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True, height=450)
        st.download_button(
            "Download complete CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            file_name="farmwiseal_all_candidates.csv",
            mime="text/csv",
        )

elif page == "Quality Review":
    hero("Quality Review", "Review data quality, OCR results, and validation status.", "QUALITY CONTROL")
    total = len(df)
    statuses = status_series(df).str.lower()
    if total:
        invalid_mask = statuses.str.contains(r"invalid|error|issue|unmatched|missing", regex=True, na=False)
        review_mask = statuses.str.contains(r"review|verify|candidate|possible|manual|unusual", regex=True, na=False)
        valid_count = int((~invalid_mask & ~review_mask).sum())
        issue_count = int((invalid_mask | review_mask).sum())
    else:
        valid_count = 0
        issue_count = 0
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Records", f"{total:,}")
    k2.metric("Valid / No Flag", f"{valid_count:,}", f"{(valid_count / total * 100):.1f}% of rows" if total else "No data")
    k3.metric("Issues / Review", f"{issue_count:,}", f"{(issue_count / total * 100):.1f}% of rows" if total else "No data")

    chart_col, issue_col = st.columns([1, 1])
    with chart_col:
        section_title("Quality Status")
        if total:
            quality_chart = pd.DataFrame({
                "Status": ["Valid / No Flag", "Needs Attention"],
                "Records": [valid_count, issue_count],
            })
            fig = px.pie(quality_chart, names="Status", values="Records", hole=.72,
                         color="Status", color_discrete_map={"Valid / No Flag": "#16bd83", "Needs Attention": "#ff6478"})
            fig.update_traces(textinfo="percent", textposition="inside", marker=dict(line=dict(color="#ffffff", width=3)))
            fig.add_annotation(text=f"{(valid_count / total * 100):.1f}%<br><sup>no flag</sup>",
                                x=.5, y=.5, showarrow=False, font=dict(size=18, color="#102b53"))
            fig.update_layout(showlegend=True, title=None, legend=dict(orientation="h", y=-.1))
            st.plotly_chart(plot_layout(fig, 300), use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No candidate records are available.")
    with issue_col:
        section_title("Common Issues")
        if total:
            issue_types = []
            if status_col:
                raw = df[status_col].astype(str).str.lower()
                for label, pattern in [
                    ("Needs review", r"review|verify|candidate|possible|manual"),
                    ("Invalid / error", r"invalid|error"),
                    ("Unmatched", r"unmatched|no match"),
                    ("Missing data", r"missing|incomplete|blank"),
                ]:
                    count = int(raw.str.contains(pattern, regex=True, na=False).sum())
                    if count:
                        issue_types.append({"Issue": label, "Records": count})
            if issue_types:
                issues_df = pd.DataFrame(issue_types)
                fig = px.bar(issues_df, x="Records", y="Issue", orientation="h", text="Records")
                fig.update_traces(marker_color="#4c9dff", textposition="outside")
                fig.update_layout(title=None, xaxis_title=None, yaxis_title=None, showlegend=False)
                st.plotly_chart(plot_layout(fig, 300), use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("No status-based issue categories were found in the available columns.")
        else:
            st.info("No data is available to calculate issue categories.")

    section_title("Recent Records")
    if not df.empty:
        recent_cols = [c for c in [survey_col, owner_col, status_col] if c]
        recent = df[recent_cols].head(10) if recent_cols else df.head(10)
        st.dataframe(recent, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download review queue",
            df[statuses.str.contains(r"review|verify|candidate|possible|manual|invalid|error|unmatched", regex=True, na=False)].to_csv(index=False).encode("utf-8-sig"),
            file_name="farmwiseal_review_queue.csv",
            mime="text/csv",
        )
    if QUALITY.exists():
        with st.expander("View original quality summary file"):
            st.code(QUALITY.read_text(encoding="utf-8", errors="replace"))
    info_banner("Automated status labels are review aids, not legal or ownership determinations. Verify flagged records against original documents.")

elif page == "Document OCR":
    hero("Document OCR Viewer", "View extracted text and OCR results from patta documents.", "DOCUMENT INTELLIGENCE")
    if not OCR.exists():
        st.warning(f"Patta OCR text not found: {OCR}")
    else:
        text = OCR.read_text(encoding="utf-8", errors="replace")
        top_a, top_b = st.columns([1.5, 1])
        with top_a:
            st.markdown('<div class="panel-title">OCR source document</div>', unsafe_allow_html=True)
            st.selectbox("Select OCR text", [OCR.name], label_visibility="collapsed")
        with top_b:
            st.markdown('<div style="height:1.7rem"></div>', unsafe_allow_html=True)
            st.download_button(
                "⬇ Download Full OCR Text",
                text.encode("utf-8"),
                file_name=OCR.name,
                mime="text/plain",
                use_container_width=True,
            )
        term = st.text_input("Search OCR text", placeholder="Find a survey number, name, or land extent")
        if term.strip():
            matches = [line for line in text.splitlines() if term.casefold() in line.casefold()]
            st.caption(f"Matching lines: {len(matches):,}")
            preview = "\n".join(matches[:500]) if matches else "No matches found."
        else:
            preview = text[:12000]
        section_title("OCR Preview")
        st.code(preview if preview.strip() else "No OCR text found in this file.", language=None)
        info_banner("OCR text is extracted from the source document and may contain recognition errors. Verify critical details against the original record.")

st.divider()
st.caption("FarmwiseAI | Land Intelligence prototype · Human verification is required before treating matches as authoritative.")
