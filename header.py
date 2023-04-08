import customtkinter
from PIL import Image

def create_header(App: customtkinter.CTk) -> None:
    # Create header_frame
    App.bg_image = customtkinter.CTkImage(Image.open("Assets/Header.png"),size=(900, 150))
    App.header_frame = customtkinter.CTkFrame(App)
    App.header_frame.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
    App.header_label = customtkinter.CTkLabel(App.header_frame, text="", image=App.bg_image)
    App.header_label.grid(row=0, column=0, sticky="nsew")
    # Create buttonFrame
    App.button_frame = customtkinter.CTkFrame(App)
    App.button_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # Create buttons
    App.add_button = customtkinter.CTkButton(App.button_frame, text="Add Today's Reading", command=App._add_reading)
    App.add_button.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    App.legacy_button = customtkinter.CTkButton(App.button_frame, text="Add Legacy Reading", command=App._add_legacy_reading)
    App.legacy_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # standing charge label
    App.standing_charge_label = customtkinter.CTkLabel(App.button_frame, text="Standing Charge (£)")
    App.standing_charge_label.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
    # standing charge number label
    App.standing_charge_number_label = customtkinter.CTkLabel(App.button_frame, text=(str(App.standing_charge) + '/day'))
    App.standing_charge_number_label.grid(row=3, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")

    # price per unit label
    App.price_per_unit_label = customtkinter.CTkLabel(App.button_frame, text="Price per Unit (£)")
    App.price_per_unit_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
    # price per unit number label
    App.price_per_unit_number_label = customtkinter.CTkLabel(App.button_frame, text=(str(App.price_per_unit) + '/kWh'))
    App.price_per_unit_number_label.grid(row=5, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")
    


    # create tabview
    App.tab_view = customtkinter.CTkTabview(App, width=250)
    App.tab_view.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    App.tab_view.add("Readings")
    App.tab_view.add("Analytics")
    App.tab_view.add("Graphs")
    App.tab_view.tab("Readings").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
    App.tab_view.tab("Analytics").grid_columnconfigure(0, weight=1)