from PyQt5.QtCore import Qt, QAbstractListModel


class SensorsListModel(QAbstractListModel):
    def __init__(self, sensors=None, *args, **kwargs):
        self.sensors = sensors or []
        super().__init__(*args, **kwargs)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            label = self.sensors[index.row()]
            return f'{label}'

    def rowCount(self, index=None):
        return len(self.sensors)

