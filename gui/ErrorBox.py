import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'



class ErrorBox(QMessageBox):
    
    def __init__(self, error_e, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Critical)
        self.setText('<b>An error has ocurred!</b>')
        self.setInformativeText(str(error_e))
        self.setWindowTitle('Error!')


if __name__ == '__main__':
    app = QApplication([])
    widget = ErrorBox('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porta est interdum, vulputate metus et, bibendum dui. Nunc fermentum tincidunt mi nec semper')
    widget.show()
    sys.exit(app.exec_())