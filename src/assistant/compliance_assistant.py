import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src" / "analysis"))
sys.path.append(str(ROOT / "src" / "dashboard"))

from risk_scoring import calculate_attorney_risk_scores
from matter_license_check import find_matter_license_risks
from dashboard_summary import generate_dashboard_summary


def show_menu():
    print("\nLegal License Compliance Assistant")
    print("----------------------------------")
    print("1. Show executive dashboard summary")
    print("2. Show attorney risk scores")
    print("3. Show high-risk attorneys")
    print("4. Show matter license risks")
    print("5. Exit")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            summary = generate_dashboard_summary()
            for key, value in summary.items():
                print(f"{key}: {value}")

        elif choice == "2":
            scores = calculate_attorney_risk_scores()
            print(scores.to_string(index=False))

        elif choice == "3":
            scores = calculate_attorney_risk_scores()
            high_risk = scores[scores["risk_tier"] == "High Risk"]
            print(high_risk.to_string(index=False))

        elif choice == "4":
            risks = find_matter_license_risks()
            print(risks.to_string(index=False))

        elif choice == "5":
            print("Exiting compliance assistant.")
            break

        else:
            print("Invalid option. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()