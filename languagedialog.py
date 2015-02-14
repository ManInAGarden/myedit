import inspect
from PyQt5.QtWidgets import *
import PyQt5.Qsci as Qsci


class LanguageDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.make_gui()
        self.loaded()

    def make_gui(self):
        self.setWindowTitle("Sprache für Syntaxhervorhebung")
        grid = QGridLayout()
        self.setLayout(grid)
        self.list = QListWidget()
        grid.addWidget(self.list, 0, 0, 1, 2)

        self.ok_bu = QPushButton("OK")
        self.ok_bu.clicked.connect(self.accept)
        self.cancel_bu = QPushButton("Abbrechen")
        self.cancel_bu.clicked.connect(self.reject)
        grid.addWidget(self.ok_bu, 1, 0)
        grid.addWidget(self.cancel_bu, 1, 1)

    def get_lexer(self):
        lexer_item = self.list.currentItem()
        # print("Lexer-name:", lexer_name)
        lexer_name = lexer_item.data(0)
        Lexer = getattr(Qsci, lexer_name)
        return  Lexer()

    def exec_(self, current=None):
        return super().exec_()

    def make_action(self, name="&ClickMe", shortCut=None, callback=None ):
        action = QAction(name, self)
        if not shortCut is None:
            action.setShortcut(shortCut)

        action.triggered.connect(callback)
        return action

    def ok_cb(self):
        self.accept()

    def loaded(self):
        print("loaded")
        for name, value in inspect.getmembers(Qsci):
            #print(cls)
            if inspect.isclass(value):
                cls = value
                if issubclass(cls, Qsci.QsciLexer):
                    self.list.addItem(cls.__name__)

