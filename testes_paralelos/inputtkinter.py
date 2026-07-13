import tkinter as tk

def inserir_valor():
    texto = entrada_tlower.get()
    rotulo.config(text=texto)
janela = tk.Tk()
janela.title = "Inserção de valores para o threshold"
janela.geometry("300x200")

entrada_tlower = tk.Entry(janela, font=("Arial", 14))
entrada_tlower.pack(pady = 10)

# entrada_tupper = tk.Entry(janela, font=("Arial", 14))
# entrada_tupper.pack(pady = 10)

botao = tk.Button(janela, text="inserir valores", command=inserir_valor)
botao.pack(pady=10)

rotulo = tk.Label(janela, text="digite dois valores", font=("Arial", 12))
rotulo.pack(pady=10)


janela.mainloop()