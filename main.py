import customtkinter as ctk
from pypresence import Presence
import time
import json
import os
from threading import Thread
from tkinter import messagebox

class DiscordCustomRPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Discord Custom Rich Presence (Python)")
        self.geometry("600x750")
        
        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.rpc = None
        self.is_connected = False
        
        self.setup_ui()
        self.load_presets()

    def setup_ui(self):
        # Main Container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Custom Rich Presence Settings")
        self.scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- ID & Type ---
        self.id_type_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.id_type_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.id_type_frame.grid_columnconfigure(0, weight=3)
        self.id_type_frame.grid_columnconfigure(1, weight=1)

        self.id_label = ctk.CTkLabel(self.id_type_frame, text="ID:")
        self.id_label.grid(row=0, column=0, sticky="w")
        
        self.type_label = ctk.CTkLabel(self.id_type_frame, text="Type:")
        self.type_label.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.client_id_entry = ctk.CTkEntry(self.id_type_frame, placeholder_text="Application ID")
        self.client_id_entry.grid(row=1, column=0, sticky="ew", pady=5)

        self.type_combo = ctk.CTkComboBox(self.id_type_frame, values=["Playing", "Listening", "Watching", "Competing"])
        self.type_combo.set("Playing")
        self.type_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        # --- Details ---
        self.details_label = ctk.CTkLabel(self.scrollable_frame, text="Details:")
        self.details_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.details_entry = ctk.CTkEntry(self.scrollable_frame, placeholder_text="Lower line of status")
        self.details_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # --- State & Party ---
        self.state_party_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.state_party_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.state_party_frame.grid_columnconfigure(0, weight=2)
        
        self.state_label = ctk.CTkLabel(self.state_party_frame, text="State:")
        self.state_label.grid(row=0, column=0, sticky="w")

        self.party_label = ctk.CTkLabel(self.state_party_frame, text="Party:")
        self.party_label.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.state_entry = ctk.CTkEntry(self.state_party_frame, placeholder_text="Upper line of status")
        self.state_entry.grid(row=1, column=0, sticky="ew", pady=5)

        self.party_frame = ctk.CTkFrame(self.state_party_frame, fg_color="transparent")
        self.party_frame.grid(row=1, column=1, padx=(10, 0))
        
        self.party_cur = ctk.CTkEntry(self.party_frame, width=40, placeholder_text="0")
        self.party_cur.grid(row=0, column=0)
        self.party_of_label = ctk.CTkLabel(self.party_frame, text=" of ")
        self.party_of_label.grid(row=0, column=1)
        self.party_max = ctk.CTkEntry(self.party_frame, width=40, placeholder_text="0")
        self.party_max.grid(row=0, column=2)

        # --- Images ---
        # Large Image
        self.img_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.img_frame.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.img_frame.grid_columnconfigure((0, 1), weight=1)

        self.large_label = ctk.CTkLabel(self.img_frame, text="Large Image:")
        self.large_label.grid(row=0, column=0, sticky="w")
        self.small_label = ctk.CTkLabel(self.img_frame, text="Small Image:")
        self.small_label.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.large_img_entry = ctk.CTkEntry(self.img_frame, placeholder_text="Key or URL")
        self.large_img_entry.grid(row=1, column=0, sticky="ew", pady=5)
        self.small_img_entry = ctk.CTkEntry(self.img_frame, placeholder_text="Key or URL")
        self.small_img_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        self.large_txt_entry = ctk.CTkEntry(self.img_frame, placeholder_text="Large Text")
        self.large_txt_entry.grid(row=2, column=0, sticky="ew", pady=2)
        self.small_txt_entry = ctk.CTkEntry(self.img_frame, placeholder_text="Small Text")
        self.small_txt_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=(10, 0))

        # --- Buttons ---
        self.buttons_label = ctk.CTkLabel(self.scrollable_frame, text="Buttons:")
        self.buttons_label.grid(row=12, column=0, padx=10, pady=(10, 0), sticky="w")

        self.btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.btn_frame.grid(row=13, column=0, padx=10, sticky="ew")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        # Button 1
        self.btn1_label = ctk.CTkEntry(self.btn_frame, placeholder_text="Button 1 Label")
        self.btn1_label.grid(row=0, column=0, padx=(0, 5), pady=2, sticky="ew")
        self.btn1_url = ctk.CTkEntry(self.btn_frame, placeholder_text="Button 1 URL")
        self.btn1_url.grid(row=1, column=0, padx=(0, 5), pady=2, sticky="ew")

        # Button 2
        self.btn2_label = ctk.CTkEntry(self.btn_frame, placeholder_text="Button 2 Label")
        self.btn2_label.grid(row=0, column=1, padx=(5, 0), pady=2, sticky="ew")
        self.btn2_url = ctk.CTkEntry(self.btn_frame, placeholder_text="Button 2 URL")
        self.btn2_url.grid(row=1, column=1, padx=(5, 0), pady=2, sticky="ew")

        # --- Controls ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)

        self.connect_btn = ctk.CTkButton(self.control_frame, text="Connect & Update", command=self.toggle_connection, fg_color="green", hover_color="#228B22")
        self.connect_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.save_btn = ctk.CTkButton(self.control_frame, text="Save Preset", command=self.save_presets, fg_color="#4682B4", hover_color="#5F9EA0")
        self.save_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="Status: Disconnected", text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(0, 10))

    def toggle_connection(self):
        if not self.is_connected:
            self.start_rpc()
        else:
            self.stop_rpc()

    def start_rpc(self):
        client_id = self.client_id_entry.get().strip()
        if not client_id:
            messagebox.showerror("Error", "Please enter an ID!")
            return

        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()
            self.is_connected = True
            self.update_presence()
            
            self.connect_btn.configure(text="Disconnect", fg_color="red", hover_color="#8B0000")
            self.status_label.configure(text="Status: Connected", text_color="green")
            self.save_presets()
        except Exception as e:
            error_msg = str(e)
            if "nd Discord" in error_msg or "Connection refused" in error_msg:
                error_msg = "Could not find Discord running! Please make sure your Discord desktop app is open."
            messagebox.showerror("Connection Error", error_msg)
            self.is_connected = False

    def update_presence(self):
        if not self.is_connected or not self.rpc:
            return

        try:
            buttons = []
            if self.btn1_label.get().strip() and self.btn1_url.get().strip():
                buttons.append({"label": self.btn1_label.get(), "url": self.btn1_url.get()})
            if self.btn2_label.get().strip() and self.btn2_url.get().strip():
                buttons.append({"label": self.btn2_label.get(), "url": self.btn2_url.get()})

            # Activity Type
            type_map = {
                "Playing": 0,
                "Listening": 2,
                "Watching": 3,
                "Competing": 5
            }
            activity_type = type_map.get(self.type_combo.get(), 0)

            # Party Size
            party_size = None
            try:
                cur = int(self.party_cur.get().strip())
                mx = int(self.party_max.get().strip())
                if mx > 0:
                    party_size = [cur, mx]
            except:
                pass

            self.rpc.update(
                details=self.details_entry.get().strip() or None,
                state=self.state_entry.get().strip() or None,
                large_image=self.large_img_entry.get().strip() or None,
                large_text=self.large_txt_entry.get().strip() or None,
                small_image=self.small_img_entry.get().strip() or None,
                small_text=self.small_txt_entry.get().strip() or None,
                buttons=buttons if buttons else None,
                party_size=party_size,
                activity_type=activity_type,
                start=time.time()
            )
        except Exception as e:
            self.status_label.configure(text=f"Update Error: {str(e)}", text_color="red")

    def stop_rpc(self):
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
        self.rpc = None
        self.is_connected = False
        self.connect_btn.configure(text="Connect & Update", fg_color="green", hover_color="#228B22")
        self.status_label.configure(text="Status: Disconnected", text_color="gray")

    def save_presets(self):
        data = {
            "client_id": self.client_id_entry.get(),
            "type": self.type_combo.get(),
            "details": self.details_entry.get(),
            "state": self.state_entry.get(),
            "party_cur": self.party_cur.get(),
            "party_max": self.party_max.get(),
            "large_image": self.large_img_entry.get(),
            "large_text": self.large_txt_entry.get(),
            "small_image": self.small_img_entry.get(),
            "small_text": self.small_txt_entry.get(),
            "btn1_label": self.btn1_label.get(),
            "btn1_url": self.btn1_url.get(),
            "btn2_label": self.btn2_label.get(),
            "btn2_url": self.btn2_url.get()
        }
        with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
            json.dump(data, f)

    def load_presets(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                self.client_id_entry.insert(0, data.get("client_id", ""))
                self.type_combo.set(data.get("type", "Playing"))
                self.details_entry.insert(0, data.get("details", ""))
                self.state_entry.insert(0, data.get("state", ""))
                self.party_cur.insert(0, data.get("party_cur", ""))
                self.party_max.insert(0, data.get("party_max", ""))
                self.large_img_entry.insert(0, data.get("large_image", ""))
                self.large_txt_entry.insert(0, data.get("large_text", ""))
                self.small_img_entry.insert(0, data.get("small_image", ""))
                self.small_txt_entry.insert(0, data.get("small_text", ""))
                self.btn1_label.insert(0, data.get("btn1_label", ""))
                self.btn1_url.insert(0, data.get("btn1_url", ""))
                self.btn2_label.insert(0, data.get("btn2_label", ""))
                self.btn2_url.insert(0, data.get("btn2_url", ""))
            except:
                pass

if __name__ == "__main__":
    app = DiscordCustomRPApp()
    app.mainloop()
