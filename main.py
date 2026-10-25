from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CitySentinel API", version="0.1.0", description="Synthetic urban incident analysis prototype")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All records below are synthetic examples created for the prototype.
INCIDENTS: list[dict[str, Any]] = [
    {"id":"CS-1042","title":"Intersection congestion","category":"Traffic","location":"Central Avenue · Sector 04","severity":"High","status":"Investigating","reported_at":"09:42","description":"Simulated vehicle-count data is 42% above the usual baseline for this time window.","metrics":{"traffic_index":82,"baseline":58,"confidence":0.91},"evidence":["Vehicle count +42% versus synthetic baseline","Average speed reduced to 11 km/h","Two adjacent junctions show elevated load"]},
    {"id":"CS-1041","title":"Water pressure anomaly","category":"Infrastructure","location":"North Grid · Sector 02","severity":"Medium","status":"New","reported_at":"09:31","description":"A simulated sensor reports a sudden pressure drop in one distribution zone.","metrics":{"pressure_drop":27,"sensor_count":3,"confidence":0.84},"evidence":["Pressure dropped 27% in 8 minutes","Three synthetic sensor readings agree","No confirmed outage report in sample feed"]},
    {"id":"CS-1040","title":"Streetlight cluster offline","category":"Energy","location":"Riverwalk · Sector 07","severity":"Low","status":"Monitoring","reported_at":"09:18","description":"Several connected streetlight devices stopped reporting status.","metrics":{"offline_devices":12,"total_devices":180,"confidence":0.88},"evidence":["12 of 180 simulated devices are offline","Failures are clustered on one feeder","No public safety incident is confirmed"]},
    {"id":"CS-1039","title":"Air quality alert","category":"Environment","location":"East Industrial Zone · Sector 09","severity":"High","status":"Needs review","reported_at":"09:05","description":"Synthetic particulate readings exceed the demo threshold for two consecutive intervals.","metrics":{"pm25":91,"threshold":60,"confidence":0.86},"evidence":["PM2.5 sample value: 91 µg/m³","Demo threshold: 60 µg/m³","Second consecutive elevated interval"]},
    {"id":"CS-1038","title":"Transit delay cluster","category":"Mobility","location":"Metro Link · Sector 01","severity":"Medium","status":"Resolved","reported_at":"08:52","description":"Simulated bus arrival delays increased after a lane restriction scenario.","metrics":{"delay_minutes":14,"routes_affected":3,"confidence":0.79},"evidence":["Three simulated routes delayed by 14 minutes","Nearby congestion index also elevated","No live transit system is connected"]},
]
ANALYSES: dict[str, dict[str, Any]] = {}

class ApprovalRequest(BaseModel):
    approved_by: str = Field(min_length=2, max_length=80)
    note: str = Field(default="Approved after human review", max_length=500)

@app.get("/health")
def health():
    return {"status":"ok", "service":"CitySentinel API", "mode":"synthetic-demo", "timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/api/incidents")
def get_incidents():
    return {"items":INCIDENTS, "count":len(INCIDENTS), "data_mode":"synthetic-demo"}

@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):
    item = next((x for x in INCIDENTS if x["id"] == incident_id), None)
    if not item:
        raise HTTPException(404, "Incident not found")
    return item

@app.post("/api/analyze/{incident_id}")
def analyze_incident(incident_id: str):
    item = next((x for x in INCIDENTS if x["id"] == incident_id), None)
    if not item:
        raise HTTPException(404, "Incident not found")

    # Deterministic, explainable agent workflow for the hackathon prototype.
    data_agent = {"agent":"Urban Data Agent", "status":"complete", "summary":f"Reviewed {len(item['evidence'])} synthetic evidence signals and the available incident metrics.", "evidence":item["evidence"]}
    investigation = {"agent":"Investigation Agent", "status":"complete", "summary":item["description"], "limitations":["Data is simulated; external sources are not connected.", "The system cannot confirm the physical cause from these signals alone."]}
    severity = item["severity"]
    score = {"High":82, "Medium":57, "Low":28}.get(severity, 40)
    risk = {"agent":"Risk Assessment Agent", "status":"complete", "risk_score":score, "risk_level":severity, "confidence":item["metrics"].get("confidence", 0.75), "rationale":f"Severity is based on the seeded demo category and evidence. Confidence is an illustrative signal, not a calibrated probability."}
    action_map = {
        "Traffic": "Recommend reviewing signal timing and checking adjacent junction capacity.",
        "Infrastructure": "Recommend dispatching an authorized field inspection to validate the pressure readings.",
        "Energy": "Recommend checking the affected feeder and scheduling a maintenance inspection.",
        "Environment": "Recommend validating readings with an approved monitoring source and escalating to an authorized city operator.",
        "Mobility": "Recommend reviewing route alternatives and publishing a service advisory if verified.",
    }
    recommendation = action_map.get(item["category"], "Recommend human review of the incident and available evidence.")
    plan = {"agent":"Planning Agent", "status":"awaiting_human_approval", "recommended_action":recommendation, "requires_human_approval":True, "steps":["Validate the supporting evidence", "Route recommendation to the authorized operator", "Record the approved action and follow-up status"]}
    verification = {"agent":"Outcome Verification Agent", "status":"not_run", "summary":"Outcome cannot be verified until an action is approved and follow-up observations are provided.", "required_follow_up":["Post-action measurement", "Timestamped operator update"]}
    result = {"incident_id":incident_id,"generated_at":datetime.now(timezone.utc).isoformat(),"data_mode":"synthetic-demo","agents":[data_agent, investigation, risk, plan, verification],"risk":risk,"recommendation":recommendation,"approval":{"required":True,"approved":False,"approved_by":None,"note":None},"notice":"Decision support only. This prototype does not dispatch emergency services or control city infrastructure."}
    ANALYSES[incident_id] = result
    return result

@app.post("/api/incidents/{incident_id}/approve")
def approve_recommendation(incident_id: str, request: ApprovalRequest):
    result = ANALYSES.get(incident_id)
    if not result:
        raise HTTPException(409, "Analyze this incident before recording approval")
    result["approval"] = {"required":True,"approved":True,"approved_by":request.approved_by,"note":request.note,"approved_at":datetime.now(timezone.utc).isoformat()}
    result["agents"][-2]["status"] = "approved_by_human"
    result["agents"][-1]["status"] = "awaiting_follow_up_data"
    result["agents"][-1]["summary"] = "Human approval recorded. Verification still requires post-action observations; approval alone is not proof of success."
    return {"success":True,"analysis":result}
