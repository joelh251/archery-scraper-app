from PyQt6.QtWidgets import QWizardPage, QLabel, QVBoxLayout

def createIntroPage():

    page = QWizardPage()
    page.setTitle("Getting started")
    label = QLabel("Here, we'll learn how to use the archery scraper")
    label.setWordWrap(True)
    layout = QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page

def create2Page():

    page = QWizardPage()
    page.setTitle("Getting started")
    label = QLabel("Here, we'll learn how to use the archery scraper")
    label.setWordWrap(True)
    layout = QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page
