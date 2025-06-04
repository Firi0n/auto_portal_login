# 🔐 Headless Auto Login Script

A minimal Python script using [Playwright](https://playwright.dev/python/) to automate login via headless browser
(WebKit) to any website that uses a standard username/password form.

---

## 📁 Repository contents

- `login.py` – Main script that performs the automated login.
- `build.py` – Build script to create standalone executables with PyInstaller.
- `requirements.txt` – Python dependencies.
- `.github/workflows/release.yml` – GitHub Actions workflow for multi-OS release automation.
- `README.md` – Project documentation (this file).

---

## ⚙️ Requirements

- **Python 3.10 or higher** installed on your system.
- **Internet connection** (required once to download Playwright browser binaries).
- Optional but **recommended**: Use a Python virtual environment (`venv`) to isolate dependencies and avoid version conflicts.
- Playwright version **1.44 or higher**.

---

## 🛠️ Installation

1. (Optional) Create and activate a virtual environment to isolate dependencies:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (WebKit):

```bash
playwright install webkit
```

> Note: The build script (`build.py`) also automates this step, downloading and bundling Playwright browsers in a custom folder `.playwright-browsers`.

---

## 🧱 Building a Standalone Executable

You can build a single executable file for your platform using the included `build.py` script. It will:

- Create and/or reuse a virtual environment.
- Install necessary Python packages (PyInstaller and Playwright).
- Download Playwright browser binaries into `.playwright-browsers`.
- Package the `login.py` script into a standalone executable using PyInstaller.
- Clean previous build artifacts when needed.

### Usage

- Build the project:

```bash
python build.py
```

- Clean previous build artifacts:

```bash
python build.py clean
```

The built executable will be located in the `dist/` directory.

---

## ▶️ Running the Login Automation

Run the login automation script directly:

```bash
python login.py
```

Or, run the standalone executable if you built it.

---

## ⚙️ Configuration JSON

The script uses a JSON file (`credentials.json` by default) to store configuration and optionally credentials.

If the file does not exist, you will be prompted to create it with:

- Target login URL
- CSS selectors for username field, password field, login button, and login success confirmation
- Optionally save your username and password in plaintext inside the JSON file

### Example configuration structure

```json
{
	"url": "https://example.com/login",
	"selectors": {
		"username_field": "#username",
		"password_field": "#password",
		"login_button": "#login-btn",
		"login_successfull": "Welcome"
	},
	"credentials": {
		"save": true,
		"username": "your_username",
		"password": "your_password"
	}
}
```

- Credentials saved in plaintext — **make sure to secure your system and files**.
- If you choose not to save credentials, the script will prompt for username and password each time it runs.

---

## 🔐 Security Considerations

- Credentials stored **unencrypted** locally in JSON if you opt to save them.
- Automated login uses a clean browser context with no cached data or cookies.
- Use this tool responsibly and secure your credential files properly.
- Avoid hardcoding sensitive data directly in code or repository.

---

## 🧪 Tested On

- Playwright WebKit browser (headless mode)
- Windows, Linux, and macOS (via GitHub Actions build workflow)

---

## 🚀 GitHub Actions Workflow

This project includes a GitHub Actions workflow `.github/workflows/release.yml` that:

- Builds standalone executables for Windows, Linux, and macOS when a git tag matching `v*.*.*` is pushed.
- Allows manual workflow dispatch with a tag name input.
- Renames build artifacts to include OS suffix.
- Creates a GitHub release with the built executables attached.

---

## ⚖️ Legal Disclaimer

This project is provided **as-is**, for **educational and demonstrative purposes only**.

By using this software, you agree that:

- You are solely responsible for how you use this code.
- The author is not liable for any damage, loss, or account issues caused by usage.
- This project is not affiliated with or endorsed by any third-party service or platform.
- You comply with the terms of service of any platform you automate with this tool.
- You secure any sensitive information stored locally.

If you do not agree with these terms, do not use this software.

---

## 📝 License

MIT License — free to use, modify, and distribute.

Please avoid sharing sensitive credentials or URLs publicly.
