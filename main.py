import customtkinter as ctk
## Class Import Below
from classes.scanner_frame import ScannerFrame
from classes.settings_frame import SettingsFrame
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scanner")
        self.geometry("1000x580")
        self.resizable(False, False)
        
        self.scannerFrame = ScannerFrame(self, self.switch_to_settings)
        self.scannerFrame.pack(fill="both", expand=True)

        self.settingsFrame = SettingsFrame(self, self.switch_to_scanner, self.themeHandler, self.update_logging)
        
    def switch_to_settings(self):
        self.scannerFrame.pack_forget()
        self.settingsFrame.pack(fill="both", expand=True)

    def switch_to_scanner(self):
        self.settingsFrame.pack_forget()
        self.scannerFrame.pack(fill="both", expand=True)
        
   
    def themeHandler(self, mode):
        ctk.set_appearance_mode(mode)
        
    def update_logging(self, logging_enabled):
        self.logging_enabled = logging_enabled
        self.scannerFrame.set_logging_enabled(logging_enabled)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()