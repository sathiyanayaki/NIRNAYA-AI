
from agents.route_agent import RouteOptimizationAgent

agent = RouteOptimizationAgent()

result = agent.run(flood_risk=3)

print("\nROUTE OPTIMIZATION AGENT RESULT")
print("--------------------------------")

for key, value in result.items():
    print(f"{key}: {value}")
