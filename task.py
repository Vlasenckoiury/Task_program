import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


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

    def connect(self):  # Подключение к бд
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=os.getenv('PORT')
            )
        except psycopg2.DatabaseError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise e

    def close(self):  # Закрывает соединение с базой данных.
        if self.connection:
            self.connection.close()

    def query(self, sql):  # Выполняет SQL запрос и возвращает данные.
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def save_product(self, name, price, quantity, category_id):  # Добавление продукта в бд
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO task (name, price, quantity, category_id) VALUES (%s, %s, %s, %s)",
                    (name, price, quantity, category_id)
                )
                self.connection.commit()
                print("Продукт успешно добавлен в базу данных.")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при сохранении с PostgreSQL:", error)

    def update_database(self, row_id, column, new_value):
        column_mapping = {
            0: 'id',
            1: 'name',
            2: 'price',
            3: 'quantity',
            4: 'category_id',
        }
        column_name = column_mapping.get(column)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE task SET {column_name} = %s WHERE id = %s", (new_value, row_id))
                self.connection.commit()
                print("Данные сохранены")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при обновлении с PostgreSQL:", error)
            self.connection.rollback()

    def delete_task(self, task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
                self.connection.commit()
                print("Запись успешно удалена")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при удалении с PostgreSQL:", error)
            self.connection.rollback()


class ProductForm(QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1191, 657)
        MainWindow.setMouseTracking(False)
        MainWindow.setWindowTitle("My Form")
        MainWindow.setWindowIcon(QIcon('icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(30, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.name.setFont(font)
        self.name.setText("Название")
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
        self.price.setText("Цена")
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
        self.quantity.setText("Количество")
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
        self.category.setText("Категория")
        self.category.setObjectName("category")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(210, 290, 231, 41))
        self.comboBox.setStyleSheet("font: 14pt MS Shell Dlg 2")
        self.comboBox.setObjectName("comboBox")
        self.load_categories()

        self.pushButtonAdd = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAdd.setGeometry(QtCore.QRect(30, 400, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAdd.setFont(font)
        self.pushButtonAdd.setStyleSheet("background-color: rgb(0, 255, 0);border-radius:10px")
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonAdd.setText("ADD")
        self.pushButtonAdd.clicked.connect(self.save_product)  # добавить возможность, если не введено ,заново вести,а не закрывать программу

        self.pushButtonEdit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEdit.setGeometry(QtCore.QRect(170, 400, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonEdit.setFont(font)
        self.pushButtonEdit.setText("EDIT")
        self.pushButtonEdit.setStyleSheet("background-color: rgb(255, 241, 38);border-radius:10px")
        self.pushButtonEdit.clicked.connect(self.toggle_editing)
        self.pushButtonEdit.setObjectName("pushButtonEdit")

        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(320, 400, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonDelete.setFont(font)
        self.pushButtonDelete.setStyleSheet("background-color:rgb(255, 0, 0);border-radius:10px")
        self.pushButtonDelete.clicked.connect(self.delete_task)
        self.pushButtonDelete.setText("DELETE")
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
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Количество", "Категория"])
        self.load_tasks()

        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.edit_mode_enabled = False

        MainWindow.setCentralWidget(self.centralwidget)

    def toggle_editing(self):
        self.edit_mode_enabled = not self.edit_mode_enabled
        self.set_editing_enabled(self.edit_mode_enabled)
        if self.edit_mode_enabled:
            # Включаем редактирование при нажатии кнопки "EDIT"
            self.set_editing_enabled(True)
            self.tableWidget.cellChanged.connect(self.handle_cell_changed)
        else:
            # Выключаем редактирование и сохраняем изменения при нажатии кнопки "SAVE"
            self.set_editing_enabled(False)

    def set_editing_enabled(self, enabled):
        if enabled:
            # Включаем редактирование для всей таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
            self.pushButtonEdit.setText("FINISH EDITING")
            self.pushButtonEdit.setStyleSheet("background-color:rgb(81, 255, 0);border-radius:10px")
        else:
            # Выключаем редактирование для всей таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.pushButtonEdit.setText("EDIT")
            self.pushButtonEdit.setStyleSheet("background-color: rgb(255, 241, 38);border-radius:10px")

    def handle_cell_changed(self, row, column):
        # Получаем ID строки
        id_item = self.tableWidget.item(row, 0)
        if id_item is not None:
            row_id = id_item.text()
            # Получаем новое значение
            new_value = self.tableWidget.item(row, column).text()
            # Отправляем запрос на изменение значения в базе данных
            db = Database.get_instance()
            db.update_database(row_id, column, new_value)

    def delete_task(self):
        if self.edit_mode_enabled:
            sel_row = self.tableWidget.currentRow()
            if sel_row >= 0:
                task_id = int(self.tableWidget.item(sel_row, 0).text())
                db = Database.get_instance()
                db.delete_task(task_id)
                self.load_tasks()
            else:
                print("Выберите задачу для удаления")
        else:
            print("Нельзя удалять записи в режиме просмотра")

    def save_product(self):
        try:
            name_val = self.lineName.text()
            price_val = int(self.linePrice.text())
            quantity_val = int(self.spinBox1.text())
            category_index = self.comboBox.currentIndex()
            category_id = self.comboBox.itemData(category_index)
            db = Database.get_instance()
            db.save_product(name_val, price_val, quantity_val, category_id)
            self.load_tasks()
        except Exception as e:
            print(f"Введите значение. Ошибка {e}")

    def load_categories(self):
        db = Database.get_instance()
        try:
            categories = db.query("SELECT * FROM category")
            for category_id, category in categories:
                self.comboBox.addItem(category, category_id)
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")

    def fetch_tasks(self):
        db = Database.get_instance()
        try:
            tasks = db.query("SELECT * FROM task ORDER BY id")
            return tasks
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")

    def fetch_category(self):
        db = Database.get_instance()
        try:
            categories = db.query("SELECT * FROM category ")
            return categories
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")

    def load_tasks(self):
        tasks = self.fetch_tasks()
        categories = self.fetch_category()
        row = 0
        self.tableWidget.setRowCount(len(tasks))
        category_dict = {category[0]: category[1] for category in categories}
        try:
            for task in tasks:
                for col, value in enumerate(task):
                    if col == 2:  # Проверяем второй элемент, который является id категории
                        category_id = value
                        category_name = category_dict.get(category_id, "Нет категории")
                        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task[0])))
                        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(task[1])))
                        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task[3])))
                        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(task[4])))
                        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(category_name)))
                        row += 1
        except Exception as e:
            print(f"Произошла ошибка при заполнении таблицы: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ProductForm(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
