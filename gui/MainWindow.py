
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton,QMainWindow,QLabel, QLineEdit, QVBoxLayout, QWidget

#button
#input
#label
#context -> option when right mouse is clicked
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sentiement Analysis")

        self.setFixedSize(QSize(400,300))

        self.button = QPushButton("Push me")
        self.button.setFixedSize(QSize(100, 40))
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_function)

        #  label
        self.label = QLabel()
        # input form
        self.input = QLineEdit() #read input
        self.input.textChanged.connect(self.label.setText)

        #layout
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # self.setCentralWidget(self.button)

    def button_function(self,checked):
        print("Clicked : ", checked)
        self.button.setText("You alreadu clicked me")
        
        # To disable the button
        self.button.setEnabled(False)
        # Also Changes window title 
        self.setWindowTitle("My new Title")