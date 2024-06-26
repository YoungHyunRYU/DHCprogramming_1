import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import xml.etree.ElementTree as ET
from datetime import datetime
from matplotlib.dates import DateFormatter
from qt_material import apply_stylesheet


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('graphPlot_2.ui', self)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 600, 400)

        self.btn1 = self.findChild(QPushButton, 'loadButton')
        self.resultLabel = self.findChild(QLabel, 'resultLabel')
        self.plotWidget = self.findChild(QWidget, 'plotWidget')
        self.stepAverage = self.findChild(QLabel, 'stepAverage')
        self.stepRecom = self.findChild(QLabel, 'stepRecom')

        self.stepAverage.setStyleSheet("font-size: 18px;")
        self.stepRecom.setStyleSheet("font-size: 18px;")
        self.resultLabel.setStyleSheet("font-size: 14px;")
        
        self.btn1.clicked.connect(self.btn_fun_FileLoad)

    def btn_fun_FileLoad(self):
        fname, _ = QFileDialog.getOpenFileName(self, '파일 선택', '', 'XML 파일 (*.xml);;모든 파일 (*)')
        if fname:
            self.resultLabel.setText(f'파일 경로: {fname}')
            self.plot_data(fname)

    def plot_data(self, fname):
        tree = ET.parse(fname)
        root = tree.getroot()

        # 2024년 이후 걸음 데이터만 가지고 오도록
        step_counts = {}
        for record in root.findall('.//Record[@type="HKQuantityTypeIdentifierStepCount"]'):
            date = record.get('startDate')
            value = int(record.get('value'))
            date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z')
            if date_obj.year >= 2024:
                day_str = date_obj.strftime('%Y-%m-%d')
                if day_str not in step_counts:
                    step_counts[day_str] = 0
                step_counts[day_str] += value

        sorted_dates = sorted(step_counts.keys())
        sorted_steps = [step_counts[date] for date in sorted_dates]

        if sorted_steps:
            average_steps = sum(sorted_steps) / len(sorted_steps)
        else:
            average_steps = 0

        self.stepAverage.setText(f'평균 걸음수: {average_steps:.2f}')
        
        if average_steps < 10000:
            steps_to_10k = 10000 - average_steps
            self.stepRecom.setText(f'24년에 1만보보다 {steps_to_10k:.2f} 걸음 덜 걸었음')
        else:
            steps_over_10k = average_steps - 10000
            self.stepRecom.setText(f'24년에 1만보보다 {steps_over_10k:.2f} 걸음 더 걸었음')

        fig, ax = plt.subplots(figsize=(12, 6))  
        ax.bar(sorted_dates, sorted_steps, label='steps')
        ax.set_xlabel('Date')
        ax.set_ylabel('Steps')
        ax.set_title('24Years Average Steps')
        ax.legend()

        ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
        plt.xticks(rotation=45)
        
        ax.tick_params(axis='x', labelsize=8)  

        canvas = FigureCanvas(fig)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(canvas)
        canvas.draw()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    apply_stylesheet(app, theme='light_teal_500.xml')
    
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()
