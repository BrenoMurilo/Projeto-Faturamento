import customtkinter as ctk
from tkinter import messagebox

class MyApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500")


        #Criação de lista suspensa
        self.options = ["Opção 1", "Opção 2", "Opção 3"]
        self.selected_option = ctk.StringVar(value=self.options[0])
        self.option_menu = ctk.CTkOptionMenu(self.master, variable=self.selected_option, values=self.options)
        self.option_menu.pack(pady=10)
        self.option_menu.place(x=120, y=50)

        #Criação de botão
        self.button = ctk.CTkButton(self.master, text="Clique aqui", command=self.button_callback)
        self.button.pack(pady=20)
        self.button.place(x=700, y=400)

    def button_callback(self):
        messagebox.showinfo("Informação", f"Botão clicado. Opção selecionada: {self.selected_option.get()}")
