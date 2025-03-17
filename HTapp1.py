import sys
import csv
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from scipy.stats import t
from scipy.stats import norm
from HTmodule import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyqtgraph as pg


class BoxPlotItem(pg.GraphicsObject):
    def __init__(self, pos, data, width=0.5, pen=None, brush=None):
        """
        pos: vị trí (x-axis) của box plot
        data: mảng dữ liệu (numpy array)
        width: chiều rộng của box plot
        pen: màu viền (mặc định trắng)
        brush: màu nền (mặc định: màu xanh nhạt)
        """
        pg.GraphicsObject.__init__(self)
        self.pos = pos
        self.data = data
        self.width = width
        self.pen = pen if pen is not None else pg.mkPen('black')
        self.brush = brush if brush is not None else pg.mkBrush(100, 100, 150, 150)
        self.generatePicture()
    
    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(self.pen)
        
        q1 = np.percentile(self.data, 25)
        median = np.percentile(self.data, 50)
        q3 = np.percentile(self.data, 75)
        min_val = np.min(self.data)
        max_val = np.max(self.data)
        
        rect = QtCore.QRectF(self.pos - self.width/2, q1, self.width, q3 - q1)
        p.fillRect(rect, self.brush)
        p.drawRect(rect)
        
        p.drawLine(QtCore.QPointF(self.pos - self.width/2, median),
                   QtCore.QPointF(self.pos + self.width/2, median))
        
        p.drawLine(QtCore.QPointF(self.pos, q3), QtCore.QPointF(self.pos, max_val))
        p.drawLine(QtCore.QPointF(self.pos, q1), QtCore.QPointF(self.pos, min_val))
        
        cap_width = self.width * 0.5
        p.drawLine(QtCore.QPointF(self.pos - cap_width/2, max_val),
                   QtCore.QPointF(self.pos + cap_width/2, max_val))
        p.drawLine(QtCore.QPointF(self.pos - cap_width/2, min_val),
                   QtCore.QPointF(self.pos + cap_width/2, min_val))
        p.end()
    
    def paint(self, painter, option, widget):
        painter.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        """Trả về vùng bao của đối tượng, cần để pyqtgraph biết kích thước đối tượng."""
        min_val = np.min(self.data)
        max_val = np.max(self.data)
        return QtCore.QRectF(self.pos - self.width/2 - 1, min_val, self.width+2, max_val - min_val)

class myapp(QMainWindow):
    
    def __init__(self):
        super(myapp, self).__init__()
        self.setGeometry(0,0,1920,1080)
        self.setWindowTitle("Hypothesis Testing Tool")
        self.setWindowIcon(QtGui.QIcon("logolab.png"))
        self.initUI() 
        
    def initUI(self):
        
        frame2 = QFrame(self)
        frame2.setGeometry(600, 30, 520, 430)
        frame2.setFrameShape(QFrame.Box)
        frame2.setFrameShadow(QFrame.Sunken)
        frame2.setStyleSheet("background-color: white;")
        
        self.frameplot = QtWidgets.QFrame(self)
        self.frameplot.setGeometry(1150,30,730,925)
        self.frameplot.setStyleSheet("background-color: grey;")
        
        frame1 = QFrame(self)
        frame1.setGeometry(30, 30, 600, 430)
        frame1.setFrameShape(QFrame.Box)
        frame1.setFrameShadow(QFrame.Sunken)
        frame1.setStyleSheet("background-color: white;")
        
        self.console = QTextEdit(self)
        self.console.setStyleSheet(
            "background-color: black; color: white; font-family: Courier; font-size: 15px;"
        )
        #self.console.setGeometry(1150,30,730,920)
        self.console.setGeometry(30, 515, 1090, 440)
        self.console.setReadOnly(False)
        self.console.setFocusPolicy(Qt.StrongFocus)
        self.console.installEventFilter(self)
        self.line_count = 1
        self.show_prompt()
        
        self.plotHis = pg.PlotWidget(self.frameplot)
        self.plotHis.setGeometry(0, 0, 730, 306)
    
        self.plotHis.setBackground('white')
        styles = {'color': 'w', 'font-size': '14px'}
        self.plotHis.setLabel('left', 'Frequency', **styles)
        self.plotHis.setLabel('bottom', 'Value', **styles)
        
        self.plotHis2 = pg.PlotWidget(self.frameplot)
        self.plotHis2.setGeometry(0, 310, 730, 306)
    
        self.plotHis2.setBackground('white')
        styles2 = {'color': 'w', 'font-size': '14px'}
        self.plotHis2.setLabel('left', 'Frequency', **styles)
        self.plotHis2.setLabel('bottom', 'Value', **styles)
        

        self.plotBox = pg.PlotWidget(self.frameplot)
        self.plotBox.setGeometry(0, 620, 730, 306)

        self.plotBox.setBackground('white')
        styles = {'color': 'w', 'font-size': '14px'}
        self.plotBox.setLabel('left', 'Frequency', **styles)
        self.plotBox.setLabel('bottom', 'Value', **styles)
        
        #data
       
        
        self.name = QtWidgets.QLabel(self)
        self.name.setText("Choose a file:")
        self.name.move(50,50)
        self.name.resize(200,30)
        
        self.poptype = QtWidgets.QLabel(self)
        self.poptype.setText("Choose population:")
        self.poptype.move(50,100)
        self.poptype.resize(200,30)
        
        self.testtype = QtWidgets.QLabel(self)
        self.testtype.setText("Choose test type:")
        self.testtype.move(50,150)
        self.testtype.resize(200,30)
        
        self.samtype = QtWidgets.QLabel(self)
        self.samtype.setText("Choose samples type:")
        self.samtype.move(50,200)
        self.samtype.resize(200,30)
        self.samtype.hide()
        
        self.miu = QtWidgets.QLabel(self)
        self.miu.setText("Enter miu:")
        self.miu.move(50,200)
        self.miu.resize(200,30)
        """self.miu.hide()"""
        
        self.los = QtWidgets.QLabel(self)
        self.los.setText("Enter level of significance:")
        self.los.move(50,300)
        self.los.resize(200,30)
        
        self.std1 = QtWidgets.QLabel(self)
        self.std1.setText("Enter standard deviation 1 (If not enter None ):")
        self.std1.move(50,350)
        self.std1.resize(280,30)
                
        self.std2 = QtWidgets.QLabel(self)
        self.std2.setText("Enter standard deviation 2 (If not enter None ):")
        self.std2.move(50,400)
        self.std2.resize(280,30)
        self.std2.hide()
        
        self.txtname = QtWidgets.QLabel(self)
        self.txtname.setText("Your file")
        self.txtname.move(150,50)
        self.txtname.resize(350,32)
                            
        self.txtmiu = QtWidgets.QLineEdit(self)
        self.txtmiu.move(350,200)
        self.txtmiu.resize(150,32)
        """self.txtmiu.hide()"""
        
        self.txtlos = QtWidgets.QLineEdit(self)
        self.txtlos.move(350,300)
        self.txtlos.resize(150,32)
        
        self.txtpair = QtWidgets.QLineEdit(self)
        self.txtpair.move(350,250)
        self.txtpair.resize(150,32)
        self.txtpair.hide()
        
        self.txtstd1 = QtWidgets.QLineEdit(self)
        self.txtstd1.move(350,350)
        self.txtstd1.resize(150,32)
        
        self.txtstd2 = QtWidgets.QLineEdit(self)
        self.txtstd2.move(350,400)
        self.txtstd2.resize(150,32)
        self.txtstd2.hide()
        
        self.butbrowse = QtWidgets.QPushButton(self)
        self.butbrowse.setText("Browse")
        self.butbrowse.move(500,50)
        self.butbrowse.resize(100,32)
        self.butbrowse.clicked.connect(self.browsefile)
        
        self.butcal = QtWidgets.QPushButton(self)
        self.butcal.setText("Calculate")
        self.butcal.move(970,470)
        self.butcal.resize(150,32)
        self.butcal.clicked.connect(self.click_cal)
        
        self.butsave = QtWidgets.QPushButton(self)
        self.butsave.setText("Save")
        self.butsave.move(900,470)
        self.butsave.resize(70,32)
        self.butsave.clicked.connect(self.click_save)
 
        self.resultname = QtWidgets.QLabel(self)
        self.resultname.setText("File: ")
        self.resultname.move(650,50)
        self.resultname.resize(370,30)
 
        self.pop = QComboBox(self)
        self.pop.addItems(["1 population", "2 population"])
        self.pop.move(350,100)
        self.pop.currentIndexChanged.connect(self.show_condition)
        
        self.lpop = QLabel("Selected: 1 population", self)
        self.lpop.move(650, 100)
        self.lpop.resize(200, 30)
        self.pop.currentIndexChanged.connect(self.combobox)
        
        self.type = QComboBox(self)
        self.type.addItems(["1 tail", "2 tail"])
        self.type.move(350,150)
        
        self.condi = QComboBox(self)
        self.condi.addItems(["Pair", "Independent"])
        self.condi.move(350,200)
        self.condi.currentIndexChanged.connect(self.show_condition)
        self.condi.hide()
        
        self.lcondi = QLabel("Selected: Pair", self)
        self.lcondi.move(650, 200)
        self.lcondi.resize(200, 30)
        self.condi.currentIndexChanged.connect(self.combobox)
        self.lcondi.hide()
        
        self.pair = QtWidgets.QLabel(self)
        self.pair.setText("Enter the difference: ")
        self.pair.move(50,250)
        self.pair.resize(200,30)
        self.pair.hide()
        
        self.equa = QtWidgets.QLabel(self)
        self.equa.setText("Equal VA given: ")
        self.equa.move(50,250)
        self.equa.hide()
        
        self.equalog = QComboBox(self)
        self.equalog.addItems(["Yes", "No"])
        self.equalog.move(350,250)
        self.equalog.currentIndexChanged.connect(self.show_condition)
        self.equalog.hide()
        
        self.ltype = QLabel("Type: 1 tail", self)
        self.ltype.move(650, 150)
        self.ltype.resize(200, 30)
        self.type.currentIndexChanged.connect(self.combobox)
        
        self.resultmiu = QtWidgets.QLabel(self)
        self.resultmiu.setText("Miu: ")
        self.resultmiu.move(650, 200)
        
        self.resultlos = QtWidgets.QLabel(self)
        self.resultlos.setText("Level of significance: ")
        self.resultlos.move(650, 250)
        self.resultlos.resize(200,30)
        
        self.resultstd1 = QtWidgets.QLabel(self)
        self.resultstd1.setText("Standard deviation 1: ")
        self.resultstd1.move(650,300)
        self.resultstd1.resize(300,30)
        
        self.resultstd2 = QtWidgets.QLabel(self)
        self.resultstd2.setText("Standard deviation 2: ")
        self.resultstd2.move(650,350)
        self.resultstd2.resize(300,30)
        self.resultstd2.hide()
        
    def show_condition(self):
        if self.pop.currentText() == "2 population":
            self.condi.show()
            self.samtype.show()
            self.txtmiu.hide()
            self.miu.hide()
            self.equalog.hide()
            self.equa.hide()
            self.resultmiu.hide()
            self.resultstd2.show()
            self.txtstd2.show()
            self.std2.show()
            if self.condi.currentText() == "Pair":
                self.pair.show()
                self.txtpair.show()
                self.lcondi.show()
                self.equalog.hide()
                self.equa.hide()
                self.txtstd1.hide()
                self.std1.hide()
                self.txtstd2.hide()
                self.std2.hide()
                self.resultstd1.hide()
                self.resultstd2.hide()
            else:
                self.pair.hide()
                self.txtpair.hide()
                self.equalog.show()
                self.equa.show()
                self.txtstd1.show()
                self.std1.show()
                self.txtstd2.show()
                self.std2.show()
                self.resultstd1.show()
                self.resultstd2.show()
        else:
            self.condi.hide()
            self.lcondi.hide()
            self.samtype.hide()
            self.txtmiu.show()
            self.miu.show()
            self.equalog.hide()
            self.equa.hide()
            self.pair.hide()
            self.txtpair.hide()
            self.resultmiu.show()
            self.resultstd2.hide()
            self.txtstd2.hide()
            self.std2.hide()
            self.txtstd1.show()
            self.std1.show()

            
    def combobox(self):
        selected_pop = self.pop.currentText()
        selected_type = self.type.currentText()
        selected_condi = self.condi.currentText()
        self.lpop.setText(f"Selected: {selected_pop}")
        self.ltype.setText(f"Type: {selected_type}")
        self.lcondi.setText(f"Selected: {selected_condi}")
        
    
    def click_cal(self):
        resultname = self.txtname.text()
        resultlos = self.txtlos.text()
        resultstd1 = self.txtstd1.text()
        resultstd2 = self.txtstd2.text()
        resultD = self.txtpair.text()
        if resultD == '':
            resultD = 0
        if self.pop.currentText() == "1 population":
            resultmiu = self.txtmiu.text()
        else:
            resultmiu=""
        self.resultname.setText("Name: " + str(resultname))
        if len(resultmiu)!=0:
            rm=float(resultmiu)
        self.resultmiu.setText("Miu: " + str(resultmiu))
        self.resultlos.setText("Level of significance: " + str(resultlos))
        self.resultstd1.setText("Standard deviation 1: " + str(resultstd1))
        self.resultstd2.setText("Standard deviation 2: " + str(resultstd2))
        
        
        file_path = self.txtname.text()
        mode = self.type.currentText()
        mode=mode[0]; mode = int(mode)
        alpha = float(self.txtlos.text())
        print("Mode: ",mode)
        
        arr_int1,arr_int2,arr_int3,arr_int4=readfile(file_path)
        smean1 = np.mean(arr_int1)
        smean2 = np.mean(arr_int2)
        n1=np.size(arr_int1)
        n2=np.size(arr_int2)
        print("n1: ",n1);print("n2: ",n2)
 # 387 tới 429 là code setup          
        if len(arr_int1) != 0 and len(arr_int2) != 0: #Arr1 và 2 đều tồn tại
            smean1 = np.mean(arr_int1)
            smean2 = np.mean(arr_int2)
            std1 = self.txtstd1.text()
            std2 = self.txtstd2.text()
            n1=len(arr_int1)
            choose = self.condi.currentText()
            choose = choose.lower()
            if choose == "pair":
               if n1!= n2:
                QMessageBox.critical(self, "Error", "Sample size of 2 samples need to be equal !!!")
               else:   
                muyd = smean1 - smean2
                print("Muy_d ",muyd)
                D = float(resultD)
                arr_int = arr_int1 - arr_int2
                print("Array difference: ", arr_int, "\n")
                std = np.std(arr_int, ddof=1)  # 1
                print(std)
                n = n1
            else:
                eVar = self.equalog.currentText()
        elif len(arr_int1) != 0 and len(arr_int2) == 0:  #chỉ có arr1 tồn tại
            muy = rm     ;arr_int1 = arr_int1  # Đảm bảo giá trị không thay đổi
            arr_int2 = []
            std1 = self.txtstd1.text()  # Lấy giá trị từ input của người dùng
            if std1.strip().lower() == "none" or not std1.strip():  # Nếu giá trị là "none" hoặc rỗng
                std1 = "none"
            else:
                try:
                    std1 = float(std1)  # Chuyển đổi thành số thực
                except ValueError:
                    QMessageBox.critical(self, "Error", "Standard deviation must be a numeric value or 'None'.")
                    return
            std2 = 0 #
            n1 = len(arr_int1)
            n2 = 0
            smean1 = np.mean(arr_int1)  # Tính giá trị trung bình của arr_int1
            smean2 = 0  # Gán giá trị mặc định cho smean2
            choose = []
        else:
            QMessageBox.critical(self, "Error", "Please provide valid input data.")
            return

        
        if n1>=30 or std1!="none":
            if len(arr_int2) != 0 and choose=="independent":
                std1 = self.txtstd1.text()
                std2 = self.txtstd2.text()
                if std1.strip().lower()=="none" and std2.strip().lower()=="none" and n2>=30:
                    std1=np.std(arr_int1,ddof=1) #2
                    std2=np.std(arr_int2,ddof=1) #3
                    y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
                    print(y.indeZ())
                    a = y.indeZ()
                else:
                    if std1.strip().lower()!="none" and std2.strip().lower()!="none":
                        std1=float(std1);std=float(std2)
                        y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
                        print(y.indeZ())
                        a = y.indeZ()
                    else:
                        evar="No" #Dù 2 thg n1,n2 đều >=30, nmà có 1 trong 2 sigma chx bik ==> T-test với evar k bằng nhau
                        if std1.strip().lower()=="none":
                            std1=np.std(arr_int1,ddof=1)
                        else:
                            std2=np.std(arr_int2,ddof=1)
                        y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
                        print(y.indeT(eVar))
                        a = y.indeT(eVar)
                for i in a:
                    self.console.append(i)
                    
            elif (n2>=30 or std2!=0) and choose=="pair":
#Cái này k cần bik std 1 và std2, bỏ UI ở std1 và std2 đi, thay là if dif có nhập hay k, nếu k nhập thì tự tính từ diff
                std_diff =self.txtpair.text()
                if std_diff.strip().lower() =="none":
                    std_diff = np.std(arr_int,ddof=1)
                else:
                    std_diff=float(std_diff)
                y=depend(muyd,D,std_diff,n,mode,alpha)
                print(y.zdepend())
                a = y.zdepend()
                for i in a:
                    self.console.append(i)
            elif n2==0:
                std1 = self.txtstd1.text()
                if std1=="none":
                    std1=np.std(arr_int1,ddof=1) #6 #ddof=1 là sample std, ddof=0 là population std
                else:
                    std1=float(std1)
                y=Onepopu(muy,alpha,std1,n1,smean1,mode)
                print(y.onep_zdis())
                a = y.onep_zdis()
                for i in a:
                    self.console.append(i)
        elif n1<30 and std1=="none" and n2!=0:
            std1=np.std(arr_int1,ddof=1) #4
            std2=np.std(arr_int1,ddof=1) #5
            if choose=="independent":
                y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
                print(y.indeT(eVar))
                a = y.indeT(eVar)
                for i in a:
                    self.console.append(i)
            else: #choose==pair
                std_diff = np.std(arr_int,ddof=1)
                y=depend(muyd,D,std_diff,n,mode,alpha)
                print(y.tdepend())
                a = y.tdepend()
                for i in a:
                    self.console.append(i)

        else: #if n1<30 and n2==0
            std1=np.std(arr_int1,ddof=1)
            print("Sample std: ",std1)
            self.console.append(f"Sample std: {std1}")
            y=Onepopu(muy,alpha,std1,n1,smean1,mode)
            print(y.onep_tdis())
            a = y.onep_tdis()
            for i in a:
                self.console.append(i)
        
        hist, bins = np.histogram(arr_int1, bins=30)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        bar_color = pg.mkBrush(27, 136, 207)
        bg = pg.BarGraphItem(x=bin_centers, height=hist, width=bins[1]-bins[0], brush=bar_color)
        self.plotHis.addItem(bg)
          
        if len(arr_int2)!=0:
            hist, bins = np.histogram(arr_int2, bins=30)
            bin_centers = (bins[:-1] + bins[1:]) / 2
            bar_color = pg.mkBrush(27, 136, 207)
            bg = pg.BarGraphItem(x=bin_centers, height=hist, width=bins[1]-bins[0], brush=bar_color)
            self.plotHis2.addItem(bg)
        
            box1 = BoxPlotItem(1, arr_int1, width=0.5, brush=pg.mkBrush(46, 204, 113, 150))
            box2 = BoxPlotItem(2, arr_int2, width=0.5, brush=pg.mkBrush(52, 152, 219, 150))
            self.plotBox.addItem(box1)
            self.plotBox.addItem(box2)
        
            self.plotBox.setXRange(0, 4)
            self.plotBox.enableAutoRange(axis='y')
        else:
            self.plotHis2.clear()
            self.plotBox.clear()
    def click_save(self):
        pass
            
    def browsefile(self):
       file=QFileDialog.getOpenFileName()
       self.txtname.setText(str(file[0]))
       self.resultname.setText(f"Name: {str(file[0])}")
       
    def show_prompt(self):
        self.console.append(f"In [{self.line_count}]: ")
        self.move_cursor_to_end()
        
    def move_cursor_to_end(self):
        cursor = self.console.textCursor()
        cursor.movePosition(cursor.End)
        self.console.setTextCursor(cursor)

    def handle_input(self, user_input):
        result = f"Out [{self.line_count}]: You entered '{user_input.strip()}'"
        self.console.append(result)
        
        self.line_count += 1
        self.show_prompt()

    def eventFilter(self, source, event):
        if source == self.console and event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            cursor = self.console.textCursor()
            cursor.movePosition(cursor.StartOfBlock, cursor.KeepAnchor)

            current_line = cursor.selectedText()

            if current_line.startswith(f"In [{self.line_count}]:"):
                user_input = current_line[len(f"In [{self.line_count}]: "):]
                self.handle_input(user_input)

            return True

        return super().eventFilter(source, event)
       


def window():
    app = QApplication(sys.argv)
    win = myapp()
    appplot = QtWidgets.QApplication(sys.argv)
    win.show()
    sys.exit(app.exec_())
    
window()
