import json
import os
import getpass
import sys
import pathlib
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class Login:

    def __init__(self, json_path):
        self.json_path = json_path
        self.data = {}
        self.load_or_create_config()

    def load_or_create_config(self):
        """
        Load the JSON configuration file if it exists,
        otherwise prompt user to create one.
        """
        if not os.path.exists(self.json_path):
            print(f"⚙️ Configuration file '{os.path.basename(self.json_path)}' not found. Creating a new one...")
            self.create_json(self.json_path)

        try:
            with open(self.json_path, "r") as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Error: Configuration file '{self.json_path}' is corrupted or not valid JSON.")
            sys.exit(1)

    @staticmethod
    def ask_yes_no(prompt):
        """
        Prompt user with a yes/no question and return True/False accordingly.
        """
        while True:
            answer = input(f"{prompt} [y/n]: ").strip().lower()
            if answer in ('y', 'yes'):
                return True
            elif answer in ('n', 'no'):
                return False
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")

    def create_json(self, json_path):
        """
        Prompt user for configuration details and save to a JSON file.
        """
        print("Please provide the following details to create your configuration:")

        url = input("Enter URL: ").strip()
        username_field = input("Enter username field CSS selector: ").strip()
        password_field = input("Enter password field CSS selector: ").strip()
        login_button = input("Enter login button CSS selector: ").strip()
        login_success_selector = input("Enter login success confirmation selector or text: ").strip()

        save_credentials = self.ask_yes_no(
            "Save username and password in plain text inside the JSON file?"
        )

        credentials = {"save": save_credentials}
        if save_credentials:
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            credentials.update({"username": username, "password": password})

        config = {
            "url": url,
            "selectors": {
                "username_field": username_field,
                "password_field": password_field,
                "login_button": login_button,
                "login_successfull": login_success_selector
            },
            "credentials": credentials
        }

        try:
            with open(json_path, "w") as f:
                json.dump(config, f, indent=4)
            print(f"✅ Configuration saved to '{json_path}'.")
        except IOError as e:
            print(f"❌ Failed to write configuration file: {e}")
            sys.exit(1)

    def get_credentials(self):
        """
        Return a tuple (username, password) either from config file
        or prompting user input if not saved.
        """
        creds = self.data.get("credentials", {})
        if creds.get("save", False):
            username = creds.get("username")
            password = creds.get("password")
            if username is None or password is None:
                print("❌ Error: Credentials marked as saved but missing from config.")
                sys.exit(1)
        else:
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
        return username, password

    def automate_login(self):
        """
        Perform the automated login using Playwright, handling exceptions.
        """
        username, password = self.get_credentials()

        print("\n🚀 Starting browser automation...")

        try:
            with sync_playwright() as p:
                browser = p.webkit.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                print(f"➡️ Navigating to {self.data['url']}...")
                page.goto(self.data["url"])
                page.wait_for_load_state("networkidle")

                print("🔑 Filling in login form...")
                page.fill(self.data["selectors"]["username_field"], username)
                page.fill(self.data["selectors"]["password_field"], password)
                page.click(self.data["selectors"]["login_button"])

                print("⏳ Waiting for login to process...")
                page.wait_for_timeout(5000)

                content = page.content().lower()
                success_indicator = self.data["selectors"]["login_successfull"].lower()

                if success_indicator in content:
                    print("✅ Login successful!")
                else:
                    print("❌ Login failed or login success indicator not found.")

                context.close()
                browser.close()

        except PlaywrightTimeoutError:
            print("❌ Timeout while waiting for page elements or navigation.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error occurred during browser automation: {e}")
            sys.exit(1)

    def start(self):
        """
        Entry point to start the login automation process.
        """
        try:
            self.automate_login()
        except KeyboardInterrupt:
            print("\n🚪 Process interrupted by user. Exiting.")
            sys.exit(0)

if __name__ == "__main__":
    # If running as a frozen executable, set PLAYWRIGHT_BROWSERS_PATH to bundled directory
    if getattr(sys, 'frozen', False):
        base_path = pathlib.Path(sys._MEIPASS)
        json_path = pathlib.Path(sys.executable).parent
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(base_path / "ms-playwright")
    else:
        json_path = pathlib.Path(__file__).parent
    json_path = json_path / "credentials.json"
    try:
        login = Login(str(json_path))
        login.start()
    except KeyboardInterrupt:
        print("\n👋 Keyboard interrupt received. Exiting cleanly.")
        sys.exit(0)

