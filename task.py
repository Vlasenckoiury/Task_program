import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import psycopg2


class ProductForm(QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1191, 657)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit_name = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_name.setGeometry(QtCore.QRect(30, 80, 158, 39))
        self.textEdit_name.setObjectName("textEdit_name")

        self.lineName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineName.setGeometry(QtCore.QRect(210, 80, 231, 41))
        self.lineName.setObjectName("lineName")

        self.textEdit_price = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_price.setGeometry(QtCore.QRect(30, 150, 158, 39))
        self.textEdit_price.setObjectName("textEdit_price")

        self.linePrice = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrice.setGeometry(QtCore.QRect(210, 150, 231, 41))
        self.linePrice.setObjectName("linePrice")

        self.textEdit_quantity = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_quantity.setGeometry(QtCore.QRect(30, 220, 158, 39))
        self.textEdit_quantity.setObjectName("textEdit_quantity")

        self.spinBox1 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox1.setGeometry(QtCore.QRect(210, 220, 231, 41))
        self.spinBox1.setObjectName("spinBox1")

        self.textEdit_category = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_category.setGeometry(QtCore.QRect(30, 290, 158, 41))
        self.textEdit_category.setObjectName("textEdit_category")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(210, 290, 231, 41))
        self.comboBox.setObjectName("comboBox")

        self.pushButtonAdd = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAdd.setGeometry(QtCore.QRect(30, 400, 121, 51))
        self.pushButtonAdd.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonAdd.clicked.connect(self.save_product)

        self.pushButtonEdit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEdit.setGeometry(QtCore.QRect(170, 400, 131, 51))
        self.pushButtonEdit.setObjectName("pushButtonEdit")

        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(320, 400, 121, 51))
        self.pushButtonDelete.setStyleSheet("background-color:rgb(255, 0, 0)")
        self.pushButtonDelete.setObjectName("pushButtonDelete")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(480, 80, 661, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("My Form", "My Form"))
        MainWindow.setWindowIcon(QIcon('icon.png'))
        self.textEdit_quantity.setHtml(_translate("MainWindow",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Количество</span></p></body></html>"))
        self.textEdit_category.setHtml(_translate("MainWindow",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Категория</span></p></body></html>"))
        self.textEdit_price.setHtml(_translate("MainWindow",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                               "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Цена</span></p></body></html>"))
        self.textEdit_name.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Название</span></p></body></html>"))
        self.pushButtonAdd.setText(_translate("MainWindow", "ADD"))
        self.pushButtonEdit.setText(_translate("MainWindow", "EDIT"))
        self.pushButtonDelete.setText(_translate("MainWindow", "DELETE"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Название"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Цена"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Количество"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Категория"))

    #
    def save_product(self):
        name_val = self.lineName.text()
        price_val = int(self.linePrice.text())
        quantity_val = int(self.spinBox1.text())
        category_val = int(self.comboBox.text())

        try:
            conn = psycopg2.connect(
                dbname="task",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO task (name, price, quantity, category_id) VALUES ( %s, %s, %s, %s)",
                           (name_val, price_val, quantity_val, category_val))
            conn.commit()
            conn.close()
            print("Продукт успешно добавлен в базу данных.")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL:", error)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ProductForm(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
