import os
import tempfile
import barcode
import win32print
from PyQt5 import QtWidgets, uic
from printer import sent_to_device


#functions:
def printers_list():
    PRINTERS = win32print.EnumPrinters ( win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    res = [printer[2] for printer in PRINTERS]
    return res


def create_barcode(data):
    ean = barcode.get('Code128', str(data), writer=barcode.writer.ImageWriter())
    ean.save(tempfile.gettempdir() + r"\barcode", {"module_width":0.25, "module_height":5, "font_size": 14, "text_distance": 3, "quiet_zone": 3})


#GUI
app = QtWidgets.QApplication([])
ui = uic.loadUi("skin.ui")
ui.comboBox.addItems(printers_list())
ui.spinBox.setRange(1, 20)


def main():
    device_selected = ui.comboBox.currentText()
    raw_label = ui.lineEdit.text()
    counter = int(ui.spinBox.text())
    if raw_label == '':
        ui.statusbar.showMessage("Введіть партію!", 0)
        return
    create_barcode(raw_label)
    barcode_path = os.path.join(tempfile.gettempdir(), 'barcode.png')
    while counter > 0:
        sent_to_device(barcode_path,device_selected)
        counter -= 1
    ui.lineEdit.clear()
    ui.spinBox.setValue(1)
    ui.statusbar.showMessage("Готово", 0)


ui.pushButton.clicked.connect(main)


ui.show()
app.exec_()
