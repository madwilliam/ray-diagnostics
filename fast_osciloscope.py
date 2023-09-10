import sys
import time
from random import randint
from threading import Thread
from time import sleep
from typing import Union
import serial
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

port = serial.Serial('COM3', 115200, timeout=0.5)
sleep(0.1)
refresh_rate=1000
class Window(QWidget):
    running = False

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.low_of_day: Union[float, None] = 5
        self.high_of_day: Union[float, None] = 15

        plot = LiveLinePlot(pen="blue")
        self.connector = DataConnector(plot, max_points=600)
        bottom_axis = LiveAxis("bottom", **{Axis.TICK_FORMAT: Axis.TIME})

        self.chart_view = LivePlotWidget(title="Voltage at port A0", axisItems={'bottom': bottom_axis})
        self.chart_view.showGrid(x=True, y=True, alpha=0.3)
        self.chart_view.setLabel('bottom', 'Datetime', units="s")
        self.chart_view.setLabel('left', 'Price')
        self.chart_view.addItem(plot)
        layout.addWidget(self.chart_view, 2, 0, -1, 3)

    def update(self):
        while self.running:
            port.write(b's') #handshake with Arduino
            if (port.inWaiting()):# if the arduino replies
                value = port.readline()# read the reply
                number = float(str(value[:-2])[2:-1]) #convert received data to integer 
                timestamp = time.time()
                self.connector.cb_append_data_point(number, timestamp)
            sleep(1/refresh_rate)

    def start_app(self):
        self.running = True
        Thread(target=self.update).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.start_app()
    app.exec()
    window.running = False