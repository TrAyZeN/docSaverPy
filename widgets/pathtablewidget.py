from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class PathTableWidget(QTableWidget):
    """ The PathTableWidget class is a widget containing 3 columns,
        the columns contains respectively the checkboxes to select paths,
        the input paths and the ouput paths """
        
    def __init__(self, parent_widget):
        """ Creates the table with the path group list of the parent widget's settings """

        super(PathTableWidget, self).__init__()
        self.setColumnCount(3)
        self.setParent(parent_widget)

        self.path_group_list = self.parent().settings.value("path_group_list", [])

        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 289)
        self.setColumnWidth(2, 289)
        self.verticalHeader().hide()

        def path_table_item_changed(item):
            """ When content of the cell changed it saves the new paths to the settings """
            if item in self.selectedItems():
                if self.column(item) != 0:      # if not an item in checkbox column
                    self.path_group_list[self.row(item)][self.column(item)-1] = item.text()
                    self.parent().settings.setValue("path_group_list", self.path_group_list)
        self.itemChanged.connect(path_table_item_changed)

        self._show_path_group_list(self.path_group_list)

    def _show_path_group_list(self, path_group_list):
        self.clear()
        self.setHorizontalHeaderLabels(("", "Input paths", "Output paths"))
        self.setRowCount(len(path_group_list))

        for i, path_group in enumerate(path_group_list):
            select_checkbox = QTableWidgetItem()
            select_checkbox.setCheckState(False)
            self.setItem(i, 0, select_checkbox)

            input_path_cell = QTableWidgetItem(path_group[0])
            self.setItem(i, 1, input_path_cell)

            output_path_cell = QTableWidgetItem(path_group[1])
            self.setItem(i, 2, output_path_cell)

        return True

    def update_to_path_matching(self, text_to_match):
        """ Updates the table showing only the row with a path matching the text
        return True if the operation is successful """

        matching_list = [path_group for path_group in self.path_group_list if text_to_match.lower() in path_group[0].lower() or text_to_match.lower() in path_group[1].lower()]
        self._show_path_group_list(matching_list)
        return True


    def select_all(self):
        """ Selects every checkboxes
            return True if the operation is successful """

        for i in range(0, self.rowCount()):
            selected_checkbox = QTableWidgetItem()
            selected_checkbox.setCheckState(True)
            self.setItem(i, 0, selected_checkbox)

        return True


    def add_path(self, path_group_to_add):
        """ Add a new group of path at the bottom of the table
            return True if the operation is successful """

        self.path_group_list.append(path_group_to_add)
        self.parent().settings.setValue("path_group_list", self.path_group_list)

        self.setRowCount(len(self.path_group_list))

        select_checkbox = QTableWidgetItem()
        select_checkbox.setCheckState(False)
        self.setItem(len(self.path_group_list)-1, 0, select_checkbox)

        input_path_cell = QTableWidgetItem(path_group_to_add[0])
        self.setItem(len(self.path_group_list)-1, 1, input_path_cell)

        output_path_cell = QTableWidgetItem(path_group_to_add[1])
        self.setItem(len(self.path_group_list)-1, 2, output_path_cell)

        return True


    def delete_path(self, path_group_to_delete):
        """ Delete the path group matching the path group list
            and update the table
            return True if the operation is successful """

        self.path_group_list.remove(path_group_to_delete)
        self.parent().settings.setValue("path_group_list", self.path_group_list)

        self._show_path_group_list(self.path_group_list)
        return True


    def get_selected_paths(self):
        """ return the list of all the group of path where their checkbox is selected """

        selected_paths = []
        for i, path_group in enumerate(self.path_group_list):
            checkbox = self.item(i, 0)
            checkbox_state = bool(checkbox.checkState())
            if checkbox_state is True:
                selected_paths.append(path_group)
        return selected_paths
    