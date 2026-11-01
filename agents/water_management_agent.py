
class RainwaterManagementAgent:

    def analyze(
        self,
        rainfall_mm,
        catchment_area_m2,
        runoff_coefficient,
        tank_capacity_liters,
        recharge_suitable=False,
        recharge_capacity_liters=0
    ):

        # Calculate collectable rainwater
        collectable_water = (
            rainfall_mm
            * catchment_area_m2
            * runoff_coefficient
        )

        # Calculate storage
        stored_water = min(
            collectable_water,
            tank_capacity_liters
        )
        domestic_water = stored_water * 0.50
        remaining_storage = stored_water - domestic_water

        # Calculate excess water
        overflow_water = max(
            0,
            collectable_water - stored_water
        )

        # Groundwater recharge allocation
        if recharge_suitable:
            recharge_water = min(
                overflow_water,
                recharge_capacity_liters
            )
        else:
            recharge_water = 0

        remaining_overflow = (
            overflow_water - recharge_water
        )

        return {
            "agent": "Rainwater Management Agent",
            "domestic_water_liters": round(domestic_water, 2),
            "remaining_storage_liters": round(remaining_storage, 2),
            "collectable_water_liters": round(collectable_water, 2),
            "stored_water_liters": round(stored_water, 2),
            "overflow_water_liters": round(overflow_water, 2),
            "groundwater_recharge_liters": round(recharge_water, 2),
            "remaining_overflow_liters": round(remaining_overflow, 2)
        }
