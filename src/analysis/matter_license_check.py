from load_data import load_all_data


def find_matter_license_risks():
    data = load_all_data()

    attorneys = data["attorneys"]
    licenses = data["licenses"]
    matters = data["matters"]
    assignments = data["matter_assignments"]

    merged = (
        assignments
        .merge(attorneys, on="attorney_id", how="left")
        .merge(matters, on="matter_id", how="left", suffixes=("_attorney", "_matter"))
        .merge(licenses, on=["attorney_id", "jurisdiction"], how="left")
    )

    risky = merged[
        (merged["license_status"].isna()) |
        (merged["license_status"].isin(["Expired", "Suspended"]))
    ]

    return risky[
        [
            "matter_id",
            "matter_name",
            "client",
            "jurisdiction",
            "revenue",
            "attorney_id",
            "name",
            "role",
            "license_status",
            "registration_expiry",
        ]
    ]


if __name__ == "__main__":
    risks = find_matter_license_risks()
    print("Matter License Risk Results")
    print(risks.to_string(index=False))