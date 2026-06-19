from PyQt6.QtWidgets import QWizardPage, QLabel, QVBoxLayout, QMessageBox, QCheckBox
import pandas as pd
from gui.widgets import *
from utils.ianseo_scraper import IanseoScraper
from utils.alt_ianseo_scraper import AltIanseoScraper
from utils.tamlyn_scraper import TamlynScraper
from utils.compilers import *
import sys


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)
        # Set page text
        self.setTitle("Getting started")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class IANSEOScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(IANSEOScraperPage, self).__init__(parent)
        # Set text of page
        self.setTitle("Scraping IANSEO")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Add file browser
        self.textbox = linkInputBox()
        layout.addWidget(self.textbox)
        self.file_browser = fileBrowser()
        layout.addWidget(self.file_browser)

        self.setLayout(layout)
    
    def validatePage(self):
        self.filepath = self.file_browser.textbox.text()
        self.links = [line.strip() for line in self.textbox.textbox.toPlainText().split('\n') if line.strip()]
        if not self.filepath and not self.links:
            QMessageBox.warning(self, "Skipping Standard IANSEO", "No urls of file provided, skipping standard IANSEO scraping.")
            self.wizard().shared["ianseo_urls"] = None
            return True
        
        elif self.filepath and self.links:
            QMessageBox.warning(self, "Invalid input", "Only input urls or a file, not both.")

            return False
        
        elif self.filepath and not self.links:
            if self.filepath.endswith(".xlsx"):
                self.wizard().shared["ianseo_urls"] = pd.read_excel(self.filepath, header=None).iloc[:, 0].tolist()
            elif self.filepath.endswith(".csv"):
                self.wizard().shared["ianseo_urls"] = pd.read_csv(self.filepath, header=None).iloc[:, 0].tolist()
            else:
                QMessageBox.warning(self, "Invalid Filepath", "File extension must be .csv or .xlsx")
            return True
        
        elif not self.filepath and self.links:
            self.wizard().shared["ianseo_urls"] = self.links
    
            return True


class altIANSEOScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(altIANSEOScraperPage, self).__init__(parent)
        # Add text to page
        self.setTitle("Alternative Scraping IANSEO")
        label = QLabel("Here, we'll learn how to use the archery scraper")
        label.setWordWrap(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Add file browser
        self.textbox = linkInputBox()
        layout.addWidget(self.textbox)
        self.file_browser = fileBrowser()
        layout.addWidget(self.file_browser)

        self.setLayout(layout)

    def validatePage(self):
        self.filepath = self.file_browser.textbox.text()
        self.links = [line.strip() for line in self.textbox.textbox.toPlainText().split('\n') if line.strip()]
        if not self.filepath and not self.links:
            QMessageBox.warning(self, "Skipping Alternative IANSEO", "No urls of file provided, skipping alternative IANSEO scraping.")
            self.wizard().shared["alt_ianseo_urls"] = None
            return True
        
        elif self.filepath and self.links:
            QMessageBox.warning(self, "Invalid input", "Only input urls or a file, not both.")

            return False
        
        elif self.filepath and not self.links:
            if self.filepath.endswith(".xlsx"):
                self.wizard().shared["alt_ianseo_urls"] = pd.read_excel(self.filepath, header=None).iloc[:, 0].tolist()
            elif self.filepath.endswith(".csv"):
                self.wizard().shared["alt_ianseo_urls"] = pd.read_csv(self.filepath, header=None).iloc[:, 0].tolist()
            else:
                QMessageBox.warning(self, "Invalid Filepath", "File extension must be .csv or .xlsx")
            return True
        
        elif not self.filepath and self.links:
            self.wizard().shared["alt_ianseo_urls"] = self.links
    
            return True


class tamlynScraperPage(QWizardPage):
    def __init__(self, parent=None):
        super(tamlynScraperPage, self).__init__(parent)
        # Set page text
        self.setTitle("Scraping TamlynScore")
        label = QLabel("Scraping TamlynScore doesn't require you finding links because the website is structured sensibly. Just choose whether you want to.")
        label.setWordWrap(True)
        
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Add checkbox
        checkbox = QCheckBox("Scrape TamlynScore?", self)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.checkbox_state_changed)
        layout.addWidget(checkbox)

        self.setLayout(layout)

    def checkbox_state_changed(self, state):
        if state == 2:
            self.wizard().shared["scrape_tamlyn"] = True
        else:
            self.wizard().shared["scrape_tamlyn"] = False


class compilerDirectoryPage(QWizardPage):
    def __init__(self, parent=None):
        super(compilerDirectoryPage, self).__init__(parent)
        # Set page text
        self.setTitle("Choose where to save results")

        # Set up layout
        layout = QVBoxLayout()

        # Add directory browser
        self.directory_browser = directoryBrowser()
        layout.addWidget(self.directory_browser)

        self.setLayout(layout)

    def validatePage(self):
        self.save_dir = self.directory_browser.textbox.text()

        if self.save_dir:
            self.wizard().shared["save_dir"] = self.save_dir
            return True
        else:
            QMessageBox.warning(self, "No Destination Folder", "You must select a destination folder to proceed")
            return False


class ProgressPage(QWizardPage):
    def __init__(self, parent=None):
        super(ProgressPage, self).__init__(parent)

        # Set page text
        self.setTitle("Scraper Progress")
        label = QLabel("Note - TamlynScore will take much longer to scrape than IANSEO.")
        label.setWordWrap(True)

        # Set layout
        self._layout = QVBoxLayout()
        self._layout.addWidget(label)
        self.setLayout(self._layout)

        # Track which compilers are running 
        self.expected_compilers = set()
        self.finished_compilers = set()

    def initializePage(self):
        self.ianseo_urls = self.wizard().shared["ianseo_urls"]
        self.alt_ianseo_urls = self.wizard().shared["alt_ianseo_urls"]
        self.scrape_tamlyn = self.wizard().shared["scrape_tamlyn"]
        self.save_dir = self.wizard().shared["save_dir"]

        if self.ianseo_urls:
            self.expected_compilers.add("ianseo")
            self.ianseo_scraper = IanseoScraper(self.ianseo_urls)
            self.ianseo_progress_bar = progressBar("Ianseo Scraper Progress", len(self.ianseo_urls))
            self._layout.addWidget(self.ianseo_progress_bar)

            self.ianseo_scraper.progress.connect(self.ianseo_progress_bar.set_progress)
            self.ianseo_scraper.finished.connect(self.compile_ianseo)
            
            self.ianseo_scraper.start()

        if self.alt_ianseo_urls:
            self.expected_compilers.add("alt_ianseo")
            self.alt_ianseo_scraper = AltIanseoScraper(self.alt_ianseo_urls)
            self.alt_ianseo_progress_bar = progressBar("Alternative Ianseo Scraper Progress", len(self.alt_ianseo_urls))
            self._layout.addWidget(self.alt_ianseo_progress_bar)

            self.alt_ianseo_scraper.progress.connect(self.alt_ianseo_progress_bar.set_progress)
            self.alt_ianseo_scraper.finished.connect(self.clean_alt_ianseo)
            
            self.alt_ianseo_scraper.start()

        if self.scrape_tamlyn:
            self.expected_compilers.add("tamlyn")
            self.tamlyn_scraper = TamlynScraper()
            self.tamlyn_progress_bar = progressBar("TamlynScore Scraper Progress", self.tamlyn_scraper.totalUrls)
            self._layout.addWidget(self.tamlyn_progress_bar)

            self.tamlyn_scraper.progress.connect(self.tamlyn_progress_bar.set_progress)
            self.tamlyn_scraper.finished.connect(self.compile_tamlyn)

            self.tamlyn_scraper.start()

        if not self.ianseo_urls and not self.alt_ianseo_urls and not self.scrape_tamlyn:
            QMessageBox.warning(self, "Bored", "There's nothing to do.")
    
    def compile_ianseo(self):
        self.ianseo_compiler = basicCompilerWorker("utils/compile_ianseo.R")
        self.ianseo_compiler.finished.connect(lambda: self.on_compiler_finished("ianseo"))
        self.ianseo_compiler.start()

    def clean_alt_ianseo(self):
        self.alt_ianseo_cleaner = basicCompilerWorker("utils/alt_ianseo_cleaner.R")
        self.alt_ianseo_cleaner.finished.connect(self.compile_alt_ianseo)
        self.alt_ianseo_cleaner.start()
    
    def compile_alt_ianseo(self):
        self.alt_ianseo_compiler = basicCompilerWorker("utils/compile_alt_ianseo.R")
        self.alt_ianseo_compiler.finished.connect(lambda: self.on_compiler_finished("alt_ianseo"))
        self.alt_ianseo_compiler.start()
     

    def compile_tamlyn(self):
        self.tamlyn_compiler = basicCompilerWorker("utils/compile_tamlyn.R")
        self.tamlyn_compiler.finished.connect(lambda: self.on_compiler_finished("tamlyn"))
        self.tamlyn_compiler.start()

    def on_compiler_finished(self, name):
        self.finished_compilers.add(name)

        if self.finished_compilers == self.expected_compilers:
            self.compile_all()    

    def compile_all(self):
        self.show_spinner()
        self.ultimate_compiler = advancedCompilerWorker("utils/compile_ianseo_and_tamlyn.R", args=[self.save_dir])
        self.ultimate_compiler.finished.connect(self.on_complete)
        self.ultimate_compiler.start()

    def on_complete(self):
        self.hide_spinner()
        filename = self.save_dir + "/total_results.csv"

        results = pd.read_csv(filename)
        num_results = len(results)

        self.completed_message_box = QMessageBox(self)
        self.completed_message_box.setWindowTitle("Finished!")
        self.completed_message_box.setText(f"{num_results} results saved to {filename}")

        close_button = self.completed_message_box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        close_button.clicked.connect(lambda: sys.exit())

        self.completed_message_box.exec()


    def show_spinner(self):
        self.spinner_container = QWidget()
        spinner_layout = QHBoxLayout()
        self.spinner_container.setLayout(spinner_layout)

        self.spinner = SpinnerWidget(
        parent=self.spinner_container,
        size=30,
        num_dots=12,
        colour=QColor(0, 0, 0)
        )

        self.spinner.start()

        self.spinner_text = QLabel("Compiling results (may take several minutes)")
        spinner_layout.addWidget(self.spinner)
        spinner_layout.addWidget(self.spinner_text)
        spinner_layout.addStretch()

        self._layout.addWidget(self.spinner_container)
    
    def hide_spinner(self):
        if hasattr(self, 'spinner'):
            self.spinner.stop()
        if hasattr(self, 'spinner_container'):
            self.spinner_container.hide()


