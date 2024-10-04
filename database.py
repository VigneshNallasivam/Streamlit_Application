import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# PostgreSQL connection details
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'streamlit'
DB_USER = 'postgres'
DB_PASSWORD = 'root'

# Function to connect to the PostgreSQL database
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        return None

# Function to fetch only the new error logs since the last check time
def fetch_new_error_logs(last_check_time):
    query = """
    SELECT *
    FROM log_table 
    WHERE severity_desc = 'High' AND data_inserted_timestamp > %s
    ORDER BY data_inserted_timestamp DESC
    """
    conn = get_connection()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (last_check_time,))
                new_error_logs = cur.fetchall()
                st.write("Fetched Error Logs:", new_error_logs)  # Debug output
            return new_error_logs
        except Exception as e:
            st.error(f"Error fetching logs: {e}")
        finally:
            conn.close()
    return []

# Streamlit UI
st.title("Real-time PostgreSQL Error Notifications")

# Initialize session state variables
if 'last_check_time' not in st.session_state:
    st.session_state['last_check_time'] = datetime(2024, 1, 1)  # Set a date in the past for testing

if 'new_error_logs' not in st.session_state:
    st.session_state['new_error_logs'] = []

if 'new_error_count' not in st.session_state:
    st.session_state['new_error_count'] = 0

# Fetch new error logs
new_error_logs = fetch_new_error_logs(st.session_state['last_check_time'])

if new_error_logs:
    # Append new error logs and update the error count
    st.session_state['new_error_logs'].extend(new_error_logs)
    st.session_state['new_error_count'] += len(new_error_logs)

    # Update the last check time to the latest log entry's timestamp
    # Ensure you are using the correct key based on your database
    st.session_state['last_check_time'] = new_error_logs[0]['data_inserted_timestamp']

# Debugging output for notification count
st.write("New Error Count:", st.session_state['new_error_count'])

# Notification Bell in the sidebar with error count
with st.sidebar:
    notification_count = st.session_state['new_error_count']
    bell_icon = st.button(f"🔔 {notification_count} notification" if notification_count > 0 else "🔔 notification")

# Show new error details when the bell is clicked
if bell_icon and st.session_state['new_error_logs']:
    st.write("### New Error Notifications") 
    for log in st.session_state['new_error_logs']:
        # Ensure you use the correct keys based on your database schema
        st.error(f"**Transaction ID**: {log['transaction_id']} - **Message**: {log['error_msg']} - **Timestamp**: {log['data_inserted_timestamp']}")
        st.write("---")
    
    # After viewing, clear the new error logs and reset the error count
    st.session_state['new_error_logs'].clear()
    st.session_state['new_error_count'] = 0
