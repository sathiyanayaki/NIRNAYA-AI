
import networkx as nx


class RouteOptimizationAgent:

    def run(self, flood_risk, safety_weight=None, max_alternatives=3):

        # STEP 1: Validate inputs
        flood_risk = float(flood_risk)

        if flood_risk < 0:
            raise ValueError("Flood risk cannot be negative")

        if max_alternatives < 1:
            raise ValueError("At least one route must be requested")

        if safety_weight is None:
            safety_weight = flood_risk

        if safety_weight < 0:
            raise ValueError("Safety weight cannot be negative")

        # STEP 2: Create simulated road network
        road_network = nx.Graph()

        roads = [
            ("A", "B", 2, 1),
            ("A", "C", 4, 2),
            ("B", "D", 3, 3),
            ("C", "D", 2, 1),
            ("C", "E", 3, 1),
            ("D", "E", 2, 4),
            ("D", "F", 4, 1),
            ("E", "F", 2, 2)
        ]

        for start, end, distance, risk in roads:

            # Dynamic risk increases with overall flood risk
            adjusted_risk = risk * flood_risk

            route_cost = (
                distance + adjusted_risk * safety_weight
            )

            road_network.add_edge(
                start,
                end,
                distance=distance,
                risk=adjusted_risk,
                cost=route_cost
            )

        # STEP 3: Generate alternative routes
        try:
            paths = list(
                nx.shortest_simple_paths(
                    road_network,
                    source="A",
                    target="F",
                    weight="cost"
                )
            )[:max_alternatives]

        except nx.NetworkXNoPath:
            return {
                "agent": "Route Optimization Agent",
                "recommended_route": [],
                "total_route_cost": None,
                "alternative_routes": [],
                "reason": "No available route"
            }

        # STEP 4: Calculate route details
        route_details = []

        for path in paths:

            total_distance = 0
            total_risk = 0
            total_cost = 0

            for i in range(len(path) - 1):

                edge = road_network[path[i]][path[i + 1]]

                total_distance += edge["distance"]
                total_risk += edge["risk"]
                total_cost += edge["cost"]

            route_details.append({
                "route": path,
                "distance": total_distance,
                "risk_score": round(total_risk, 2),
                "total_cost": round(total_cost, 2)
            })

        # STEP 5: Return best route and alternatives
        best_route = route_details[0]

        return {
            "agent": "Route Optimization Agent",
            "recommended_route": best_route["route"],
            "total_route_cost": best_route["total_cost"],
            "distance": best_route["distance"],
            "risk_score": best_route["risk_score"],
            "alternative_routes": route_details[1:],
            "reason": "Selected the route with the lowest combined distance and flood-risk cost"
        }
