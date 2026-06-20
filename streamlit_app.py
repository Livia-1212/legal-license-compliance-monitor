import streamlit as st
import pandas as pd

from src.dashboard.dashboard_summary import generate_dashboard_summary
from src.analysis.risk_scoring import calculate_attorney_risk_scores
from src.analysis.matter_license_check import find_matter_license_risks
from src.analysis.load_data import load_all_data


st.set_page_config(
    page_title="Attorney License Compliance Monitor",
    page_icon="⚖️",
    layout="wide",
)


# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown(
    """
    <style>
    /* -----------------------------
       Main app background
    ----------------------------- */
    .stApp {
        background-color: #F4F6F9;
        color: #1F2937;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* -----------------------------
       Sidebar base styling
    ----------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB !important;
    }

    /* Reduce default Streamlit sidebar spacing */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Sidebar header */
    .sidebar-header {
        margin-bottom: 1.25rem;
    }

    .sidebar-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F9FAFB;
        line-height: 1.2;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }

    .sidebar-subtitle {
        font-size: 0.95rem;
        color: #9CA3AF !important;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* Remove empty radio label spacing */
    section[data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }

    /* Pull navigation buttons closer to header */
    section[data-testid="stSidebar"] .stRadio {
        margin-top: 0.25rem;
    }

    /* Hide the default radio circles */
    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* Navigation button style */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;
        padding: 16px 18px !important;
        margin-bottom: 14px;
        min-height: 56px;
        display: flex !important;
        align-items: center !important;
        cursor: pointer;
        transition: all 0.18s ease-in-out;
    }

    /* Navigation hover effect */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: rgba(201, 162, 39, 0.14);
        border-color: rgba(201, 162, 39, 0.42);
        transform: translateX(2px);
    }

    /* Navigation text */
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }

    /* Selected navigation item */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background-color: rgba(201, 162, 39, 0.20);
        border: 1px solid rgba(201, 162, 39, 0.75);
        box-shadow: 0 0 0 1px rgba(201, 162, 39, 0.18);
    }

    /* Gold selected indicator */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked)::before {
        content: "";
        width: 4px;
        height: 28px;
        background-color: #C9A227;
        border-radius: 999px;
        margin-right: 12px;
        flex-shrink: 0;
    }

    /* -----------------------------
       Main title styling
    ----------------------------- */
    .app-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }

    .app-subtitle {
        font-size: 1.0rem;
        color: #6B7280;
        margin-bottom: 1.75rem;
    }

    /* -----------------------------
       Section headers
    ----------------------------- */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.5rem;
        margin-bottom: 1.0rem;
        border-left: 6px solid #C9A227;
        padding-left: 12px;
    }

    .subsection-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1F2937;
        margin-top: 1.25rem;
        margin-bottom: 0.75rem;
    }

    /* -----------------------------
       KPI cards
    ----------------------------- */
    .kpi-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-left: 6px solid #C9A227;
        border-radius: 14px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
        min-height: 110px;
    }

    .kpi-label {
        font-size: 0.9rem;
        color: #6B7280;
        margin-bottom: 0.45rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.2;
    }

    /* -----------------------------
    Clickable KPI button cards
    ----------------------------- */
    div[data-testid="stButton"] > button {
        background: white;
        border: 1px solid #E5E7EB;
        border-left: 6px solid #C9A227;
        border-radius: 14px;
        padding: 22px 18px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
        min-height: 120px;
        text-align: left;
        color: #111827;
        font-weight: 800;
        white-space: pre-line;
        transition: all 0.18s ease-in-out;
    }

    div[data-testid="stButton"] > button:hover {
        border-left: 6px solid #A67C00;
        border-color: #C9A227;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
        transform: translateY(-2px);
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(0px);
    }

    /* -----------------------------
       Panel / table styling
    ----------------------------- */
    .panel-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 18px 18px 10px 18px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        overflow: hidden;
        background: white;
    }

    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E5E7EB;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
    }

    /* Optional divider if needed elsewhere */
    .divider {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin-top: 0.5rem;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Cached Data Loaders
# -----------------------------
@st.cache_data
def get_data():
    return load_all_data()


@st.cache_data
def get_dashboard_summary():
    return generate_dashboard_summary()


@st.cache_data
def get_risk_scores():
    return calculate_attorney_risk_scores()


@st.cache_data
def get_matter_license_risks():
    return find_matter_license_risks()


# -----------------------------
# Load data
# -----------------------------
data = get_data()
summary = get_dashboard_summary()
risk_scores = get_risk_scores()
matter_license_risks = get_matter_license_risks()

attorneys = data["attorneys"]
licenses = data["licenses"]
cle_records = data["cle_records"]
matters = data["matters"]
assignments = data["matter_assignments"]


# -----------------------------
# Helper UI functions
# -----------------------------
def render_kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def subsection_title(text):
    st.markdown(f'<div class="subsection-title">{text}</div>', unsafe_allow_html=True)

def go_to_page(page_name):
    st.session_state["page"] = page_name


def render_clickable_kpi_card(label, value, target_page, key):
    st.button(
        f"{label}\n\n{value}",
        key=key,
        use_container_width=True,
        on_click=go_to_page,
        args=(target_page,),
    )


def render_attorney_filters(attorney_df):
    st.markdown("#### Filter Attorneys")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        office_filter = st.multiselect(
            "Office",
            options=sorted(attorney_df["office"].dropna().unique()),
            default=sorted(attorney_df["office"].dropna().unique()),
        )

    with c2:
        title_filter = st.multiselect(
            "Title",
            options=sorted(attorney_df["title"].dropna().unique()),
            default=sorted(attorney_df["title"].dropna().unique()),
        )

    with c3:
        practice_filter = st.multiselect(
            "Practice Area",
            options=sorted(attorney_df["practice_area"].dropna().unique()),
            default=sorted(attorney_df["practice_area"].dropna().unique()),
        )

    with c4:
        attorney_search = st.text_input(
            "Search Name / Attorney ID",
            placeholder="Type to search...",
        )

    filtered_df = attorney_df.copy()

    filtered_df = filtered_df[
        filtered_df["office"].isin(office_filter)
        & filtered_df["title"].isin(title_filter)
        & filtered_df["practice_area"].isin(practice_filter)
    ]

    if attorney_search:
        search_value = attorney_search.lower()
        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(lambda row: row.str.lower().str.contains(search_value).any(), axis=1)
        ]

    return filtered_df

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.markdown(
    """
    <div class="sidebar-header">
        <div class="sidebar-title">Compliance Monitor</div>
        <div class="sidebar-subtitle">Legal, licensing, CLE, and revenue risk analytics</div>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_pages = [
    "Executive Summary",
    "Attorney Directory",
    "Matters Directory",
    "CLE Compliance",
    "Platform Help",
]

hidden_pages = [
    "Revenue Exposure",
    "License Exceptions",
]

all_pages = sidebar_pages + hidden_pages

if "page" not in st.session_state:
    st.session_state["page"] = "Executive Summary"

sidebar_index = (
    sidebar_pages.index(st.session_state["page"])
    if st.session_state["page"] in sidebar_pages
    else 0
)

if "sidebar_selection" not in st.session_state:
    st.session_state["sidebar_selection"] = sidebar_pages[sidebar_index]


def update_page_from_sidebar():
    st.session_state["page"] = st.session_state["sidebar_selection"]

selected_page = st.sidebar.radio(
    "",
    sidebar_pages,
    index=sidebar_index,
    key="sidebar_selection",
    on_change=update_page_from_sidebar,
)

page = st.session_state["page"]


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="app-title">Attorney License Compliance Monitor</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">Attorney licensing, CLE compliance, matter assignment risk, and revenue exposure analytics.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Executive Summary
# -----------------------------
if page == "Executive Summary":
    section_title("Executive Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_clickable_kpi_card(
            "TOTAL ATTORNEYS",
            f"{summary['total_attorneys']}",
            "Attorney Directory",
            "kpi_total_attorneys",
        )

    with c2:
        render_clickable_kpi_card(
            "EXPIRED LICENSES",
            f"{summary['expired_licenses']}",
            "License Exceptions",
            "kpi_expired_licenses",
        )

    with c3:
        render_clickable_kpi_card(
            "CLE DEFICIENT RECORDS",
            f"{summary['cle_deficient_records']}",
            "CLE Compliance",
            "kpi_cle_deficient",
        )

    with c4:
        render_clickable_kpi_card(
            "TOTAL REVENUE EXPOSURE",
            f"${summary['total_revenue_exposure']:,.0f}",
            "Revenue Exposure",
            "kpi_total_revenue",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        subsection_title("Attorney Compliance Overview")

        risk_tier_counts = (
            risk_scores["risk_tier"]
            .value_counts()
            .reset_index()
        )
        risk_tier_counts.columns = ["Risk Tier", "Attorney Count"]

        st.bar_chart(
            risk_tier_counts,
            x="Risk Tier",
            y="Attorney Count",
        )

    with right:
        subsection_title("License Status Distribution")

        license_status_counts = (
            licenses["license_status"]
            .value_counts()
            .reset_index()
        )
        license_status_counts.columns = ["License Status", "Count"]

        st.bar_chart(
            license_status_counts,
            x="License Status",
            y="Count",
        )


# -----------------------------
# Attorney Directory
# -----------------------------
elif page == "Attorney Directory":
    section_title("Attorney Directory")

    st.write(
        "This view provides the full attorney population used by the compliance monitor. "
        "Use the filters below to review attorneys by office, title, practice area, or keyword."
    )

    filtered_attorneys = render_attorney_filters(attorneys)

    c1, c2, c3 = st.columns(3)

    with c1:
        render_kpi_card("Displayed Attorneys", len(filtered_attorneys))

    with c2:
        render_kpi_card("Total Attorneys", len(attorneys))

    with c3:
        render_kpi_card("Practice Areas", attorneys["practice_area"].nunique())

    subsection_title("Attorney Table")

    st.dataframe(
        filtered_attorneys,
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------
# Matters Directory
# -----------------------------
elif page == "Matters Directory":
    section_title("Matters Directory")

    st.write(
        "This view provides the full matter population, including active matters, closed matters, "
        "and new intake matters."
    )

    matter_view = matters.copy()

    c1, c2, c3 = st.columns(3)

    with c1:
        render_kpi_card("Total Matters", matter_view["matter_id"].nunique())

    with c2:
        render_kpi_card("Jurisdictions", matter_view["jurisdiction"].nunique())

    with c3:
        render_kpi_card("Total Matter Revenue", f"${matter_view['revenue'].sum():,.0f}")

    subsection_title("Matter Filters")

    f1, f2, f3 = st.columns(3)

    with f1:
        jurisdiction_filter = st.multiselect(
            "Jurisdiction",
            options=sorted(matter_view["jurisdiction"].dropna().unique()),
            default=sorted(matter_view["jurisdiction"].dropna().unique()),
        )

    with f2:
        matter_type_filter = st.multiselect(
            "Matter Type",
            options=sorted(matter_view["matter_type"].dropna().unique()),
            default=sorted(matter_view["matter_type"].dropna().unique()),
        )

    with f3:
        matter_search = st.text_input(
            "Search Matter",
            placeholder="Search by matter ID, client, type, or jurisdiction...",
        )

    filtered_matters = matter_view[
        matter_view["jurisdiction"].isin(jurisdiction_filter)
        & matter_view["matter_type"].isin(matter_type_filter)
    ]

    if matter_search:
        search_value = matter_search.lower()
        filtered_matters = filtered_matters[
            filtered_matters.astype(str)
            .apply(lambda row: row.str.lower().str.contains(search_value).any(), axis=1)
        ]

    subsection_title("Matter Table")

    st.dataframe(
        filtered_matters,
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Attorney Risk
# -----------------------------
elif page == "Attorney Risk":
    section_title("Attorney Risk Scores")

    risk_filter = st.multiselect(
        "Filter by risk tier",
        options=sorted(risk_scores["risk_tier"].unique()),
        default=sorted(risk_scores["risk_tier"].unique()),
    )

    filtered_risk_scores = risk_scores[
        risk_scores["risk_tier"].isin(risk_filter)
    ]

    subsection_title("Attorney Risk Detail")
    st.dataframe(
        filtered_risk_scores,
        use_container_width=True,
        hide_index=True,
    )

    subsection_title("Top Risk Attorneys")
    top_risk = (
        filtered_risk_scores
        .sort_values("total_risk_score", ascending=False)
        .head(5)
    )

    st.dataframe(
        top_risk[
            [
                "attorney_id",
                "name",
                "title",
                "office",
                "practice_area",
                "revenue_exposure",
                "total_risk_score",
                "risk_tier",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Matter License Risks
# -----------------------------
elif page == "Matter License Risks":
    section_title("Matter License Risks")

    st.write(
        "This view identifies attorneys assigned to matters where they do not have an active "
        "license in the matter jurisdiction, or where the relevant license is expired or suspended."
    )

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        render_kpi_card("Risk Count", len(matter_license_risks))
    with c2:
        render_kpi_card("Assigned Matters", len(assignments))
    with c3:
        render_kpi_card("Control Focus", "Jurisdiction Matching")

    subsection_title("Flagged Matter Assignments")
    st.dataframe(
        matter_license_risks,
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Platform Help
# -----------------------------
elif page == "Platform Help":
    section_title("Platform Help")

    st.write(
        "This section can be used for platform guidance, data definitions, user notes, "
        "and compliance-monitoring methodology."
    )

    subsection_title("How to Use This Dashboard")

    st.markdown(
        """
        **Executive Summary** provides a high-level overview of attorney licensing, CLE status, and revenue exposure.

        **Attorney Directory** provides the full attorney population with filters.

        **Matters Directory** provides the full matter population, including active, closed, and intake matters.

        **CLE Compliance** provides CLE completion status and deficiency review.

        KPI cards on the Executive Summary page act as drill-down shortcuts into the relevant detail pages.
        """
    )

    subsection_title("Suggested Future Admin Features")

    st.markdown(
        """
        - User login and role-based access
        - Data upload controls
        - Audit log
        - Export permissions
        - Compliance methodology notes
        - Data refresh timestamp
        """
    )


# -----------------------------
# License Exceptions
# -----------------------------
elif page == "License Exceptions":
    section_title("License Exceptions")

    st.write(
        "This view summarizes attorneys with expired, suspended, or otherwise non-active licenses. "
        "Use these findings to investigate license remediation and matter coverage gaps."
    )

    exception_view = licenses[licenses["license_status"] != "Active"].merge(
        attorneys[["attorney_id", "name", "title", "office", "practice_group"]],
        on="attorney_id",
        how="left",
    )

    exception_view["issue_detail"] = exception_view.apply(
        lambda row: (
            "Suspended license" if row["license_status"] == "Suspended"
            else "Expired registration" if row["license_status"] == "Expired"
            else "Review required"
        ),
        axis=1,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_kpi_card("Expired / Suspended Licenses", len(exception_view))
    with c2:
        render_kpi_card("Affected Attorneys", exception_view["attorney_id"].nunique())
    with c3:
        render_kpi_card("Jurisdictions", exception_view["jurisdiction"].nunique())

    subsection_title("License Exception Detail")
    st.dataframe(
        exception_view[
            [
                "attorney_id",
                "name",
                "title",
                "office",
                "practice_group",
                "jurisdiction",
                "license_status",
                "registration_expiry",
                "issue_detail",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# CLE Compliance
# -----------------------------
elif page == "CLE Compliance":
    section_title("CLE Compliance")

    cle_view = cle_records.copy()
    cle_view["cle_status"] = cle_view.apply(
        lambda row: "Compliant"
        if row["completed_hours"] >= row["required_hours"]
        else "Deficient",
        axis=1,
    )
    cle_view["hours_short"] = (
        cle_view["required_hours"] - cle_view["completed_hours"]
    ).clip(lower=0)

    cle_enriched = cle_view.merge(
        attorneys[["attorney_id", "name", "title", "office", "practice_area"]],
        on="attorney_id",
        how="left",
    )

    compliant_count = len(cle_enriched[cle_enriched["cle_status"] == "Compliant"])
    deficient_count = len(cle_enriched[cle_enriched["cle_status"] == "Deficient"])

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("CLE Compliant", compliant_count)
    with c2:
        render_kpi_card("CLE Deficient", deficient_count)
    with c3:
        render_kpi_card("Total CLE Records", len(cle_enriched))

    subsection_title("CLE Status Distribution")
    cle_status_counts = cle_enriched["cle_status"].value_counts().reset_index()
    cle_status_counts.columns = ["CLE Status", "Count"]

    st.bar_chart(cle_status_counts, x="CLE Status", y="Count")

    subsection_title("CLE Detail")
    st.dataframe(
        cle_enriched[
            [
                "attorney_id",
                "name",
                "title",
                "office",
                "practice_area",
                "jurisdiction",
                "required_hours",
                "completed_hours",
                "hours_short",
                "deadline",
                "cle_status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Revenue Exposure
# -----------------------------
elif page == "Revenue Exposure":
    section_title("Revenue Exposure")

    total_revenue = matters["revenue"].sum()
    matter_count = matters["matter_id"].nunique()
    jurisdiction_count = matters["jurisdiction"].nunique()

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("Total Revenue", f"${total_revenue:,.0f}")
    with c2:
        render_kpi_card("Matter Count", f"{matter_count}")
    with c3:
        render_kpi_card("Jurisdictions", f"{jurisdiction_count}")

    subsection_title("Revenue by Matter Type")
    revenue_by_type = (
        matters.groupby("matter_type", as_index=False)
        .agg(
            matter_count=("matter_id", "count"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    st.bar_chart(
        revenue_by_type,
        x="matter_type",
        y="total_revenue",
    )

    st.dataframe(
        revenue_by_type,
        use_container_width=True,
        hide_index=True,
    )

    subsection_title("Revenue by Jurisdiction")
    revenue_by_jurisdiction = (
        matters.groupby("jurisdiction", as_index=False)
        .agg(
            matter_count=("matter_id", "count"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    st.bar_chart(
        revenue_by_jurisdiction,
        x="jurisdiction",
        y="total_revenue",
    )

    st.dataframe(
        revenue_by_jurisdiction,
        use_container_width=True,
        hide_index=True,
    )

    subsection_title("Matter Detail")
    st.dataframe(
        matters,
        use_container_width=True,
        hide_index=True,
    )