import psycopg2
import diagnostic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import re
from fastapi import HTTPException
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any page to access the API
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="diesel_startup",
        user="postgres",
        password="YOUR_ACTUAL_PASSWORD"
    )
def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
class LeadData(BaseModel):
    name: str
    email: str
    interest: str
    message: str
class UserSignup(BaseModel):
    username: str
    email: str
    password: str
class ProgressUpdate(BaseModel):
    user_id: int
    trade: str
    is_correct: bool


@app.get("/get-challenge")
def get_challenge(trade: str = "Diesel", last_id: int = None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Primary randomized query with active exclusion filter
        query = """
            SELECT component, symptom, failure_mode, explanation, trade_type, id 
            FROM diagnostic_challenges 
            WHERE trade_type = %s
        """
        params = [trade]
        
        if last_id:
            query += " AND id != %s"
            params.append(last_id)
            
        query += " ORDER BY RANDOM() LIMIT 1;"
        
        cur.execute(query, tuple(params))
        row = cur.fetchone()

        # 2. Safety Valve: If pool is empty, strip exclusion criteria and fetch any valid sector row
        if not row and last_id:
            fallback_query = """
                SELECT component, symptom, failure_mode, explanation, trade_type, id 
                FROM diagnostic_challenges 
                WHERE trade_type = %s 
                ORDER BY RANDOM() LIMIT 1;
            """
            cur.execute(fallback_query, (trade,))
            row = cur.fetchone()
        
        # 3. CRITICAL: Only close database access streams AFTER all potential queries complete
        cur.close()
        conn.close()

        if row:
            # Process payload mechanics via diagnostic script engine layer
            processed = diagnostic.process_engine_data(row[:-1])
            processed["id"] = row[-1] 
            return processed
            
        return {"error": "No challenges found."}
    except Exception as e:
        # Emergency exception catching in case database streams lock up
        return {"error": str(e)}

@app.post("/register")
def register_user(user_data: UserSignup):
    # 1. Extract values from the model
    username = user_data.username
    email = user_data.email
    password = user_data.password

    # 2. Backend Password Validation (The Security Guard)
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Needs an uppercase letter")
    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Needs a number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Needs a special character")

    # 3. Hash the password
    hashed_pwd = get_password_hash(password)

    # 4. Save to Database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_pwd)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Technician profile created!"}
    except Exception as e:
        # This catches if the username or email already exists in PSQL
        return {"status": "error", "message": "Username or Email already taken"}



@app.post("/submit-interest")
def submit_interest(lead: LeadData):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO user_leads (full_name, email, interest_area, message) VALUES (%s, %s, %s, %s)",
            (lead.name, lead.email, lead.interest, lead.message)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Lead captured!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/update-progress")
def record_progress(data: ProgressUpdate):
    try:
        import progress_tracker
        progress_tracker.update_user_performance(data.user_id, data.trade, data.is_correct)
        return {"status": "success", "message": "Stats updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

if __name__ == "__main__":
    # This starts the server when you run 'python diagnostictest_api.py'
    uvicorn.run("diagnostictest_api:app", host="127.0.0.1", port=8000, reload=True)