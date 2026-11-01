
from agents.prediction_agent import PredictionAgent
# Initialize agent
agent = PredictionAgent()

# Sample flood conditions
flood_data = {
    "rainfall_mm": 150,
    "water_level_cm": 170,
    "drainage_capacity": 25,
    "previous_flooding": 1,
    "elevation_m": 5
}

# Execute agent
result = agent.run(flood_data)

print("\nPREDICTION AGENT RESULT")
print("-----------------------")

for key, value in result.items():
    print(f"{key}: {value}")
