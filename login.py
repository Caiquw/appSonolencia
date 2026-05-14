import tkinter as tk
from tkinter import messagebox
from auth import (
    login_funcionario,
    login_gestor,
    cadastrar_funcionario,
    listar_funcionarios,
    alternar_acesso
)

COR_FUNDO    = "#0f0f1a"
COR_PAINEL   = "#1a1a2e"
COR_DESTAQUE = "#4e9af1"
COR_TEXTO    = "#ffffff"
COR_ERRO     = "#ff5555"
COR_OK       = "#50fa7b"
FONTE_TITULO = ("Consolas", 15, "bold")
FONTE_NORMAL = ("Consolas", 10)
FONTE_BTN    = ("Consolas", 10, "bold")


# ──────────────────────────────────────────
# TELA INICIAL
# ──────────────────────────────────────────
def tela_inicial(callback_funcionario):
    janela = tk.Tk()
    janela.title("Sistema de Deteccao de Sonolencia")
    janela.geometry("420x320")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)
    centralizar(janela, 420, 320)

    tk.Label(janela, text="DETECCAO DE SONOLENCIA",
             font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_DESTAQUE).pack(pady=30)

    tk.Label(janela, text="Selecione o tipo de acesso:",
             font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=5)

    def ir_funcionario():
        janela.destroy()
        tela_login_funcionario(callback_funcionario)

    def ir_gestor():
        janela.destroy()
        tela_login_gestor(callback_funcionario)

    tk.Button(janela, text="FUNCIONARIO", font=FONTE_BTN,
              bg=COR_DESTAQUE, fg=COR_TEXTO, width=22, height=2,
              command=ir_funcionario).pack(pady=10)

    tk.Button(janela, text="GESTOR", font=FONTE_BTN,
              bg="#6272a4", fg=COR_TEXTO, width=22, height=2,
              command=ir_gestor).pack(pady=5)

    janela.mainloop()


# ──────────────────────────────────────────
# LOGIN DO FUNCIONÁRIO
# ──────────────────────────────────────────
def tela_login_funcionario(callback_sucesso):
    janela = tk.Tk()
    janela.title("Login - Funcionario")
    janela.geometry("400x340")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)
    centralizar(janela, 400, 340)

    tk.Label(janela, text="ACESSO DO FUNCIONARIO",
             font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_DESTAQUE).pack(pady=20)

    frame = tk.Frame(janela, bg=COR_PAINEL, padx=20, pady=20)
    frame.pack(padx=30, fill="x")

    tk.Label(frame, text="Matricula:", font=FONTE_NORMAL,
             bg=COR_PAINEL, fg=COR_TEXTO).pack(anchor="w")
    campo_matricula = tk.Entry(frame, font=FONTE_NORMAL, width=28,
                               bg="#2a2a3e", fg=COR_TEXTO, insertbackground="white")
    campo_matricula.pack(pady=4, fill="x")

    tk.Label(frame, text="Senha:", font=FONTE_NORMAL,
             bg=COR_PAINEL, fg=COR_TEXTO).pack(anchor="w", pady=(8, 0))
    campo_senha = tk.Entry(frame, font=FONTE_NORMAL, width=28, show="*",
                           bg="#2a2a3e", fg=COR_TEXTO, insertbackground="white")
    campo_senha.pack(pady=4, fill="x")

    label_erro = tk.Label(janela, text="", font=FONTE_NORMAL,
                          bg=COR_FUNDO, fg=COR_ERRO)
    label_erro.pack(pady=5)

    def tentar_login():
        matricula = campo_matricula.get().strip()
        senha     = campo_senha.get().strip()

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

    tk.Button(janela, text="ENTRAR", font=FONTE_BTN,
              bg=COR_DESTAQUE, fg=COR_TEXTO, width=20,
              command=tentar_login).pack(pady=5)

    tk.Button(janela, text="Voltar", font=FONTE_NORMAL,
              bg=COR_FUNDO, fg="#888", bd=0,
              command=lambda: [janela.destroy(), tela_inicial(callback_sucesso)]).pack()

    janela.bind("<Return>", lambda e: tentar_login())
    campo_matricula.focus()
    janela.mainloop()


# ──────────────────────────────────────────
# LOGIN DO GESTOR
# ──────────────────────────────────────────
def tela_login_gestor(callback_funcionario):
    janela = tk.Tk()
    janela.title("Login - Gestor")
    janela.geometry("400x340")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)
    centralizar(janela, 400, 340)

    tk.Label(janela, text="ACESSO DO GESTOR",
             font=FONTE_TITULO, bg=COR_FUNDO, fg="#6272a4").pack(pady=20)

    frame = tk.Frame(janela, bg=COR_PAINEL, padx=20, pady=20)
    frame.pack(padx=30, fill="x")

    tk.Label(frame, text="Email:", font=FONTE_NORMAL,
             bg=COR_PAINEL, fg=COR_TEXTO).pack(anchor="w")
    campo_email = tk.Entry(frame, font=FONTE_NORMAL, width=28,
                           bg="#2a2a3e", fg=COR_TEXTO, insertbackground="white")
    campo_email.pack(pady=4, fill="x")

    tk.Label(frame, text="Senha:", font=FONTE_NORMAL,
             bg=COR_PAINEL, fg=COR_TEXTO).pack(anchor="w", pady=(8, 0))
    campo_senha = tk.Entry(frame, font=FONTE_NORMAL, width=28, show="*",
                           bg="#2a2a3e", fg=COR_TEXTO, insertbackground="white")
    campo_senha.pack(pady=4, fill="x")

    label_erro = tk.Label(janela, text="", font=FONTE_NORMAL,
                          bg=COR_FUNDO, fg=COR_ERRO)
    label_erro.pack(pady=5)

    def tentar_login():
        email = campo_email.get().strip()
        senha = campo_senha.get().strip()

        if not email or not senha:
            label_erro.config(text="Preencha todos os campos")
            return

        id_gestor, nome, status = login_gestor(email, senha)

        if status == "OK":
            janela.destroy()
            painel_gestor(id_gestor, nome, callback_funcionario)
        else:
            label_erro.config(text=status)
            campo_senha.delete(0, tk.END)

    tk.Button(janela, text="ENTRAR", font=FONTE_BTN,
              bg="#6272a4", fg=COR_TEXTO, width=20,
              command=tentar_login).pack(pady=5)

    tk.Button(janela, text="Voltar", font=FONTE_NORMAL,
              bg=COR_FUNDO, fg="#888", bd=0,
              command=lambda: [janela.destroy(), tela_inicial(callback_funcionario)]).pack()

    janela.bind("<Return>", lambda e: tentar_login())
    campo_email.focus()
    janela.mainloop()


# ──────────────────────────────────────────
# PAINEL DO GESTOR
# ──────────────────────────────────────────
def painel_gestor(id_gestor, nome_gestor, callback_funcionario):
    janela = tk.Tk()
    janela.title(f"Painel do Gestor - {nome_gestor}")
    janela.geometry("580x500")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)
    centralizar(janela, 580, 500)

    tk.Label(janela, text=f"Painel do Gestor: {nome_gestor}",
             font=FONTE_TITULO, bg=COR_FUNDO, fg="#6272a4").pack(pady=15)

    # ── Cadastro de funcionário ──
    frame_cad = tk.LabelFrame(janela, text=" Cadastrar Funcionario ",
                               font=FONTE_NORMAL, bg=COR_PAINEL,
                               fg=COR_TEXTO, padx=10, pady=10)
    frame_cad.pack(padx=20, fill="x", pady=5)

    campos = {}
    for label, key in [("Matricula:", "matricula"), ("Nome:", "nome"), ("Senha:", "senha")]:
        f = tk.Frame(frame_cad, bg=COR_PAINEL)
        f.pack(fill="x", pady=2)
        tk.Label(f, text=label, font=FONTE_NORMAL, bg=COR_PAINEL,
                 fg=COR_TEXTO, width=10, anchor="w").pack(side="left")
        show = "*" if key == "senha" else ""
        e = tk.Entry(f, font=FONTE_NORMAL, bg="#2a2a3e", fg=COR_TEXTO,
                     insertbackground="white", show=show)
        e.pack(side="left", fill="x", expand=True)
        campos[key] = e

    label_cad = tk.Label(frame_cad, text="", font=FONTE_NORMAL, bg=COR_PAINEL)
    label_cad.pack()

    def cadastrar():
        mat  = campos["matricula"].get().strip()
        nome = campos["nome"].get().strip()
        sen  = campos["senha"].get().strip()

        if not mat or not nome or not sen:
            label_cad.config(text="Preencha todos os campos", fg=COR_ERRO)
            return
        try:
            cadastrar_funcionario(mat, nome, sen, id_gestor)
            label_cad.config(text=f"Funcionario {nome} cadastrado!", fg=COR_OK)
            for c in campos.values():
                c.delete(0, tk.END)
            atualizar_lista()
        except Exception as e:
            label_cad.config(text="Matricula ja existe", fg=COR_ERRO)

    tk.Button(frame_cad, text="CADASTRAR", font=FONTE_BTN,
              bg=COR_DESTAQUE, fg=COR_TEXTO,
              command=cadastrar).pack(pady=5)

    # ── Lista de funcionários ──
    frame_lista = tk.LabelFrame(janela, text=" Funcionarios ",
                                 font=FONTE_NORMAL, bg=COR_PAINEL,
                                 fg=COR_TEXTO, padx=10, pady=5)
    frame_lista.pack(padx=20, fill="both", expand=True, pady=5)

    lista = tk.Listbox(frame_lista, font=FONTE_NORMAL, bg="#2a2a3e",
                       fg=COR_TEXTO, selectbackground=COR_DESTAQUE,
                       height=6)
    lista.pack(fill="both", expand=True)

    funcionarios_cache = []

    def atualizar_lista():
        lista.delete(0, tk.END)
        funcionarios_cache.clear()
        for f in listar_funcionarios(id_gestor):
            funcionarios_cache.append(f)
            status = "ATIVO" if f[3] else "INATIVO"
            cor_status = "[+]" if f[3] else "[-]"
            lista.insert(tk.END, f"{cor_status} {f[1]} - {f[2]} ({status})")

    def alternar():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um funcionario")
            return
        func = funcionarios_cache[sel[0]]
        alternar_acesso(func[0])
        atualizar_lista()

    tk.Button(frame_lista, text="ATIVAR / DESATIVAR SELECIONADO",
              font=FONTE_BTN, bg="#6272a4", fg=COR_TEXTO,
              command=alternar).pack(pady=5)

    def sair_painel():
        janela.destroy()
        tela_inicial(callback_funcionario)

    tk.Button(janela, text="Sair do Painel", font=FONTE_NORMAL,
              bg=COR_FUNDO, fg="#888", bd=0,
              command=sair_painel).pack(pady=5)

    atualizar_lista()
    janela.mainloop()


# ──────────────────────────────────────────
# UTILITÁRIO
# ──────────────────────────────────────────
def centralizar(janela, largura, altura):
    sw = janela.winfo_screenwidth()
    sh = janela.winfo_screenheight()
    x  = (sw - largura) // 2
    y  = (sh - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


# ──────────────────────────────────────────
# PONTO DE ENTRADA PÚBLICO
# ──────────────────────────────────────────
def abrir_login(callback_sucesso):
    tela_inicial(callback_sucesso)