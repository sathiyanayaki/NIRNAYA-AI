
from agents.prediction_agent import PredictionAgent
from agents.geospatial_agent import GeospatialAgent
from agents.route_agent import RouteOptimizationAgent
from agents.decision_auditor import DecisionAuditor
from agents.water_management_agent import RainwaterManagementAgent


class AgentCoordinator:

    def __init__(self):
        self.prediction_agent = PredictionAgent()
        self.geospatial_agent = GeospatialAgent()
        self.route_agent = RouteOptimizationAgent()
        self.auditor = DecisionAuditor()
        self.water_agent = RainwaterManagementAgent()

    def run_all(self, flood_data):

        print("NIRNAYA AI: Starting Multi-Agent Analysis...")

        # Agent 1: Flood prediction
        prediction_result = self.prediction_agent.run(flood_data)

        # Agent 2: Geographical vulnerability
        geospatial_result = self.geospatial_agent.run(flood_data)

        # Agent 3: Route optimization
        flood_risk = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }[prediction_result["flood_risk"]]

        route_result = self.route_agent.run(flood_risk)

        # Agent 4: Rainwater management
        water_result = self.water_agent.analyze(
            rainfall_mm=flood_data["rainfall_mm"],
            catchment_area_m2=100,
            runoff_coefficient=0.8,
            tank_capacity_liters=3000,
            recharge_suitable=True,
            recharge_capacity_liters=800
        )

        # Agent 5: Decision auditing
        audit_result = self.auditor.run(
            prediction_result,
            geospatial_result,
            route_result,
            water_result
        )

        # Combine all agent results
        final_result = {
            "project": "NIRNAYA AI",
            "prediction": prediction_result,
            "geospatial_analysis": geospatial_result,
            "route_optimization": route_result,
            "water_management": water_result,
            "decision_audit": audit_result,
            "final_decision": (
                "EARLY FLOOD WARNING"
                if prediction_result["flood_risk"] == "High"
                or geospatial_result["vulnerability"] == "High"
                else "CONTINUE MONITORING"
            )
        }

        return final_result
