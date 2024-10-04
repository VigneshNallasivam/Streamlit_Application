import streamlit as st
from jira import JIRA

# JIRA configuration
jira_options = {'server': 'https://intelizign.atlassian.net'}

# Directly include your credentials (not recommended for security reasons)
username = 'vigneshwaran.n@intelizign.com'
api_token = 'ATATT3xFfGF0bDmcrG0ZYOb5HsJ8nbnGVg1YnUl3MbQ0teGM_YPr4N0NI3Km6AJHmcvVjBFck9KVkuZpr0oWhbgkR4DoI5zZa8_eW4KI7FQtHDoMja_-GB3Px5THHk0uaLFqJZp5QVxBdAfWrArI5e-PQZUospOCwxW07yuAUR4nn6OM38OcwS8=1AF3DAB9'  # Replace with your actual API token

def jira_func():
    try:
        jira = JIRA(options=jira_options, basic_auth=(username, api_token))
        
        # Add a form to create a new JIRA ticket
        st.header("Create a New JIRA Ticket")
        with st.form(key='create_ticket_form'):
            summary = st.text_input('Summary', '')
            description = st.text_area('Description', '')
            issue_type = st.selectbox('Issue Type', [issue_type.name for issue_type in jira.issue_types()])
            submit_button = st.form_submit_button(label='Create Ticket')

            if submit_button:
                new_issue_dict = {
                    'project': {'key': 'KAN'},
                    'summary': summary,
                    'description': description,
                    'issuetype': {'name': issue_type},
                }
                new_issue = jira.create_issue(fields=new_issue_dict)
                st.success(f"Ticket created: {new_issue.key}")


        # Fetch issues from a project
        issues = jira.search_issues('project=KAN')

        # Display issues in Streamlit
        st.title('Jira Issues')
        for issue in issues:
            st.write(f"{issue.key}: {issue.fields.summary}")

        # Filter issues by status
        status = st.selectbox('Select Status', ['To Do', 'In Progress', 'Done'])
        filtered_issues = [issue for issue in issues if issue.fields.status.name == status]

        st.write(f"Issues with status {status}:")
        for issue in filtered_issues:
            st.write(f"{issue.key}: {issue.fields.summary}")
            
            
            
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    jira_func()
