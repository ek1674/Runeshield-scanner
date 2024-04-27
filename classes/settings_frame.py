import customtkinter as ctk
import yaml
import os


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, switch_frame_callback, theme_callback, logging_callback, **kwargs):
        super().__init__(master, **kwargs)
        # Callback for switching frames
        self.switch_frame_callback = switch_frame_callback
        self.theme_callback = theme_callback
        self.logging_callback = logging_callback
        
        # logging_var needs to be here because python is quirky
        self.logging_var = ctk.StringVar(value="off")
        self.light_mode = ctk.StringVar(value="off")
                
        #event handler for settings         
        def settings_event_handler():
                logging_status =  self.logging_var.get()
                light_status = self.light_mode.get()
                config_data = {'logging': logging_status,
                               'Theme': light_status
                               }
                with open("config.yaml", 'w') as yamlfile:
                        data=yaml.dump(config_data, yamlfile)
                        print("Saved succesfully")
                
                if light_status == "light":
                    self.theme_callback("light")
                else:
                    self.theme_callback("dark")  

                                
        #loads the settings file                
        self.load_settings()
        self.apply_Theme()
        self.apply_Logging
        
################################################################################################        
##                                  UI SETUP
##      

        
        self.side_Bar = ctk.CTkFrame(self, height=580, width=200, corner_radius=8)
        self.side_Bar.grid(row=0, column=0, rowspan=8, sticky="nsew")
        
        self.side_Bar_Setting_Button = ctk.CTkButton(self, text="Scanner", command=self.switch_frame_callback)
        self.side_Bar_Setting_Button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
      
        self.checkBox_Logging = ctk.CTkCheckBox(self, text="Enable logging", command=settings_event_handler, variable=self.logging_var, onvalue="enabled", offvalue="disabled")
        self.checkBox_Logging.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        self.switch_Light_Mode = ctk.CTkSwitch(self, text="Light Mode", variable=self.light_mode, command=settings_event_handler, onvalue="light", offvalue="dark")
        self.switch_Light_Mode.grid(row=1, column=1, padx=20, pady=0, sticky="ew")
##
##        
################################################################################################         
##
##                              PUT Settings function below


    def load_settings(self):
        default_settings = {'logging': 'off',
                            'Theme': 'dark'                            
                            }
        settings_file = "config.yaml"

        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as yamlfile:
                    self.settings = yaml.safe_load(yamlfile) or default_settings
            except yaml.YAMLError as e:
                print(f"Error reading settings file: {e}")
                self.settings = default_settings
        else:
            self.settings = default_settings
        
        # Set the checkbox state based on the loaded settings
        self.logging_var.set(self.settings.get('logging', 'off'))
        # Set the light mode state based on the loaded settings
        self.light_mode.set(self.settings.get('Theme', 'dark'))
        
    
    def apply_Theme(self):
         theme_mode = self.settings.get('Theme', 'dark')
         ctk.set_appearance_mode(theme_mode)
         if self.theme_callback:
            self.theme_callback(theme_mode)
            
    def apply_Logging(self):
        logging_mode = self.settings.get("logging", 'off')
        if self.logging_callback:
            self.logging_callback(logging_mode)        
        
       