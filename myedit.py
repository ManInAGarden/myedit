import sys
import os.path as path
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *

from languagedialog import *


class MyEdit(QMainWindow):
    lexer_extension_dict = {"py": QsciLexerPython,
                            "cs": QsciLexerCSharp,
                            "css": QsciLexerCSS,
                            "bat": QsciLexerBatch,
                            "xml": QsciLexerXML,
                            "js": QsciLexerJavaScript,
                            "jav": QsciLexerJava,
                            "sql": Qsci.QsciLexerSQL,
                            "html": QsciLexerHTML,
                            "htm": QsciLexerHTML}

    def __init__(self, parent=None, filename=None):
        super().__init__(parent)
        self.make_gui()
        self.current_file_name = filename
        self.loaded()

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

        edit_actions = []
        edit_actions.append(self.make_action(name="&Einfügen",
                                     statusTip="Text einfügen",
                                     callback=self.paste,
                                     shortCut="Ctrl+V"))

        edit_actions.append(self.make_action(name="&Ausschneiden",
                                     statusTip="Text ausschneiden",
                                     callback = self.cut,
                                     shortCut="Ctrl+X"))

        edit_actions.append(self.make_action(name="&Kopieren",
                                     statusTip="Text kopieren",
                                     callback = self.copy,
                                     shortCut="Ctrl+C"))

        extra_actions = []
        extra_actions.append(self.make_action(name="&Syntaxeinfärbung",
                                             statusTip="Sprache für Syntaxeinfärbung einstellen",
                                             callback=self.set_lexer))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addActions(fileActions)
        
        editMenu = menubar.addMenu("&Bearbeiten")
        editMenu.addActions(edit_actions)

        extrasMenu = menubar.addMenu("&Extras")
        extrasMenu.addActions(extra_actions)

        self.text = QsciScintilla()
        self.setCentralWidget(self.text)
        self.do_text_settings(self.text)

    def loaded(self):
        if self.current_file_name is not None:
            self.read_from_file(self.current_file_name)

    def do_text_settings(self, text):
        lex = QsciLexerPython()
        text.setTabWidth(4)
        text.setUtf8(True)
        text.setLexer(lex)

        text.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        # text.setFolding()
        text.setIndentationWidth(4)
        text.setIndentationGuides(True)
        text.setAutoIndent(True)
        text.setAutoCompletionSource(QsciScintilla.AcsAll);
        text.setAutoCompletionThreshold(2)

        # brace matching
        text.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        text.setMarginsFont(font)
        fontmetrics = QFontMetrics(font)
        text.setMarginWidth(0, fontmetrics.width("00000") + 6)
        text.setMarginLineNumbers(0, True)

        text.setEolVisibility(True)

        # default seems to be operating system dependent which woul dbe nice
        # text.setEolMode(QsciScintilla.EolMac)
        # print(text.eolMode())


    def new_file(self):
        self.text.setText("")

    def open_file(self):
        fname, whatever = QFileDialog.getOpenFileName(self, 'Datei öffnen', '/home')
        self.read_from_file(fname)

    def read_from_file(self, fname):
        f = open(fname, 'r')
        with f:
            data = f.read()
            self.text.setText(data)
            print(self.text.eolMode())
            path_parts = path.splitext(fname)
            if len(path_parts) > 1:
                lex = self.get_lexer_from_ext(path_parts[1])
                if not lex is None:
                    self.text.setLexer(lex)

        self.set_curr_file(fname)


    def get_lexer_from_ext(self, ext):
        answ = None
        if ext.startswith("."):
            myext = ext[1:].lower()
        else:
            myext = ext.lower()

        if myext in self.lexer_extension_dict:
            answ = self.lexer_extension_dict[myext]()

        return answ

    def set_curr_file(self, fname):
        self.current_file_name = fname
        self.setWindowTitle(fname)

    def save_text(self, filename):
        f = open(filename, "w")
        print(self.text.eolMode())
        with f:
            f.write(self.text.text())
            self.text.text

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
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = None

    scr = MyEdit(filename=file_name)
    scr.show()
    sys.exit(app.exec_())
