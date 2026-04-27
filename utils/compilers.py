import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class basicCompilerWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, script_path, parent=None):
        super(basicCompilerWorker, self).__init__(parent)
        self.script_path = script_path

    def run(self):
        self.result = subprocess.run(
            ["Rscript", self.script_path]
        )
        self.finished.emit()