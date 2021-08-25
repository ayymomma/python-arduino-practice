from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import settings

class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class GraphWindow(QWidget):

    def __init__(self, parent=None):
        super(GraphWindow, self).__init__(parent)

        _translate = QtCore.QCoreApplication.translate
        self.setObjectName("Temperature / Voltage Graphic")
        self.setWindowTitle(_translate("Form", "Temperature / Voltage Graphic"))
        self.canvas = MplCanvas()  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()  # Set box for plotting
        self.navi_toolbar = NavigationToolbar(self.canvas, self)

        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout(self.vbl)

        self.n_data = 60
        self.xdata = list(range(self.n_data))
        self.temperatureData = [settings.temperature] * self.n_data
        self.voltageData = [settings.voltage] * self.n_data
        self.update_plot()

        self.show()
        # Setup a timer to trigger the redraw by calling update_plot.

    def start_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.temperatureData = self.temperatureData[1:] + [settings.temperature]
        self.voltageData = self.voltageData[1:] + [settings.voltage]
        self.xdata = list(range(len(self.temperatureData)))
        self.canvas.axes.autoscale()
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.voltageData, 'b', label='Voltage  (V)')
        self.canvas.axes.twinx()
        self.canvas.axes.plot(self.xdata, self.temperatureData, 'r', label='Temperature (C)')
        self.canvas.axes.legend()
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def stop_plot(self):
        self.timer.stop()

