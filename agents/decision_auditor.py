
class DecisionAuditor:

    def run(self, prediction_result, geospatial_result,
            route_result, water_result):

        warnings = []
        recommendations = []

        predicted_risk = prediction_result["flood_risk"]
        vulnerability = geospatial_result["vulnerability"]
        confidence = prediction_result["confidence"]

        # 1. Check disagreement between agents
        if predicted_risk != vulnerability:
            warnings.append(
                "Prediction and geographical vulnerability results differ."
            )

        # 2. Check prediction confidence
        if confidence < 0.70:
            warnings.append(
                "Prediction confidence is low. Further verification is required."
            )

        # 3. Check high-risk conditions
        if predicted_risk == "High" or vulnerability == "High":
            recommendations.append(
                "Issue an early flood warning."
            )

            recommendations.append(
                "Prioritize vulnerable locations for inspection."
            )
        else:
            recommendations.append(
                "Continue monitoring rainfall and water levels."
            )

        # 4. Check simulated route availability
        if not route_result.get("recommended_route"):
            warnings.append(
                "No simulated route was generated."
            )

        # 5. Check rainwater storage calculation
        stored = water_result["stored_water_liters"]
        domestic = water_result["domestic_water_liters"]
        remaining = water_result["remaining_storage_liters"]

        if abs(stored - (domestic + remaining)) > 0.01:
            warnings.append(
                "Rainwater storage allocation calculation is inconsistent."
            )

        # 6. Check overflow and recharge calculation
        overflow = water_result["overflow_water_liters"]
        recharge = water_result["groundwater_recharge_liters"]
        remaining_overflow = water_result["remaining_overflow_liters"]

        if abs(overflow - (recharge + remaining_overflow)) > 0.01:
            warnings.append(
                "Overflow and groundwater recharge calculation is inconsistent."
            )

        # 7. Rainwater recommendations
        if remaining_overflow > 0:
            recommendations.append(
                "Evaluate additional rainwater storage or suitable overflow management."
            )

        if recharge > 0:
            recommendations.append(
                "Verify groundwater recharge suitability, filtration and site conditions."
            )

        if domestic > 0:
            recommendations.append(
                "Verify water quality and treatment before domestic use."
            )

        # 8. Final audit status
        audit_status = "WARNING" if warnings else "APPROVED"

        return {
            "agent": "Decision Auditor",
            "audit_status": audit_status,
            "warnings": warnings,
            "recommendations": recommendations
        }
