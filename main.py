from PyQt5 import QtWidgets, uic
from qt_material import apply_stylesheet


main_ui = 'mainGUI.ui'
bmi_ui = 'bmiCal.ui'
graph_ui = 'graphPlot.ui'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(main_ui, self)

        self.bmiCalButton.clicked.connect(self.open_bmi_cal)
        self.walkingButton.clicked.connect(self.open_diet)
        self.graphPlotButton.clicked.connect(self.open_graph_plot)
        self.inforBtn.clicked.connect(self.open_inforBtn)

        self.label.setStyleSheet("font-size: 20px; ")

    
    def open_bmi_cal(self):
        from bmiCal import WindowClass
        self.bmi_window = WindowClass()
        self.bmi_window.show()
    
    def open_diet(self):
        from diet import WindowClass
        self.diet_window = WindowClass()
        self.diet_window.show()

    def open_graph_plot(self):
        from graph import WindowClass
        self.graph_window = WindowClass()
        self.graph_window.show()

    def open_inforBtn(self):
        from information import WindowClass
        self.infor_window = WindowClass()
        self.infor_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    apply_stylesheet(app, theme='light_teal_500.xml')
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
