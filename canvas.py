from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                as FigureCanvas)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtWidgets

from models import CustomTableModel

plt.style.use('dark_background')


class MplCanvas(FigureCanvas):
    """
    Base class to define how matplotlib canvas will be displayed
    """
    def __init__(self, parent=None, width=5.5, height=2.5, dpi=100):
        # Initialize TableModel to track temps
        self.model = CustomTableModel(1000)

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.patch.set_facecolor((0.2, 0.2, 0.2))

        fig.set_tight_layout(True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.compute_initial_figure()

    def compute_initial_figure(self):
        pass


class DynamicMplCanvas(MplCanvas):
    """
    A canvas that updates every 5 seconds
    with a new matplotlib plot
    """
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.model.device_to_plot = 0

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5000)

    def compute_initial_figure(self):
        self.axes.cla()

        self.axes.grid(True)
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Temperature (°C)')
        self.axes.set_ylim(30, 80)
        self.axes.set_xlim(60, 0)
        self.axes.set_xticklabels([-i for i in range(0, 70, 10)])
        self.axes.tick_params(labelleft=True, labelright=True)
        self.draw()

    def update_figure(self):
        self.axes.cla()

        self.axes.grid(True)
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Temperature (°C)')
        self.axes.set_ylim(30, 80)
        self.axes.set_xlim(60, 0)
        self.axes.set_xticklabels([-i for i in range(0, 70, 10)])
        self.axes.tick_params(labelleft=True, labelright=True)
        self.axes.plot(self.model.temp_tracker, 'y')
        self.draw()

    def change_device(self, device):
        self.model.device_to_plot = device
        self.model.temp_tracker.clear()
        self.update_figure()
