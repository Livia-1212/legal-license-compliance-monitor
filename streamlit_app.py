import streamlit as st
import pandas as pd
import os

from src.dashboard.dashboard_summary import generate_dashboard_summary
from src.analysis.risk_scoring import calculate_attorney_risk_scores
from src.analysis.matter_license_check import find_matter_license_risks
from src.analysis.load_data import load_all_data
from src.persistence import EXPECTED_COLUMNS, save_uploaded_csv, BACKUP_DIR
from src.auth import init_user_store, authenticate, create_user, list_users
import streamlit.components.v1 as components


from src.ui.styles import load_css


st.set_page_config(
    page_title="Attorney License Compliance Monitor",
    page_icon="⚖️",
    layout="wide",
)

load_css()

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
    st.markdown('<div class="kpi-button-wrapper">', unsafe_allow_html=True)

    if st.button(
        f"{label}\n\n{value}",
        key=key,
        use_container_width=True,
    ):
        go_to_page(target_page)

    st.markdown("</div>", unsafe_allow_html=True)


def render_attorney_filters(attorney_df):
    st.markdown("#### Filter Attorneys")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        office_filter = st.multiselect(
            "Office",
            options=sorted(attorney_df["office"].dropna().unique()),
            default=[],
        )

    with c2:
        title_filter = st.multiselect(
            "Title",
            options=sorted(attorney_df["title"].dropna().unique()),
            default=[],
        )

    with c3:
        practice_filter = st.multiselect(
            "Practice Area",
            options=sorted(attorney_df["practice_area"].dropna().unique()),
            default=[],
        )

    with c4:
        attorney_search = st.text_input(
            "Search Name / Attorney ID",
            placeholder="Type to search...",
        )

    filtered_df = attorney_df.copy()

    if office_filter:
        filtered_df = filtered_df[filtered_df["office"].isin(office_filter)]

    if title_filter:
        filtered_df = filtered_df[filtered_df["title"].isin(title_filter)]

    if practice_filter:
        filtered_df = filtered_df[filtered_df["practice_area"].isin(practice_filter)]

    if attorney_search:
        search_value = attorney_search.lower()
        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(lambda row: row.str.lower().str.contains(search_value).any(), axis=1)
        ]

    return filtered_df


def render_auth_ui():
    """Render the sign-in / register and data management UI."""
    # User authentication + upload / download
    init_user_store()

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None

    def _sign_out():
        st.session_state["current_user"] = None

    if st.session_state["current_user"] is None:
        # Use side-by-side columns so both forms are visible
        col_sign, col_reg = st.columns(2)

        with col_sign:
            subsection_title("Sign In")
            u_name = st.text_input("Username", key="signin_user")
            u_pw = st.text_input("Password", type="password", key="signin_pw")
            st.markdown('<div class="auth-buttons">', unsafe_allow_html=True)
            if st.button("Sign In", key="sign_in_btn"):
                user = authenticate(u_name, u_pw)
                if user:
                    st.session_state["current_user"] = user
                    st.success(f"Signed in as {user['username']} ({user['role']})")
                else:
                    st.error("Invalid credentials")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_reg:
            subsection_title("Register")
            new_user = st.text_input("New username", key="reg_user")
            new_pw = st.text_input("New password", type="password", key="reg_pw")
            new_pw_confirm = st.text_input("Confirm password", type="password", key="reg_pw2")
            st.markdown('<div class="auth-buttons">', unsafe_allow_html=True)
            if st.button("Register", key="register_btn"):
                if not new_user or not new_pw:
                    st.error("Provide username and password")
                elif new_pw != new_pw_confirm:
                    st.error("Passwords do not match")
                else:
                    success, msg = create_user(new_user, new_pw, role="user")
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)

        

    else:
        user = st.session_state["current_user"]
        st.success(f"Signed in as {user['username']} ({user['role']})")
        if st.button("Sign out"):
            _sign_out()

        # Upload / Download available to signed-in users (both user and admin roles)
        subsection_title("Upload CSV Data")
        st.write("Upload a dataset CSV to replace or append to the existing data file.")

        dataset = st.selectbox("Dataset to upload", options=list(EXPECTED_COLUMNS.keys()))
        upload_file = st.file_uploader("Choose CSV file", type=["csv"]) 
        upload_mode = st.radio("Upload mode", options=["replace", "append"], index=0)

        if upload_file is not None:
            try:
                preview_cols = pd.read_csv(upload_file, nrows=0).columns.tolist()
            except Exception:
                preview_cols = []
            st.markdown(f"**Detected columns:** {', '.join(preview_cols) if preview_cols else 'Could not read columns.'}")

            if st.button("Process upload"):
                upload_file.seek(0)
                uploader_name = user.get("username")
                success, message = save_uploaded_csv(upload_file, dataset, mode=upload_mode, uploader=uploader_name)
                if success:
                    try:
                        get_data.clear()
                    except Exception:
                        pass

                    data = get_data()
                    # refresh globals
                    globals()["attorneys"] = data["attorneys"]
                    globals()["licenses"] = data["licenses"]
                    globals()["cle_records"] = data["cle_records"]
                    globals()["matters"] = data["matters"]
                    globals()["assignments"] = data["matter_assignments"]

                    st.success(f"Upload successful: {message}")
                else:
                    st.error(f"Upload failed: {message}")

        subsection_title("Download CSV Exports")
        st.write("Download current datasets as CSV files.")

        datasets = {
            "attorneys": attorneys,
            "licenses": licenses,
            "cle_records": cle_records,
            "matters": matters,
            "matter_assignments": assignments,
        }

        for name, df in datasets.items():
            try:
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"Download {name}.csv",
                    data=csv_bytes,
                    file_name=f"{name}.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.warning(f"Unable to prepare download for {name}: {e}")

        # Admin-only extra tools
        if user.get("role") == "admin":
            subsection_title("Admin: Audit Log")
            try:
                if (BACKUP_DIR / "upload_audit.csv").exists():
                    audit_df = pd.read_csv(BACKUP_DIR / "upload_audit.csv")
                    st.dataframe(audit_df, use_container_width=True)
                    st.download_button(
                        label="Download Audit Log",
                        data=audit_df.to_csv(index=False).encode("utf-8"),
                        file_name="upload_audit.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No audit log found yet.")
            except Exception as e:
                st.warning(f"Unable to load audit log: {e}")

            subsection_title("Admin: User List")
            try:
                users = list_users()
                st.dataframe(pd.DataFrame(users), use_container_width=True)
            except Exception as e:
                st.warning(f"Unable to list users: {e}")


def render_data_management_ui():
    """Render upload/download and admin tools for signed-in users."""
    user = st.session_state.get("current_user")
    if not user:
        st.info("Please sign in using the 'Sign In' button in the sidebar.")
        return

    st.success(f"Signed in as {user['username']} ({user['role']})")
    if st.button("Sign out", key="dm_signout"):
        st.session_state["current_user"] = None

    subsection_title("Upload CSV Data")
    st.write("Upload a dataset CSV to replace or append to the existing data file.")

    dataset = st.selectbox("Dataset to upload", options=list(EXPECTED_COLUMNS.keys()), key="dm_dataset")
    upload_file = st.file_uploader("Choose CSV file", type=["csv"], key="dm_uploader")
    upload_mode = st.radio("Upload mode", options=["replace", "append"], index=0, key="dm_mode")

    if upload_file is not None:
        try:
            preview_cols = pd.read_csv(upload_file, nrows=0).columns.tolist()
        except Exception:
            preview_cols = []
        st.markdown(f"**Detected columns:** {', '.join(preview_cols) if preview_cols else 'Could not read columns.'}")

        if st.button("Process upload", key="dm_process_upload"):
            upload_file.seek(0)
            uploader_name = user.get("username")
            success, message = save_uploaded_csv(upload_file, dataset, mode=upload_mode, uploader=uploader_name)
            if success:
                try:
                    get_data.clear()
                except Exception:
                    pass

                data = get_data()
                globals()["attorneys"] = data["attorneys"]
                globals()["licenses"] = data["licenses"]
                globals()["cle_records"] = data["cle_records"]
                globals()["matters"] = data["matters"]
                globals()["assignments"] = data["matter_assignments"]

                st.success(f"Upload successful: {message}")
            else:
                st.error(f"Upload failed: {message}")

    subsection_title("Download CSV Exports")
    st.write("Download current datasets as CSV files.")

    datasets = {
        "attorneys": attorneys,
        "licenses": licenses,
        "cle_records": cle_records,
        "matters": matters,
        "matter_assignments": assignments,
    }

    for name, df in datasets.items():
        try:
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {name}.csv",
                data=csv_bytes,
                file_name=f"{name}.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.warning(f"Unable to prepare download for {name}: {e}")

    if user.get("role") == "admin":
        subsection_title("Admin: Audit Log")
        try:
            if (BACKUP_DIR / "upload_audit.csv").exists():
                audit_df = pd.read_csv(BACKUP_DIR / "upload_audit.csv")
                st.dataframe(audit_df, use_container_width=True)
                st.download_button(
                    label="Download Audit Log",
                    data=audit_df.to_csv(index=False).encode("utf-8"),
                    file_name="upload_audit.csv",
                    mime="text/csv",
                )
            else:
                st.info("No audit log found yet.")
        except Exception as e:
            st.warning(f"Unable to load audit log: {e}")

        subsection_title("Admin: User List")
        try:
            users = list_users()
            st.dataframe(pd.DataFrame(users), use_container_width=True)
        except Exception as e:
            st.warning(f"Unable to list users: {e}")

# -----------------------------
# Sidebar Navigation
# -----------------------------
# Sign-in shortcut above the header
if st.sidebar.button("Sign In", key="sidebar_signin_btn"):
    go_to_page("AuthChoice")

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
    "Tableau Dashboard",
    "CLE Compliance",
    "Platform Help",
]

hidden_pages = [
    "Revenue Exposure",
    "License Exceptions",
    "AuthChoice",
    "AuthSignIn",
    "AuthRegister",
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
            default=[],
        )

    with f2:
        matter_type_filter = st.multiselect(
            "Matter Type",
            options=sorted(matter_view["matter_type"].dropna().unique()),
            default=[],
        )

    with f3:
        matter_search = st.text_input(
            "Search Matter",
            placeholder="Search by matter ID, client, type, or jurisdiction...",
        )

    filtered_matters = matter_view.copy()
    if jurisdiction_filter:
        filtered_matters = filtered_matters[filtered_matters["jurisdiction"].isin(jurisdiction_filter)]
    if matter_type_filter:
        filtered_matters = filtered_matters[filtered_matters["matter_type"].isin(matter_type_filter)]

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
# Tableau Dashboard
# -----------------------------
elif page == "Tableau Dashboard":
    section_title("Tableau Dashboard")

    st.write("Embedded Tableau dashboard (configure TABLEAU_DASHBOARD_URL env var to embed).")

    tableau_url = os.environ.get("TABLEAU_DASHBOARD_URL", "") if 'os' in globals() else os.environ.get("TABLEAU_DASHBOARD_URL", "")
    if tableau_url:
        try:
            components.iframe(tableau_url, height=800)
        except Exception as e:
            st.warning(f"Unable to embed Tableau dashboard: {e}")
            st.markdown(f"[Open Tableau Dashboard]({tableau_url})")
    else:
        st.info("No Tableau dashboard URL configured. Set TABLEAU_DASHBOARD_URL environment variable.")
        st.markdown("To embed a Tableau dashboard, set `TABLEAU_DASHBOARD_URL` environment variable to the share URL.")


# -----------------------------
# Auth flow pages (hidden)
# -----------------------------
elif page == "AuthChoice":
    section_title("Sign In")
    st.write("Choose an option to continue.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Sign In"):
            go_to_page("AuthSignIn")
    with c2:
        if st.button("Register"):
            go_to_page("AuthRegister")

elif page == "AuthSignIn":
    section_title("Sign In")
    u_name = st.text_input("Username", key="signin_page_user")
    u_pw = st.text_input("Password", type="password", key="signin_page_pw")
    if st.button("Sign In", key="signin_page_btn"):
        user = authenticate(u_name, u_pw)
        if user:
            st.session_state["current_user"] = user
            st.success(f"Signed in as {user['username']} ({user['role']})")
            go_to_page("Platform Help")
        else:
            st.error("Invalid credentials")

elif page == "AuthRegister":
    section_title("Register")
    new_user = st.text_input("New username", key="reg_page_user")
    new_pw = st.text_input("New password", type="password", key="reg_page_pw")
    new_pw_confirm = st.text_input("Confirm password", type="password", key="reg_page_pw2")
    if st.button("Register", key="reg_page_btn"):
        if not new_user or not new_pw:
            st.error("Provide username and password")
        elif new_pw != new_pw_confirm:
            st.error("Passwords do not match")
        else:
            success, msg = create_user(new_user, new_pw, role="user")
            if success:
                st.success(msg)
                go_to_page("AuthSignIn")
            else:
                st.error(msg)


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

    subsection_title("Authentication")
    st.write("Use the Sign In button at the top-left of the sidebar to sign in. After signing in you'll be redirected here to access data management tools.")
    render_data_management_ui()

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
        attorneys[["attorney_id", "name", "title", "office", "practice_area"]],
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
                "practice_area",
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