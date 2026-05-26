CREATE TABLE diagnostic_challenges (
    component TEXT NOT NULL,
    symptom TEXT NOT NULL,
    failure_mode TEXT NOT NULL
);

CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    trade_type TEXT NOT NULL,
    correct_count INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE diagnostic_challenges ADD COLUMN explanation TEXT;
ALTER TABLE diagnostic_challenges ADD COLUMN trade_type TEXT DEFAULT 'Diesel';

-- Insert a few Caterpillar-specific diagnostic challenges
INSERT INTO diagnostic_challenges (component, symptom, failure_mode) VALUES 
('Fuel Injector', 'Engine cranks but won''t fire; smoke from exhaust is absent.', 'Fuel'),
('Glow Plugs', 'Difficult cold start in winter conditions.', 'Spark'),
('Cylinder Head', 'White smoke and loss of power; bubbles in coolant.', 'Compression'),
('High Pressure Pump', 'Engine stalls under heavy load; low rail pressure code.', 'Fuel');

INSERT INTO diagnostic_challenges (component, symptom, failure_mode, explanation, trade_type) VALUES 
('Step Transformer', 'Audible humming and oil residue on the casing.', 'Electrical', 'Internal winding failure or bushing leak causing overheating.', 'Lineman'),
('Suspension Insulator', 'Visible flashover scars and carbon tracking.', 'Insulation', 'Contamination on the surface allowed electricity to arc across.', 'Lineman'),
('Cross-arm', 'Noticeable sagging and hairline timber fractures.', 'Structural', 'Wood rot or extreme mechanical stress from line tension.', 'Lineman'),
('Capacitor Bank', 'Low power factor readings and phase imbalance.', 'Electrical', 'Blown internal fuses or capacitor cell rupture.', 'Lineman'),
('Guy Wire', 'Severe corrosion and lack of tension on a leaning pole.', 'Structural', 'Anchor point failure or oxidation of the galvanized steel.', 'Lineman');

-- 1. HVAC Specialist Challenges
INSERT INTO diagnostic_challenges (component, symptom, failure_mode, explanation, trade_type) VALUES 
('Compressor', 'Unit hums loudly but will not start; thermal overload trips quickly.', 'Electrical', 'Failed start capacitor or locked rotor condition preventing mechanical rotation.', 'HVAC'),
('Evaporator Coil', 'System runs constantly but airflow is low and ice buildup is visible.', 'Airflow', 'Restricted air movement due to a severely clogged filter or dirty coil surfaces.', 'HVAC'),
('TXV (Thermal Expansion Valve)', 'Suction pressure is unusually low; high superheat at evaporator outlet.', 'Restriction', 'The valve orifice is restricted or the sensing bulb has lost its charge, starving the coil.', 'HVAC');

-- 2. Power Plant Ops Challenges
INSERT INTO diagnostic_challenges (component, symptom, failure_mode, explanation, trade_type) VALUES 
('Steam Turbine', 'Sudden spike in high-frequency vibration readings at 3600 RPM.', 'Mechanical', 'Blade scaling or rotor imbalance causing dynamic distortion under full load.', 'PowerPlant'),
('Condenser', 'Back-pressure is rising steadily; cooling water temperature delta is dropping.', 'Thermal', 'Tube fouling or air ingress reducing heat transfer efficiency in the vacuum stage.', 'PowerPlant'),
('Exciter', 'Main generator output voltage dropping while rotor speed remains stable.', 'Electrical', 'Loss of residual magnetism or brush wear interrupting the field excitation current.', 'PowerPlant');