from PyQt6.QtWidgets import QApplication, QMainWindow, QWizard
from wizard_pages import createIntroPage, create2Page


app = QApplication([])

wizard = QWizard()
wizard.addPage(createIntroPage())
wizard.addPage(create2Page())

wizard.setWindowTitle("Wizard")
wizard.setWizardStyle(QWizard.WizardStyle.ModernStyle)
wizard.show()

app.exec()