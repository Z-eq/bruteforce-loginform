import requests
from bs4 import BeautifulSoup
import urllib3
import logging
from urllib.parse import urljoin  # For handling relative URLs

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# Replace with the actual login URL and hardcoded credentials
login_url = "https://yourwebsitehere"  # Actual test URL
credentials = [('admin', 'admin123')]  # Example credentials

def find_login_form(html):
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form')
    if form:
        logger.info("Form found.")
        inputs = form.find_all('input')
        fields = {}
        
        # Get the action attribute from the form
        form_action = form.get('action')
        
        # Handle relative URLs
        if form_action:
            form_action = urljoin(login_url, form_action)

        for input_tag in inputs:
            field_name = input_tag.get('name')
            if field_name:
                if 'user' in field_name.lower():
                    fields['username_field'] = field_name
                elif 'pass' in field_name.lower():
                    fields['password_field'] = field_name

        if fields:
            logger.info(f"Login form detected: {fields} with action: {form_action}")
            return fields, form_action  # Return fields and action
    return None, None

def login(url, username, password, username_field, password_field):
    response = requests.post(url, data={username_field: username, password_field: password}, verify=False)
    return response

def run_automatic_login():
    logger.info("Running automatic login with hardcoded credentials...")
    try:
        response = requests.get(login_url, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info("Page loaded with status code: 200")
        login_form, form_action = find_login_form(response.text)
        
        if login_form:
            username_field = login_form.get('username_field')
            password_field = login_form.get('password_field')

            # Attempt login with each set of credentials
            for username, password in credentials:
                logger.info(f"Attempting login with {username}:{password}")
                response = login(form_action, username, password, username_field, password_field)  # Use the form action URL
                if "Login" in response.text:
                    logger.info(f"Login successful with {username}:{password}")
                else:
                    logger.info(f"Login failed with {username}:{password}")

            # Generate Hydra command
            hydra_command = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {form_action} form={username_field}:{password_field}"
            print("Hydra command to run:")
            print(hydra_command)  # Directly print the command for easy copying
    except requests.exceptions.RequestException:
        logger.error("The website you entered is probably wrong or not reachable.")

def manual_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    logger.info(f"Attempting manual login with {username}:{password}")
    
    try:
        # Find the login form to get the action URL again
        response = requests.get(login_url, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info("Page loaded with status code: 200")
        login_form, form_action = find_login_form(response.text)
        
        if login_form:
            username_field = login_form.get('username_field')
            password_field = login_form.get('password_field')
            response = login(form_action, username, password, username_field, password_field)  # Use the form action URL
            if "Login" in response.text:
                logger.info(f"Login successful with {username}:{password}")
            else:
                logger.info(f"Login failed with {username}:{password}")
    except requests.exceptions.RequestException:
        logger.error("The website you entered is probably wrong or not reachable for manual login.")

def main():
    print("Select an option:")
    print("1. Automatic login with hardcoded credentials")
    print("2. Manual login")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        run_automatic_login()
    elif choice == '2':
        manual_login()
    else:
        print("Invalid choice. Exiting.")

# Directly call the main function
main()
