from PyQt5.QtCore import Qt, QAbstractTableModel


class ParametersTableModel(QAbstractTableModel):
    def __init__(self, parameters=None, *args, **kwargs):
        self.parameters = parameters or {}
        super().__init__(*args, **kwargs)

    def rowCount(self, parent):
        return len(self.parameters)

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return list(self.parameters.keys())[index.row()]
            elif index.column() == 1:
                return list(self.parameters.values())[index.row()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'key'
                elif section == 1:
                    return 'value'
        return None

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        return QAbstractTableModel.flags(self, index)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole and index.isValid() and index.column() == 1:
            row = index.row()
            key = list(self.parameters.keys())[row]
            self.parameters[key] = value
            self.dataChanged.emit(index, index)  # Notify that the data has changed
            return True
        return False
