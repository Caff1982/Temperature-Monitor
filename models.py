import os
import subprocess
from datetime import datetime
import csv

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

INTEL_PATH = '/sys/class/thermal/'
AMD_PATH = '/sys/class/hwmon/'


class CustomTableModel(QtCore.QAbstractTableModel):
    """
    Custom Table Model to handle temperature device data
    """
    def __init__(self, refresh_rate):
        QtCore.QAbstractTableModel.__init__(self)

        self.path = AMD_PATH
        self.device_paths = [self.path + fn for fn in os.listdir(self.path)]
        self.get_device_data()

        self.refresh_rate = refresh_rate
        self.logging = False
        self.filename = None
        self.rows = len(self.device_data) 
        self.columns = ['Device', 'Temp', 'Min', 'Max']

        self.timer = QtCore.QTimer()  
        self.timer.setInterval(self.refresh_rate)
        self.timer.timeout.connect(self.update_model)
        self.timer.start(self.refresh_rate)

    def get_device_data(self):
        """
        creates a 2d array where each each row is the device and the columns
        are: device_path, device name, current temp, min temp, max temp:
        """
        self.device_data = []
        for i in range(len(self.device_paths)):
                device_name = subprocess.check_output(['cat', self.device_paths[i] + '/name'], encoding='utf-8').strip()
                temp_filename = [fn for fn in os.listdir(self.device_paths[i]) if '_input' in fn][0]
                temp_path = os.path.join(self.device_paths[i], temp_filename)
                cur_temp = int(subprocess.check_output(['cat', os.path.join(self.device_paths[i], temp_path)], encoding='utf-8')[:2])
                row_data = [self.device_paths[i], device_name, cur_temp, cur_temp, cur_temp, temp_path]
                self.device_data.append(row_data)

    def update_model(self):
        self.layoutAboutToBeChanged.emit()
        for i in range(len(self.device_data)):
            cur_temp = int(subprocess.check_output(['cat', self.device_data[i][5]], encoding='utf-8')[:2])
            self.device_data[i][2] = cur_temp
            self.device_data[i][3] = min(cur_temp, self.device_data[i][3])
            self.device_data[i][4] = max(cur_temp, self.device_data[i][4])
        self.layoutChanged.emit()

        if self.logging:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.filename, 'a') as f:
                writer = csv.writer(f)
                for device in self.device_data:
                    row = [current_time, device[1], device[2]]
                    writer.writerow(row)

    def rowCount(self, *args, **kwargs):
        return len(self.device_data)

    def columnCount(self, *args, **kwargs):
        return len(self.columns)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        set column header data
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section].title()

    def data(self, index, role):
        """
        Display Data in table cells
        Gets info from device data skipping col 1 as this is path
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column() + 1

        if role == QtCore.Qt.DisplayRole:
            return self.device_data[row][col]


    def create_log_file(self):
        """
        Creates a csv log file for temperatures,
        filename is the current date and time
        """
        self.logging = True
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.filename = current_time + '.csv'
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            for device in self.device_data:
                # for each row we write time, device name and current temp
                row = [current_time, device[1], device[2]]
                writer.writerow(row)

    def reset_min_max(self):
        self.layoutAboutToBeChanged.emit()
        for row in self.device_data:
            cur_temp = row[2]
            row[3] = cur_temp
            row[4] = cur_temp
        self.layoutChanged.emit()

    def set_refresh_rate(self, new_rate):
        self.layoutAboutToBeChanged.emit()
        self.refresh_rate = new_rate
        self.timer.setInterval(self.refresh_rate)
        self.timer.timeout.connect(self.update_model)
        self.timer.start(self.refresh_rate)
        print(self.refresh_rate)
        self.layoutChanged.emit()

    def remove_device(self, device):
        self.layoutAboutToBeChanged.emit()
        for row in self.device_data:
            if row[1] == device:
                self.device_data.remove(row) 
        self.layoutChanged.emit()

    def add_device(self, device):
        self.layoutAboutToBeChanged.emit()
        for path in self.device_paths:
            device_name = subprocess.check_output(['cat', path + '/type'], encoding='utf-8').strip()
            if device_name == device:
                cur_temp = subprocess.check_output(['cat', path +'/temp'], encoding='utf-8')[:2]
                row_data = [path, device_name, cur_temp, cur_temp, cur_temp]
                self.device_data.append(row_data)
        self.layoutChanged.emit()


class InLineEditDelegate(QtWidgets.QItemDelegate):
    """
    Delegate is for inline editing of table cells
    """
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parent, option, index):
        return super(InLineEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))


  


