from PyQt5.QtCore import Qt, QAbstractTableModel


class PlotParametersTableModel(QAbstractTableModel):
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
            elif orientation == Qt.Vertical:
                return f'{section + 1}'
        return None
