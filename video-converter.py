import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from utils import collect_mp4, compress_files

class FolderSelectorApp(QWidget):

    selected_folder = ""
    mp4_files = {}

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Selector")
        self.setGeometry(100, 100, 400, 200)

        # Layout and widgets
        self.layout = QVBoxLayout()

        self.label = QLabel("Please select a folder")
        self.layout.addWidget(self.label)

        # Button to select folder
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_button)

        # Button to run conversion
        self.run_conversion_button = QPushButton("Run Conversion")
        self.run_conversion_button.clicked.connect( self.run_conversion)
        self.layout.addWidget(self.run_conversion_button)
        self.setLayout(self.layout)

    def select_folder(self):
        """prompts the user to select a file and both displays and keeps track of the folder selected
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder_path:
            self.label.setText(f"Selected Folder: {folder_path}")
            self.selected_folder = folder_path
    
    def run_conversion(self):
        """runs when the "run conversion button is pressed.
        """
        # Check if a folder is selected
        if self.selected_folder:
            # Reference the folder path here
            print(f"Running conversion on: {self.selected_folder}")
            self.label.setText(f"Conversion started on: {self.selected_folder}")
            
            self.mp4_files =  collect_mp4(self.selected_folder)
            print(f"files: {self.mp4_files}")
            
            #compress files
            
            for key in self.mp4_files:
                print(key)
                compress_files(self.mp4_files[key])
                
            self.label.setText("conversion finished")
            
        else:
            self.label.setText("Please select a folder first.")
            print("No folder selected.")
            
    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FolderSelectorApp()
    window.show()

    sys.exit(app.exec())