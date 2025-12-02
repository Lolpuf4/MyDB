import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit,  QApplication
from DBhelper import execute_command


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database")
        self.setGeometry(600, 600, 600, 300)

        self.set_up_ui()

    def set_up_ui(self):
        layout = QVBoxLayout()

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Enter command")
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Output")

        self.button = QPushButton("Done")
        self.button.clicked.connect(self.get_output)

        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.output_box)
        self.setLayout(layout)

    def get_output(self):
        self.output_box.clear()
        print(1)
        print(self.input_box.toPlainText())
        text = execute_command(self.input_box.toPlainText(), "admin", "123", "messenger")
        print(text)
        self.output_box.append("hello")
        print(text)
        self.input_box.clear()
        print(text)


#correct output as a table/text
#thread in exec command

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())