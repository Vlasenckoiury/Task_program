import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
import psycopg2


class Database:
    _instance = None

    def __init__(self):
        if Database._instance is None:
            Database._instance = self
            self.connection = None
            self.connect()
        else:
            raise Exception("You cannot create another Database class")

    @staticmethod
    def get_instance():
        if not Database._instance:
            Database()
        return Database._instance

    def connect(self):
        """Подключается к базе данных."""
        try:
            self.connection = psycopg2.connect(
                dbname="task",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
        except psycopg2.DatabaseError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise e

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()

    def query(self, sql):
        """Выполняет SQL запрос и возвращает данные."""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def save_product(self, name, price, quantity, category_id):
        """Добавляет продукт в базу данных."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO task (name, price, quantity, category_id) VALUES (%s, %s, %s, %s)",
                    (name, price, quantity, category_id)
                )
                self.connection.commit()
                print("Продукт успешно добавлен в базу данных.")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL:", error)
            self.connection.rollback()


class ProductForm(QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1191, 657)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(30, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.name.setFont(font)
        self.name.setObjectName("name")

        self.lineName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineName.setGeometry(QtCore.QRect(210, 80, 231, 41))
        self.lineName.setStyleSheet("font: 14pt MS Shell Dlg 2")
        self.lineName.setObjectName("lineName")

        self.price = QtWidgets.QLabel(self.centralwidget)
        self.price.setGeometry(QtCore.QRect(30, 150, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.price.setFont(font)
        self.price.setObjectName("price")

        self.linePrice = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrice.setGeometry(QtCore.QRect(210, 150, 231, 41))
        self.linePrice.setStyleSheet("font: 14pt MS Shell Dlg 2")
        self.linePrice.setObjectName("linePrice")

        self.quantity = QtWidgets.QLabel(self.centralwidget)
        self.quantity.setGeometry(QtCore.QRect(30, 220, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.quantity.setFont(font)
        self.quantity.setObjectName("quantity")

        self.spinBox1 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox1.setGeometry(QtCore.QRect(210, 220, 231, 41))
        self.spinBox1.setStyleSheet("font: 14pt MS Shell Dlg 2")
        self.spinBox1.setMaximum(100000000)
        self.spinBox1.setObjectName("spinBox1")

        self.category = QtWidgets.QLabel(self.centralwidget)
        self.category.setGeometry(QtCore.QRect(30, 290, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.category.setFont(font)
        self.category.setObjectName("category")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(210, 290, 231, 41))
        self.comboBox.setObjectName("comboBox")
        self.load_categories()

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

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 350, 151, 41))
        self.label.setMouseTracking(True)
        self.label.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")

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
        self.name.setText(_translate("MainWindow", "Название"))
        self.price.setText(_translate("MainWindow", "Цена"))
        self.quantity.setText(_translate("MainWindow", "Количество"))
        self.category.setText(_translate("MainWindow", "Категория"))

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

    def save_product(self):
        name_val = self.lineName.text()
        price_val = int(self.linePrice.text())
        quantity_val = int(self.spinBox1.text())
        category_index = self.comboBox.currentIndex()
        category_id = self.comboBox.itemData(category_index)
        db = Database.get_instance()
        db.save_product(name_val, price_val, quantity_val, category_id)

    def load_categories(self):
        db = Database.get_instance()
        try:
            categories = db.query("SELECT * FROM category")
            for category_id, category in categories:
                self.comboBox.addItem(category, category_id)
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ProductForm(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
