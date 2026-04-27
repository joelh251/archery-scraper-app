from PyQt6.QtWidgets import QApplication, QWizard, QMessageBox
from gui.wizard_pages import *
import shutil

class Wizard(QWizard):
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self.shared = {
            "ianseo_urls" : None,
            "alt_ianseo_urls" : None,
            "scrape_tamlyn" : True,
            "save_directory" : None
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

app = QApplication([])
wizard = Wizard()
wizard.show()
app.exec()