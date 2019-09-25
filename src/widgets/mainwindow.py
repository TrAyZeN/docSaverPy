from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QSpinBox, QMainWindow, QSystemTrayIcon, QMenu, QProgressBar, QApplication
from PyQt5.QtCore import QTimer, QSettings, QPoint
from PyQt5.QtGui import QIcon, QPixmap
from widgets.pathtablewidget import PathTableWidget
from dialog.addpathdialog import AddPathDialog
from thread.saver import SaverThread

class MainWindow(QMainWindow):
    """ The main window class, is divided into two pannels:
        the left pannel which contains options buttons
        and the paths pannel which contains the path table and the buttons related to it """

    def __init__(self):
        """ Creates the main window """

        super(MainWindow, self).__init__()

        self.settings = QSettings()
        self.setFixedSize(800, 400)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.settings.value("main_window_pos", QPoint(int((screen_geometry.width()-800)/2), int((screen_geometry.height()-450)/2))))      # by default move window to the middle
        self.setStyleSheet(open("style/" + self.settings.value("theme", "light") + "theme.css").read())

        self.saver_thread = SaverThread()

        self.search_path = QLineEdit("Search...", self)
        self.search_path.setCursorPosition(0)
        self.search_path.setGeometry(400, 5, 200, 30)

        def search_path_text_edited():
            """ When the search field is edited it updates the grid letting the only paths matching the search field """
            self.path_table.update_to_path_matching(self.search_path.text())
        self.search_path.textEdited.connect(search_path_text_edited)

        def search_path_cursor_pos_changed(x, y):
            """ When cursor change in search path field and text is 'Search...' select all """
            if self.search_path.text() == "Search...":
                self.search_path.selectAll()
        self.search_path.cursorPositionChanged.connect(search_path_cursor_pos_changed)

        def search_path_edit_finished():
            """ When search path field edit is finished if there is no text set text to 'Search...' """
            if self.search_path.text() == "":
                self.search_path.setText("Search...")
                self.search_path.setCursorPosition(0)
                self.search_path.deselect()
        self.search_path.editingFinished.connect(search_path_edit_finished)


        self.path_table = PathTableWidget(self)
        self.path_table.setGeometry(5, 40, 595, 355)

        self.themes_button = QPushButton("Change Theme", self)
        self.themes_button.setGeometry(640, 10, 120, 25)
        def themes_button_pushed():
            """ When the theme button is clicked
                it change the theme of the main window """
            theme = self.settings.value("theme", "dark")
            if theme == "dark":
                theme = "light"
                self.settings.setValue("theme", theme)
            elif theme == "light":
                theme = "dark"
                self.settings.setValue("theme", theme)
            else:   
                self.settings.setValue("theme", "light")
            self.setStyleSheet(open("style/" + theme + "theme.css").read())
            self.add_path_dialog.setStyleSheet(open("style/" + theme + "theme.css").read())
        self.themes_button.clicked.connect(themes_button_pushed)


        self.paths_label = QLabel("Paths", self)
        self.paths_label.setGeometry(680, 45, 90, 25)

        self.select_all_button = QPushButton("Select all", self)
        self.select_all_button.setGeometry(610, 75, 90, 25)
        def select_all_button_clicked():
            """ When the select all button is clicked it selects all paths """
            self.path_table.select_all()
        self.select_all_button.clicked.connect(select_all_button_clicked)

        self.add_path_dialog = AddPathDialog(self.path_table)
        self.add_path_button = QPushButton("Add path", self)
        self.add_path_button.setGeometry(610, 110, 90, 25)
        def add_path_button_on_click():
            """ When the add path button is clicked open a dialog
                to select the input path and the output path to add """
            self.add_path_dialog.open()
        self.add_path_button.clicked.connect(add_path_button_on_click)

        self.delete_path_button = QPushButton("Delete path", self)
        self.delete_path_button.setGeometry(705, 110, 90, 25)
        def delete_path_button_clicked():
            """ When the delete path button is clicked it delets all the selected paths """
            paths_to_delete = self.path_table.get_selected_paths()
            for path_group in paths_to_delete:
                self.path_table.delete_path(path_group)
        self.delete_path_button.clicked.connect(delete_path_button_clicked)


        self.save_options_label = QLabel("Save options", self)
        self.save_options_label.setGeometry(665, 150, 140, 20)

        self.save_delay_label = QLabel("Save delay: ", self)
        self.save_delay_label.setGeometry(610, 175, 140, 20)
        self.save_delay_spinbox = QSpinBox(self)
        self.save_delay_spinbox.setRange(5, 1000)
        self.save_delay_spinbox.setSingleStep(1)
        self.save_delay_spinbox.setValue(self.settings.value("save_delay", 10))
        self.save_delay_spinbox.setGeometry(735, 176, 58, 20)
        def save_delay_spinbox_value_changed(new_value):
            """ When the value of the spinbox change it updates the settings """
            self.settings.setValue("save_delay", new_value)
        self.save_delay_spinbox.valueChanged.connect(save_delay_spinbox_value_changed)


        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(710, 320, 80, 40)
        def start_button_clicked():
            """ When the start button is clicked it saves files and then start the timer """
            self.saver_thread.set_path_group_list(self.settings.value("path_group_list", []))
            self.saver_thread.start()

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.save_delay_spinbox.setEnabled(False)
            self.timer.start(self.settings.value("save_delay", 10)*1000*60)
        self.start_button.clicked.connect(start_button_clicked)


        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(610, 320, 80, 40)
        self.stop_button.setEnabled(False)
        def stop_button_clicked():
            """ When the stop button is clicked it stops the timer """
            self.stop_button.setEnabled(False)
            self.start_button.setEnabled(True)
            self.save_delay_spinbox.setEnabled(True)
            self.timer.stop()
        self.stop_button.clicked.connect(stop_button_clicked)

        self.hide_button = QPushButton("Hide", self)
        self.hide_button.setGeometry(610, 270, 80, 40)
        def hide_button_clicked():
            self.hide()
            self.tray_icon.showMessage("docSaverPy", "The application is now running in background", QIcon(QPixmap("resources/icon.png")))
        self.hide_button.clicked.connect(hide_button_clicked)
        
        self.tray_menu = QMenu()
        def open_action():
            self.show()
        self.tray_menu.addAction("Open", open_action)
        self.tray_menu.addAction("Start", start_button_clicked)
        self.tray_menu.addAction("Stop", stop_button_clicked)
        def quit_action():
            self.close()
        self.tray_menu.addAction("Quit", quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(QPixmap("resources/icon.png")))
        self.tray_icon.setToolTip("docSaverPy")
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        def tray_icon_activated(reason):
            """ When the tray icon is clicked it shows the main window """
            if reason == QSystemTrayIcon.Trigger:
                self.show()
        self.tray_icon.activated.connect(tray_icon_activated)
        def tray_icon_messageClicked():
            """ When the tray icon message is clicked it shows the main window""" 
            self.show()
        self.tray_icon.messageClicked.connect(tray_icon_messageClicked)

        self.save_progress_bar = QProgressBar(self)
        self.save_progress_bar.setGeometry(610, 375, 180, 20)
        self.save_progress_bar.setMinimum(0)
        self.save_progress_bar.setMaximum(100)
        def update_save_progress_bar(percentage):
            """ Updates the progress bar percentage with the saving percentage """
            self.save_progress_bar.setValue(percentage)
        self.saver_thread.update_percentage_signal.connect(update_save_progress_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)


    def update(self):
        """ Update method called to save every save_delay min """

        if not self.saver_thread.isRunning():
            self.saver_thread.set_path_group_list(self.settings.value("path_group_list", []))
            self.saver_thread.run()


    def closeEvent(self, QCloseEvent):
        """ When the application closes, it hides the tray icon """

        self.tray_icon.setVisible(False)
        self.settings.setValue("main_window_pos", self.pos())
        QCloseEvent.accept()