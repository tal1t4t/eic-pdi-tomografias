import os
import shutil
from pathlib import PurePath
from csv import DictReader # classe que lê arquivos CSV e passa cada linha para um dicionário

def copiar_origem_destino(nomearquivo):
    with open(nomearquivo) as meucsv:
        reader = DictReader(meucsv)
        for linha in reader:
            orig = linha['origem']
            dest = linha['destino']

            if os.path.exists(dest):
                nome = PurePath(orig).name
                dest = os.path.join(dest, nome)
            #faz uma cópia da pasta e tudo em seu interior
            shutil.copytree(orig, dest)
            print(linha['origem'])
            print(linha['destino'])
            print('----------------')

if __name__ == '__main__':
    copiar_origem_destino('input/diretorios.csv')