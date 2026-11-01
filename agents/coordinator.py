
import time

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

    # Common function to execute and monitor agents
    def execute_agent(self, agent_name, function, *args, **kwargs):

        start_time = time.perf_counter()

        try:
            result = function(*args, **kwargs)

            if not isinstance(result, dict):
                raise TypeError("Agent must return a dictionary")

            execution_time = time.perf_counter() - start_time

            return result, {
                "status": "SUCCESS",
                "execution_time_seconds": round(execution_time, 4),
                "error": None
            }

        except Exception as error:

            execution_time = time.perf_counter() - start_time

            return None, {
                "status": "FAILED",
                "execution_time_seconds": round(execution_time, 4),
                "error": str(error)
            }

    def run_all(self, flood_data):

        print("NIRNAYA AI: Starting Multi-Agent Analysis...")

        agent_status = {}

        # Agent 1: Flood prediction
        prediction_result, agent_status["prediction"] = (
            self.execute_agent(
                "Prediction Agent",
                self.prediction_agent.run,
                flood_data
            )
        )

        # Agent 2: Geospatial analysis
        geospatial_result, agent_status["geospatial"] = (
            self.execute_agent(
                "Geospatial Agent",
                self.geospatial_agent.run,
                flood_data
            )
        )

        # Agent 3: Route optimization
        route_result = None

        if (
            prediction_result is not None
            and prediction_result.get("flood_risk") in
            ["Low", "Medium", "High"]
        ):

            flood_risk = {
                "Low": 1,
                "Medium": 2,
                "High": 3
            }[prediction_result["flood_risk"]]

            route_result, agent_status["route"] = (
                self.execute_agent(
                    "Route Optimization Agent",
                    self.route_agent.run,
                    flood_risk
                )
            )

        else:
            agent_status["route"] = {
                "status": "SKIPPED",
                "execution_time_seconds": 0,
                "error": "Valid prediction unavailable"
            }

        # Agent 4: Rainwater management
        water_result, agent_status["water"] = (
            self.execute_agent(
                "Rainwater Management Agent",
                self.water_agent.analyze,
                rainfall_mm=flood_data["rainfall_mm"],
                catchment_area_m2=100,
                runoff_coefficient=0.8,
                tank_capacity_liters=3000,
                recharge_suitable=True,
                recharge_capacity_liters=800
            )
        )

        # Agent 5: Decision auditing
        audit_result = None

        required_results = [
            prediction_result,
            geospatial_result,
            route_result,
            water_result
        ]

        if all(result is not None for result in required_results):

            audit_result, agent_status["auditor"] = (
                self.execute_agent(
                    "Decision Auditor",
                    self.auditor.run,
                    prediction_result,
                    geospatial_result,
                    route_result,
                    water_result
                )
            )

        else:
            agent_status["auditor"] = {
                "status": "SKIPPED",
                "execution_time_seconds": 0,
                "error": "One or more required agents failed"
            }

        # Final decision
        if (
            prediction_result is None
            or geospatial_result is None
            or audit_result is None
            or audit_result.get("audit_status") != "APPROVED"
        ):
            final_decision = "SYSTEM_REVIEW_REQUIRED"

        elif (
            prediction_result["flood_risk"] == "High"
            or geospatial_result["vulnerability"] == "High"
        ):
            final_decision = "EARLY FLOOD WARNING"

        else:
            final_decision = "CONTINUE MONITORING"

        # Combine all results
        final_result = {
            "project": "NIRNAYA AI",
            "prediction": prediction_result,
            "geospatial_analysis": geospatial_result,
            "route_optimization": route_result,
            "water_management": water_result,
            "decision_audit": audit_result,
            "agent_status": agent_status,
            "final_decision": final_decision
        }

        print("\nAgent execution summary:")

        for agent, status in agent_status.items():
            print(
                f"{agent}: {status['status']} | "
                f"{status['execution_time_seconds']} seconds"
            )

        return final_result
