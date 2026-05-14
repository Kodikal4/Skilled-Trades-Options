import psycopg2

def update_user_progress(user_id, trade, is_correct):
    conn = psycopg2.connect(database="diesel_startup", user="postgres", password="YOUR_PASSWORD")
    cur = conn.cursor()

    # Check if a record exists for this user/trade combo
    cur.execute("SELECT id FROM user_stats WHERE user_id = %s AND trade_type = %s", (user_id, trade))
    record = cur.fetchone()

    if record:
        # Update existing stats
        sql = """
            UPDATE user_stats 
            SET total_attempts = total_attempts + 1,
                correct_count = correct_count + %s,
                last_activity = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cur.execute(sql, (1 if is_correct else 0, record[0]))
    else:
        # Create new record for this trade
        sql = """
            INSERT INTO user_stats (user_id, trade_type, correct_count, total_attempts)
            VALUES (%s, %s, %s, 1)
        """
        cur.execute(sql, (user_id, trade, 1 if is_correct else 0))

    conn.commit()
    cur.close()
    conn.close()