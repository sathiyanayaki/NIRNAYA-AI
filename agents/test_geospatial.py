from agents.geospatial_agent import GeospatialAgent

agent = GeospatialAgent()

flood_data = {
    "rainfall_mm": 150,
    "water_level_cm": 170,
    "drainage_capacity": 25,
    "previous_flooding": 1,
    "elevation_m": 5
}

result = agent.run(flood_data)

print("\nGEOSPATIAL AGENT RESULT")
print("-----------------------")

for key, value in result.items():
    print(f"{key}: {value}")
