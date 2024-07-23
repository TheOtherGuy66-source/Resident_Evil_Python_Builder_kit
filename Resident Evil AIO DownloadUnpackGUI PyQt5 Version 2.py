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
    asyncio.run(coroutine)

class DownloadAndUnpackApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.zip_path = None
        self.dest_dir = None
        self.blinking_button = None
        self.blinking_state = False
        self.renaming_context = ""
        self.setup_ui()
        self.setup_timers()

    def setup_ui(self):
        self.setWindowTitle("Resident Evil AIO DownloadUnpackGUI PyQt5 Version 2")
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.resize(1000, 800)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setMenuBar(self.create_menubar())
        layout.addLayout(self.create_game_selection_layout())
        
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.background_label)
        
        layout.addLayout(self.create_mod_selection_layout())
        layout.addWidget(self.create_log_area())
        layout.addLayout(self.create_auto_button_layout())
        layout.addWidget(self.create_credits_label())
        
        self.setLayout(layout)

    def create_menubar(self):
        menubar = QtWidgets.QMenuBar(self)
        help_menu = menubar.addMenu("Help")
        help_action = QtWidgets.QAction("Show Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        return menubar

    def create_game_selection_layout(self):
        layout = QtWidgets.QHBoxLayout()
        games = {
            "Resident Evil 1": "re1",
            "Resident Evil 2": "re2",
            "Resident Evil 3": "re3"
        }
        for game, command in games.items():
            button = QtWidgets.QPushButton(game, self)
            button.setStyleSheet("background-color: #333333; color: white;")
            button.clicked.connect(lambda _, cmd=command: self.load_game(cmd))
            layout.addWidget(button)
        return layout

    def create_mod_selection_layout(self):
        layout = QtWidgets.QHBoxLayout()
        mod_label = QtWidgets.QLabel("Select Mod to Download:", self)
        mod_label.setStyleSheet("color: white;")
        layout.addWidget(mod_label)

        self.mod_dropdown = QtWidgets.QComboBox(self)
        self.mod_dropdown.setStyleSheet("background-color: #333333; color: white;")
        mods = [
            ("Biohazard_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Biohazard_mod.zip"),
            ("Bio2_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio2_mod.zip"),
            ("Bio3_mod.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/Bio3_mod.zip"),
            ("dgVoodoo_AMD_fix.zip", "https://github.com/TheOtherGuy66-source/Resident_Evil_Python_Builder_kit/releases/download/amd/dgVoodoo_AMD_fix.zip")
        ]
        for mod, url in mods:
            self.mod_dropdown.addItem(mod, url)
        layout.addWidget(self.mod_dropdown)

        download_button = QtWidgets.QPushButton("Download Selected Mod", self)
        download_button.setStyleSheet("background-color: #333333; color: white;")
        download_button.clicked.connect(self.download_selected_mod)
        layout.addWidget(download_button)
        return layout

    def create_log_area(self):
        self.log_area = QtWidgets.QTextEdit(self)
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100)
        self.log_area.setStyleSheet("background-color: #1E1E1E; color: white;")
        return self.log_area

    def create_auto_button_layout(self):
        layout = QtWidgets.QHBoxLayout()
        self.auto_button = self.create_auto_button("Auto", self.auto_process, visible=False)
        layout.addWidget(self.auto_button)
        self.auto_amd_button = self.create_auto_button("Auto AMD", self.auto_amd_process, visible=False)
        layout.addWidget(self.auto_amd_button)
        self.auto_nvidia_button = self.create_auto_button("Auto Nvidia", self.auto_nvidia_process, visible=False)
        layout.addWidget(self.auto_nvidia_button)
        return layout

    def create_auto_button(self, text, handler, visible=True):
        button = QtWidgets.QPushButton(text, self)
        button.setStyleSheet("background-color: #333333; color: white;")
        button.clicked.connect(lambda: run_async(handler()))
        button.setVisible(visible)
        return button

    def create_credits_label(self):
        return QtWidgets.QLabel('<font color="white">Credits:</font> <font color="red">TeamX <font color="white">[Textures]</font></font>, <font color="red">RESHDP <font color="white">[Textures]</font></font>, <font color="red">Gemini <font color="white">[Classic Rebirth]</font></font>', self)

    def setup_timers(self):
        self.blinking_timer = QtCore.QTimer()
        self.blinking_timer.timeout.connect(self.blink)

    def load_game(self, game):
        self.reset_auto_buttons()

        if game == "re1":
            bg_image_url = "https://www.reshdp.com/img/re1header_uw.jpg"
            self.setup_game_context("BIOHAZARD Mediakite", "Biohazard_mod.zip", bg_image_url, amd_visible=True, nvidia_visible=True)
        elif game == "re2":
            bg_image_url = "https://www.reshdp.com/img/re2header_uw.jpg"
            self.setup_game_context("biohazard-2-apan-source-next", "Bio2_mod.zip", bg_image_url)
        elif game == "re3":
            bg_image_url = "https://www.reshdp.com/img/re3header_uw.jpg"
            self.setup_game_context("Bio Hazard 3 (SOURCENEXT)", "Bio3_mod.zip", bg_image_url)

    def setup_game_context(self, renaming_context, zip_name, bg_image_url, amd_visible=False, nvidia_visible=False):
        self.renaming_context = renaming_context
        self.zip_name = zip_name
        self.bg_image_path = self.download_image(bg_image_url, f"{renaming_context}_Background")
        pixmap = QtGui.QPixmap(self.bg_image_path)
        self.background_label.setPixmap(pixmap.scaled(self.width(), int(self.height() * 0.6), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.auto_button.setVisible(renaming_context != "BIOHAZARD Mediakite")
        self.auto_amd_button.setVisible(amd_visible)
        self.auto_nvidia_button.setVisible(nvidia_visible)

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
        self.log_area.setTextColor(QtGui.QColor("red") if error else QtGui.QColor("white"))
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

    async def biohazard_mediakite(self, include_amd_fix):
        await self.process_biohazard_mediakite(include_amd_fix)

    async def biohazard_source_next(self):
        await self.process_game("biohazard-2-apan-source-next", "Bio2_mod.zip")
        await self.process_bio_hazard_3()

    async def process_game(self, renaming_context, zip_name):
        desktop_dir = self.get_desktop_path()
        target_dir = os.path.join(desktop_dir, renaming_context, 'data')
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip_path = self.find_zip_file(zip_name)
        if not zip_path:
            self.log_message(f"{zip_name} not found. Please download the file first.", error=True)
            return
        
        temp_extract_dir = os.path.join(desktop_dir, renaming_context, 'temp_extract')
        if not os.path.exists(temp_extract_dir):
            os.makedirs(temp_extract_dir)

        await self.unpack_file(zip_path, temp_extract_dir)
        self.copy_files_to_target(temp_extract_dir, target_dir)
        shutil.rmtree(temp_extract_dir)
        self.copy_to_desktop(target_dir, renaming_context)
        self.auto_cleanup_files(target_dir, renaming_context)

    async def process_bio_hazard_3(self):
        desktop_dir = self.get_desktop_path()
        source_dir = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)', 'data')

        # Ensure the data directory exists
        if not os.path.exists(source_dir):
            self.log_message("Bio Hazard 3 (SOURCENEXT)/data folder not found.", error=True)
            return

        # Process Bio3_mod.zip
        zip_path = self.find_zip_file('Bio3_mod.zip')
        if not zip_path:
            self.log_message("Bio3_mod.zip not found. Please download the file first.", error=True)
            return
        await self.unpack_file(zip_path, source_dir)

        # Rename the data folder and perform cleanup
        self.rename_and_cleanup_bio_hazard_3()

    async def process_biohazard_mediakite(self, include_amd_fix):
        desktop_dir = self.get_desktop_path()
        source_dir = os.path.join(desktop_dir, 'BIOHAZARD Mediakite', 'horr')

        # Ensure the horr directory exists
        if not os.path.exists(source_dir):
            self.log_message("BIOHAZARD Mediakite/horr folder not found.", error=True)
            return

        # Process Biohazard_mod.zip
        zip_path = self.find_zip_file('Biohazard_mod.zip')
        if not zip_path:
            self.log_message("Biohazard_mod.zip not found. Please download the file first.", error=True)
            return
        await self.unpack_file(zip_path, source_dir)

        # Process dgVoodoo_AMD_fix.zip if required
        if include_amd_fix:
            zip_path = self.find_zip_file('dgVoodoo_AMD_fix.zip')
            if not zip_path:
                self.log_message("dgVoodoo_AMD_fix.zip not found. Please download the file first.", error=True)
                return
            await self.unpack_file(zip_path, source_dir)

        # Rename the horr folder and perform cleanup
        self.rename_and_cleanup_biohazard_mediakite()

    def reset_auto_buttons(self):
        self.auto_button.setVisible(False)
        self.auto_amd_button.setVisible(False)
        self.auto_nvidia_button.setVisible(False)

    def start_blinking(self, button):
        self.blinking_button = button
        self.blinking_state = True
        self.blinking_timer.start(500)

    def stop_blinking(self):
        self.blinking_timer.stop()
        if self.blinking_button:
            self.blinking_button.setStyleSheet("background-color: #333333; color: white;")
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
        await self.process_biohazard_mediakite(include_amd_fix=True)
        self.stop_blinking()
        self.auto_amd_button.setEnabled(True)
        self.log_message("Auto AMD process completed.")

    async def auto_nvidia_process(self):
        self.log_message("Starting Auto Nvidia process...")
        self.start_blinking(self.auto_nvidia_button)
        self.auto_nvidia_button.setEnabled(False)
        await self.process_biohazard_mediakite(include_amd_fix=False)
        self.stop_blinking()
        self.auto_nvidia_button.setEnabled(True)
        self.log_message("Auto Nvidia process completed.")

    async def auto_process(self):
        self.log_message(f"Starting Auto process for {self.renaming_context}...")
        self.start_blinking(self.auto_button)
        self.auto_button.setEnabled(False)
        await self.process_game(self.renaming_context, self.zip_name)
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
        self.dest_dir = os.path.join(desktop_dir, self.renaming_context, 'data' if self.renaming_context != "BIOHAZARD Mediakite" else 'horr')
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

    def copy_to_desktop(self, target_dir, renaming_context):
        new_name = f"RE{'1' if renaming_context == 'BIOHAZARD Mediakite' else ('2' if renaming_context == 'biohazard-2-apan-source-next' else '3')}SHDP - RE Seamless HD Project ({renaming_context})"
        desktop_path = os.path.join(self.get_desktop_path(), new_name)
        if os.path.exists(desktop_path):
            shutil.rmtree(desktop_path)
        shutil.copytree(target_dir, desktop_path, dirs_exist_ok=True)
        self.log_message(f"Copied '{os.path.basename(target_dir)}' folder to {desktop_path}")
        self.auto_create_savedata_folder()

    def auto_create_savedata_folder(self):
        savedata_path = os.path.join(self.get_desktop_path(), 'horr' if self.renaming_context == "BIOHAZARD Mediakite" else 'data', 'savedata')
        os.makedirs(savedata_path, exist_ok=True)
        self.log_message(f"Created 'savedata' folder at {savedata_path}")

    def rename_and_cleanup_biohazard_mediakite(self):
        desktop_dir = self.get_desktop_path()
        game_dir = os.path.join(desktop_dir, 'BIOHAZARD Mediakite', 'horr')
        new_name = os.path.join(desktop_dir, f'RE1SHDP - RE Seamless HD Project (BIOHAZARD Mediakite)')
        if os.path.exists(game_dir):
            if os.path.exists(new_name):
                shutil.rmtree(new_name)
            os.rename(game_dir, new_name)
            self.log_message(f"Renamed '{game_dir}' to '{new_name}'")
            # Delete the original BIOHAZARD Mediakite folder
            original_folder = os.path.join(desktop_dir, 'BIOHAZARD Mediakite')
            if os.path.exists(original_folder):
                shutil.rmtree(original_folder)
                self.log_message(f"Deleted '{original_folder}'")
        self.auto_cleanup_files()

    def rename_and_cleanup_bio_hazard_3(self):
        desktop_dir = self.get_desktop_path()
        game_dir = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)', 'data')
        new_name = os.path.join(desktop_dir, f'RE3SHDP - RE Seamless HD Project (Bio Hazard 3 (SOURCENEXT))')
        if os.path.exists(game_dir):
            if os.path.exists(new_name):
                shutil.rmtree(new_name)
            os.rename(game_dir, new_name)
            self.log_message(f"Renamed '{game_dir}' to '{new_name}'")
            # Delete the original Bio Hazard 3 (SOURCENEXT) folder
            original_folder = os.path.join(desktop_dir, 'Bio Hazard 3 (SOURCENEXT)')
            if os.path.exists(original_folder):
                shutil.rmtree(original_folder)
                self.log_message(f"Deleted '{original_folder}'")
        self.auto_cleanup_files()

    def auto_cleanup_files(self, target_dir=None, renaming_context=None):
        desktop_dir = self.get_desktop_path()
        if renaming_context and renaming_context != "BIOHAZARD Mediakite":
            game_dir = os.path.join(desktop_dir, renaming_context)
            if os.path.exists(game_dir):
                shutil.rmtree(game_dir)
                self.log_message(f"Deleted '{game_dir}'")
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
                self.log_message(f"Deleted '{target_dir}'")

        # Remove any extra `data` folder left on the desktop
        extra_data_folder = os.path.join(desktop_dir, 'data')
        if os.path.exists(extra_data_folder):
            shutil.rmtree(extra_data_folder)
            self.log_message(f"Deleted extra 'data' folder: {extra_data_folder}")

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

    def download_selected_mod(self):
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
