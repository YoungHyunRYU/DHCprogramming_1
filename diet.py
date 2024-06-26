from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QComboBox, QLCDNumber, QPushButton, QCheckBox, QButtonGroup
from qt_material import apply_stylesheet
from PyQt5 import uic,QtWidgets
import config

form_class = uic.loadUiType("diet.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super(WindowClass, self).__init__()
        uic.loadUi('diet.ui', self)

        # 위젯 연결
        self.weightInput = self.findChild(QLineEdit, 'weightInput')
        self.heightInput = self.findChild(QLineEdit, 'heightInput')
        self.selectGender = self.findChild(QComboBox, 'selectGender')
        self.appropriateWeight = self.findChild(QLCDNumber, 'appropriateWeight')
        self.consumedCal = self.findChild(QLCDNumber, 'consumedCal')
        self.carbohydrateLCD = self.findChild(QLCDNumber, 'carbohydrateLCD')
        self.proteinLCD = self.findChild(QLCDNumber, 'proteinLCD')
        self.fatLCD = self.findChild(QLCDNumber, 'fatLCD')
        self.sendData = self.findChild(QPushButton, 'sendData')

        self.noExercise = self.findChild(QCheckBox, 'noExercise')
        self.normalExercise = self.findChild(QCheckBox, 'normalExercise')
        self.hardExercise = self.findChild(QCheckBox, 'hardExercise')

        self.exerciseGroup = QButtonGroup(self)
        self.exerciseGroup.addButton(self.noExercise)
        self.exerciseGroup.addButton(self.normalExercise)
        self.exerciseGroup.addButton(self.hardExercise)
        self.exerciseGroup.setExclusive(True)

        self.label.setStyleSheet("font-size: 22px;")
        self.noExercise.setStyleSheet("font-size: 16px; ")
        self.normalExercise.setStyleSheet("font-size: 16px;")
        self.hardExercise.setStyleSheet("font-size: 16px;")
        self.heightInput.setStyleSheet("font-size: 20px;")

        if self.selectGender.count() == 0:
            self.selectGender.addItems(["남성", "여성"])

        self.sendData.clicked.connect(self.check_nutrition)

        self.heightInput.setText(str(config.get_key()))

    def check_nutrition(self):
        height_cm = self.heightInput.text()
        gender = self.selectGender.currentText()

        try:
            height_m = float(height_cm) / 100.0
            if gender == "남성":
                appropriate_weight = height_m ** 2 * 22
            else:  # "여성"
                appropriate_weight = height_m ** 2 * 21

            self.appropriateWeight.display(appropriate_weight)

            if self.noExercise.isChecked():
                consumed_calories = appropriate_weight * 25
            elif self.normalExercise.isChecked():
                consumed_calories = appropriate_weight * 30
            elif self.hardExercise.isChecked():
                consumed_calories = appropriate_weight * 35
            else:
                consumed_calories = 0

            self.consumedCal.display(consumed_calories)

            # 비율에 따라 섭취 칼로리 분배 탄단지 6:2:2
            carbohydrate_cal = consumed_calories * 0.6
            protein_cal = consumed_calories * 0.2
            fat_cal = consumed_calories * 0.2

            self.carbohydrateLCD.display(carbohydrate_cal)
            self.proteinLCD.display(protein_cal)
            self.fatLCD.display(fat_cal)
            
        except ValueError:
            self.appropriateWeight.display(0)
            self.consumedCal.display(0)
            self.carbohydrateLCD.display(0)
            self.proteinLCD.display(0)
            self.fatLCD.display(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    apply_stylesheet(app, theme='light_teal_500.xml')
    
    main_window = WindowClass()
    main_window.show()
    sys.exit(app.exec_())