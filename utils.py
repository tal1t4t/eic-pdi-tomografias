import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# pega o caminho relativo ao utils.py
# __file__ corresponde ao caminho do arquivo que está em execução ou sendo importado
# os.path.abspath(__file__) transforma em caminho absoluto
# os.path.dirname(os.path.abspath(__file__)) retorna o caminho onde se encontra o arquivo em execução,
# sem indicar o arquivo propriamente dito

INPUT_FOLDER = os.path.join(BASE_DIR,"input")
OUTPUT_FOLDER = os.path.join(BASE_DIR,"output")

def in_file(filename):
    return os.path.join(INPUT_FOLDER, filename)

def out_file(filename):
    return os.path.join(OUTPUT_FOLDER, filename)

def out_thresholds(nome_original, filename, kgauss, low, high):
    # gauss = f'gauss{kgauss}'
    thresholds = f'{low}_{high}'
    if not os.path.exists(out_file(nome_original)):
        os.mkdir(out_file(nome_original))

    # if not os.path.exists(os.path.join(OUTPUT_FOLDER, nome_original, gauss)):
    #     os.mkdir(os.path.join(OUTPUT_FOLDER, nome_original, gauss))
    interno = True
    path_gauss = out_gauss(nome_original, filename, kgauss, interno)

    if not os.path.exists(os.path.join(path_gauss, thresholds)):
        os.mkdir(os.path.join(path_gauss, thresholds))

    caminho = os.path.join(path_gauss, thresholds, filename)

    return caminho

def out_gauss(nome_original, filename, kgauss, interno=False):
    gauss = f'gauss{kgauss}'
    
    if not os.path.exists(os.path.join(OUTPUT_FOLDER, nome_original, gauss)):
        os.mkdir(os.path.join(OUTPUT_FOLDER, nome_original, gauss))
    
    if interno:
        caminho_gauss = os.path.join(OUTPUT_FOLDER, nome_original, gauss)
    
    else:
        caminho_gauss = os.path.join(OUTPUT_FOLDER, nome_original, gauss, filename)

    return caminho_gauss