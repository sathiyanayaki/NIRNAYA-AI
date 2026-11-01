
from agents.decision_auditor import DecisionAuditor


def test_valid_water_calculation():

    auditor = DecisionAuditor()

    prediction = {
        "flood_risk": "High",
        "confidence": 0.97
    }

    geospatial = {
        "vulnerability": "High"
    }

    route = {
        "recommended_route": ["A", "C", "D", "F"]
    }

    water = {
        "stored_water_liters": 3000,
        "domestic_water_liters": 1500,
        "remaining_storage_liters": 1500,
        "overflow_water_liters": 9000,
        "groundwater_recharge_liters": 800,
        "remaining_overflow_liters": 8200
    }

    result = auditor.run(prediction, geospatial, route, water)

    assert result["audit_status"] == "APPROVED"
    assert len(result["warnings"]) == 0

    print("Test 1 Passed: Valid water calculations")


def test_invalid_storage_calculation():

    auditor = DecisionAuditor()

    prediction = {"flood_risk": "High", "confidence": 0.97}
    geospatial = {"vulnerability": "High"}
    route = {"recommended_route": ["A", "C", "D", "F"]}

    water = {
        "stored_water_liters": 3000,
        "domestic_water_liters": 2000,
        "remaining_storage_liters": 1500,
        "overflow_water_liters": 9000,
        "groundwater_recharge_liters": 800,
        "remaining_overflow_liters": 8200
    }

    result = auditor.run(prediction, geospatial, route, water)

    assert result["audit_status"] == "WARNING"
    assert any(
        "storage allocation" in warning
        for warning in result["warnings"]
    )

    print("Test 2 Passed: Invalid storage calculation detected")


if __name__ == "__main__":
    test_valid_water_calculation()
    test_invalid_storage_calculation()

    print("\nAll Decision Auditor tests passed!")
