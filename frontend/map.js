
let nirnayaMap = null;
let routeLayers = [];

const mapNodes = {
    A: [13.0067, 80.2206],
    B: [13.0213, 80.2231],
    C: [13.0063, 80.2570],
    D: [12.9815, 80.2180],
    E: [12.9860, 80.2480],
    F: [12.9830, 80.2590]
};

const roads = [
    ["A", "B"], ["A", "C"],
    ["B", "D"], ["C", "D"],
    ["C", "E"], ["D", "E"],
    ["D", "F"], ["E", "F"]
];

function initializeFloodMap() {

    if (nirnayaMap) {
        setTimeout(() => nirnayaMap.invalidateSize(), 200);
        return;
    }

    const container = document.getElementById("floodMap");

    if (!container || typeof L === "undefined") {
        console.error("Map container or Leaflet is missing.");
        return;
    }

    nirnayaMap = L.map("floodMap").setView(
        [13.005, 80.240], 12
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors",
            maxZoom: 19
        }
    ).addTo(nirnayaMap);

    // Simulated road network
    roads.forEach(([start, end]) => {

        L.polyline(
            [mapNodes[start], mapNodes[end]],
            {
                color: "#94a3b8",
                weight: 3,
                opacity: 0.6,
                dashArray: "5,7"
            }
        ).addTo(nirnayaMap);

    });

    // Illustrative Chennai risk markers
    const locations = [
        { name: "Guindy", node: "A", risk: "High" },
        { name: "Saidapet", node: "B", risk: "Medium" },
        { name: "Adyar", node: "C", risk: "High" },
        { name: "Velachery", node: "D", risk: "High" },
        { name: "Taramani", node: "E", risk: "Medium" },
        { name: "Thiruvanmiyur", node: "F", risk: "Low" }
    ];

    const colors = {
        Low: "#16a34a",
        Medium: "#eab308",
        High: "#dc2626"
    };

    locations.forEach(location => {

        const marker = L.circleMarker(
            mapNodes[location.node],
            {
                radius: 10,
                color: colors[location.risk],
                fillColor: colors[location.risk],
                fillOpacity: 0.8,
                weight: 2
            }
        ).addTo(nirnayaMap);

        marker.bindPopup(
            `<b>${location.name}</b><br>
             Illustrative risk: ${location.risk}`
        );

    });

    setTimeout(() => nirnayaMap.invalidateSize(), 300);
}


// Remove previously displayed routes
function clearRoutes() {

    routeLayers.forEach(layer => {
        nirnayaMap.removeLayer(layer);
    });

    routeLayers = [];
}


// Convert route names to coordinates
function getCoordinates(route) {

    return route
        .filter(node => mapNodes[node])
        .map(node => mapNodes[node]);
}


// Draw API-generated routes
function updateFloodMap(data) {

    if (!nirnayaMap || !data) return;

    clearRoutes();

    const routeData = data.route_optimization || {};

    const recommended = routeData.recommended_route || [];

    const alternatives = routeData.alternative_routes || [];

    // Recommended route
    if (recommended.length >= 2) {

        const line = L.polyline(
            getCoordinates(recommended),
            {
                color: "#2563eb",
                weight: 7,
                opacity: 0.95
            }
        ).addTo(nirnayaMap);

        line.bindPopup("Recommended simulated route");

        routeLayers.push(line);

        document.getElementById(
            "mapRecommendedRoute"
        ).textContent =
            "Recommended: " + recommended.join(" → ");

        nirnayaMap.fitBounds(
            line.getBounds(),
            { padding: [40, 40] }
        );

    } else {

        document.getElementById(
            "mapRecommendedRoute"
        ).textContent = "No recommended route available.";

    }

    // Alternative routes
    const alternativeContainer = document.getElementById(
        "mapAlternativeRoutes"
    );

    alternativeContainer.innerHTML = "";

    alternatives.forEach((item, index) => {

        const route = item.route || [];

        if (route.length < 2) return;

        const line = L.polyline(
            getCoordinates(route),
            {
                color: "#9333ea",
                weight: 5,
                opacity: 0.85,
                dashArray: "8,8"
            }
        ).addTo(nirnayaMap);

        line.bindPopup(`Alternative route ${index + 1}`);

        routeLayers.push(line);

        const paragraph = document.createElement("p");

        paragraph.className = "alternative-route";

        paragraph.textContent =
            `Alternative ${index + 1}: ${route.join(" → ")} | Cost: ${item.total_cost}`;

        alternativeContainer.appendChild(paragraph);

    });

    // Agent execution status
    updateAgentStatus(data.agent_status || {});
}


// Display agent status
function updateAgentStatus(statuses) {

    const panel = document.getElementById(
        "agentStatusPanel"
    );

    if (!panel) return;

    panel.innerHTML = "";

    const grid = document.createElement("div");

    grid.className = "agent-status-grid";

    Object.entries(statuses).forEach(([name, details]) => {

        const card = document.createElement("div");

        card.className = "agent-status-item";

        if (details.status === "SUCCESS") {
            card.classList.add("success");
        } else if (details.status === "FAILED") {
            card.classList.add("failed");
        } else {
            card.classList.add("skipped");
        }

        const title = document.createElement("strong");
        title.textContent = name.toUpperCase();

        const status = document.createElement("p");
        status.textContent = details.status;

        const timing = document.createElement("small");
        timing.textContent =
            `Execution: ${details.execution_time_seconds} seconds`;

        card.append(title, status, timing);

        grid.appendChild(card);

    });

    panel.appendChild(grid);
}


// Receive analysis response from existing script.js
window.addEventListener("nirnaya-analysis-complete", event => {

    initializeFloodMap();

    updateFloodMap(event.detail);

});


// Initialize when the results section becomes visible
const resultsSection = document.getElementById("results");

if (resultsSection) {

    const observer = new MutationObserver(() => {

        if (!resultsSection.classList.contains("hidden")) {
            initializeFloodMap();
        }

    });

    observer.observe(resultsSection, {
        attributes: true,
        attributeFilter: ["class"]
    });

}
