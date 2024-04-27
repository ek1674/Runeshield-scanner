import customtkinter as ctk
import nmap
import threading  # Import threading module
import logging



class ScannerFrame(ctk.CTkFrame):
    def __init__(self, master, switch_frame_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.logging_enabled = False
        if self.logging_enabled:
            logging.basicConfig(filename='network_scan.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            self.logger = logging.getLogger('ApplicationLogger')
        
        # Callback for switching frames
        self.switch_frame_callback = switch_frame_callback
################################################################################################        
##                                  UI SETUP
##
        
        self.side_Bar = ctk.CTkFrame(self, height=580, width=200, corner_radius=8)
        self.side_Bar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.side_Bar_Setting_Button = ctk.CTkButton(self, text="Settings", command=self.switch_frame_callback)
        self.side_Bar_Setting_Button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        
        self.ip_Label = ctk.CTkLabel(self, text="IP Address: ")
        self.ip_Label.grid(row=0, column=1, padx=30, pady=20, sticky="ew")
        
        self.ip_Entry = ctk.CTkEntry(self, placeholder_text="IP Address...")
        self.ip_Entry.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
        self.scan_Button = ctk.CTkButton(self, text="Scan", command=self.start_scan_thread)
        self.scan_Button.grid(row=3, column=2,  padx=20, pady=20, sticky="ew")
        
        self.display_Scan = ctk.CTkTextbox(self, width=750, height=400, state="disabled")
        self.display_Scan.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="nsew")
##
##        
################################################################################################              
    def start_scan_thread(self):
        """Starts the scan function in a new thread."""
        self.display_scan_results("Starting Scan. . .\n")
        scan_thread = threading.Thread(target=self.scan_Function)
        scan_thread.start()

    def set_logging_enabled(self, enabled):
        self.logging_enabled = enabled
        
    def scan_Function(self):
        scan_ip = self.ip_Entry.get()
        if scan_ip:
            scan_ip += '/24'  # Adjust as necessary for your needs
            nm = nmap.PortScanner()
            nm.scan(hosts=scan_ip, arguments='-T4 -sS -n')
            
            for host in nm.all_hosts():
                if 'mac' in nm[host]['addresses']:
                    mac_address = nm[host]['addresses']['mac']
                    ip_address = nm[host]['addresses']['ipv4']
                    self.display_scan_results(f"IP Address: {ip_address} MAC Address: {mac_address}\n")
                    if self.logging_enabled == True:
                        self.logger.info(f"IP Address: {ip_address} MAC Address: {mac_address}\n")
            self.display_scan_results("Scan Complete\n")       
        else:
            pass

    def display_scan_results(self, text):
        """Inserts scan results into the display_Scan widget in a thread-safe manner."""
        if self.display_Scan.winfo_exists():  # Check if the widget exists
            self.display_Scan.configure(state="normal")
            self.display_Scan.insert("end", text)
            self.display_Scan.configure(state="disabled")

