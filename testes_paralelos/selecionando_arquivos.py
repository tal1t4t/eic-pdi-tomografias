import os
from tkinter import filedialog, messagebox
from copiar import copiar_origem_destino

def deve_continuar():
    # askyesno retorna True para sim e False para não
    return messagebox.askyesno(title='Adicionar linha', 
                                    message='Gostaria de selecionar caminhos de origem e destino?')

def construir_origem_destino(nomearquivo, modo='w'):
    # com a cláusula 'with', o arquivo só estará aberto enquanto o código identado estiver em 
    # execução
    with open(os.path.join('.','pillow', 'input', 'diretorios.csv'), modo) as dircsv:
        #cabeçalho do csv
        dircsv.write('origem,destino\n')

        while deve_continuar(): 
            # askdirectory retorna o caminho do diretório selecionado
            in_path = filedialog.askdirectory()
            out_path = filedialog.askdirectory()
            dircsv.write(f'{in_path},{out_path}\n')
     
if __name__ == '__main__':
    arquivo = os.path.join('.','pillow', 'input', 'diretorios.csv')
    construir_origem_destino(arquivo, 'a')# w sobrescreve o arquivo e 'a' acrescenta no fim(append)
    copiar_origem_destino(arquivo)