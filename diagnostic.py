import random

def process_engine_data(db_row):
    """
    Takes raw database info and turns it into a 
    Creative Diagnostic Experience.
    """
    # db_row order: component, symptom, failure_mode, explanation
    component, symptom, failure, explanation, trade = db_row

    # Industrial Vitals for Linework
    if trade == 'Lineman':
        vitals = {
            "primary_kv": "12.4 kV",
            "secondary_v": "240V",
            "load_amps": random.randint(150, 400),
            "insulation_rating": "Class 2"
        }
        status_label = "GRID STATUS: ALERT"
    else:
        # Keep your Diesel logic here
        vitals = {"fuel_psi": "24,500", "rpm": "850", "load": "14%"}
        status_label = "ENGINE STATUS: FAULT"
    
    # Add 'Nitty-Gritty' tech hints
    tech_notes = [
        "Check harness for continuity.",
        "Inspect for fluid aeration.",
        "Verify ECM ground source."
    ]
    
    # Create fake live sensor data to make the UI look complex
    live_vitals = {
        "pressure": random.randint(2000, 30000),
        "temp": random.randint(150, 220),
        "status": "DETERIORATED" if random.random() > 0.5 else "CRITICAL"
    }

    return {
        "component": component,
        "symptom": symptom,
        "failure_mode": failure,
        "explanation": explanation,
        "hint": random.choice(tech_notes),
        "vitals": live_vitals
    }

    