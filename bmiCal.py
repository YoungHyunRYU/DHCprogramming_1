# import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import config
from qt_material import apply_stylesheet

form_class = uic.loadUiType("bmiCal.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super(WindowClass, self).__init__()
        uic.loadUi('bmiCal.ui', self)

        self.horizontalSlider_height.valueChanged.connect(self.update_height)
        self.horizontalSlider_Weight.valueChanged.connect(self.calculateBMI)

        initial_height = config.get_key()
        self.horizontalSlider_height.setValue(int(initial_height))
        self.label_HeightValue.setText(f"{initial_height} cm")

        self.labelColor.setStyleSheet("font-size: 18px;")
        self.label_Title.setStyleSheet("font-size: 25px; ")
        self.label_height.setStyleSheet("font-size: 20px;")
        self.label_weight.setStyleSheet("font-size: 20px;")
        self.label.setStyleSheet("font-size: 18px;")
        self.label_HeightValue.setStyleSheet("font-size: 17px;")
        self.label_WeightValue.setStyleSheet("font-size: 17px;")
        self.resultLabel.setStyleSheet("font-size: 18px;")


    def update_height(self):
        height = self.horizontalSlider_height.value()
        self.label_HeightValue.setText(f"{height} cm")
        config.set_key(height)
        self.calculateBMI()

    def calculateBMI(self):
        height = self.horizontalSlider_height.value() / 100.0
        weight = self.horizontalSlider_Weight.value()
        bmi = weight / (height ** 2)

        self.label_HeightValue.setText(f"{height * 100} cm")
        self.label_WeightValue.setText(f"{weight} kg")

        self.lcdNumber.display(round(bmi, 1))

        if bmi < 18.5:
            result = "저체중"
        elif 18.5 <= bmi < 22.9:
            result = "정상 체중"
        elif 23 <= bmi < 24.9:
            result = "과체중"
        elif 25 <= bmi < 29.9:
            result = "1단계 비만❗"
        elif 30 <= bmi < 34.9:
            result = "2단계 비만❗❗"
        else:
            result = "3단계 비만❗❗❗"

        self.labelColor.setText(result)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_teal_500.xml')

    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
