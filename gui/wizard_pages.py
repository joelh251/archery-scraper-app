from PyQt6.QtWidgets import QWizardPage, QLabel, QVBoxLayout, QMessageBox
from widgets import *


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)
        self.setTitle("Getting started")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class IANSEOScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(IANSEOScraperPage, self).__init__(parent)
        self.setTitle("Scraping IANSEO")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.textbox = linkInputBox()
        layout.addWidget(self.textbox)
        self.file_browser = fileBrowser()
        layout.addWidget(self.file_browser)
        self.setLayout(layout)
    
    def validatePage(self):
        self.file = self.file_browser.textbox.text()
        self.links = [line.strip() for line in self.textbox.textbox.toPlainText().split('\n') if line.strip()]
        print(self.links)
        if not self.file and not self.links:
            scrapeIanseo = False
            QMessageBox.warning(self, "Skipping Standard IANSEO", "No urls of file provided, skipping standard IANSEO scraping.")
            
            return True
        
        elif self.file and self.links:
            QMessageBox.warning(self, "Invalid input", "Only input urls or a file, not both.")

            return False
        
        else:
            return True


class altIANSEOScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(altIANSEOScraperPage, self).__init__(parent)
        self.setTitle("Alternative Scraping IANSEO")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.textbox = linkInputBox()
        layout.addWidget(self.textbox)
        self.file_browser = fileBrowser()
        layout.addWidget(self.file_browser)
        self.setLayout(layout)

    def validatePage(self):
        self.file = self.file_browser.textbox.text()
        self.links = [line.strip() for line in self.textbox.textbox.toPlainText().split('\n') if line.strip()]
        print(self.links)
        if not self.file and not self.links:
            scrapeIanseo = False
            QMessageBox.warning(self, "Skipping Standard IANSEO", "No urls of file provided, skipping standard IANSEO scraping.")
            
            return True
        
        elif self.file and self.links:
            QMessageBox.warning(self, "Invalid input", "Only input urls or a file, not both.")

            return False
        
        else:
            return True


class tamlynScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(tamlynScraperPage, self).__init__(parent)
        self.setTitle("Scraping TamlynScore")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class compilerDirectoryPage(QWizardPage):
    def __init__(self, parent=None):
        super(compilerDirectoryPage, self).__init__(parent)
        self.setTitle("Choose where to save results")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.directory_browser = directoryBrowser()
        layout.addWidget(self.directory_browser)
        self.setLayout(layout)


class ProgressPage(QWizardPage):
    def __init__(self, parent=None):
        super(ProgressPage, self).__init__(parent)
        self.setTitle("Scraper Progress")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.directory_browser = directoryBrowser()
        layout.addWidget(self.directory_browser)
        self.setLayout(layout)