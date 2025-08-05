import customtkinter

import customtkinter
import threading
import time
from flask import request
import requests




def GUIselection():


    result = {}

    def button_click_event():
        result["latitude"] = entry1.get()
        result["longitude"] = entry2.get()
        result["elevation"] = entry3.get()
        result["type_of_body"] = choice1.get()
        result["body_name"] = choice2.get()
        result["moon_planet"] = moon_planet_entry.get()
        result["moon"] = moon_name_entry.get()
        result["calibration"] = selected_option.get()
        root.destroy()  # closes GUI and allows function to return


    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1200x800")



    frame = customtkinter.CTkFrame(master = root)

    frame.pack(pady = 20, padx = 60, fill="both", expand = True)





    my_font_1 = customtkinter.CTkFont(family= "", size=24)
    my_font_2 = customtkinter.CTkFont(family= "", size=12)

    label = customtkinter.CTkLabel(master = frame, text = "Mussy_v1", font = my_font_1)
    label.pack(pady = 12, padx = 10)


    textbox = customtkinter.CTkTextbox(master = frame, width = 800, height = 145)

    textbox.insert("0.0", "First insert your coordinates and your elevation.\n To select the object you want to track complete the missing fields with the appropriate names.\n For stars provide the HIP number, e.g. 69420, for nebulas and galaxies, the M number, e.g. 'M12', while for planets and moons provide the name in lowercase.\n For satellites look at the file 'active_satellites.txt'.\n\n Finally chose your calibration body between the 3 choices, and hit the 'Calibrate' button")  # insert at line 0 character 0

    textbox.pack(pady = 12, padx = 10)


    entry_frame = customtkinter.CTkFrame(master=frame, fg_color=frame.cget("fg_color"))
    entry_frame.pack(pady=20)

    # Latitude
    lat_label = customtkinter.CTkLabel(master=entry_frame, text="Latitude", font=my_font_2)
    lat_label.grid(row=0, column=0, padx=10, pady=(0, 5))
    entry1 = customtkinter.CTkEntry(master=entry_frame, placeholder_text = "47.52", font=my_font_2, width=200)
    entry1.grid(row=1, column=0, padx=20)

    # Longitude
    lon_label = customtkinter.CTkLabel(master=entry_frame, text="Longitude", font=my_font_2)
    lon_label.grid(row=0, column=1, padx=10, pady=(0, 5))
    entry2 = customtkinter.CTkEntry(master=entry_frame, placeholder_text = "8.26", font=my_font_2, width=200)
    entry2.grid(row=1, column=1, padx=20)

    # Elevation
    elev_label = customtkinter.CTkLabel(master=entry_frame, text="Elevation (m)", font=my_font_2)
    elev_label.grid(row=0, column=2, padx=10, pady=(0, 5))
    entry3 = customtkinter.CTkEntry(master=entry_frame, placeholder_text = "430", font=my_font_2, width=200)
    entry3.grid(row=1, column=2, padx=20)


    choice_frame = customtkinter.CTkFrame(master=frame, fg_color=frame.cget("fg_color"))
    choice_frame.pack(pady=20)

    choice1_label = customtkinter.CTkLabel(master = choice_frame, text = "Type of the object you want to observe:", font = my_font_2)
    choice1_label.grid(row = 0, column= 0, padx = 20, pady = (0, 5))
    choice1 = customtkinter.CTkComboBox(master = choice_frame, values = ["Nebula", "Galaxy", "Star","Planet", "Moon", "Satellite"])
    choice1.grid(row = 1, column = 0, padx = 20)
    choice1.set("Star")




    choice2 = customtkinter.CTkEntry(master = choice_frame, placeholder_text = "mars", font = my_font_2)
    choice2_label = customtkinter.CTkLabel(master = choice_frame, text = "Name of the object you want to observe:", font = my_font_2)


    moon_planet_label = customtkinter.CTkLabel(master=choice_frame, text="Which planet does the moon orbit?", font=my_font_2)
    moon_planet_entry = customtkinter.CTkEntry(master=choice_frame, placeholder_text="jupiter", font=my_font_2)

    moon_name_label = customtkinter.CTkLabel(master=choice_frame, text="Name of the moon:", font=my_font_2)
    moon_name_entry = customtkinter.CTkEntry(master=choice_frame, placeholder_text="europa", font=my_font_2)



    def update_moon_fields(event=None):
        if choice1.get() == "Moon":
            # Show moon-specific inputs
            moon_planet_label.grid(row=2, column=0, padx=20, pady=(20, 5))
            moon_planet_entry.grid(row=3, column=0, padx=20)

            moon_name_label.grid(row=2, column=1, padx=20, pady=(20, 5))
            moon_name_entry.grid(row=3, column=1, padx=20)
            choice2_label.grid_forget()
            choice2.grid_forget()
        else:
            # Hide them
            moon_planet_label.grid_forget()
            moon_planet_entry.grid_forget()
            moon_name_label.grid_forget()
            moon_name_entry.grid_forget()
            choice2_label.grid(row = 0, column= 1, padx = 20, pady = (0, 5))
            choice2.grid(row = 1, column = 1, padx = 20)



    choice1.configure(command=update_moon_fields)
    update_moon_fields()



    radio_frame = customtkinter.CTkFrame(master=frame, fg_color=frame.cget("fg_color"))
    radio_frame.pack(pady=40)

    radio_label = customtkinter.CTkLabel(master = radio_frame, text = "What celestial body will you use to calibrate?")
    radio_label.pack(side = "top", padx = 20)

    selected_option = customtkinter.StringVar(value="Polaris")  # default selection



    radio1 = customtkinter.CTkRadioButton(master=radio_frame, text="Polaris", variable=selected_option, value="Polaris")
    radio1.pack(side="left", padx=20)

    radio2 = customtkinter.CTkRadioButton(master=radio_frame, text="Moon", variable=selected_option, value="Moon")
    radio2.pack(side="left", padx=20)

    radio3 = customtkinter.CTkRadioButton(master=radio_frame, text="Sun", variable=selected_option, value="Sun")
    radio3.pack(side="left", padx=20)



    button = customtkinter.CTkButton(master = frame, text = "Calibrate", command = button_click_event)
    button.pack(side = "bottom", padx = 20)



    root.mainloop()
    return result



def open_manual_calibration_window(send_key_callback=None):
    manual_root = customtkinter.CTk()
    manual_root.geometry("500x300")
    manual_root.title("Manual Calibration - Use WASD")


    key_state = {
        'w': False,
        'a': False,
        's': False,
        'd': False,
    }

    font = customtkinter.CTkFont(size=20, weight="bold")

    # Create buttons
    btn_w = customtkinter.CTkButton(manual_root, text="W", font=font, fg_color = "#3a7ebf")
    btn_a = customtkinter.CTkButton(manual_root, text="A", font=font, fg_color = "#3a7ebf")
    btn_s = customtkinter.CTkButton(manual_root, text="S", font=font, fg_color = "#3a7ebf")
    btn_d = customtkinter.CTkButton(manual_root, text="D", font=font, fg_color = "#3a7ebf")
    btn_q = customtkinter.CTkButton(manual_root, text="Q (Quit)", font=font, fg_color="red", command=manual_root.destroy)

    # Positioning like WASD layout
    btn_w.grid(row=0, column=1, padx=10, pady=10)
    btn_a.grid(row=1, column=0, padx=10, pady=10)
    btn_s.grid(row=1, column=1, padx=10, pady=10)
    btn_d.grid(row=1, column=2, padx=10, pady=10)
    btn_q.grid(row=2, column=1, padx=10, pady=20)

    def send_calibration_command(key):
            url = "http://127.0.0.1:5000/manual" # Replace with your server's IP address
            try:
                response = requests.post(url, json={'command': key})
                if response.status_code == 200:
                    print(f"Successfully sent command: {key}")
                else:
                    print(f"Failed to send command: {key}, Status: {response.status_code}")
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: Could not reach the server at {url}. Error: {e}")

    after_ids = {}
    original_color = "#3a7ebf"  # Replace with the actual default fg_color if needed

    def highlight_key(key):
        button_map = {'w': btn_w, 'a': btn_a, 's': btn_s, 'd': btn_d}
        button = button_map[key]

        # Cancel previous scheduled reset (if any)
        if key in after_ids:
            manual_root.after_cancel(after_ids[key])

        # Highlight the button
        button.configure(fg_color="#1F6AA5")

        # Schedule reset to original color
        after_ids[key] = manual_root.after(300, lambda b=button, k=key: reset_button_color(b, k))

    def reset_button_color(button, key):
        button.configure(fg_color=original_color)
        if key in after_ids:
            del after_ids[key]

        # Schedule reset and store ID
        after_id = manual_root.after(300, lambda: button.configure(fg_color=original_color))
        after_ids[key] = after_id



    def on_key_press(event):

        key = event.char.lower()
        if key in ['w', 'a', 's', 'd']:
            highlight_key(key)
            send_calibration_command(key)
        elif key == 'q':
            send_calibration_command('stop') # send a stop command when quitting
            manual_root.destroy()

    manual_root.bind("<KeyPress>", on_key_press)
    manual_root.mainloop()





