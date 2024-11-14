import tkinter as tk
from tkinter import messagebox

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exemplo de GUI com Tkinter")
        self.root.geometry("400x300")

        # Criação de um rótulo
        self.label = tk.Label(root, text="Digite seu nome:")
        self.label.pack(pady=10)

        # Criação de uma entrada de texto
        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        # Criação de um botão
        self.submit_button = tk.Button(root, text="Enviar", command=self.submit)
        self.submit_button.pack(pady=10)

        # Criação de um botão para sair
        self.exit_button = tk.Button(root, text="Sair", command=root.quit)
        self.exit_button.pack(pady=10)


    def submit(self):
        # Recupera o texto da entrada
        name = self.entry.get()
        if name:
            messagebox.showinfo("Nome", f"Olá, {name}!")
        else:
            messagebox.showwarning("Nome", "Por favor, digite seu nome.")
