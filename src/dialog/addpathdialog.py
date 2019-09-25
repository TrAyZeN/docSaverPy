from PyQt5.QtWidgets import QDialog, QFileDialog, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QSettings, QDir

class AddPathDialog(QDialog):
    """ The AddPathDialog class is a dialog that permit the user to select
        an input paths and an output paths, this dialog is composed of
        two text entries with their browse button, and at the bottom
        a cancel button and an ok button """

    def __init__(self, path_table):
        """ Creates the add path dialog """

        super(AddPathDialog, self).__init__()

        self.settings = QSettings()

        self.setWindowTitle("Add path")
        self.setFixedSize(300, 200)
        self.setStyleSheet(open("style/" + self.settings.value("theme", "light") + "theme.css").read())

        self.path_table = path_table
        self.input_path_label = QLabel(self)
        self.input_path_label.setText("Select an input path:")
        self.input_path_label.setGeometry(10, 10, 200, 20)

        self.input_path_line_edit = QLineEdit(self)
        self.input_path_line_edit.setGeometry(10, 40, 200, 30)

        self.input_path_browse_button = QPushButton(self)
        self.input_path_browse_button.setText("Browse")
        self.input_path_browse_button.setGeometry(220, 40, 70, 30)
        def input_path_browse_button_clicked():
            """ When the browse button is clicked it opens the file browser and
                the fill the input path field with directory if one is selected """
            directory =  QFileDialog.getExistingDirectory(self, "Find Files", QDir.currentPath())
            self.input_path_line_edit.setText(directory)
        self.input_path_browse_button.clicked.connect(input_path_browse_button_clicked)


        self.output_path_label = QLabel(self)
        self.output_path_label.setText("Select an output path:")
        self.output_path_label.setGeometry(10, 80, 200, 20)

        self.output_path_line_edit = QLineEdit(self)
        self.output_path_line_edit.setGeometry(10, 110, 200, 30)

        self.output_path_browse_button = QPushButton(self)
        self.output_path_browse_button.setText("Browse")
        self.output_path_browse_button.setGeometry(220, 110, 70, 30)
        def output_path_browse_button_clicked():
            """ When the browse button is clicked it opens the file browser and
                the fill the output path field with directory if one is selected """
            directory =  QFileDialog.getExistingDirectory(self, "Find Files", QDir.currentPath())
            self.output_path_line_edit.setText(directory)
        self.output_path_browse_button.clicked.connect(output_path_browse_button_clicked)


        self.ok_button = QPushButton(self)
        self.ok_button.setText("Ok")
        self.ok_button.setGeometry(190, 160, 100, 30)
        def ok_button_clicked():
            """ When the ok button is clicked
                if the input and the output path field are filled it add this
                new group of paths to the settings and to the paths table
                else it closes the dialog and show the error """
            input_path = self.input_path_line_edit.text()
            output_path = self.output_path_line_edit.text()
            if input_path != "" and output_path != "":
                self.path_table.add_path((input_path, output_path))
            elif input_path == "" and output_path != "":
                print("input path is missing")
                error_label.setText("input path is missing")
            elif input_path != "" and output_path == "":
                print("output path is missing")
                error_label.setText("output path is missing")
            else:
                print("both paths are missing")
                error_label.setText("both paths are missing")

            self.close()
            self.input_path_line_edit.setText("")
            self.output_path_line_edit.setText("")
        self.ok_button.clicked.connect(ok_button_clicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setGeometry(10, 160, 100, 30)
        def cancel_button_clicked():
            """ When the cancel button is clicked it closes the dialog """
            self.close()
            self.input_path_line_edit.setText("")
            self.output_path_line_edit.setText("")
        self.cancel_button.clicked.connect(cancel_button_clicked)
