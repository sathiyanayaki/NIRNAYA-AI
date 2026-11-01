
from agents.coordinator import AgentCoordinator

coordinator = AgentCoordinator()

flood_data = {
    "rainfall_mm": 150,
    "water_level_cm": 170,
    "drainage_capacity": 25,
    "previous_flooding": 1,
    "elevation_m": 5
}

result = coordinator.run_all(flood_data)

print("\n========== NIRNAYA AI FINAL REPORT ==========")

for key, value in result.items():
    print(f"\n{key}: {value}")
