from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QWidget, QVBoxLayout, QTabWidget
import Arduino_input as ar
import Afunc as al
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class moisture_main():
#pyinstaller -F -i moisture_level.ico moisture_level.py
    def __init__(self):
        # main window
        self.window = QMainWindow()
        self.window.resize(1400, 700)
        self.window.move(200, 15)
        self.window.setWindowTitle('moisture_level 0104B *hoshipu')

        self.inputallow = False
        
        # user input adjustments
        self.userinput1 = QPlainTextEdit(self.window)
        self.userinput1.move(20, 35)
        self.userinput1.resize(200, 70)
        self.userinput1.setPlaceholderText("port = COM6")
        self.userinput2 = QPlainTextEdit(self.window)
        self.userinput2.move(230, 35)
        self.userinput2.resize(200, 70)
        self.userinput2.setPlaceholderText("baudrate = 57600")

        # button for detection
        self.detect = QPushButton('Test Connection ', self.window)
        self.detect.move(20,120)
        self.detect.resize(200, 65)
        self.detect.clicked.connect(self.detect_connection)
        
        # output text section to indicate program state
        self.useroutput = QPlainTextEdit(self.window)
        self.useroutput.move(230, 120)
        self.useroutput.resize(200, 170)
        self.useroutput.setPlaceholderText("Output Section")
        self.useroutput.setReadOnly(True)

        # button for input
        self.inputdata = QPushButton('Input Data ', self.window)
        self.inputdata.move(20,220)
        self.inputdata.resize(200, 65)
        self.inputdata.clicked.connect(self.import_data)

        # analysis text section to indicate watering 
        self.anaoutput = QPlainTextEdit(self.window)
        self.anaoutput.move(500, 35)
        self.anaoutput.resize(850, 250)
        self.anaoutput.setPlaceholderText("Analysis Section")
        self.anaoutput.setReadOnly(True)

        # window for graphs
        self.tabwidget = QTabWidget(self.window)
        self.tabwidget.setGeometry(10, 300, 1380, 350)

    def detect_connection(self):
        
        if not self.userinput1.toPlainText():
            pt = 'COM6'
        else:
            pt = self.userinput1.toPlainText()
        bd = 57600
        try:
            bd = int(self.userinput2.toPlainText())
        except Exception as e:
            pass
        info = ar.check_serial_connection(port = pt,\
                                        baudrate = bd)
        if info == True:
            self.useroutput.setPlainText('Connected!')
            self.inputallow = True
        else:
            self.useroutput.setPlainText('Connection failed\n'+str(info))
            self.inputallow = False

    def import_data(self):
        if not self.inputallow:
            self.useroutput.setPlainText('You have not yet detected the connection!')
            return
        self.inputallow = False
        read_data = ar.read_arduino(port = self.userinput1.toPlainText(),\
                                    baudrate = self.userinput2.toPlainText())
        new_data = ar.process_arduino_data(read_data)
        if new_data == False:
            self.useroutput.setPlainText('input is invalid')
            return
        analysis = al.input(input_data = new_data)
        self.anaoutput.setPlainText(analysis)
        plt1 = al.graph_data_change()
        plt2 = al.graph_data_before()
        plt3 = al.graph_data_after()
        
        self.show_figure(plt1, "Moisture Change")
        self.show_figure(plt2, "Before")
        self.show_figure(plt3, "After")

    def show_figure(self, plot, label):
        # 创建一个新的 FigureCanvas 实例，并将图形对象添加到其中
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        # 解压缩时间和湿度变化
        time, moisture_change = plot

        # 绘制散点图
        ax.scatter(time, moisture_change)
        
        # 设置标题和标签
        ax.set_title(label)
        ax.set_xlabel('Time')
        ax.set_ylabel('Moisture Change')

        # 创建一个新的 Tab
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        tab.setLayout(layout)
        
        # 将 Tab 添加到 TabWidget 中
        self.tabwidget.addTab(tab, label)

if __name__ == "__main__":
    app = QApplication([])
    moisture = moisture_main()
    moisture.window.show()
    app.exec_()