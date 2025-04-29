import sys
import os
import locale

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QPushButton, QLineEdit, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QFont, QColor, QPainter, QMouseEvent, QIcon

from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

icon_path = os.path.join(base_path, "fcdy.ico")

lang, _ = locale.getdefaultlocale()
IS_ENGLISH = lang.startswith("en")
IS_SPANISH = lang.startswith("es")

translations = {
    "title": {
        "en": "FOV Editor - Dying Light",
        "es": "Editor de FOV - Dying Light"
    },
    "title_label": {
        "en": "FOV Editor",
        "es": "Editor de FOV"
    },
    "fov_placeholder": {
        "en": "Enter new FOV (e.g. 90)",
        "es": "Ingresa el nuevo FOV (ej: 90)"
    },
    "apply_button": {
        "en": "Apply changes",
        "es": "Aplicar cambios"
    },
    "close_button": {
        "en": "Close",
        "es": "Cerrar"
    },
    "invalid_number_message": {
        "en": "Please enter a valid number.",
        "es": "Por favor ingresa un número válido."
    },
    "file_not_found_message": {
        "en": "video.scr file not found.",
        "es": "No se encontró el archivo video.scr."
    },
    "success_message": {
        "en": "FOV updated successfully!",
        "es": "Se aplicó el nuevo FOV correctamente."
    }
}

def translate(key):
    if IS_ENGLISH:
        return translations[key]["en"]
    elif IS_SPANISH:
        return translations[key]["es"]
    else:
    
        return translations[key]["en"]

class CustomMessage(QWidget):
    def __init__(self, parent, text, success=True):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(300, 120)

        # Centrar sobre ventana principal
        parent_center = parent.geometry().center()
        self.move(parent_center.x() - self.width() // 2, parent_center.y() - self.height() // 2)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        icon = "✅" if success else "❌"
        label = QLabel(f"{icon}  {text}")
        label.setFont(QFont("Segoe UI", 12))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        # Efecto de opacidad
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

        QTimer.singleShot(2500, self.close)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(20, 20, 20, 230))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

class FovEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(translate("title"))
        self.resize(400, 300)
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.file_path = self.get_scr_path()
        self.old_pos = QPoint(0, 0)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.title = QLabel(translate("title_label"))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 16))
        self.title.setStyleSheet("color: white;")
        self.layout.addWidget(self.title)

        self.fov_input = QLineEdit()
        self.fov_input.setPlaceholderText(translate("fov_placeholder"))
        self.layout.addWidget(self.fov_input)

        self.save_button = QPushButton(translate("apply_button"))
        self.save_button.clicked.connect(self.apply_fov_change)
        self.layout.addWidget(self.save_button)

        self.close_button = QPushButton(translate("close_button"))
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.apply_styles()

    def get_scr_path(self):
        documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")
        scr_path = os.path.join(documents_folder, "DyingLight", "out", "settings", "video.scr")
        return scr_path

    def apply_styles(self):
        button_style = """
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
        """
        input_style = """
            QLineEdit {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }
        """
        self.save_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style)
        self.fov_input.setStyleSheet(input_style)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(30, 30, 30, 230))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def show_message(self, text, success=True):
        self.msg = CustomMessage(self, text, success)
        self.msg.show()

    def apply_fov_change(self):
        fov_value = self.fov_input.text().strip()

        if not fov_value.isdigit():
            self.show_message(translate("invalid_number_message"), success=False)
            return

        if not os.path.exists(self.file_path):
            self.show_message(translate("file_not_found_message"), success=False)
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines):
            if line.strip().startswith("ExtraGameFov"):
                lines[i] = f"ExtraGameFov {fov_value}\n"
                found = True
                break

        if not found:
            lines.append(f"\nExtraGameFov {fov_value}\n")

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        self.show_message(translate("success_message"), success=True)
        self.setWindowIcon(QIcon(icon_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FovEditor()
    window.show()
    sys.exit(app.exec())
