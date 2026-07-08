import streamlit as st
from datetime import date

from src.db.repositories import (
    create_attorney,
    create_license,
    create_cle_record,
    create_matter,
    create_matter_assignment,
)


def render_admin_data_entry_page(refresh_callback):
    """
    Render admin-only PostgreSQL data entry forms.

    refresh_callback should clear Streamlit caches and reload dashboard data
    after successful inserts.
    """
    section_title("Admin Data Entry")
    st.caption("Add new compliance records directly into PostgreSQL.")

    if st.session_state.get("role") != "admin":
        st.error("Admin access is required for this page.")
        return

    with st.expander("Add Attorney", expanded=True):
        with st.form("add_attorney_form"):
            name = st.text_input("Name", placeholder="Alex Chen")
            email = st.text_input("Email", placeholder="alex@example.com")

            date_of_birth = st.date_input(
                "Date of Birth",
                value=date(1990, 1, 1),
                min_value=date(1940, 1, 1),
                max_value=date.today(),
            )

            title = st.text_input("Title", placeholder="Paralegal")
            office = st.text_input("Office", placeholder="New York")
            practice_area = st.text_input("Practice Area", placeholder="Corporate")

            employment_status = st.selectbox(
                "Employment Status",
                ["Active", "Inactive", "Terminated"],
            )

            submitted = st.form_submit_button("Save Attorney")

            if submitted:
                if not name or not email:
                    st.error("Name and email are required.")
                else:
                    attorney_data = {
                        "name": name.strip(),
                        "email": email.strip(),
                        "date_of_birth": date_of_birth,
                        "title": title.strip(),
                        "office": office.strip(),
                        "practice_area": practice_area.strip(),
                        "employment_status": employment_status,
                    }

                    try:
                        create_attorney(attorney_data)
                        refresh_callback()
                        st.success("Attorney added successfully.")
                    except Exception as e:
                        st.error(f"Could not add attorney: {e}")

    with st.expander("Add License"):
        with st.form("add_license_form"):
                attorney_id = st.number_input(
                    "Attorney ID",
                    min_value=1,
                    step=1,
                    value=100,
                    key="license_attorney_id",
                )
                jurisdiction = st.text_input("Jurisdiction", placeholder="NY")
                admission_date = st.date_input("Admission Date")
                admission_year = st.number_input(
                    "Admission Year",
                    min_value=1900,
                    max_value=2100,
                    value=2024,
                    step=1,
                )
                license_status = st.selectbox(
                    "License Status",
                    ["Active", "Expired", "Suspended", "Inactive"],
                )
                registration_expiry = st.date_input("Registration Expiry")

                submitted = st.form_submit_button("Save License")

                if submitted:
                    if not attorney_id or not jurisdiction or not license_status:
                        st.error("Attorney ID, jurisdiction, and license status are required.")
                    else:
                        license_data = {
                            "attorney_id": int(attorney_id),
                            "jurisdiction": jurisdiction.strip(),
                            "admission_date": admission_date,
                            "admission_year": int(admission_year),
                            "license_status": license_status,
                            "registration_expiry": registration_expiry,
                        }

                        try:
                            create_license(license_data)
                            refresh_callback()
                            st.success("License added successfully.")
                        except Exception as e:
                            st.error(f"Could not add license: {e}")

    with st.expander("Add CLE Record"):
            with st.form("add_cle_record_form"):
                attorney_id = st.number_input(
                    "Attorney ID",
                    key="cle_attorney_id",
                    placeholder="A009",
                )
                jurisdiction = st.text_input(
                    "Jurisdiction",
                    key="cle_jurisdiction",
                    placeholder="NY",
                )
                required_hours = st.number_input(
                    "Required Hours",
                    min_value=0.0,
                    value=24.0,
                    step=0.5,
                )
                completed_hours = st.number_input(
                    "Completed Hours",
                    min_value=0.0,
                    value=0.0,
                    step=0.5,
                )
                deadline = st.date_input("CLE Deadline")

                submitted = st.form_submit_button("Save CLE Record")

                if submitted:
                    if not attorney_id or not jurisdiction:
                        st.error("Attorney ID and jurisdiction are required.")
                    else:
                        cle_data = {
                            "attorney_id": int(attorney_id),
                            "jurisdiction": jurisdiction.strip(),
                            "required_hours": float(required_hours),
                            "completed_hours": float(completed_hours),
                            "deadline": deadline,
                        }

                        try:
                            create_cle_record(cle_data)
                            refresh_callback()
                            st.success("CLE record added successfully.")
                        except Exception as e:
                            st.error(f"Could not add CLE record: {e}")

    with st.expander("Add Matter"):
            with st.form("add_matter_form"):
                matter_id = st.text_input("Matter ID", placeholder="M009")
                matter_name = st.text_input("Matter Name", placeholder="Sample Matter")
                jurisdiction = st.text_input(
                    "Jurisdiction",
                    key="matter_jurisdiction",
                    placeholder="NY",
                )
                client = st.text_input("Client", placeholder="Sample Client")
                revenue = st.number_input(
                    "Revenue",
                    min_value=0.0,
                    value=0.0,
                    step=1000.0,
                )
                matter_type = st.text_input("Matter Type", placeholder="Corporate")
                status = st.selectbox(
                    "Matter Status",
                    ["Open", "Pending", "Closed"],
                )

                submitted = st.form_submit_button("Save Matter")

                if submitted:
                    if not matter_id or not matter_name or not jurisdiction or not client:
                        st.error("Matter ID, matter name, jurisdiction, and client are required.")
                    else:
                        matter_data = {
                            "matter_id": matter_id.strip(),
                            "matter_name": matter_name.strip(),
                            "jurisdiction": jurisdiction.strip(),
                            "client": client.strip(),
                            "revenue": float(revenue),
                            "matter_type": matter_type.strip(),
                            "status": status,
                        }

                        try:
                            create_matter(matter_data)
                            refresh_callback()
                            st.success("Matter added successfully.")
                        except Exception as e:
                            st.error(f"Could not add matter: {e}")

    with st.expander("Add Matter Assignment"):
            with st.form("add_matter_assignment_form"):
                matter_id = st.text_input(
                    "Matter ID",
                    key="assignment_matter_id",
                    placeholder="M009",
                )
                attorney_id = st.number_input(
                    "Attorney ID",
                    key="assignment_attorney_id",
                    placeholder="A009",
                )
                role = st.selectbox(
                    "Assignment Role",
                    ["Lead Attorney", "Supporting Attorney", "Reviewer"],
                )
                assignment_date = st.date_input("Assignment Date")

                submitted = st.form_submit_button("Save Matter Assignment")

                if submitted:
                    if not matter_id or not attorney_id or not role:
                        st.error("Matter ID, attorney ID, and role are required.")
                    else:
                        assignment_data = {
                            "matter_id": matter_id.strip(),
                            "attorney_id": int(attorney_id),
                            "role": role,
                            "assignment_date": assignment_date,
                        }

                        try:
                            create_matter_assignment(assignment_data)
                            refresh_callback()
                            st.success("Matter assignment added successfully.")
                        except Exception as e:
                            st.error(f"Could not add matter assignment: {e}")


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)