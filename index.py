import psutil
import win32api
import ctypes
import win32process
import pystray
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5 import QtWidgets, QtCore, QtGui
import os
import sys

app = QtWidgets.QApplication.instance()

# Create and show the main window or any other widgets
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

    def __init__(self):
        # have to initialize this to the size of MEMORYSTATUSEX
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()

def get_standby_list_usage():
    memory_status = MEMORYSTATUSEX()
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
    return (memory_status.ullTotalPageFile - memory_status.ullAvailPageFile) >> 20 # Convert to MB

class MemoryOptimizerPro(QtWidgets.QSystemTrayIcon):

    MAX_DATA_POINTS = 100

    def __init__(self, parent=None):
        super(MemoryOptimizerPro, self).__init__(parent)
        print("Application started")

        # Set up the tray icon
        self.setIcon(QtGui.QIcon("icon.png"))
        self.setVisible(True)

        # Set up the menu
        self.menu = QtWidgets.QMenu(parent)
        self.menu.addAction("Start Hacking", self.start_hacking)
        self.menu.addAction("Stop Hacking", self.stop_hacking)
        self.menu.addSeparator()
        self.menu.addAction("Exit", self.exit)

        # Connect the triggered signal to the show_menu method
        self.activated.connect(self.show_menu)

        # Set up the timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_memory_usage)

        # Start the program in off mode
        self.hacking = False

        # Set up the matplotlib figure and axes for the visualization
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.ax.set_title("Memory Efficiency Hacking Terminal", color='green')
        self.ax.set_xlabel("Time (s)", color='green')
        self.ax.set_ylabel("Standby List Usage (MB)", color='green')
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot(self.xdata, self.ydata)
        self.fig.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.spines['bottom'].set_color('green')
        self.ax.spines['top'].set_color('green')
        self.ax.spines['left'].set_color('green')
        self.ax.spines['right'].set_color('green')
        self.ax.tick_params(axis='x', colors='green')
        self.ax.tick_params(axis='y', colors='green')
        self.line.set_color('green')

        # Set up the console widget for the hacking terminal
        self.console = QtWidgets.QTextEdit()
        self.console.setFont(QtGui.QFont("Courier New", 10))
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: black; color: green; border: none;")
        self.console.setPlaceholderText("Welcome to the Memory Efficiency Hacking Terminal!")
        self.console.setMaximumHeight(200)
        self.console.setCursorWidth(0)

        # Set up the input widget for the hacking terminal
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Enter your command here...")
        self.input.setStyleSheet("background-color: black; color: green; border: none;")
        self.input.returnPressed.connect(self.execute_command)

        # Set up the layout for the main window
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.console, 5)  # Add a stretch factor of 1 to the console widget
        main_layout.addWidget(self.input, 1)


        # Set up the PyQt window for the visualization
        self.win = QtWidgets.QWidget()
        self.win.setStyleSheet("background-color: black;")
        self.canvas = FigureCanvas(self.fig)
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.canvas, 4)
        self.graph_layout.addLayout(main_layout, 1)
        self.win.setLayout(self.graph_layout)
        self.win.resize(800, 600)

        # Automatically execute the "info" command on startup
        self.input.setText("info")
        self.execute_command()

    def show_menu(self, reason):
        if reason == self.Trigger:
            self.menu.exec_(QtGui.QCursor.pos())

    def start_hacking(self):
        self.hacking = True
        self.timer.start(1000) # Update the memory usage every second
        self.win.show()

    def stop_hacking(self):
        self.hacking = False
        self.timer.stop()

    def update_memory_usage(self):
        # Get the standby list usage
        standby_list_usage = get_standby_list_usage()

        # Update the visualization with the new data
        if not self.canvas:  # Check if the canvas object is still alive
            return
        self.xdata.append(len(self.xdata) + 1)
        self.ydata.append(standby_list_usage)
        if len(self.xdata) > self.MAX_DATA_POINTS:
            self.xdata.pop(0)
            self.ydata.pop(0)
        self.line.set_data(self.xdata, self.ydata)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Update the console with the current memory usage
        self.console.append(f"Standby List Usage: {standby_list_usage} MB")

    def execute_command(self):
        # Get the user's input and clear the input field
        command = self.input.text()
        self.input.clear()

        # Execute the command and update the console with the output
        if command == "help":
            output = "Available commands:\n\nhelp - Show this help message\noptimize - Optimize memory usage\ninfo - Display system information\nexit - Exit the hacking terminal"
        elif command == "optimize":


            # Call the SetProcessWorkingSetSizeEx function from the Windows API
            result = ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_int(-1))
            if result == 0:
                output = "Failed to optimize memory usage."
            else:
                output = "Optimizing memory usage...\nDone!"
        elif command == "info":
            cpu_percent = psutil.cpu_percent(interval=None)
            virtual_memory = psutil.virtual_memory()
            output = f"CPU Usage: {cpu_percent}%\nTotal Memory: {virtual_memory.total >> 20} MB\nAvailable Memory: {virtual_memory.available >> 20} MB"
        elif command == "exit":
            self.stop_hacking()
            QtWidgets.qApp.quit()
            return
        else:
            output = f"Unknown command: {command}"

        # Output the command and its result to the console
        self.console.append(f"> {command}")
        self.console.append(output)

    def exit(self):
        self.stop_hacking()
        QtWidgets.qApp.quit()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    optimizer = MemoryOptimizerPro()
    app.exec_()
    app.closeAllWindows()
    app.quit()
    sys.exit()
