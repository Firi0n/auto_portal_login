import os
import sys
import subprocess
import shutil
from pathlib import Path

class Build:

    @staticmethod
    def run_cmd(cmd, **kwargs):
        """
        Execute a shell command and ensure it completes successfully.
        If the command fails, print an error message and terminate the script.

        Args:
            cmd (list): List of command arguments to execute.
            **kwargs: Additional keyword arguments passed to subprocess.run.
        """
        print(f"\n>>> Running command:\n    {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, **kwargs)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ ERROR: Command failed with exit code {e.returncode}")
            sys.exit(e.returncode)

    @staticmethod
    def get_playwright_browsers_path():
        """
        Determine the filesystem path where Playwright browser binaries are installed.

        In this version, we use a custom path (.playwright-browsers) to ensure consistency across systems.

        Returns:
            str or None: The absolute path if it exists, otherwise None.
        """
        path = os.path.abspath(".playwright-browsers")
        if os.path.exists(path):
            return path
        return None

    def __init__(self, venv_dir="venv", app_name="LoginApp", app_script="login.py", ico="icon"):
        """
        Initialize the build configuration and environment.

        Args:
            venv_dir (str): Directory name/path for the virtual environment.
            app_name (str): Desired name of the packaged executable.
            app_script (str): Main Python script to package.
            ico (str): Path to an optional icon file for the executable.
        """
        self.app_name = app_name
        self.app_script = app_script
        self.ico = ico

        # Detect operating system platform and set flags accordingly
        self.platform = sys.platform
        self.is_win = self.platform.startswith("win")
        print(f"🌐 Detected platform: {self.platform}")

        # Define virtual environment directory
        self.venv_dir = venv_dir

        # Compute paths to Python and pip executables inside the virtual environment
        self.python_exe, self.pip_exe = self.get_python_pip_paths()

        # Set custom path for Playwright browsers
        self.playwright_browsers_path = os.path.abspath(".playwright-browsers")

    def get_python_pip_paths(self):
        """
        Construct the paths for Python and pip executables inside the virtual environment,
        adapting to platform-specific folder structure and executable suffix.

        Returns:
            tuple: (python_executable_path, pip_executable_path)
        """
        path_dir = "Scripts" if self.is_win else "bin"
        exe_suffix = ".exe" if self.is_win else ""
        python_path = os.path.join(self.venv_dir, path_dir, f"python{exe_suffix}")
        pip_path = os.path.join(self.venv_dir, path_dir, f"pip{exe_suffix}")
        return python_path, pip_path

    def clean(self):
        """
        Remove previously generated build artifacts to ensure a clean build environment.
        Specifically removes 'dist' and 'build' folders, as well as the PyInstaller spec file.
        """
        print("\n🧹 Cleaning previous build artifacts if any...")
        for folder in ("dist", "build", self.playwright_browsers_path):
            if os.path.exists(folder):
                print(f"    - Removing folder: {folder}")
                shutil.rmtree(folder)

        spec_file = self.app_name + ".spec"
        if os.path.exists(spec_file):
            print(f"    - Removing spec file: {spec_file}")
            os.remove(spec_file)

    def create_venv(self):
        """
        Create a Python virtual environment if it does not already exist.
        This isolates dependencies for the build process.
        """
        if not os.path.exists(self.venv_dir):
            print(f"\n🛠 Creating virtual environment in '{self.venv_dir}'...")
            self.run_cmd([sys.executable, "-m", "venv", self.venv_dir])
        else:
            print(f"\n✔ Virtual environment already exists at '{self.venv_dir}'.")

    def build_project(self):
        """
        Execute the complete build workflow:
        1. Ensure virtual environment exists
        2. Upgrade pip inside the venv
        3. Install necessary packages (PyInstaller and Playwright)
        4. Install Playwright browser binaries (webkit)
        5. Clean previous build outputs
        6. Package the application with PyInstaller using optimized options
        """
        self.create_venv()

        print("\n⬆️ Upgrading pip to the latest version...")
        self.run_cmd([self.python_exe, "-m", "pip", "install", "--upgrade", "pip"])

        print("\n📦 Installing required packages: pyinstaller and playwright...")
        self.run_cmd([self.pip_exe, "install", "pyinstaller", "playwright"])

        print("\n🌐 Installing Playwright browser binaries (webkit)...")
        env = os.environ.copy()
        env["PLAYWRIGHT_BROWSERS_PATH"] = self.playwright_browsers_path
        self.run_cmd([self.python_exe, "-m", "playwright", "install", "webkit"], env=env)

        # Get path to Playwright browsers folder to bundle with the app
        playwright_browsers_path = self.get_playwright_browsers_path()
        if playwright_browsers_path is None:
            print("\n❌ ERROR: Playwright browsers folder not found! Please ensure Playwright is installed properly.")
            sys.exit(1)

        # Determine correct separator for the --add-data flag based on platform
        separator = ";" if self.is_win else ":"
        add_data_option = f"{playwright_browsers_path}{separator}ms-playwright"

        print(f"\n📦 Packaging application '{self.app_name}' with PyInstaller...")

        # Construct PyInstaller command with necessary options and exclusions
        pyinstaller_cmd = [
            self.python_exe,
            "-m",
            "PyInstaller",
            "--onefile",                # Create a single executable file
            "--add-data",              # Include Playwright browsers folder inside the executable
            add_data_option,
            "--exclude-module", "tkinter",   # Exclude unused modules to reduce executable size
            "--exclude-module", "test",
            "--exclude-module", "unittest",
            "--exclude-module", "pydoc",
            "--exclude-module", "email",
            "--exclude-module", "http",
            "--name", self.app_name,    # Name of the output executable
        ]

        # Add icon parameter only if an icon path is specified
        if self.ico:
            ext = ".svg"
            if self.is_win:
                ext = ".ico"
            pyinstaller_cmd.extend(["--icon", self.ico+ext])

        # Append the main application script at the end
        pyinstaller_cmd.append(self.app_script)

        print(f"\n🚀 Running PyInstaller with the following command:\n    {' '.join(pyinstaller_cmd)}\n")
        self.run_cmd(pyinstaller_cmd)

        print("\n✅ Build finished successfully! Your executable is available in the 'dist' directory.\n")


def main():
    """
    Parse command line arguments and either clean previous builds or execute build process.
    """
    build = Build(venv_dir = "venv", ico = str(Path("icons") / "icon"))
    if len(sys.argv) > 1 and sys.argv[1].lower() == "clean":
        build.clean()
    else:
        build.build_project()


if __name__ == "__main__":
    main()
