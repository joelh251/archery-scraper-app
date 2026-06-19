import subprocess
import os
from PyQt6.QtCore import QThread, pyqtSignal

class basicCompilerWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, script_path, parent=None):
        super(basicCompilerWorker, self).__init__(parent)
        self.script_path = script_path

    def run(self):
        self.result = subprocess.run(
            ["Rscript", self.script_path],
            cwd=os.path.abspath(".")
        )
        self.finished.emit()

class advancedCompilerWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, script_path, args=None, parent=None):
        super(advancedCompilerWorker, self).__init__(parent)
        self.script_path = script_path
        self.args = args or []

    def run(self):
        self.result = subprocess.run(
            ["Rscript", self.script_path, ] + self.args,
            cwd=os.path.abspath(".")
        )
        self.finished.emit()