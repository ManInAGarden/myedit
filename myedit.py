import sys
import os.path as path
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *

from languagedialog import *


class MyEdit(QMainWindow):
    lexer_extension_dict = {"py": QsciLexerPython,
                            "cs": QsciLexerCSharp,
                            "css": QsciLexerCSS,
                            "bat": QsciLexerBatch,
                            "xml": QsciLexerXML}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.make_gui()
        self.current_file_name = None

    def make_action(self, name="&ClickMe", shortCut=None, statusTip="Click Me Test Entry", callback=None ):
        action = QAction(name, self)
        if not shortCut is None:
            action.setShortcut(shortCut)

        if not statusTip is None:
            action.setStatusTip(statusTip)
            
        action.triggered.connect(callback)
        return action

    def make_gui(self):
        self.setWindowTitle("MyEdit")
        self.statusBar().showMessage('')

        # lex = QsciLexerJavaScript()

        fileActions = []
        fileActions.append(self.make_action(name="&Neu", shortCut="Ctrl+N",
                                  statusTip="Neuer Text",
                                  callback=self.new_file))

        fileActions.append(self.make_action(name="&Öffnen", shortCut="Ctrl+O",
                                  statusTip="Text aus Datei laden",
                                  callback=self.open_file))

        fileActions.append(self.make_action(name="&Sichern", shortCut="Ctrl+S",
                                  statusTip="Text sichern",
                                  callback=self.save_file))

        fileActions.append(self.make_action(name="Sichern &als...",
                                  statusTip="Text sichern unter anderem Namen",
                                  callback=self.save_as))

        fileActions.append(self.make_action(name="&Beenden", shortCut="Ctrl+Q",
                                  statusTip="MyEdit beenden",
                                  callback=qApp.quit))

        editActions = []
        editActions.append(self.make_action(name="&Einfügen",
                                     statusTip="Text einfügen",
                                     callback = self.paste,
                                     shortCut="Ctrl+V"))

        editActions.append(self.make_action(name="&Ausschneiden",
                                     statusTip="Text ausschneiden",
                                     callback = self.cut,
                                     shortCut="Ctrl+X"))

        editActions.append(self.make_action(name="&Kopieren",
                                     statusTip="Text kopieren",
                                     callback = self.copy,
                                     shortCut="Ctrl+C"))

        extraActions = []
        extraActions.append(self.make_action(name="&Syntaxeinfärbung",
                                             statusTip="Sprache für Syntaxeinfärbung einstellen",
                                             callback=self.set_lexer))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addActions(fileActions)
        
        editMenu = menubar.addMenu("&Bearbeiten")
        editMenu.addActions(editActions)

        extrasMenu = menubar.addMenu("&Extras")
        extrasMenu.addActions(extraActions)

        self.text = QsciScintilla()
        self.setCentralWidget(self.text)
        self.do_text_settings(self.text)

    def do_text_settings(self, text):
        lex = QsciLexerPython()
        text.setTabWidth(4)
        text.setUtf8(True)
        text.setLexer(lex)

    def new_file(self):
        self.text.setText("")

    def open_file(self):
        fname, whatever = QFileDialog.getOpenFileName(self, 'Datei öffnen', '/home')
        f = open(fname, 'r')
        with f:
            data = f.read()
            self.text.setText(data)
            path_parts = path.splitext(fname)
            if len(path_parts) > 1:
                lex = self.get_lexer_from_ext(path_parts[1])
                if not lex is None:
                    self.text.setLexer(lex)

        self.set_curr_file(fname)


    def get_lexer_from_ext(self, ext):
        answ = None
        if ext in lexer_extension_dict:
            answ = lexer_extension_dict[ext]()

        return answ

    def set_curr_file(self, fname):
        self.current_file_name = fname
        self.setWindowTitle(fname)

    def save_text(self, filename):
        f = open(filename, "w")

        with f:
            f.write(self.text.text())

        self.set_curr_file(filename)

    def save_file(self):
        if self.current_file_name is None:
            self.save_as()
        else:
            self.save_text(self.current_file_name)

    def save_as(self):
        fname, whatever = QFileDialog.getSaveFileName(self, "Datei sichern", "\home")
        self.save_text(fname)

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def set_lexer(self):
        lang_dia = LanguageDialog()
        ret = lang_dia.exec_()
        if ret == QDialog.Accepted:
            lexer = lang_dia.get_lexer()
            self.text.setLexer(lexer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scr = MyEdit()
    scr.show()
    sys.exit(app.exec_())
