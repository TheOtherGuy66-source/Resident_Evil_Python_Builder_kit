import os
import sys
import subprocess

# Ensure required packages are installed
required_packages = ['requests', 'PyQt5', 'Pillow']

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in required_packages:
    install_and_import(package)

# Now proceed with other imports
import webbrowser
import shutil
import zipfile
import asyncio
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image
import requests

def run_async(coroutine):
    """Run an asyncio coroutine in the existing event loop."""
    asyncio.run(coroutine)

class DownloadAndUnpackApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.zip_path = None
        self.dest_dir = None
        self.blinking_timer = QtCore.QTimer()
        self.blinking_timer.timeout.connect(self.blink)
        self.blinking_button = None
        self.blinking_state = False
        self.renaming_context = ""

    def initUI(self):
        self.setWindowTitle("Bio Hazard 3 (SOURCENEXT) DownloadUnpackGUI PyQt5 1.0")
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        layout = QtWidgets.QVBoxLayout(self)

        # Background image
        appdata_dir = os.getenv('APPDATA')
        background_dir = os.path.join(appdata_dir, 'BIO3PyQt5Background')
        os.makedirs(background_dir, exist_ok=True)
        bg_image_path = os.path.join(background_dir, 'background.jpg')

        if not os.path.exists(bg_image_path):
            bg_image_url = "https://www.reshdp.com/img/re3header_uw.jpg"
            self.download_image(bg_image_url, bg_image_path)

        pixmap = QtGui.QPixmap(bg_image_path)
        background_label = QtWidgets.QLabel(self)
        background_label.setPixmap(pixmap)
        layout.addWidget(background_label)

        # Menu bar
        menubar = QtWidgets.QMenuBar(self)
        layout.setMenuBar(menubar)
        menubar.setStyleSheet("QMenuBar { background-color: #2E2E2E; color: white; }"
                              "QMenuBar::item { background-color: #2E2E2E; color: white; }"
                              "QMenuBar::item:selected { background-color: lightblue; }"
                              "QMenu { background-color: #2E2E2E; color: white; }"
                              "QMenu::item { background-color: #2E2E2E; color: white; }"
                              "QMenu::item:selected { background-color: lightblue; }")

        source_next_menu = menubar.addMenu("Bio Hazard 3 (SOURCENEXT)")
        source_next_menu.addAction("Bio Hazard 3 (SOURCENEXT)", lambda: run_async(self.biohazard_sourcenext()))
        source_next_menu.addAction("Download Bio3_mod.zip", self.download_biohazard2)

        # Log area
        self.log_area = QtWidgets.QTextEdit(self)
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100)  # Adjust height here
        self.log_area.setStyleSheet("background-color: #1E1E1E; color: white;")
        layout.addWidget(self.log_area)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()

        self.select_zip_button = QtWidgets.QPushButton("Select Zip File", self)
        self.select_zip_button.setStyleSheet("background-color: #333333; color: white;")
        self.select_zip_button.clicked.connect(self.select_zip_file)
        button_layout.addWidget(self.select_zip_button)

        self.select_dest_button = QtWidgets.QPushButton("Select Destination Folder", self)
        self.select_dest_button.setStyleSheet("background-color: #333333; color: white;")
        self.select_dest_button.clicked.connect(self.select_dest_folder)
        button_layout.addWidget(self.select_dest_button)

        self.extract_button = QtWidgets.QPushButton("Extract Files", self)
        self.extract_button.setStyleSheet("background-color: #333333; color: white;")
        self.extract_button.setDisabled(True)
        self.extract_button.clicked.connect(lambda: run_async(self.extract_files()))
        button_layout.addWidget(self.extract_button)

        self.auto_button = QtWidgets.QPushButton("Auto", self)
        self.auto_button.setStyleSheet("background-color: #333333; color: white;")
        self.auto_button.clicked.connect(lambda: run_async(self.auto_process()))
        button_layout.addWidget(self.auto_button)

        layout.addLayout(button_layout)

        # Credits
        credits_label = QtWidgets.QLabel('<font color="white">Credits:</font> <font color="red">TeamX <font color="white">[Textures]</font></font>, <font color="red">RESHDP <font color="white">[Textures]</font></font>, <font color="red">Gemini <font color="white">[Classic Rebirth]</font></font>', self)
        credits_label.setStyleSheet("font-weight: bold; font-family: Arial;")
        layout.addWidget(credits_label)
        layout.addWidget(credits_label)

        self.setLayout(layout)

    def download_image(self, url, save_path):
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    def log_message(self, message, error=False):
        cursor = self.log_area.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.log_area.setTextCursor(cursor)
        if error:
            self.log_area.setTextColor(QtGui.QColor("red"))
        else:
            self.log_area.setTextColor(QtGui.QColor("white"))
        self.log_area.append(message)
        QtCore.QCoreApplication.processEvents()

    def select_zip_file(self):
        self.zip_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Zip File", "", "Zip files (*.zip)")
        if self.zip_path:
            self.log_message(f"Selected zip file: {self.zip_path}")
            if self.dest_dir:
                self.extract_button.setDisabled(False)

    def select_dest_folder(self):
        self.dest_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if self.dest_dir:
            self.log_message(f"Selected destination folder: {self.dest_dir}")
            if self.zip_path:
                self.extract_button.setDisabled(False)

    async def extract_files(self):
        if not self.zip_path or not self.dest_dir:
            self.log_message("Zip file or destination folder not selected.", error=True)
            return

        await self.unpack_file(self.zip_path, self.dest_dir)

    async def unpack_file(self, zip_path, extract_dir):
        try:
            self.log_message(f"Starting extraction of {zip_path} to {extract_dir}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                common_path = os.path.commonpath(zip_ref.namelist())
                for member in zip_ref.namelist():
                    if not member.endswith('/'):
                        new_path = os.path.join(extract_dir, os.path.relpath(member, common_path))
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        with zip_ref.open(member) as source, open(new_path, "wb") as target:
                            shutil.copyfileobj(source, target)
            self.log_message(f"Successfully extracted {zip_path} to {extract_dir}")
        except Exception as e:
            self.log_message(f"Error extracting {zip_path}: {str(e)}", error=True)

    async def biohazard_sourcenext(self):
        self.renaming_context = "Bio Hazard 3 (SOURCENEXT)"
        download_url = "https://drive.google.com/file/d/1DGJ3XwetXQV3Gt7-SebH30aCWdb6sU08/view?usp=drive_link"
        desktop_dir = self.get_desktop_path()
        target_dir = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)', 'data')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip_path = self.find_zip_file('Bio3_mod.zip')
        if not zip_path:
            self.log_message("Bio3_mod.zip not found. Please download the file first.", error=True)
            download_confirm = QtWidgets.QMessageBox.question(self, "Download Required", "Did you download Bio3_mod.zip?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if download_confirm == QtWidgets.QMessageBox.No:
                self.download_biohazard2()
                return
            else:
                zip_path = self.find_zip_file('Bio3_mod.zip')

        temp_extract_dir = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)', 'temp_extract')
        if not os.path.exists(temp_extract_dir):
            os.makedirs(temp_extract_dir)

        await self.unpack_file(zip_path, temp_extract_dir)
        self.copy_files_to_target(temp_extract_dir, target_dir)
        shutil.rmtree(temp_extract_dir)
        self.copy_to_desktop(target_dir)
        self.auto_cleanup_files()

    def start_blinking(self, button):
        self.blinking_button = button
        self.blinking_state = True
        self.blinking_timer.start(500)

    def stop_blinking(self):
        self.blinking_timer.stop()
        self.blinking_button.setStyleSheet("background-color: green; color: white;")
        self.blinking_button = None
        self.blinking_state = False

    def blink(self):
        if self.blinking_button:
            if self.blinking_button.styleSheet() == "background-color: green; color: white;":
                self.blinking_button.setStyleSheet("background-color: #333333; color: white;")
            else:
                self.blinking_button.setStyleSheet("background-color: green; color: white;")

    async def auto_process(self):
        self.renaming_context = "AUTO"
        self.log_message("Starting Auto process...")
        self.start_blinking(self.auto_button)
        self.auto_button.setEnabled(False)
        self.auto_select_file('Bio3_mod.zip')
        self.auto_select_destination()
        await self.auto_extract_files()
        await self.biohazard_sourcenext()
        self.stop_blinking()
        self.auto_button.setEnabled(True)
        self.log_message("Auto completed.")

    def auto_select_file(self, filename):
        desktop_dir = self.get_desktop_path()
        file_path = os.path.join(desktop_dir, filename)
        if os.path.exists(file_path):
            self.log_message(f"Auto-selected {filename}: {file_path}")
            self.zip_path = file_path
        else:
            self.log_message(f"{filename} not found on the desktop. Checking downloads folder.", error=True)
            downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
            file_path = os.path.join(downloads_dir, filename)
            if os.path.exists(file_path):
                self.log_message(f"Auto-selected {filename}: {file_path}")
                self.zip_path = file_path
            else:
                self.log_message(f"{filename} not found in downloads folder.", error=True)

    def auto_select_destination(self):
        desktop_dir = self.get_desktop_path()
        self.dest_dir = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)', 'data')
        self.log_message(f"Auto-selected destination folder: {self.dest_dir}")

    async def auto_extract_files(self):
        if not self.zip_path or not self.dest_dir:
            self.log_message("Zip file or destination folder not selected.", error=True)
            return

        await self.unpack_file(self.zip_path, self.dest_dir)

    def find_zip_file(self, filename):
        search_dirs = [
            self.get_desktop_path(),
            os.path.join(os.path.expanduser("~"), 'Downloads'),
            'C:\\'
        ]
        for search_dir in search_dirs:
            self.log_message(f"Searching for {filename} in {search_dir}")
            for root, _, files in os.walk(search_dir):
                if filename in files:
                    file_path = os.path.join(root, filename)
                    self.log_message(f"Found {filename} at {file_path}")
                    return file_path
        return None

    def copy_files_to_target(self, source_dir, target_dir):
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(target_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        self.log_message(f"Copied contents from '{source_dir}' to '{target_dir}'")

    def copy_to_desktop(self, target_dir):
        desktop_path = os.path.join(self.get_desktop_path(), 'data')
        if os.path.exists(desktop_path):
            shutil.rmtree(desktop_path)
        shutil.copytree(target_dir, desktop_path, dirs_exist_ok=True)
        self.log_message(f"Copied 'data' folder to {desktop_path}")

        self.auto_create_savedata_folder()

    def auto_create_savedata_folder(self):
        savedata_path = os.path.join(self.get_desktop_path(), 'data', 'savedata')
        os.makedirs(savedata_path, exist_ok=True)
        self.log_message(f"Created 'savedata' folder at {savedata_path}")

    def auto_cleanup_files(self):
        mediakite_dir = os.path.join(self.get_desktop_path(), 'Bio Hazard 3 (SOURCENEXT)')
        if os.path.exists(mediakite_dir):
            shutil.rmtree(mediakite_dir)

        # Rename 'data' folder to 'RE3SHDP - RE Seamless HD Project' with context-specific suffix
        data_path = os.path.join(self.get_desktop_path(), 'data')
        suffix = "Bio Hazard 3 (SOURCENEXT)" if self.renaming_context == "Bio Hazard 3 (SOURCENEXT)" else self.renaming_context
        new_name = os.path.join(self.get_desktop_path(), f'RE3SHDP - RE Seamless HD Project ({suffix})')
        if os.path.exists(data_path):
            if os.path.exists(new_name):
                shutil.rmtree(new_name)
            os.rename(data_path, new_name)
            self.log_message(f"Renamed 'data' folder to 'RE3SHDP - RE Seamless HD Project ({suffix})'")

        # Clean up unnecessary files and folders after renaming
        self.cleanup_after_rename()

        self.log_message("Auto-cleanup complete.")
        QtCore.QTimer.singleShot(5000, self.close)

    def cleanup_after_rename(self):
        desktop_dir = self.get_desktop_path()
        downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')

        junk_files = [
            os.path.join(desktop_dir, 'Bio3_mod.zip'),
            os.path.join(downloads_dir, 'Bio3_mod.zip'),
        ]

        for file_path in junk_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.log_message(f"Removed junk file: {file_path}")
                except Exception as e:
                    self.log_message(f"Failed to remove {file_path}: {str(e)}", error=True)

    def download_biohazard2(self):
        webbrowser.open("https://drive.google.com/file/d/1DGJ3XwetXQV3Gt7-SebH30aCWdb6sU08/view?usp=drive_link")

    def get_desktop_path(self):
        """Get the path to the Desktop directory, accounting for OneDrive redirection."""
        user_home = os.path.expanduser("~")
        desktop_path = os.path.join(user_home, 'Desktop')
        onedrive_desktop_path = os.path.join(user_home, 'OneDrive', 'Desktop')

        if os.path.exists(onedrive_desktop_path):
            self.log_message("Using OneDrive Desktop path.")
            return onedrive_desktop_path
        else:
            self.log_message("Using local Desktop path.")
            return desktop_path

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DownloadAndUnpackApp()
    window.show()
    sys.exit(app.exec_())
