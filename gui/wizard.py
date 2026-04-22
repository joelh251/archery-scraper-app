from PyQt6.QtWidgets import QApplication, QWizard, QMessageBox
from wizard_pages import *

class Wizard(QWizard):
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self.setWindowTitle("Archery Scraper")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.addPage(IntroPage(self))
        self.addPage(IANSEOScraperPage(self))
        self.addPage(altIANSEOScraperPage(self))
        self.addPage(tamlynScraperPage(self))
        self.addPage(compilerDirectoryPage(self))

    def closeEvent(self, event):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure?", 
                                            QMessageBox.StandardButton.Yes, 
                                            QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            # TODO: empty temporary files
            event.accept() 
        else:
            event.ignore()

app = QApplication([])
wizard = Wizard()
wizard.show()
app.exec()