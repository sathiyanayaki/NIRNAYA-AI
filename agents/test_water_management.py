
from agents.water_management_agent import RainwaterManagementAgent

# Create agent object
agent = RainwaterManagementAgent()

# Give sample rainfall data
result = agent.analyze(
    rainfall_mm=50,
    catchment_area_m2=100,
    runoff_coefficient=0.8,
    tank_capacity_liters=3000,
    recharge_suitable=True,
    recharge_capacity_liters=800
)

# Display results
for key, value in result.items():
    print(key, ":", value)
