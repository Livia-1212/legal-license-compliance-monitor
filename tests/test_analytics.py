from src.analysis.load_data import load_all_data
from src.analysis.risk_scoring import calculate_attorney_risk_scores
from src.analysis.matter_license_check import find_matter_license_risks
from src.dashboard.dashboard_summary import generate_dashboard_summary


def test_load_data():
    data = load_all_data()
    assert len(data["attorneys"]) == 8
    assert len(data["licenses"]) == 9
    assert len(data["matters"]) == 8


def test_risk_scoring_output():
    scores = calculate_attorney_risk_scores()
    assert len(scores) == 8
    assert "risk_tier" in scores.columns
    assert "total_risk_score" in scores.columns


def test_high_risk_attorneys_exist():
    scores = calculate_attorney_risk_scores()
    high_risk = scores[scores["risk_tier"] == "High Risk"]
    assert len(high_risk) == 2


def test_matter_license_risks():
    risks = find_matter_license_risks()
    assert len(risks) > 0
    assert "risk_reason" in risks.columns


def test_dashboard_summary():
    summary = generate_dashboard_summary()
    assert summary["total_attorneys"] == 8
    assert summary["high_risk_attorneys"] == 2
    assert summary["total_revenue_exposure"] == 1230000