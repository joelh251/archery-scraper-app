from PyQt6.QtWidgets import QApplication, QWizard, QMessageBox
from gui.wizard_pages import *
import shutil
from utils.setup_r import run_setup
import sys

class Wizard(QWizard):
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self.shared = {
            "ianseo_urls" : None,
            "alt_ianseo_urls" : None,
            "scrape_tamlyn" : True,
            "save_dir" : None
        }

        self.setWindowTitle("Archery Scraper")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        self.addPage(IntroPage(self))
        self.addPage(IANSEOScraperPage(self))
        self.addPage(altIANSEOScraperPage(self))
        self.addPage(tamlynScraperPage(self))
        self.addPage(compilerDirectoryPage(self))
        self.addPage(ProgressPage(self))

    def closeEvent(self, event):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure?", 
                                            QMessageBox.StandardButton.Yes, 
                                            QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            shutil.rmtree("temp", ignore_errors=True)
            event.accept() 
        else:
            event.ignore()


VENV_SENTINEL = os.path.join(os.path.dirname(__file__), "venv", ".dependencies_installed")

def get_venv_paths():
    """Get venv Python and pip paths based on OS."""
    base = os.path.join(os.path.dirname(__file__), "venv")
    if sys.platform == "win32":
        return (
            os.path.join(base, "Scripts", "python.exe"),
            os.path.join(base, "Scripts", "pip.exe")
        )
    else:
        return (
            os.path.join(base, "bin", "python"),
            os.path.join(base, "bin", "pip")
        )


def install_dependencies(venv_pip):
    """Install dependencies only if not already installed."""
    if not os.path.exists(VENV_SENTINEL):
        print("Installing dependencies...")
        subprocess.run(
            [venv_pip, "install", "-r", "requirements.txt"],
            check=True
        )

        open(VENV_SENTINEL, "w").close()
        print("Dependencies installed!")
    else:
        print("Dependencies already installed, skipping.")


def ensure_venv():
    venv_python, venv_pip = get_venv_paths()

    if not os.path.exists(venv_python):
        print("ERROR: venv not found. Please run setup.py first.")
        sys.exit(1)

    install_dependencies(venv_pip)

    if sys.executable != os.path.abspath(venv_python):
        subprocess.run([venv_python] + sys.argv)
        sys.exit()


if __name__ == "__main__":
    ensure_venv()
    app = QApplication(sys.argv)
    run_setup()
    wizard = Wizard()
    wizard.show()
    sys.exit(app.exec())