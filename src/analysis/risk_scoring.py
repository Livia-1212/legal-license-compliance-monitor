from load_data import load_all_data


def calculate_attorney_risk_scores():
    data = load_all_data()

    attorneys = data["attorneys"]
    licenses = data["licenses"]
    cle = data["cle_records"]
    matters = data["matters"]
    assignments = data["matter_assignments"]

    matter_exposure = (
        assignments
        .merge(matters, on="matter_id", how="left")
        .groupby("attorney_id", as_index=False)
        .agg(
            assigned_matter_count=("matter_id", "nunique"),
            revenue_exposure=("revenue", "sum"),
        )
    )

    license_scores = licenses.copy()
    license_scores["license_risk_score"] = license_scores["license_status"].map(
        {
            "Active": 0,
            "Expired": 40,
            "Suspended": 50,
        }
    ).fillna(30)

    license_scores = (
        license_scores
        .groupby("attorney_id", as_index=False)
        .agg(license_risk_score=("license_risk_score", "max"))
    )

    cle_scores = cle.copy()
    cle_scores["cle_risk_score"] = cle_scores.apply(
        lambda row: 25 if row["completed_hours"] < row["required_hours"] else 0,
        axis=1,
    )

    cle_scores = (
        cle_scores
        .groupby("attorney_id", as_index=False)
        .agg(cle_risk_score=("cle_risk_score", "max"))
    )

    risk = (
        attorneys
        .merge(license_scores, on="attorney_id", how="left")
        .merge(cle_scores, on="attorney_id", how="left")
        .merge(matter_exposure, on="attorney_id", how="left")
    )

    risk[["license_risk_score", "cle_risk_score", "assigned_matter_count", "revenue_exposure"]] = (
        risk[["license_risk_score", "cle_risk_score", "assigned_matter_count", "revenue_exposure"]]
        .fillna(0)
    )

    risk["revenue_exposure_risk_score"] = risk["revenue_exposure"].apply(
        lambda revenue: 20 if revenue >= 200000 else 10 if revenue >= 100000 else 0
    )

    risk["total_risk_score"] = (
        risk["license_risk_score"]
        + risk["cle_risk_score"]
        + risk["revenue_exposure_risk_score"]
    )

    risk["risk_tier"] = risk["total_risk_score"].apply(
        lambda score: "High Risk" if score >= 70 else "Medium Risk" if score >= 40 else "Low Risk"
    )

    return risk[
        [
            "attorney_id",
            "name",
            "title",
            "office",
            "practice_area",
            "assigned_matter_count",
            "revenue_exposure",
            "license_risk_score",
            "cle_risk_score",
            "revenue_exposure_risk_score",
            "total_risk_score",
            "risk_tier",
        ]
    ].sort_values("total_risk_score", ascending=False)


if __name__ == "__main__":
    scores = calculate_attorney_risk_scores()
    print("Attorney Risk Scores")
    print(scores.to_string(index=False))