import sys
import os
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QCheckBox
from utils import collect_mp4, compress_files, stitch_videos_in_folder


class ConversionThread(QThread):
    update_status = Signal(str)
    conversion_finished = Signal()

    def __init__(self, input_folder_path, output_folder_path, zip, stitch_only):
        super().__init__()
        self.folder_path = input_folder_path
        self.output_folder_path = output_folder_path
        self.zip = zip
        self.stitch_only = stitch_only

    def run(self):
        if not self.folder_path:
            self.update_status.emit("No folder selected.")
            return

        self.update_status.emit(f"Running conversion on: {self.folder_path}")
        mp4_files = collect_mp4(self.folder_path)
        
        for key in mp4_files:
            self.update_status.emit(f"Processing: {key}")
            # if the videos should be compressed, otherwise, only run stitch_videos_in_folder
            if not self.stitch_only:
                compress_files(mp4_files[key])
            else: 
                dir, filename = os.path.split(mp4_files[key][0])
                stitch_videos_in_folder(dir, self.output_folder_path)

            
        
        self.update_status.emit("Conversion finished.")
        self.conversion_finished.emit()


class FolderSelectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Selector")
        self.setGeometry(100, 100, 400, 200)

        self.selected_folder = ""
        self.selected_output_folder = ""
        self.conversion_thread = None

        self.layout = QVBoxLayout()

        self.label = QLabel("Please select a folder")
        self.layout.addWidget(self.label)

        self.select_folder_button = QPushButton("Select Input Folder")
        self.select_folder_button.clicked.connect(self.select_input_folder)
        self.layout.addWidget(self.select_folder_button)

        self.select_output_folder_button = QPushButton("Select Output Folder")
        self.select_output_folder_button.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.select_output_folder_button)

        self.run_conversion_button = QPushButton("Run Conversion")
        self.run_conversion_button.clicked.connect(self.run_conversion)
        self.layout.addWidget(self.run_conversion_button)

        self.stitch_only = QCheckBox("Only Stitch videos")
        self.layout.addWidget(self.stitch_only)

        self.compress_originals = QCheckBox("Compress original videos")
        self.compress_originals.setChecked(True)
        self.layout.addWidget(self.compress_originals)

        self.setLayout(self.layout)
        

    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.label.setText(f"Selected Folder: {folder_path}")
            self.selected_folder = folder_path

    def select_output_folder(self): 
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path: 
            self.selected_output_folder = folder_path
            

    def run_conversion(self):
        if not self.selected_folder or not self.selected_output_folder:
            self.label.setText("Please select a folder first.")
            return

        self.label.setText("Conversion started...")
        self.conversion_thread = ConversionThread(self.selected_folder, self.selected_output_folder, False, self.stitch_only.isChecked())
        self.conversion_thread.update_status.connect(self.label.setText)
        self.conversion_thread.conversion_finished.connect(self.on_conversion_finished)
        self.conversion_thread.start()

    def on_conversion_finished(self):
        self.label.setText("Conversion finished.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderSelectorApp()
    window.show()
    sys.exit(app.exec())