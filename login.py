
import tkinter as tk
from tkinter import messagebox
from auth import login_funcionario

def abrir_login(callback_sucesso):
    janela = tk.Tk()
    janela.title("Sistema de Detecção de Sonolência")
    janela.geometry("400x300")
    janela.resizable(False, False)
    janela.configure(bg="#1e1e2e")

    # Título
    tk.Label(janela, text="LOGIN DO FUNCIONÁRIO", font=("Arial", 14, "bold"),
             bg="#1e1e2e", fg="white").pack(pady=20)

    # Matrícula
    tk.Label(janela, text="Matrícula:", bg="#1e1e2e", fg="white").pack()
    campo_matricula = tk.Entry(janela, font=("Arial", 12), width=25)
    campo_matricula.pack(pady=5)

    # Senha
    tk.Label(janela, text="Senha:", bg="#1e1e2e", fg="white").pack()
    campo_senha = tk.Entry(janela, font=("Arial", 12), width=25, show="*")
    campo_senha.pack(pady=5)

    # Mensagem de erro
    label_erro = tk.Label(janela, text="", bg="#1e1e2e", fg="#ff5555")
    label_erro.pack(pady=5)

    def tentar_login():
        matricula = campo_matricula.get().strip()
        senha = campo_senha.get().strip()

        if not matricula or not senha:
            label_erro.config(text="Preencha todos os campos")
            return

        nome, status = login_funcionario(matricula, senha)

        if status == "OK":
            janela.destroy()
            callback_sucesso(nome)
        else:
            label_erro.config(text=status)
            campo_senha.delete(0, tk.END)

    # Botão login
    tk.Button(janela, text="ENTRAR", font=("Arial", 11, "bold"),
              bg="#4e9af1", fg="white", width=20,
              command=tentar_login).pack(pady=10)

    # Enter também faz login
    janela.bind("<Return>", lambda e: tentar_login())

    janela.mainloop()