
class GeospatialAgent:

    def run(self, flood_data):

        elevation = flood_data["elevation_m"]
        drainage = flood_data["drainage_capacity"]
        previous_flooding = flood_data["previous_flooding"]

        vulnerability_score = 0
        reasons = []

        # Check elevation
        if elevation < 10:
            vulnerability_score += 40
            reasons.append("Low elevation")

        elif elevation < 30:
            vulnerability_score += 20
            reasons.append("Moderate elevation")

        # Check drainage
        if drainage < 30:
            vulnerability_score += 30
            reasons.append("Poor drainage")

        elif drainage < 60:
            vulnerability_score += 15
            reasons.append("Moderate drainage")

        # Check previous flooding
        if previous_flooding == 1:
            vulnerability_score += 30
            reasons.append("Previous flooding reported")

        # Classify vulnerability
        if vulnerability_score >= 70:
            vulnerability = "High"

        elif vulnerability_score >= 35:
            vulnerability = "Medium"

        else:
            vulnerability = "Low"

        return {
            "agent": "Geospatial Agent",
            "vulnerability": vulnerability,
            "vulnerability_score": vulnerability_score,
            "reasons": reasons
        }
