import random

def process_engine_data(db_row):
    """
    Takes raw database info across multiple trade sectors and 
    generates randomized, live simulation vitals and hints.
    """
    # Unpack the database row
    component, symptom, failure, explanation, trade = db_row

    # 1. HVAC Specialist Logic
    if trade == 'HVAC':
        vitals = {
            "suction_psi": f"{random.randint(110, 130)} PSI",
            "liquid_psi": f"{random.randint(320, 380)} PSI",
            "superheat": f"{random.randint(8, 18)}°F",
            "status": "HVAC ALERT"
        }
        tech_notes = [
            "Check delta-T across the evaporator coil.",
            "Verify contactor points aren't pitted or welded.",
            "Test airflow static pressure in the return plenum."
        ]

    # 2. Power Plant Ops Logic
    elif trade == 'PowerPlant':
        vitals = {
            "turbine_rpm": f"{random.randint(3590, 3610)} RPM",
            "steam_temp": f"{random.randint(950, 1050)}°F",
            "megawatts": f"{random.randint(250, 500)} MW",
            "status": "PLANT ALERT"
        }
        tech_notes = [
            "Monitor vibration harmonics on bearing pads.",
            "Check condenser vacuum drop rate.",
            "Verify automatic voltage regulator tracking."
        ]

    # 3. Power Grid (Lineman) Logic
    elif trade == 'Lineman':
        vitals = {
            "primary_kv": f"{random.uniform(11.9, 12.6):.1f} kV",
            "secondary_v": f"{random.randint(235, 245)}V",
            "load_balance": f"{random.randint(80, 100)}%",
            "ambient_temp": f"{random.randint(40, 105)}°F",
            "status": "GRID ALERT"
        }
        tech_notes = [
            "Check for signs of tracking on insulators.",
            "Verify transformer oil level and temperature.",
            "Inspect primary tap connections for hotspots.",
            "Verify guy wire tension."
        ]
    elif trade == 'Automation':
        vitals = {
            "bus_voltage": f"{random.randint(23, 27)} VDC",
            "vfd_frequency": f"{random.randint(20, 60)} Hz",
            "cycle_time": f"{random.randint(50, 70)} ms",
            "status": "Bus Fault"
        }
        tech_notes = [
            "Monitor Profinet/EtherNetIP packet drop rates.",
            "Trace schematic back to terminal strip junction box.",
            "Verify logic continuity in the online ladder diagram."
        ]

    # 4. Default: Heavy Equipment (Diesel) Logic
    else:
        vitals = {
            "fuel_psi": f"{random.randint(22000, 26000)} PSI", 
            "rpm": f"{random.randint(700, 900)} RPM", 
            "load": "14%",
            "status": "ENGINE FAULT"
        }
        tech_notes = [
            "Check harness for continuity.",
            "Inspect for fluid aeration.",
            "Verify ECM ground source."
        ]

    # A single, unified exit point for all trades
    return {
        "component": component,
        "symptom": symptom,
        "failure_mode": failure,
        "explanation": explanation,
        "hint": random.choice(tech_notes),
        "vitals": vitals
    }