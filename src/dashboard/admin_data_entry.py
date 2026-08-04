import streamlit as st
from datetime import date

from src.db.repositories import (
    create_attorney,
    create_license,
    create_cle_record,
    create_matter,
    create_matter_assignment,
    search_attorneys,
    update_attorney,
    get_eligible_cle_attorneys,
    get_unassigned_open_matters,
    get_eligible_attorneys_for_matter,
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


    with st.expander("Edit Attorney"):
        search_term = st.text_input(
            "Search Attorney",
            placeholder=(
                "Enter name, email, attorney ID, office, "
                "or practice area"
            ),
            key="edit_attorney_search",
        )

        cleaned_search_term = search_term.strip()

        if len(cleaned_search_term) < 2:
            st.info("Enter at least two characters to search.")
        else:
            try:
                attorneys = search_attorneys(cleaned_search_term)
            except Exception as e:
                attorneys = []
                st.error(f"Could not search attorneys: {e}")

            if not attorneys:
                st.warning("No matching attorney records were found.")
            else:
                attorney_options = {
                    (
                        f"{attorney['name']} — "
                        f"ID {attorney['attorney_id']} — "
                        f"{attorney['email']} — "
                        f"{attorney['office'] or 'No office'}"
                    ): attorney
                    for attorney in attorneys
                }

                selected_label = st.selectbox(
                    "Matching Attorneys",
                    options=list(attorney_options.keys()),
                    key="edit_attorney_result",
                )

                selected_attorney = attorney_options[selected_label]
                selected_attorney_id = int(
                    selected_attorney["attorney_id"]
                )

                previous_attorney_id = st.session_state.get(
                    "loaded_edit_attorney_id"
                )

                if previous_attorney_id != selected_attorney_id:
                    st.session_state["edit_attorney_name"] = (
                        selected_attorney["name"] or ""
                    )
                    st.session_state["edit_attorney_email"] = (
                        selected_attorney["email"] or ""
                    )
                    st.session_state["edit_attorney_date_of_birth"] = (
                        selected_attorney["date_of_birth"]
                    )
                    st.session_state["edit_attorney_title"] = (
                        selected_attorney["title"] or ""
                    )
                    st.session_state["edit_attorney_office"] = (
                        selected_attorney["office"] or ""
                    )
                    st.session_state["edit_attorney_practice_area"] = (
                        selected_attorney["practice_area"] or ""
                    )
                    st.session_state[
                        "edit_attorney_employment_status"
                    ] = (
                        selected_attorney["employment_status"]
                        or "Active"
                    )
                    st.session_state["loaded_edit_attorney_id"] = (
                        selected_attorney_id
                    )

                with st.form("edit_attorney_form"):
                    st.text_input(
                        "Attorney ID",
                        value=str(selected_attorney_id),
                        disabled=True,
                    )

                    edit_name = st.text_input(
                        "Name",
                        key="edit_attorney_name",
                    )

                    edit_email = st.text_input(
                        "Email",
                        key="edit_attorney_email",
                    )

                    edit_date_of_birth = st.date_input(
                        "Date of Birth",
                        min_value=date(1940, 1, 1),
                        max_value=date.today(),
                        key="edit_attorney_date_of_birth",
                    )

                    edit_title = st.text_input(
                        "Title",
                        key="edit_attorney_title",
                    )

                    edit_office = st.text_input(
                        "Office",
                        key="edit_attorney_office",
                    )

                    edit_practice_area = st.text_input(
                        "Practice Area",
                        key="edit_attorney_practice_area",
                    )

                    status_options = [
                        "Active",
                        "Inactive",
                        "Terminated",
                    ]

                    current_status = st.session_state.get(
                        "edit_attorney_employment_status",
                        "Active",
                    )

                    if current_status not in status_options:
                        current_status = "Active"

                    edit_employment_status = st.selectbox(
                        "Employment Status",
                        options=status_options,
                        index=status_options.index(current_status),
                        key="edit_attorney_employment_status_select",
                    )

                    submitted = st.form_submit_button(
                        "Update Attorney"
                    )

                    if submitted:
                        if not edit_name.strip() or not edit_email.strip():
                            st.error(
                                "Name and email are required."
                            )
                        else:
                            attorney_data = {
                                "name": edit_name.strip(),
                                "email": edit_email.strip(),
                                "date_of_birth": edit_date_of_birth,
                                "title": edit_title.strip(),
                                "office": edit_office.strip(),
                                "practice_area": (
                                    edit_practice_area.strip()
                                ),
                                "employment_status": (
                                    edit_employment_status
                                ),
                            }

                            try:
                                updated = update_attorney(
                                    selected_attorney_id,
                                    attorney_data,
                                )

                                if updated:
                                    refresh_callback()

                                    st.session_state[
                                        "edit_attorney_employment_status"
                                    ] = edit_employment_status

                                    st.success(
                                        "Attorney updated successfully."
                                    )
                                else:
                                    st.error(
                                        "Attorney could not be updated "
                                        "because the record no longer exists."
                                    )

                            except Exception as e:
                                st.error(
                                    f"Could not update attorney: {e}"
                                )

    with st.expander("Add License"):
        with st.form("add_license_form"):
                attorney_id = st.number_input(
                    "Attorney ID",
                    min_value=1,
                    value=1,
                    step=1,
                    format="%d",
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
        try:
            eligible_attorneys = get_eligible_cle_attorneys()
        except Exception as e:
            eligible_attorneys = []
            st.error(f"Could not load eligible attorneys: {e}")

        if not eligible_attorneys:
            st.warning(
                "No eligible attorneys are available. An attorney must have "
                "active employment status, an active unexpired license, and "
                "a configured jurisdiction CLE rule."
            )
        else:
            attorney_options = {
                (
                    f"{attorney['name']} — "
                    f"Attorney ID {attorney['attorney_id']} — "
                    f"{attorney['jurisdiction']}"
                ): attorney
                for attorney in eligible_attorneys
            }

            selected_label = st.selectbox(
                "Attorney Name",
                options=list(attorney_options.keys()),
                key="cle_attorney_selection",
            )

            selected_attorney = attorney_options[selected_label]

            attorney_id = int(selected_attorney["attorney_id"])
            attorney_name = selected_attorney["name"]
            email = selected_attorney["email"]
            office = selected_attorney["office"]
            practice_area = selected_attorney["practice_area"]
            jurisdiction = selected_attorney["jurisdiction"]
            admission_date = selected_attorney["admission_date"]
            license_status = selected_attorney["license_status"]
            registration_expiry = selected_attorney["registration_expiry"]
            required_hours = float(selected_attorney["cle_required_hours"])
            registration_cycle = selected_attorney["registration_cycle"]

            calculated_deadline = calculate_next_cle_deadline(
                admission_date,
                registration_cycle,
            )

            st.markdown("#### Attorney and License Details")

            detail_col_1, detail_col_2 = st.columns(2)

            with detail_col_1:
                st.text_input(
                    "Attorney ID",
                    value=str(attorney_id),
                    disabled=True,
                    key="cle_display_attorney_id",
                )

                st.text_input(
                    "Attorney Name",
                    value=attorney_name,
                    disabled=True,
                    key="cle_display_attorney_name",
                )

                st.text_input(
                    "Email",
                    value=email or "",
                    disabled=True,
                    key="cle_display_email",
                )

                st.text_input(
                    "Office",
                    value=office or "",
                    disabled=True,
                    key="cle_display_office",
                )

            with detail_col_2:
                st.text_input(
                    "Practice Area",
                    value=practice_area or "",
                    disabled=True,
                    key="cle_display_practice_area",
                )

                st.text_input(
                    "Jurisdiction",
                    value=jurisdiction,
                    disabled=True,
                    key="cle_display_jurisdiction",
                )

                st.text_input(
                    "License Status",
                    value=license_status,
                    disabled=True,
                    key="cle_display_license_status",
                )

                st.text_input(
                    "License Registration Expiry",
                    value=str(registration_expiry),
                    disabled=True,
                    key="cle_display_registration_expiry",
                )

            st.markdown("#### CLE Calculation")

            completed_hours = st.number_input(
                "Completed Hours",
                min_value=0.0,
                value=0.0,
                step=0.5,
                key="cle_completed_hours",
            )

            remaining_hours = max(
                required_hours - float(completed_hours),
                0.0,
            )

            calculation_col_1, calculation_col_2, calculation_col_3 = st.columns(3)

            with calculation_col_1:
                st.metric(
                    "Required Hours",
                    f"{required_hours:.1f}",
                )

            with calculation_col_2:
                st.metric(
                    "Remaining Hours",
                    f"{remaining_hours:.1f}",
                )

            with calculation_col_3:
                st.metric(
                    "Registration Cycle",
                    registration_cycle,
                )

            if calculated_deadline:
                st.text_input(
                    "Calculated CLE Deadline",
                    value=str(calculated_deadline),
                    disabled=True,
                    key="cle_display_deadline",
                )
            else:
                st.error(
                    "The CLE deadline could not be calculated because the "
                    "jurisdiction registration cycle is not supported."
                )

            st.markdown("#### Review Before Saving")

            st.info(
                f"""
                **Attorney:** {attorney_name}  
                **Attorney ID:** {attorney_id}  
                **Jurisdiction:** {jurisdiction}  
                **Required Hours:** {required_hours:.1f}  
                **Completed Hours:** {float(completed_hours):.1f}  
                **Remaining Hours:** {remaining_hours:.1f}  
                **CLE Deadline:** {calculated_deadline or "Unavailable"}
                """
            )

            save_cle_record = st.button(
                "Save CLE Record",
                key="save_cle_record_button",
                disabled=calculated_deadline is None,
            )

            if save_cle_record:
                cle_data = {
                    "attorney_id": attorney_id,
                    "jurisdiction": jurisdiction,
                    "required_hours": required_hours,
                    "completed_hours": float(completed_hours),
                    "deadline": calculated_deadline,
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
        st.markdown("#### Unassigned Matters")

        try:
            unassigned_matters = get_unassigned_open_matters()
        except Exception as e:
            unassigned_matters = []
            st.error(f"Could not load unassigned matters: {e}")

        if not unassigned_matters:
            st.info(
                "There are currently no open, unassigned matters available."
            )
        else:
            matter_options = {
                (
                    f"{matter['matter_id']} — "
                    f"{matter['matter_name']} — "
                    f"{matter['jurisdiction']}"
                ): matter
                for matter in unassigned_matters
            }

            selected_matter_label = st.selectbox(
                "Matter ID",
                options=list(matter_options.keys()),
                key="assignment_matter_selection",
            )

            selected_matter = matter_options[selected_matter_label]

            matter_id = selected_matter["matter_id"]
            matter_name = selected_matter["matter_name"]
            jurisdiction = selected_matter["jurisdiction"]
            client = selected_matter["client"]
            matter_status = selected_matter["status"]

            
            st.markdown("#### Matter Details")

            matter_col_1, matter_col_2 = st.columns(2)

            with matter_col_1:
                st.markdown("**Selected Matter ID**")
                st.write(str(matter_id))

                st.markdown("**Matter Name**")
                st.write(matter_name)

            with matter_col_2:
                st.markdown("**Jurisdiction**")
                st.write(jurisdiction)

                st.markdown("**Client**")
                st.write(client)

            st.markdown("**Matter Status**")
            st.write(matter_status)
            
            try:
                eligible_attorneys = get_eligible_attorneys_for_matter(
                    jurisdiction
                )
            except Exception as e:
                eligible_attorneys = []
                st.error(
                    f"Could not load eligible attorneys: {e}"
                )

            if not eligible_attorneys:
                st.warning(
                    f"No eligible attorneys have an active, unexpired "
                    f"{jurisdiction} license."
                )
            else:
                st.markdown("#### Select Assigned Attorney")

                attorney_options = {
                    (
                        f"{attorney['name']} — "
                        f"Attorney ID {attorney['attorney_id']} — "
                        f"{attorney['jurisdiction']}"
                    ): attorney
                    for attorney in eligible_attorneys
                }

                selected_attorney_label = st.selectbox(
                    "Available Attorney",
                    options=list(attorney_options.keys()),
                    key="assignment_attorney_selection",
                )

                selected_attorney = attorney_options[
                    selected_attorney_label
                ]

                attorney_id = int(
                    selected_attorney["attorney_id"]
                )

                attorney_name = selected_attorney["name"]

                attorney_col_1, attorney_col_2 = st.columns(2)

                with attorney_col_1:
                    st.markdown("**Attorney Name**")
                    st.write(attorney_name)

                    st.markdown("**Attorney ID**")
                    st.write(str(attorney_id))

                with attorney_col_2:
                    st.markdown("**License Jurisdiction**")
                    st.write(selected_attorney["jurisdiction"])

                    st.markdown("**License Status**")
                    st.write(selected_attorney["license_status"])

                role = st.selectbox(
                    "Assignment Role",
                    [
                        "Lead Attorney",
                        "Supporting Attorney",
                        "Reviewer",
                    ],
                    key="assignment_role",
                )

                assignment_date = st.date_input(
                    "Assignment Date",
                    value=date.today(),
                    key="assignment_date",
                )

                st.markdown("#### Review Before Saving")

                st.info(
                    f"""
                    **Matter ID:** {matter_id}  
                    **Matter Name:** {matter_name}  
                    **Client:** {client}  
                    **Jurisdiction:** {jurisdiction}  
                    **Assigned Attorney:** {attorney_name}  
                    **Assigned Attorney ID:** {attorney_id}  
                    **Assignment Role:** {role}  
                    **Assignment Date:** {assignment_date}
                    """
                )

                save_assignment = st.button(
                    "Save Matter Assignment",
                    key="save_matter_assignment_button",
                )

                if save_assignment:
                    assignment_data = {
                        "matter_id": str(matter_id).strip(),
                        "attorney_id": attorney_id,
                        "role": role,
                        "assignment_date": assignment_date,
                    }

                    try:
                        create_matter_assignment(
                            assignment_data
                        )
                        refresh_callback()

                        st.success(
                            "Matter assignment added successfully."
                        )

                        st.rerun()

                    except Exception as e:
                        st.error(
                            f"Could not add matter assignment: {e}"
                        )


def add_years_safely(original_date, years):
    """
    Add whole years to a date while safely handling February 29.
    """
    try:
        return original_date.replace(year=original_date.year + years)
    except ValueError:
        return original_date.replace(
            year=original_date.year + years,
            month=2,
            day=28,
        )


def get_cycle_years(registration_cycle):
    """
    Convert the jurisdiction registration cycle into a year count.
    """
    cycle_years = {
        "Annual": 1,
        "Biennial": 2,
        "Triennial": 3,
    }

    return cycle_years.get(registration_cycle)


def calculate_next_cle_deadline(admission_date, registration_cycle):
    """
    Calculate the next CLE deadline based on the attorney's admission date
    and the jurisdiction's configured registration cycle.
    """
    cycle_years = get_cycle_years(registration_cycle)

    if not admission_date or not cycle_years:
        return None

    deadline = add_years_safely(admission_date, cycle_years)

    while deadline < date.today():
        deadline = add_years_safely(deadline, cycle_years)

    return deadline

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)