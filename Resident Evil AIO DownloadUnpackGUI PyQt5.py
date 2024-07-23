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
        self.setWindowTitle("Resident Evil AIO DownloadUnpackGUI PyQt5")
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.resize(1000, 800)

        layout = QtWidgets.QVBoxLayout(self)

        # Menu bar
        menubar = QtWidgets.QMenuBar(self)
        layout.setMenuBar(menubar)

        help_menu = menubar.addMenu("Help")
        help_action = QtWidgets.QAction("Show Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        self.game_selection_layout = QtWidgets.QHBoxLayout()

        self.re1_button = QtWidgets.QPushButton("Resident Evil 1", self)
        self.re1_button.setStyleSheet("background-color: #333333; color: white;")
        self.re1_button.clicked.connect(lambda: self.load_game("re1"))
        self.game_selection_layout.addWidget(self.re1_button)

        self.re2_button = QtWidgets.QPushButton("Resident Evil 2", self)
        self.re2_button.setStyleSheet("background-color: #333333; color: white;")
        self.re2_button.clicked.connect(lambda: self.load_game("re2"))
        self.game_selection_layout.addWidget(self.re2_button)

        self.re3_button = QtWidgets.QPushButton("Resident Evil 3", self)
        self.re3_button.setStyleSheet("background-color: #333333; color: white;")
        self.re3_button.clicked.connect(lambda: self.load_game("re3"))
        self.game_selection_layout.addWidget(self.re3_button)

        layout.addLayout(self.game_selection_layout)

        # Background image
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.background_label)

        # Mod selection dropdown
        self.mod_selection_layout = QtWidgets.QHBoxLayout()
        self.mod_selection_label = QtWidgets.QLabel("Select Mod to Download:", self)
        self.mod_selection_label.setStyleSheet("color: white;")
        self.mod_selection_layout.addWidget(self.mod_selection_label)

        self.mod_dropdown = QtWidgets.QComboBox(self)
        self.mod_dropdown.setStyleSheet("background-color: #333333; color: white;")
        self.mod_dropdown.addItem("Biohazard_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Biohazard_mod.zip")
        self.mod_dropdown.addItem("Bio2_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio2_mod.zip")
        self.mod_dropdown.addItem("Bio3_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio3_mod.zip")
        self.mod_dropdown.addItem("dgVoodoo_AMD_fix.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/dgVoodoo_AMD_fix.zip")
        self.mod_selection_layout.addWidget(self.mod_dropdown)

        self.download_mod_button = QtWidgets.QPushButton("Download Selected Mod", self)
        self.download_mod_button.setStyleSheet("background-color: #333333; color: white;")
        self.download_mod_button.clicked.connect(self.download_selected_mod)
        self.mod_selection_layout.addWidget(self.download_mod_button)

        layout.addLayout(self.mod_selection_layout)

        # Log area
        self.log_area = QtWidgets.QTextEdit(self)
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100)
        self.log_area.setStyleSheet("background-color: #1E1E1E; color: white;")
        layout.addWidget(self.log_area)

        # Buttons for auto-processing
        self.auto_button_layout = QtWidgets.QHBoxLayout()
        self.auto_button = QtWidgets.QPushButton("Auto", self)
        self.auto_button.setStyleSheet("background-color: #333333; color: white;")
        self.auto_button.clicked.connect(lambda: run_async(self.auto_process()))
        self.auto_button_layout.addWidget(self.auto_button)

        self.auto_amd_button = QtWidgets.QPushButton("Auto AMD", self)
        self.auto_amd_button.setStyleSheet("background-color: #333333; color: white;")
        self.auto_amd_button.clicked.connect(lambda: run_async(self.auto_amd_process()))
        self.auto_amd_button.setVisible(False)
        self.auto_button_layout.addWidget(self.auto_amd_button)

        self.auto_nvidia_button = QtWidgets.QPushButton("Auto Nvidia", self)
        self.auto_nvidia_button.setStyleSheet("background-color: #333333; color: white;")
        self.auto_nvidia_button.clicked.connect(lambda: run_async(self.auto_nvidia_process()))
        self.auto_nvidia_button.setVisible(False)
        self.auto_button_layout.addWidget(self.auto_nvidia_button)

        layout.addLayout(self.auto_button_layout)

        # Credits
        credits_label = QtWidgets.QLabel('<font color="white">Credits:</font> <font color="red">TeamX <font color="white">[Textures]</font></font>, <font color="red">RESHDP <font color="white">[Textures]</font></font>, <font color="red">Gemini <font color="white">[Classic Rebirth]</font></font>', self)
        credits_label.setStyleSheet("font-weight: bold; font-family: Arial;")
        layout.addWidget(credits_label)

        self.setLayout(layout)

    def load_game(self, game):
        self.auto_button.setVisible(False)
        self.auto_amd_button.setVisible(False)
        self.auto_nvidia_button.setVisible(False)

        if game == "re1":
            bg_image_url = "https://www.reshdp.com/img/re1header_uw.jpg"
            self.renaming_context = "BIOHAZARD Mediakite"
            self.zip_name = "Biohazard_mod.zip"
            self.bg_image_path = self.download_image(bg_image_url, "BIO1PyQt5Background")
            self.auto_amd_button.setVisible(True)
            self.auto_nvidia_button.setVisible(True)
        elif game == "re2":
            bg_image_url = "https://www.reshdp.com/img/re2header_uw.jpg"
            self.renaming_context = "biohazard-2-apan-source-next"
            self.zip_name = "Bio2_mod.zip"
            self.bg_image_path = self.download_image(bg_image_url, "BIO2PyQt5Background")
            self.auto_button.setVisible(True)
        elif game == "re3":
            bg_image_url = "https://www.reshdp.com/img/re3header_uw.jpg"
            self.renaming_context = "Bio Hazard 3 (SOURCENEXT)"
            self.zip_name = "Bio3_mod.zip"
            self.bg_image_path = self.download_image(bg_image_url, "BIO3PyQt5Background")
            self.auto_button.setVisible(True)
        
        pixmap = QtGui.QPixmap(self.bg_image_path)
        self.background_label.setPixmap(pixmap.scaled(self.width(), int(self.height() * 0.6), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def download_image(self, url, folder_name):
        appdata_dir = os.getenv('APPDATA')
        background_dir = os.path.join(appdata_dir, folder_name)
        os.makedirs(background_dir, exist_ok=True)
        bg_image_path = os.path.join(background_dir, 'background.jpg')

        if not os.path.exists(bg_image_path):
            response = requests.get(url, stream=True)
            with open(bg_image_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)

        return bg_image_path

    def download_selected_mod(self):
        selected_mod_url = self.mod_dropdown.currentData()
        webbrowser.open(selected_mod_url)

    def show_help(self):
        help_text = (
        "Game Versions/Folder Names:\n\n"
        "My download links do not contain the actual game files; you’ll have to find those yourself!\n\n"
        "RE1 Folder Name:\nBIOHAZARD Mediakite\n\n"
        "RE2 Folder Name:\nbiohazard-2-apan-source-next\n\n"
        "RE3 Folder Name:\nBio Hazard 3 (SOURCENEXT)\n\n"
        "Folders MUST BE ON THE DESKTOP.\n\n"
        ".zips can be stored in C: But they don't get deleted when stored in C:\n\n"
        ".zips should be stored in the downloads folder or the desktop.\n\n"
        "The folders must be named these for the corresponding game titles, and it must be the Japanese versions of the games.\n\n"
        "You just use 7zip and dump the game into the correct named folder from the ISO.\n\n"
        "You don’t need to do anything else but download the zip mod for the corresponding game.\n\n"
        "The script will do the job for you.\n\n"
        "And a word of advice: Don’t have all the files in the same place at once. One game at a time…\n\n"
        "This was a hard task to create, not perfect by any stretch of the imagination though.\n\n"
        )
        help_dialog = QtWidgets.QMessageBox(self)
        help_dialog.setWindowTitle("Help")
        help_dialog.setText(help_text)
        help_dialog.exec_()

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

    async def biohazard_mediakite(self):
        self.renaming_context = "BIOHAZARD Mediakite"
        download_url = "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Biohazard_mod.zip"
        desktop_dir = self.get_desktop_path()
        target_dir = os.path.join(desktop_dir, 'BIOHAZARD Mediakite', 'horr')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip_path = self.find_zip_file('Biohazard_mod.zip')
        if not zip_path:
            self.log_message("Biohazard_mod.zip not found. Please download the file first.", error=True)
            download_confirm = QtWidgets.QMessageBox.question(self, "Download Required", "Did you download Biohazard_mod.zip?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if download_confirm == QtWidgets.QMessageBox.No:
                self.download_biohazard()
                return
            else:
                zip_path = self.find_zip_file('Biohazard_mod.zip')

        temp_extract_dir = os.path.join(desktop_dir, 'BIOHAZARD Mediakite', 'temp_extract')
        if not os.path.exists(temp_extract_dir):
            os.makedirs(temp_extract_dir)

        await self.unpack_file(zip_path, temp_extract_dir)
        self.copy_files_to_target(temp_extract_dir, target_dir)
        shutil.rmtree(temp_extract_dir)
        self.copy_to_desktop(target_dir)
        self.auto_cleanup_files()

    async def biohazard_source_next(self):
        download_url = ""
        desktop_dir = self.get_desktop_path()
        if self.renaming_context == "biohazard-2-apan-source-next":
            download_url = "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio2_mod.zip"
        elif self.renaming_context == "Bio Hazard 3 (SOURCENEXT)":
            download_url = "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio3_mod.zip"
        
        target_dir = os.path.join(desktop_dir, self.renaming_context, 'data')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip_path = self.find_zip_file(self.zip_name)
        if not zip_path:
            self.log_message(f"{self.zip_name} not found. Please download the file first.", error=True)
            download_confirm = QtWidgets.QMessageBox.question(self, "Download Required", f"Did you download {self.zip_name}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if download_confirm == QtWidgets.QMessageBox.No:
                self.download_biohazard()
                return
            else:
                zip_path = self.find_zip_file(self.zip_name)

        temp_extract_dir = os.path.join(desktop_dir, self.renaming_context, 'temp_extract')
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

    async def auto_amd_process(self):
        self.log_message("Starting Auto AMD process...")
        self.start_blinking(self.auto_amd_button)
        self.auto_amd_button.setEnabled(False)

        if self.renaming_context == "BIOHAZARD Mediakite":
            self.auto_select_file('Biohazard_mod.zip')
            self.auto_select_file('dgVoodoo_AMD_fix.zip')
            self.auto_select_destination()
            await self.auto_extract_files()
            await self.biohazard_mediakite()
        else:
            self.auto_select_file(self.zip_name)
            self.auto_select_file('dgVoodoo_AMD_fix.zip')
            self.auto_select_destination()
            await self.auto_extract_files()
            await self.biohazard_source_next()

        self.stop_blinking()
        self.auto_amd_button.setEnabled(True)
        self.log_message("Auto AMD process completed.")

    async def auto_nvidia_process(self):
        self.log_message("Starting Auto Nvidia process...")
        self.start_blinking(self.auto_nvidia_button)
        self.auto_nvidia_button.setEnabled(False)

        if self.renaming_context == "BIOHAZARD Mediakite":
            self.auto_select_file('Biohazard_mod.zip')
            self.auto_select_destination()
            await self.auto_extract_files()
            await self.biohazard_mediakite()
        else:
            self.auto_select_file(self.zip_name)
            self.auto_select_destination()
            await self.auto_extract_files()
            await self.biohazard_source_next()

        self.stop_blinking()
        self.auto_nvidia_button.setEnabled(True)
        self.log_message("Auto Nvidia process completed.")

    async def auto_process(self):
        self.log_message(f"Starting Auto process for {self.renaming_context}...")
        self.start_blinking(self.auto_button)
        self.auto_button.setEnabled(False)

        if self.renaming_context == "biohazard-2-apan-source-next":
            self.auto_select_file('Bio2_mod.zip')
        elif self.renaming_context == "Bio Hazard 3 (SOURCENEXT)":
            self.auto_select_file('Bio3_mod.zip')
        self.auto_select_destination()
        await self.auto_extract_files()
        await self.biohazard_source_next()

        self.stop_blinking()
        self.auto_button.setEnabled(True)
        self.log_message(f"Auto process for {self.renaming_context} completed.")

    def auto_select_file(self, filename=None):
        if filename is None:
            filename = self.zip_name
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
        if self.renaming_context == "BIOHAZARD Mediakite":
            self.dest_dir = os.path.join(desktop_dir, 'BIOHAZARD Mediakite', 'horr')
        else:
            self.dest_dir = os.path.join(desktop_dir, self.renaming_context, 'data')
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
        desktop_path = os.path.join(self.get_desktop_path(), os.path.basename(target_dir))
        if os.path.exists(desktop_path):
            shutil.rmtree(desktop_path)
        shutil.copytree(target_dir, desktop_path, dirs_exist_ok=True)
        self.log_message(f"Copied '{os.path.basename(target_dir)}' folder to {desktop_path}")

        self.auto_create_savedata_folder()

    def auto_create_savedata_folder(self):
        if self.renaming_context == "BIOHAZARD Mediakite":
            savedata_path = os.path.join(self.get_desktop_path(), 'horr', 'savedata')
        else:
            savedata_path = os.path.join(self.get_desktop_path(), 'data', 'savedata')
        os.makedirs(savedata_path, exist_ok=True)
        self.log_message(f"Created 'savedata' folder at {savedata_path}")

    def auto_cleanup_files(self):
        if self.renaming_context == "BIOHAZARD Mediakite":
            game_dir = os.path.join(self.get_desktop_path(), 'BIOHAZARD Mediakite')
        else:
            game_dir = os.path.join(self.get_desktop_path(), self.renaming_context)

        if os.path.exists(game_dir):
            shutil.rmtree(game_dir)

        # Rename 'horr' or 'data' folder to the appropriate name
        if self.renaming_context == "BIOHAZARD Mediakite":
            folder_path = os.path.join(self.get_desktop_path(), 'horr')
            new_name = os.path.join(self.get_desktop_path(), f'RE1SHDP - RE Seamless HD Project ({self.renaming_context})')
        else:
            folder_path = os.path.join(self.get_desktop_path(), 'data')
            new_name = os.path.join(self.get_desktop_path(), f'RESHDP - RE Seamless HD Project ({self.renaming_context})')

        if os.path.exists(folder_path):
            if os.path.exists(new_name):
                shutil.rmtree(new_name)
            os.rename(folder_path, new_name)
            self.log_message(f"Renamed '{folder_path}' to '{new_name}'")

        # Clean up unnecessary files and folders after renaming
        self.cleanup_after_rename()

        self.log_message("Auto-cleanup complete.")
        QtCore.QTimer.singleShot(5000, self.close)

    def cleanup_after_rename(self):
        desktop_dir = self.get_desktop_path()
        downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')

        junk_files = [
            os.path.join(desktop_dir, 'Biohazard_mod.zip'),
            os.path.join(desktop_dir, 'dgVoodoo_AMD_fix.zip'),
            os.path.join(desktop_dir, 'Bio2_mod.zip'),
            os.path.join(desktop_dir, 'Bio3_mod.zip'),
            os.path.join(downloads_dir, 'Biohazard_mod.zip'),
            os.path.join(downloads_dir, 'dgVoodoo_AMD_fix.zip'),
            os.path.join(downloads_dir, 'Bio2_mod.zip'),
            os.path.join(downloads_dir, 'Bio3_mod.zip'),
        ]

        for file_path in junk_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.log_message(f"Removed junk file: {file_path}")
                except Exception as e:
                    self.log_message(f"Failed to remove {file_path}: {str(e)}", error=True)

    def download_biohazard(self):
        selected_mod_url = self.mod_dropdown.currentData()
        webbrowser.open(selected_mod_url)

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
