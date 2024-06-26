from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QComboBox, QLCDNumber, QPushButton, QCheckBox, QButtonGroup
from qt_material import apply_stylesheet
from PyQt5 import uic,QtWidgets
import webbrowser

form_class = uic.loadUiType("information.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super(WindowClass, self).__init__()
        uic.loadUi('information.ui', self)

        self.btn1.clicked.connect(lambda: webbrowser.open('https://www.diabetes.or.kr/general/exercise/exercise_01.php'))
        self.btn2.clicked.connect(lambda: webbrowser.open('https://general.kosso.or.kr/html/'))
        self.btn3.clicked.connect(lambda: webbrowser.open('https://younghyunryu.github.io/examWeb/'))
        self.btn4.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/@thankyoububu'))
        self.label.setStyleSheet("font-size: 15px; ")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    apply_stylesheet(app, theme='light_teal_500.xml')
    
    main_window = WindowClass()
    main_window.show()
    sys.exit(app.exec_())