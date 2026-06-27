import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
'''
pega o caminho relativo ao utils.py
__file__ corresponde ao caminho do arquivo que está em execução ou sendo importado
os.path.abspath(__file__) transforma em caminho absoluto
os.path.dirname(os.path.abspath(__file__)) retorna o caminho onde se encontra o arquivo em execução,
sem indicar o arquivo propriamente dito
'''


INPUT_FOLDER = os.path.join(BASE_DIR,"input")
OUTPUT_FOLDER = os.path.join(BASE_DIR,"output")

def in_file(filename):
    return os.path.join(INPUT_FOLDER, filename)

def out_file(filename):
    return os.path.join(OUTPUT_FOLDER, filename)
