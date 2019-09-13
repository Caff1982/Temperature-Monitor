import subprocess
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

import qtmodern.styles
import qtmodern.windows

from models import CustomTableModel, InLineEditDelegate
from mainwindow import Ui_MainWindow


class TemperatureMonitor(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(TemperatureMonitor, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.refresh_rate = 10000
        self.model = CustomTableModel(self.refresh_rate)
        self.delegate = InLineEditDelegate()
        
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(self.delegate)
        self.tableView.resizeColumnsToContents()

        self.logfileButton.clicked.connect(self.create_log)
        self.refreshRateButton.clicked.connect(self.refresh_rate_popup)
        self.resetMinMaxButton.clicked.connect(self.reset_min_max)

        for path in self.model.device_paths:
            device_name = subprocess.check_output(['cat', path + '/type'], encoding='utf-8').strip()
            device_action = QtWidgets.QAction(device_name, self, checkable=True, checked=True)
            device_action.device = device_name
            device_action.toggled.connect(self.device_manager)
            self.menuDevices.addAction(device_action)

        self.actionOpen_New_Window.triggered.connect(self.open_new_window)
        self.actionClose.triggered.connect(self.close_application)
        self.actionReset_Min_Max.triggered.connect(self.reset_min_max)
        self.actionSet_Refresh_Rate.triggered.connect(self.refresh_rate_popup)

    def create_log(self):
        self.model.create_log_file()
        self.logfileButton.setText("Stop csv log file")
        self.logfileButton.clicked.connect(self.stop_log)

    def stop_log(self):
        self.model.logging = False
        self.logfileButton.setText("Create csv log file")
        self.logfileButton.clicked.connect(self.create_log)

    def refresh_rate_popup(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Change Refresh Rate', 'Enter time in seconds:')
        if ok:            
            try:
                new_rate = int(text)*1000
                self.model.set_refresh_rate(new_rate)
                self.refreshLabel.setText(f"Refresh Rate: {text}s")
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", "Invalid Request")

    def reset_min_max(self):
        self.model.reset_min_max()

    def open_new_window(self):
        subprocess.run(['python', 'main.py'])

    def close_application(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close Application',
                                            "Are you sure you want to quit?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def device_manager(self):
        device_checkbox = self.sender()
        if device_checkbox.isChecked():
            self.model.add_device(device_checkbox.device)
        else:
            self.model.remove_device(device_checkbox.device)
            

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    qtmodern.styles.dark(app)
    my_app = TemperatureMonitor()
    my_app.show()
    app.exec_()