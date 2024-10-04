import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from jira import JIRA

# PostgreSQL connection details
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'streamlit'
DB_USER = 'postgres'
DB_PASSWORD = 'root'

# JIRA configuration
jira_options = {'server': 'https://intelizign.atlassian.net'}
username = 'vigneshwaran.n@intelizign.com'
api_token = 'ATATT3xFfGF0bDmcrG0ZYOb5HsJ8nbnGVg1YnUl3MbQ0teGM_YPr4N0NI3Km6AJHmcvVjBFck9KVkuZpr0oWhbgkR4DoI5zZa8_eW4KI7FQtHDoMja_-GB3Px5THHk0uaLFqJZp5QVxBdAfWrArI5e-PQZUospOCwxW07yuAUR4nn6OM38OcwS8=1AF3DAB9'  # Replace with your actual API token

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

# Function to get available issue types
def get_available_issue_types():
    try:
        jira = JIRA(options=jira_options, basic_auth=(username, api_token))
        issue_types = jira.issue_types()
        return {issue_type.name: issue_type.id for issue_type in issue_types}
    except Exception as e:
        st.error(f"Failed to fetch issue types: {e}")
        return {}

# Function to create a JIRA ticket
def create_jira_ticket(transaction_id, error_msg, timestamp):
    try:
        jira = JIRA(options=jira_options, basic_auth=(username, api_token))
        issue_types = get_available_issue_types()  # Fetch available issue types
        
        # Specify the issue type name
        issue_type_name = 'Bug'  
        if issue_type_name not in issue_types:
            st.error("Specified issue type does not exist in JIRA.")
            return
        
        new_issue_dict = {
            'project': {'key': 'KAN'},
            'summary': f"High Severity Error: {transaction_id}",
            'description': f"Error Message: {error_msg}\nTimestamp: {timestamp}",
            'issuetype': {'id': issue_types[issue_type_name]},  # Use ID for issue type
        }
        new_issue = jira.create_issue(fields=new_issue_dict)
        st.success(f"Ticket created: {new_issue.key}")
    except Exception as e:
        st.error(f"Failed to create JIRA ticket: {e}")

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

    # Create JIRA tickets for each new error log
    for log in new_error_logs:
        create_jira_ticket(log['transaction_id'], log['error_msg'], log['data_inserted_timestamp'])

    # Update the last check time to the latest log entry's timestamp
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
        st.error(f"**Transaction ID**: {log['transaction_id']} - **Message**: {log['error_msg']} - **Timestamp**: {log['data_inserted_timestamp']}")
        st.write("---")
    
    # After viewing, clear the new error logs and reset the error count
    st.session_state['new_error_logs'].clear()
    st.session_state['new_error_count'] = 0
