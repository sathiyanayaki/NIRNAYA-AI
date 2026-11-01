
let waterChart = null;

// ==========================================
// 1. MAIN FLOOD ANALYSIS
// ==========================================

async function analyzeFlood() {

    const button = document.getElementById("analyzeBtn");
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const results = document.getElementById("results");

    error.textContent = "";
    results.classList.add("hidden");

    const floodData = {
        rainfall_mm: Number(document.getElementById("rainfall").value),
        water_level_cm: Number(document.getElementById("waterLevel").value),
        drainage_capacity: Number(document.getElementById("drainage").value),
        previous_flooding: Number(document.getElementById("previousFlooding").value),
        elevation_m: Number(document.getElementById("elevation").value)
    };

    // Input validation
    if (Object.values(floodData).some(value => !Number.isFinite(value))) {
        error.textContent = "Please enter valid numbers in all fields.";
        return;
    }

    if (
        floodData.rainfall_mm < 0 || floodData.rainfall_mm > 500 ||
        floodData.water_level_cm < 0 || floodData.water_level_cm > 500 ||
        floodData.drainage_capacity < 0 || floodData.drainage_capacity > 100 ||
        floodData.elevation_m < 0 || floodData.elevation_m > 500
    ) {
        error.textContent = "Please check the input ranges and try again.";
        return;
    }

    button.disabled = true;
    loading.classList.remove("hidden");
    button.textContent = "Analyzing...";

    try {

        const response = await fetch("https://nirnaya-ai-wxjl.onrender.com", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(floodData)
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        const data = await response.json();

        // ----------------------------------
        // Prediction Agent
        // ----------------------------------

        document.getElementById("floodRisk").textContent =
            data.prediction.flood_risk;

        document.getElementById("confidence").textContent =
            (data.prediction.confidence * 100).toFixed(1) + "%";

        // ----------------------------------
        // Geospatial Agent
        // ----------------------------------

        document.getElementById("vulnerability").textContent =
            data.geospatial_analysis.vulnerability;

        document.getElementById("vulnerabilityScore").textContent =
            data.geospatial_analysis.vulnerability_score;

        // ----------------------------------
        // Route Optimization Agent
        // ----------------------------------

        document.getElementById("route").textContent =
            data.route_optimization.recommended_route.join(" → ");

        document.getElementById("routeCost").textContent =
            "Simulated route cost: " +
            data.route_optimization.total_route_cost;

        // ----------------------------------
        // Rainwater Management Agent
        // ----------------------------------

        const water = data.water_management;

        document.getElementById("collectable").textContent =
            water.collectable_water_liters.toLocaleString() + " L";

        document.getElementById("stored").textContent =
            water.stored_water_liters.toLocaleString() + " L";

        document.getElementById("domestic").textContent =
            water.domestic_water_liters.toLocaleString() + " L";

        document.getElementById("recharge").textContent =
            water.groundwater_recharge_liters.toLocaleString() + " L";

        document.getElementById("overflow").textContent =
            water.remaining_overflow_liters.toLocaleString() + " L";

        document.getElementById("remaining").textContent =
            water.remaining_storage_liters.toLocaleString() + " L";

        // Update chart AFTER receiving API data
        updateWaterChart(water);

        // ----------------------------------
        // Decision Auditor
        // ----------------------------------

        document.getElementById("auditStatus").textContent =
            "Audit Status: " + data.decision_audit.audit_status;

        displayList("warnings", data.decision_audit.warnings);

        displayList("recommendations", data.decision_audit.recommendations);

        // ----------------------------------
        // Final Decision
        // ----------------------------------

        document.getElementById("finalDecision").textContent =
            data.final_decision.replaceAll("_", " ");

        results.classList.remove("hidden");

    } catch (err) {

        error.textContent =
            "Analysis failed: " + err.message;

        console.error("Flood analysis error:", err);

    } finally {

        button.disabled = false;
        button.textContent = "Analyze Flood Risk";
        loading.classList.add("hidden");

    }
}


// ==========================================
// 2. DISPLAY WARNINGS AND RECOMMENDATIONS
// ==========================================

function displayList(elementId, items) {

    const list = document.getElementById(elementId);

    list.innerHTML = "";

    if (!items || items.length === 0) {

        const item = document.createElement("li");
        item.textContent = "None";

        list.appendChild(item);
        return;
    }

    items.forEach(text => {

        const item = document.createElement("li");
        item.textContent = text;

        list.appendChild(item);

    });
}


// ==========================================
// 3. WHAT-IF FLOOD SIMULATION
// ==========================================

async function runSimulation() {

    const button = document.getElementById("simulateBtn");
    const loading = document.getElementById("simulationLoading");
    const error = document.getElementById("simulationError");
    const results = document.getElementById("simulationResults");
    const cards = document.getElementById("scenarioCards");

    error.textContent = "";
    results.classList.add("hidden");

    button.disabled = true;
    button.textContent = "Simulating...";

    loading.classList.remove("hidden");

    const baseData = {

        rainfall_mm: 0,

        water_level_cm: Number(document.getElementById("waterLevel").value),

        drainage_capacity: Number(document.getElementById("drainage").value),

        previous_flooding: Number(document.getElementById("previousFlooding").value),

        elevation_m: Number(document.getElementById("elevation").value)

    };

    const rainfallScenarios = [

        { name: "Low Rainfall", rainfall: 100 },

        { name: "Moderate Rainfall", rainfall: 200 },

        { name: "Heavy Rainfall", rainfall: 300 }

    ];

    try {

        cards.innerHTML = "";

        for (const scenario of rainfallScenarios) {

            const response = await fetch("http://127.0.0.1:8000/analyze", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    ...baseData,

                    rainfall_mm: scenario.rainfall

                })

            });

            if (!response.ok) {

                throw new Error(`Backend error: ${response.status}`);

            }

            const data = await response.json();

            const card = document.createElement("div");

            card.className = "scenario-card";

            const heading = document.createElement("h3");

            heading.textContent = scenario.name;

            const rainfall = document.createElement("p");

            rainfall.textContent =
                `Rainfall: ${scenario.rainfall} mm`;

            const risk = document.createElement("p");

            risk.textContent =
                `Flood Risk: ${data.prediction.flood_risk}`;

            const water = document.createElement("p");

            water.textContent =
                `Collectable Water: ${Number(
                    data.water_management.collectable_water_liters
                ).toLocaleString()} L`;

            const decision = document.createElement("p");

            decision.textContent =
                `Decision: ${data.final_decision.replaceAll("_", " ")}`;

            card.append(
                heading,
                rainfall,
                risk,
                water,
                decision
            );

            cards.appendChild(card);

        }

        results.classList.remove("hidden");

    } catch (err) {

        error.textContent =
            "Simulation failed: " + err.message;

        console.error("Simulation error:", err);

    } finally {

        button.disabled = false;

        button.textContent = "Run Scenario Simulation";

        loading.classList.add("hidden");

    }

}


// ==========================================
// 4. RAINWATER DISTRIBUTION CHART
// ==========================================

function updateWaterChart(water) {

    const canvas = document.getElementById("waterChart");

    if (!canvas) {

        console.error("Water chart canvas not found.");

        return;

    }

    if (typeof Chart === "undefined") {

        console.error("Chart.js library is not loaded.");

        return;

    }

    // Destroy previous chart before creating new one
    if (waterChart) {

        waterChart.destroy();

    }

    waterChart = new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: [

                "Domestic Allocation",

                "Remaining Storage",

                "Groundwater Recharge",

                "Remaining Overflow"

            ],

            datasets: [{

                data: [

                    water.domestic_water_liters,

                    water.remaining_storage_liters,

                    water.groundwater_recharge_liters,

                    water.remaining_overflow_liters

                ],

                backgroundColor: [

                    "#35c9d0",

                    "#3498db",

                    "#4adea5",

                    "#e99b45"

                ],

                borderWidth: 2,

                borderColor: "#111d31"

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#e8eef8",

                        padding: 18

                    }

                },

                title: {

                    display: true,

                    text: "Rainwater Allocation (Liters)",

                    color: "#e8eef8"

                }

            }

        }

    });

}
