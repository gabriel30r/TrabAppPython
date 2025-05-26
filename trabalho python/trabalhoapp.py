import tkinter as tk
from tkinter import messagebox
import sqlite3

# ======================
# BANCO DE DADOS
# ======================

def inicializar_banco():
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            curso TEXT NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10)
        )
    ''')
    conn.commit()
    cursor.execute("SELECT * FROM alunos")
    print(cursor.fetchall())
    conn.close()

def cadastrar_aluno():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    curso = entry_curso.get()
    nota = entry_nota.get()

    if all([matricula, nome, curso, nota]):
        try:
            nota = float(nota)
            if 0 <= nota <= 10:
                conn = sqlite3.connect('alunos.db')
                cursor = conn.cursor()

                try:
                    cursor.execute('''
                        INSERT INTO alunos (matricula, nome, curso, nota)
                        VALUES (?, ?, ?, ?)
                    ''', (matricula, nome, curso, nota))
                    conn.commit()
                    messagebox.showinfo("Cadastro Realizado", f"Aluno {nome} cadastrado com sucesso!")
                    limpar_campos()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Erro", "Já existe um aluno com essa matrícula.")
                finally:
                    conn.close()
            else:
                messagebox.showwarning("Nota Inválida", "A nota deve estar entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro de Valor", "A nota deve ser um número.")
    else:
        messagebox.showwarning("Campos Vazios", "Preencha todos os campos antes de cadastrar.")

def remover_aluno():
    matricula = entry_matricula.get()

    if matricula:
        conn = sqlite3.connect('alunos.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
        resultado = cursor.fetchone()

        if resultado:
            confirmacao = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o aluno com matrícula {matricula}?")
            if confirmacao:
                cursor.execute('DELETE FROM alunos WHERE matricula = ?', (matricula,))
                conn.commit()
                messagebox.showinfo("Remoção", "Aluno removido com sucesso.")
                limpar_campos()
        else:
            messagebox.showwarning("Não Encontrado", "Nenhum aluno encontrado com essa matrícula.")

        conn.close()
    else:
        messagebox.showwarning("Campo Requerido", "Informe a matrícula do aluno para remover.")

def consultar_aluno():
    matricula = entry_matricula.get()

    if matricula:
        conn = sqlite3.connect('alunos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome, curso, nota FROM alunos WHERE matricula = ?', (matricula,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            nome, curso, nota = resultado
            mensagem = (
                f"Nome: {nome}\n"
                f"Curso: {curso}\n"
                f"Nota: {nota}"
            )
            messagebox.showinfo("Consulta de Aluno", mensagem)
        else:
            messagebox.showwarning("Não Encontrado", "Aluno não encontrado com a matrícula fornecida.")
    else:
        messagebox.showwarning("Campo Requerido", "Informe a matrícula do aluno.")

def limpar_campos():
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_curso.delete(0, tk.END)
    entry_nota.delete(0, tk.END)

# ======================
# INTERFACE
# ======================

root = tk.Tk()
root.title("Sistema Acadêmico - Cadastro de Notas")
root.geometry("1024x768")
root.configure(bg="#e9eef1")

# Frame container que ocupa a tela inteira
frame_container = tk.Frame(root, bg="#e9eef1")
frame_container.pack(fill="both", expand=True)

# Frame centralizado para o formulário
frame_formulario = tk.Frame(frame_container, bg="#ffffff", padx=40, pady=30)
frame_formulario.pack(expand=True)

# Título
titulo = tk.Label(frame_formulario, text="Cadastro Acadêmico de Notas", font=("Segoe UI", 20, "bold"), bg="#ffffff")
titulo.grid(row=0, column=0, columnspan=2, pady=(0, 30))

# Campos
campos = [
    ("Matrícula:", "entry_matricula"),
    ("Nome Completo:", "entry_nome"),
    ("Curso:", "entry_curso"),
    ("Nota (0 a 10):", "entry_nota")
]

entries = {}

for i, (label_text, var_name) in enumerate(campos, start=1):
    label = tk.Label(frame_formulario, text=label_text, font=("Segoe UI", 11), bg="#ffffff")
    label.grid(row=i, column=0, sticky="e", pady=10, padx=10)

    entry = tk.Entry(frame_formulario, font=("Segoe UI", 11), width=40)
    entry.grid(row=i, column=1, sticky="w", pady=10, padx=10)

    entries[var_name] = entry

entry_matricula = entries["entry_matricula"]
entry_nome = entries["entry_nome"]
entry_curso = entries["entry_curso"]
entry_nota = entries["entry_nota"]

# Botões
btn_cadastrar = tk.Button(
    frame_formulario, text="Cadastrar Aluno", font=("Segoe UI", 12, "bold"),
    bg="#4CAF50", fg="white", padx=20, pady=10, command=cadastrar_aluno
)
btn_cadastrar.grid(row=6, column=0, pady=30, sticky="e", padx=10)

btn_consultar = tk.Button(
    frame_formulario, text="Consultar por Matrícula", font=("Segoe UI", 12, "bold"),
    bg="#2196F3", fg="white", padx=20, pady=10, command=consultar_aluno
)
btn_consultar.grid(row=6, column=1, pady=30, sticky="w", padx=10)

btn_remover = tk.Button(
    frame_formulario, text="Remover Aluno", font=("Segoe UI", 12, "bold"),
    bg="#f44336", fg="white", padx=20, pady=10, command=remover_aluno
)
btn_remover.grid(row=7, column=0, columnspan=2, pady=(0, 20))


# Responsividade
for i in range(7):
    frame_formulario.grid_rowconfigure(i, weight=1)
frame_formulario.grid_columnconfigure(0, weight=1)
frame_formulario.grid_columnconfigure(1, weight=2)

# Inicializar o banco
inicializar_banco()

# Loop da interface
root.mainloop()
