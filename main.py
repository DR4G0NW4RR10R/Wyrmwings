import sys, re, os

from DatapackMaker import DatapackMaker

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from PySide6.QtGui import QPixmap

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wyrmwings Wizard")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Wyrmwings Wizard"))
        layout.addWidget(QHLine())

        layout.addWidget(QLabel("Choose a pack name for the datapack:"))
        self.packNameField = QLineEdit()
        layout.addWidget(self.packNameField)
        layout.addWidget(QHLine())

        layout.addWidget(QLabel("Choose a namespace for the datapack:"))
        self.namespaceField = QLineEdit()
        layout.addWidget(self.namespaceField)
        layout.addWidget(QHLine())

        layout.addWidget(QLabel("Choose a name for the in-game tag:"))
        self.tagField = QLineEdit()
        layout.addWidget(self.tagField)
        layout.addWidget(QHLine())

        layout.addWidget(QLabel("Choose a name for the in-game scoreboard.\nIt is a good idea to make it representative of the image:"))
        self.scoreboardField = QLineEdit()
        layout.addWidget(self.scoreboardField)
        layout.addWidget(QHLine())

        layout.addWidget(QLabel("Enter the filename of the image you wish to use:\n(Recommended max 64x64, transparent png)"))
        self.imageField = QLineEdit("assets\\no-preview.png")
        layout.addWidget(self.imageField)

        self.previewButton = QPushButton("Preview")
        layout.addWidget(self.previewButton)
        self.previewButton.clicked.connect(self.preview)

        self.previewBox = QLabel()
        pixmap = QPixmap("assets\\no-preview.png")
        self.previewBox.setPixmap(pixmap)
        self.previewBox.resize(pixmap.width(), pixmap.height())
        layout.addWidget(self.previewBox)
        layout.addWidget(QHLine())

        self.submitButton = QPushButton("Click to make a datapack!")
        layout.addWidget(self.submitButton)
        self.submitButton.clicked.connect(self.submit)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
    
    def preview(self):
        # image validation - exists and is valid path, is png or jpg
        reasons = []
        valid = True
        imageExists = os.path.isfile(self.imageField.displayText())
        imageValidFormat = self.imageField.displayText().endswith(".png") | self.imageField.displayText().endswith(".jpg") | self.imageField.displayText().endswith(".jpeg")
        if (not imageExists) | (not imageValidFormat):
            reasons.append("Image either does not exist, or is not .png, .jpg or .jpeg")
            valid = False
        
        if not valid:
            errorWindow = QDialog(self)
            errorWindow.setWindowTitle("Error")
            layout = QVBoxLayout()
            for reason in reasons:
                layout.addWidget(QLabel(reason))
            errorWindow.setLayout(layout)
            errorWindow.exec()
            return
        else:
            pixmap = QPixmap(self.imageField.displayText())
            self.previewBox.setPixmap(pixmap)
            self.previewBox.resize(pixmap.width(), pixmap.height())
    
    def submit(self):
        # input validation
        reasons = []
        valid = True
        # packname validation - valid Windows folder
        packInvalid = re.search("r[\\.\\\\\\/\\<\\>\\:\\\"\\|\\?\\*]", self.packNameField.displayText())
        if packInvalid:
            reasons.append("Pack name cannot include Windows reserved characters for directories")
            valid = False
        
        # packname validation - valid Windows folder and valid datapack namespace
        namespaceValid = re.fullmatch("[a-z0-9_\\-\\.]+", self.namespaceField.displayText())
        if (not namespaceValid) | (self.namespaceField.displayText() == ".."):
            reasons.append("Namespace must contain only lowecase letters, numbers, underscores, hyphens or periods")
            valid = False
        
        # tag validation - only uppercase, lowercase, numbers, hyphens, underscores. No spaces
        tagValid = re.fullmatch("[a-zA-Z0-9_\\-]+", self.namespaceField.displayText())
        if not tagValid:
            reasons.append("Tag name must contain only letters, numbers, underscores or hyphens")
            valid = False
        
        # scoreboard validation - only uppercase, lowercase, numbers, hyphens, underscores, periods, plus. No spaces
        scoreboardValid = re.fullmatch("[a-zA-Z0-9_\\-\\.\\+]+", self.namespaceField.displayText())
        if not scoreboardValid:
            reasons.append("Scoreboard name must contain only letters, numbers, underscores, hyphens, periods or plus signs")
            valid = False
        
        # image validation - exists and is valid path, is png or jpg
        imageExists = os.path.isfile(self.imageField.displayText())
        imageValidFormat = self.imageField.displayText().endswith(".png") | self.imageField.displayText().endswith(".jpg") | self.imageField.displayText().endswith(".jpeg")
        if (not imageExists) | (not imageValidFormat):
            reasons.append("Image either does not exist, or is not .png, .jpg or .jpeg")
            valid = False
        
        if not valid:
            errorWindow = QDialog(self)
            errorWindow.setWindowTitle("Error")
            layout = QVBoxLayout()
            for reason in reasons:
                layout.addWidget(QLabel(reason))
            errorWindow.setLayout(layout)
            errorWindow.exec()
            return
        else:
            packname = self.packNameField.displayText()
            namespace = self.namespaceField.displayText()
            imagepath = self.imageField.displayText()
            tagname = self.tagField.displayText()
            scoreboardname = self.scoreboardField.displayText()

            dm = DatapackMaker(packname, namespace, imagepath, tagname, scoreboardname)

            dm.makeDatapack("Datapack made by Wyrmwings (https://github.com/DR4G0NW4RR10R/Wyrmwings) to display an image behind a player")

            successWindow = QDialog(self)
            successWindow.setWindowTitle("Success!")
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Datapack \"{packname}\" successfully made!"))
            successWindow.setLayout(layout)
            successWindow.exec()
            return



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()