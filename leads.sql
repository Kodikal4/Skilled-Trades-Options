CREATE TABLE user_leads (
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    interest_area TEXT,
    message TEXT,
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);