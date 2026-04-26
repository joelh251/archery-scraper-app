from PyQt6.QtWidgets import QPlainTextEdit, QPushButton, QFileDialog, QWidget, QHBoxLayout, QLineEdit, QProgressBar, QLabel

class fileBrowser(QWidget):
    def __init__(self, parent=None):
        super(fileBrowser, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.setCheckable(True)
        self.textbox.setPlaceholderText("Enter filepath or click browse...")

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.textbox.setText(selected_files[0])

class directoryBrowser(QWidget):
    def __init__(self, parent=None):
        super(directoryBrowser, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.setCheckable(True)
        self.textbox.setPlaceholderText("Enter filepath or click browse...")

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.textbox.setText(selected_files[0])

class linkInputBox(QWidget):
    def __init__(self, parent=None):
        super(linkInputBox, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QPlainTextEdit()
        self.textbox.setPlaceholderText("Enter urls separated by line breaks...")

        layout.addWidget(self.textbox)

class progressBar(QWidget):
    def __init__(self, text, max_value, parent=None):
        super(progressBar, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)


    def set_progress(self, value):
        self.progress_bar.setValue(value)


            