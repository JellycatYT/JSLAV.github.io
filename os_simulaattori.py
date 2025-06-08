import sys, os, random, importlib.util
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Yritetään tuoda pygame musan soittoa varten
try:
    import pygame
    HAVE_PYGAME = True
    pygame.mixer.init()
except Exception:
    HAVE_PYGAME = False

ICON_MAP = {
    "Calculator": "icons/calculator.png",
    "Notepad": "icons/notepad.png",
    "Games": "icons/games.png",
    "Browser": "icons/browser.png",
    "YouTube": "icons/youtube.png",
    "Music": "icons/music.png",
    "ImportPy": "icons/importpy.png",
    "Folder": "icons/folder.png",
    "TicTacToe": "icons/tictactoe.png",
    "GuessNumber": "icons/guess.png",
    "Background": "icons/background.png",
    "SisuCompiler": "icons/sisu.png"
}

EMOJI_MAP = {
    "Calculator": "🧮",
    "Notepad": "📝",
    "Games": "🎮",
    "Browser": "🌐",
    "YouTube": "▶️",
    "Music": "🎵",
    "ImportPy": "⬇️",
    "Folder": "📁",
    "TicTacToe": "❎",
    "GuessNumber": "❓",
    "Background": "🌄",
    "SisuCompiler": "🦾"
}

def get_icon(name, fallback="icons/folder.png"):
    path = ICON_MAP.get(name, fallback)
    if os.path.exists(path):
        return QIcon(path)
    return None

class DesktopIcon(QPushButton):
    def __init__(self, key, icon, callback, parent=None):
        super().__init__("", parent)
        self.setFixedSize(100, 100)
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(56, 56))
            self.setText("")
        else:
            emoji = EMOJI_MAP.get(key, "❓")
            self.setText(emoji)
            self.setFont(QFont("Arial", 36))
        self.setStyleSheet("QPushButton {background: #f9f9f9; border-radius: 20px; border: 2px solid #aaa; font-size: 15px;}")
        self.label = QLabel(key, self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.label.setGeometry(0, 70, 100, 30)
        self.clicked.connect(callback)

class BrowserApp(QDialog):
    def __init__(self, url="https://www.google.com", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Web Browser")
        self.setModal(False)
        self.setMinimumSize(900, 650)
        layout = QVBoxLayout()
        nav_layout = QHBoxLayout()
        self.urlbar = QLineEdit(url)
        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.navigate)
        nav_layout.addWidget(self.urlbar)
        nav_layout.addWidget(self.go_btn)
        layout.addLayout(nav_layout)
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(url))
        layout.addWidget(self.webview)
        self.setLayout(layout)
        self.urlbar.returnPressed.connect(self.navigate)

    def navigate(self):
        url = self.urlbar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.webview.setUrl(QUrl(url))

class NotepadApp(QDialog):
    def __init__(self, filename="notepad.txt", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notepad")
        self.setModal(False)
        self.setMinimumSize(500, 400)
        self.filename = filename
        layout = QVBoxLayout()
        self.textedit = QTextEdit()
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as f:
                self.textedit.setPlainText(f.read())
        layout.addWidget(self.textedit)
        btn_layout = QHBoxLayout()
        savebtn = QPushButton("Save")
        savebtn.clicked.connect(self.save)
        impbtn = QPushButton("Import")
        impbtn.clicked.connect(self.import_file)
        expbtn = QPushButton("Export")
        expbtn.clicked.connect(self.export_file)
        btn_layout.addWidget(savebtn)
        btn_layout.addWidget(impbtn)
        btn_layout.addWidget(expbtn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(self.textedit.toPlainText())
        QMessageBox.information(self, "Saved", "Notepad saved to " + self.filename)

    def import_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Import Text File", "", "Text Files (*.txt)")
        if fname:
            with open(fname, encoding="utf-8") as f:
                self.textedit.append(f.read())
            QMessageBox.information(self, "Imported", f"Imported from {fname}")

    def export_file(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Notepad", "export.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(self.textedit.toPlainText())
            QMessageBox.information(self, "Exported", f"Exported to {fname}")

class CalculatorApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")
        self.setModal(False)
        self.setFixedSize(320, 170)
        layout = QVBoxLayout()
        self.input = QLineEdit()
        layout.addWidget(self.input)
        calcbtn = QPushButton("Calculate")
        calcbtn.clicked.connect(self.calculate)
        layout.addWidget(calcbtn)
        self.result = QLabel("")
        layout.addWidget(self.result)
        self.setLayout(layout)

    def calculate(self):
        expr = self.input.text()
        try:
            allowed = "0123456789+-*/()., "
            if all(c in allowed for c in expr):
                self.result.setText(str(eval(expr, {"__builtins__": {}})))
            else:
                self.result.setText("Only + - * / and numbers allowed")
        except Exception:
            self.result.setText("Error")

class MusicPlayerApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Music Player")
        self.setModal(False)
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        self.nowplaying = QLabel("No file loaded")
        layout.addWidget(self.nowplaying)
        loadbtn = QPushButton("Open MIDI/MP3")
        loadbtn.clicked.connect(self.load_music)
        layout.addWidget(loadbtn)
        self.playbtn = QPushButton("Play")
        self.playbtn.clicked.connect(self.play_music)
        self.playbtn.setEnabled(False)
        layout.addWidget(self.playbtn)
        self.stopbtn = QPushButton("Stop")
        self.stopbtn.clicked.connect(self.stop_music)
        self.stopbtn.setEnabled(False)
        layout.addWidget(self.stopbtn)
        self.musicfile = None
        self.setLayout(layout)

    def load_music(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open music", "", "Audio Files (*.mp3 *.mid *.midi)")
        if fname:
            self.musicfile = fname
            self.nowplaying.setText(os.path.basename(fname))
            self.playbtn.setEnabled(True)
            self.stopbtn.setEnabled(True)
            if HAVE_PYGAME:
                pygame.mixer.music.load(fname)

    def play_music(self):
        if self.musicfile and HAVE_PYGAME:
            pygame.mixer.music.play()
        elif not HAVE_PYGAME:
            QMessageBox.warning(self, "Error", "pygame required for music playback (pip install pygame)")

    def stop_music(self):
        if HAVE_PYGAME:
            pygame.mixer.music.stop()

class GuessNumberApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guess Number")
        self.setModal(False)
        self.number = random.randint(1, 100)
        self.setFixedSize(280, 160)
        layout = QVBoxLayout()
        self.info = QLabel("Guess a number 1-100")
        self.guess = QLineEdit()
        guessbtn = QPushButton("Guess")
        guessbtn.clicked.connect(self.check)
        layout.addWidget(self.info)
        layout.addWidget(self.guess)
        layout.addWidget(guessbtn)
        self.setLayout(layout)

    def check(self):
        try:
            g = int(self.guess.text())
            if g < self.number:
                self.info.setText("Too low!")
            elif g > self.number:
                self.info.setText("Too high!")
            else:
                self.info.setText("Correct!")
        except:
            self.info.setText("Enter a number.")

class TicTacToeApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TicTacToe")
        self.setModal(False)
        self.setFixedSize(310, 340)
        layout = QVBoxLayout()
        self.turn = "X"
        self.board = [""] * 9
        self.buttons = []
        grid = QGridLayout()
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(80, 80)
            btn.setFont(QFont("Arial", 26))
            btn.clicked.connect(lambda _, idx=i: self.play(idx))
            self.buttons.append(btn)
            grid.addWidget(btn, i//3, i%3)
        self.info = QLabel("Turn: X")
        layout.addWidget(self.info)
        layout.addLayout(grid)
        self.setLayout(layout)

    def play(self, idx):
        if self.board[idx] == "":
            self.board[idx] = self.turn
            self.buttons[idx].setText(self.turn)
            if self.check_win(self.turn):
                self.info.setText(f"{self.turn} wins!")
                for b in self.buttons: b.setEnabled(False)
            elif all(x != "" for x in self.board):
                self.info.setText("Draw!")
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.info.setText(f"Turn: {self.turn}")

    def check_win(self, p):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(all(self.board[i] == p for i in w) for w in wins)

class FolderApp(QDialog):
    def __init__(self, name, icons, parent=None):
        super().__init__(parent)
        self.setWindowTitle(name)
        self.setModal(False)
        self.setFixedSize(440, 340)
        layout = QGridLayout()
        for idx, (key, icon, callback) in enumerate(icons):
            btn = DesktopIcon(key, icon, callback, self)
            layout.addWidget(btn, idx//3, idx%3)
        self.setLayout(layout)

class BackgroundApp(QDialog):
    def __init__(self, update_bg_func, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Background")
        self.setModal(True)
        self.setFixedSize(400, 150)
        self.update_bg_func = update_bg_func
        layout = QVBoxLayout()
        label = QLabel("Select PNG image for desktop background:")
        btn = QPushButton("Browse")
        btn.clicked.connect(self.change_bg)
        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)

    def change_bg(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select PNG", "", "PNG Files (*.png)")
        if fname:
            with open(fname, "rb") as src, open("background.png", "wb") as dst:
                dst.write(src.read())
            self.update_bg_func()
            QMessageBox.information(self, "Done", "Background changed!")
            self.accept()

class ImportPyApp(QDialog):
    def __init__(self, add_py_cb, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Python App")
        self.setModal(True)
        self.setFixedSize(400, 150)
        self.add_py_cb = add_py_cb
        layout = QVBoxLayout()
        label = QLabel("Import a .py file and it will appear as an icon on the desktop")
        btn = QPushButton("Import Python File")
        btn.clicked.connect(self.import_py)
        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)

    def import_py(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Import Python App", "", "Python Files (*.py)")
        if fname:
            dest = os.path.join("imported_apps", os.path.basename(fname))
            os.makedirs("imported_apps", exist_ok=True)
            with open(fname, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            self.add_py_cb(dest)
            QMessageBox.information(self, "Imported", f"{os.path.basename(fname)} imported!")
            self.accept()

class SisuCompilerApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sisu Compiler (demo)")
        self.setModal(False)
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        label = QLabel("Tämä on paikka tulevalle Sisu-kielikääntäjälle!\n(Tänne voi myöhemmin liittää Sisu-kääntäjän Python-modulina.)")
        layout.addWidget(label)
        self.setLayout(layout)

class OSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Simulaattori")
        self.resize(1400, 900)
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.bg_label = QLabel(self.central)
        self.bg_label.setGeometry(0, 0, 1400, 900)
        self.bg_label.lower()

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(24)
        self.central.setLayout(self.grid_layout)

        self.imported_pyapps = []
        self.create_desktop_icons()
        self.update_background()
        self.central.resizeEvent = self.on_resize

    def on_resize(self, event):
        self.update_background()
        self.layout_icons()

    def create_desktop_icons(self):
        # Sovellukset ja kansiot työpöydälle:
        self.desktop_icons = [
            ("Calculator", get_icon("Calculator"), self.open_calculator),
            ("Notepad", get_icon("Notepad"), self.open_notepad),
            ("Games", get_icon("Games"), self.open_games_folder),
            ("Browser", get_icon("Browser"), self.open_browser),
            ("YouTube", get_icon("YouTube"), self.open_youtube),
            ("Music", get_icon("Music"), self.open_musicplayer),
            ("ImportPy", get_icon("ImportPy"), self.open_importpy),
            ("SisuCompiler", get_icon("SisuCompiler"), self.open_sisu_compiler),
            ("Change BG", get_icon("Background"), self.open_background)
        ]
        # Kansioesimerkki
        self.folder_icons = [
            ("TicTacToe", get_icon("TicTacToe"), self.open_tictactoe),
            ("GuessNumber", get_icon("GuessNumber"), self.open_guess_number)
        ]
        self.desktop_icons.append(("Games Folder", get_icon("Folder"), lambda: self.open_folder("Games", self.folder_icons)))
        # Lisää importatut python-appit
        self.desktop_icons += self.imported_pyapps
        self.layout_icons()

    def layout_icons(self):
        # Tyhjennä grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        cols = max(1, self.central.width() // 140)
        for idx, (key, icon, callback) in enumerate(self.desktop_icons):
            btn = DesktopIcon(key, icon, callback, self.central)
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(btn, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.on_resize(event)

    def update_background(self):
        w, h = self.central.width(), self.central.height()
        if os.path.exists("background.png"):
            pix = QPixmap("background.png").scaled(w, h, Qt.KeepAspectRatioByExpanding)
            self.bg_label.setPixmap(pix)
        else:
            self.bg_label.setStyleSheet("background-color: #008080;")
            self.bg_label.clear()
        self.bg_label.resize(w, h)

    # Sovellusten avaukset:
    def open_browser(self):
        self.browser = BrowserApp("https://www.google.com", self)
        self.browser.show()

    def open_youtube(self):
        self.browser = BrowserApp("https://www.youtube.com", self)
        self.browser.show()

    def open_notepad(self):
        self.notepad = NotepadApp("notepad.txt", self)
        self.notepad.show()

    def open_musicplayer(self):
        self.music = MusicPlayerApp(self)
        self.music.show()

    def open_importpy(self):
        dlg = ImportPyApp(self.add_python_app, self)
        dlg.exec_()

    def add_python_app(self, filepath):
        filename = os.path.basename(filepath)
        modulename = filename[:-3]
        # Lisää työpöydälle uusi kuvake ja callback joka ajaa .py-tiedoston
        def run_py():
            spec = importlib.util.spec_from_file_location(modulename, filepath)
            foo = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(foo)
            except Exception as e:
                QMessageBox.warning(self, "Python App Error", f"{filename} crashed:\n{e}")
        self.imported_pyapps.append((filename, None, run_py))
        self.create_desktop_icons()

    def open_sisu_compiler(self):
        self.sisu = SisuCompilerApp(self)
        self.sisu.show()

    def open_calculator(self):
        self.calculator = CalculatorApp(self)
        self.calculator.show()

    def open_guess_number(self):
        self.gn = GuessNumberApp(self)
        self.gn.show()

    def open_tictactoe(self):
        self.ttt = TicTacToeApp(self)
        self.ttt.show()

    def open_games_folder(self):
        self.open_folder("Games", self.folder_icons)

    def open_folder(self, name, icons):
        self.folder = FolderApp(name, icons, self)
        self.folder.show()

    def open_background(self):
        dlg = BackgroundApp(self.update_background, self)
        dlg.exec_()

if __name__ == "__main__":
    os.makedirs("icons", exist_ok=True)
    os.makedirs("imported_apps", exist_ok=True)
    app = QApplication(sys.argv)
    win = OSWindow()
    win.show()
    sys.exit(app.exec_())
