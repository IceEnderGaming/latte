import sys
import sqlite3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from coffee import Coffee
from addEdit import addEdit
from PyQt5 import QtGui
from PyQt5 import uic


class Expresso(QMainWindow, Coffee):
    def __init__(self):
        super().__init__()
        QtGui.QFontDatabase.addApplicationFont(fr'VAG_WORLD.ttf')
        self.setupUi(self)
        self.show_table()
        self.change.clicked.connect(self.openEdit)

    def openEdit(self):
        global ex
        ex = AddEdit()
        ex.show()

    def load_from_db(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        coffee = [list(i) for i in cur.execute("SELECT * FROM coffee").fetchall()]
        return coffee

    def show_table(self):
        coffee = self.load_from_db()
        for k, i in enumerate(coffee):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(i[1::]):
                self.tableWidget.setItem(k, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


class AddEdit(QMainWindow, addEdit):
    def __init__(self):
        super().__init__()
        QtGui.QFontDatabase.addApplicationFont(fr'VAG_WORLD.ttf')
        self.setupUi(self)
        self.add.clicked.connect(self.add_in_db)
        self.confirm.clicked.connect(self.edit_in_db)

    def add_in_db(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute(f"""
        INSERT INTO coffee(variety, roasting, type, taste, price, volume) 
        VALUES('{self.addName.toPlainText()}', '{self.addStep.toPlainText()}', '{self.addSern.toPlainText()}', 
        '{self.addTaste.toPlainText()}', '{self.addPrice.toPlainText()}', '{self.addOb.toPlainText()}')"""
                    )
        con.commit()
        global ex
        ex = Expresso()
        ex.show()

    def edit_in_db(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute(f"""
        UPDATE coffee SET variety='{self.changeName.toPlainText()}', roasting='{self.changeStep.toPlainText()}', 
        type='{self.changeSern.toPlainText()}', taste='{self.changeTaste.toPlainText()}', 
        price='{self.changePrice.toPlainText()}', volume='{self.changeOb.toPlainText()}'
        WHERE id={int(self.changeId.toPlainText())}"""
                    )
        con.commit()
        global ex
        ex = Expresso()
        ex.show()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Expresso()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
