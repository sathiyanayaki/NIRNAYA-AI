
import networkx as nx


class RouteOptimizationAgent:

    def run(self, flood_risk):

        # Create a sample road network
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

        # Add roads with distance and flood risk
        for start, end, distance, risk in roads:

            road_network.add_edge(
                start,
                end,
                distance=distance,
                risk=risk
            )

        # Calculate combined route cost
        for u, v, data in road_network.edges(data=True):

            data["cost"] = (
                data["distance"] + data["risk"] * flood_risk
            )

        # Find safest route from A to F
        route = nx.shortest_path(
            road_network,
            source="A",
            target="F",
            weight="cost"
        )

        total_cost = nx.shortest_path_length(
            road_network,
            source="A",
            target="F",
            weight="cost"
        )

        return {
            "agent": "Route Optimization Agent",
            "recommended_route": route,
            "total_route_cost": round(total_cost, 2),
            "reason": "Selected the route with the lowest distance-risk cost"
        }
