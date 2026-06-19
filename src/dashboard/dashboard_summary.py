import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src" / "analysis"))

from load_data import load_all_data
from risk_scoring import calculate_attorney_risk_scores


def generate_dashboard_summary():
    data = load_all_data()

    attorneys = data["attorneys"]
    licenses = data["licenses"]
    cle = data["cle_records"]
    matters = data["matters"]

    risk_scores = calculate_attorney_risk_scores()

    summary = {
        "total_attorneys": len(attorneys),
        "active_attorneys": len(attorneys[attorneys["employment_status"] == "Active"]),
        "active_licenses": len(licenses[licenses["license_status"] == "Active"]),
        "expired_licenses": len(licenses[licenses["license_status"] == "Expired"]),
        "suspended_licenses": len(licenses[licenses["license_status"] == "Suspended"]),
        "cle_compliant_records": len(cle[cle["completed_hours"] >= cle["required_hours"]]),
        "cle_deficient_records": len(cle[cle["completed_hours"] < cle["required_hours"]]),
        "total_revenue_exposure": matters["revenue"].sum(),
        "high_risk_attorneys": len(risk_scores[risk_scores["risk_tier"] == "High Risk"]),
        "medium_risk_attorneys": len(risk_scores[risk_scores["risk_tier"] == "Medium Risk"]),
        "low_risk_attorneys": len(risk_scores[risk_scores["risk_tier"] == "Low Risk"]),
    }

    return summary


if __name__ == "__main__":
    dashboard = generate_dashboard_summary()

    print("Executive Dashboard Summary")
    print("---------------------------")
    for key, value in dashboard.items():
        print(f"{key}: {value}")