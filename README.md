# 🔐 Headless Auto Login Script

A minimal Python script using [Playwright](https://playwright.dev/python/) to automate login via headless browser
(Chromium) to any website that uses a standard username/password form.

---

## 📁 Repository contents

-   `login.py` – Main script that performs the automated login
-   `requirements.txt` – Python dependencies
-   `.github/workflows/release.yml` – GitHub Actions workflow for release automation
-   `README.md` – This file

---

## ⚙️ Requirements

-   **Python 3.10 or higher** installed on your system
-   **Internet connection** (required once to download Playwright browser binaries)
-   Optional but **recommended**: Use a Python virtual environment (`venv`) to isolate dependencies and avoid version
    conflicts

---

## 🛠️ Installation

1. (Optional) Create and activate a virtual environment to keep dependencies isolated:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

2. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (Chromium):

```bash
playwright install
```

> This will install all dependencies and download a clean instance of Chromium for automated, isolated usage.

---

## ▶️ Usage

```bash
python login.py
```

-   If no config file is found, the script will:

    -   Prompt you to enter:
        -   The target login URL
        -   Selectors for username, password, and login button
    -   Optionally ask if you'd like to save the credentials in **plain text** within the JSON file (locally only).

-   On next runs, the script will reuse this configuration.

---

## 📄 Configuration JSON

The script uses a JSON file to store configuration data and optionally credentials. This file is created automatically
if not found.

### JSON Structure

```json
{
	"url": "https://example.com/login",
	"selectors": {
		"username_field": "#username",
		"password_field": "#password",
		"login_button": "#login-btn"
	},
	"credentials": {
		"save": true,
		"username": "your_username",
		"password": "your_password"
	}
}
```

-   `url`: The login page URL.
-   `selectors`: CSS selectors for the username input, password input, and login button.
-   `credentials.save`: Boolean indicating whether to save credentials.
-   `credentials.username` and `credentials.password`: Stored only if `save` is true.  
    **Credentials are saved in plaintext locally — ensure your system’s security.**

### Notes

-   If `credentials.save` is `false`, the script will prompt for username and password each run.
-   This design keeps the tool generic and user-configurable for any login page.

---

## 🔐 Security

-   If saved, **credentials are stored unencrypted** in a local JSON file.
-   This behavior is clearly prompted before saving.
-   Login is performed using a **clean browser context** (no cache, cookies, or saved data).

---

## ⚖️ Legal Disclaimer

This project is provided **as-is**, for **educational and demonstrative purposes only**.

By using this software, you agree to the following:

-   You are **fully and solely responsible** for how you use this code.
-   The author **does not assume any responsibility** for any direct or indirect damage, loss of data, account
    suspension, or other consequences resulting from the use or misuse of this code.
-   This project is **not affiliated with, endorsed by, or officially connected** to any third-party service, platform,
    or institution, including those potentially configured through the external JSON file.
-   Any website, URL, or selector used by this script is **externalized and user-defined**, making this tool **generic
    and not tied to any specific platform**.
-   If you choose to store your login credentials, they are saved in a local **plaintext JSON file**. It is your
    responsibility to ensure the security of your system and files.

### You are solely responsible for:

-   Complying with the Terms of Service and acceptable use policies of any service you use this tool with.
-   Securing any sensitive data and avoiding credential leakage.
-   Not using this tool in any way that violates laws or regulations in your country or jurisdiction.

> **If you do not agree with these terms, do not use this software.**

## 🧪 Tested On

-   Chromium (via Playwright)
-   Windows / Linux

---

## 📦 GitHub Actions

The included GitHub workflow builds and publishes releases automatically when a new version is pushed with a Git tag.

---

## 📝 License

MIT – you're free to use, modify, and distribute this script.  
Please avoid hardcoding or distributing sensitive URLs or login data publicly.
