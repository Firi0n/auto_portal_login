import json
import os
import getpass
import time
from playwright.sync_api import sync_playwright

class Login:

    # Prompt the user for a yes/no answer, returning a boolean
    @staticmethod
    def ask_yes_no(prompt):
        while True:
            answer = input(f"{prompt} [y/n]: ").strip().lower()
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")

    # Create the JSON config file if it doesn't exist
    def create_json(self, json_filename):
        url = input("Enter url: ")
        username_field = input("Enter username field selector: ")
        password_field = input("Enter password field selector: ")
        login_button = input("Enter login button selector: ")
        save_username_password = self.ask_yes_no(
            "Save username and password in plain text (visible) inside the JSON file?"
        )

        # Build configuration structure
        json_structure = {
            "url": url,
            "selectors": {
                "username_field": username_field,
                "password_field": password_field,
                "login_button": login_button
            },
            "credentials": {
                "save": save_username_password
            }
        }

        # If user wants to save credentials, collect them
        if save_username_password:
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            json_structure["credentials"]["username"] = username
            json_structure["credentials"]["password"] = password

        # Save configuration to file
        with open(json_filename, "w") as f:
            json.dump(json_structure, f, indent=4)

    # Initialize: create or load the JSON config
    def __init__(self, json_filename):
        if not os.path.exists(json_filename):
            self.create_json(json_filename)
        with open(json_filename, "r") as f:
            self.data = json.load(f)

    # Main automation logic
    def start(self):
        # Get credentials (from file or user input)
        if self.data["credentials"]["save"]:
            username = self.data["credentials"]["username"]
            password = self.data["credentials"]["password"]
        else:
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")

        with sync_playwright() as p:
            # Launch browser in headless mode (no GUI)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()  # Fresh session with no cache or cookies
            page = context.new_page()
            page.goto(self.data["url"])

            # Wait for page load to complete
            page.wait_for_load_state("networkidle")

            # Fill in login form and submit
            page.fill(self.data["selectors"]["username_field"], username)
            page.fill(self.data["selectors"]["password_field"], password)
            page.click(self.data["selectors"]["login_button"])

            # Wait a few seconds after submitting
            page.wait_for_timeout(5000)

            # Simple success check based on presence of "logout" in page content
            page_content = page.content().lower()
            if "logout" in page_content:
                print("✅ Login successful!")
            else:
                print("❌ Login failed or not recognized.")

            # Clean up browser context
            context.close()
            browser.close()


# Entry point
if __name__ == "__main__":
    login = Login("credentials.json")
    login.start()
