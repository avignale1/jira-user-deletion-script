import csv
import requests
import time
import json

#This code:
# Reads emails from a CSV file.
# Extracts the username (everything before @) from each email.
# Calls the Jira API to:
# Search for users based on that username.
# Fetch detailed info on each matched user (account_id) from a second org (via get_user_details).
# Prints user details to the console.
# Sleeps between requests to avoid API rate limiting.

#User deletion is irreversible so I have commented out the delete user portion
#To make it delete users, paste the below code into main function where user details are getting printed (if user_details: print(user_details)

# if user_details:
#         delete_user(account_id)



# Constants
CSV_FILE_PATH =   # Path to your CSV file
ORG_ID = ''  # Replace with your actual org ID
ORG_ID_2 = ''  # Replace with your actual second org ID
API_TOKEN = ''  # Replace with your actual API token
SEARCH_API_URL = f'https://api.atlassian.com/admin/v1/orgs/{ORG_ID}/users/search'
DETAILS_API_URL_TEMPLATE = f'https://api.atlassian.com/admin/v1/orgs/{ORG_ID_2}/directory/users/{{}}'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

def extract_username(email):
    """Extract the username from an email address."""
    return email.split('@')[0]

def read_emails_from_csv(file_path):
    """Read emails from a CSV file."""
    emails = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            emails.append(row[0])  # Adjust index if the email is not in the first column
    return emails

def search_user(username):
    """Search for a user by username."""
    params = {
        'query': username
    }
    response = requests.get(SEARCH_API_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to search user {username}: {response.status_code} {response.text}")
        return None

def get_user_details(account_id):
    """Get user details by account ID."""
    url = DETAILS_API_URL_TEMPLATE.format(account_id)
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get details for account ID {account_id}: {response.status_code} {response.text}")
        return None

def delete_user(account_id):
    """Delete a user by account ID."""
    url = f'https://api.atlassian.com/admin/v1/orgs/{ORG_ID_2}/directory/users/{account_id}'
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f" Successfully deleted user with account ID {account_id}")
    else:
        print(f" Failed to delete user {account_id}: {response.status_code} {response.text}")


def main():
    emails = read_emails_from_csv(CSV_FILE_PATH)
    for email in emails:
        username = extract_username(email)
        search_results = search_user(username)
        if search_results and 'values' in search_results:
            for user in search_results['values']:
                account_id = user.get('account_id')
                if account_id:
                    user_details = get_user_details(account_id)

                     #replace these 2 lines with deletion code 
                    if user_details:
                        print(user_details) 
                       

                time.sleep(1)  # To avoid hitting the rate limit
        time.sleep(1)  # To avoid hitting the rate limit

if __name__ == "__main__":
    main()
