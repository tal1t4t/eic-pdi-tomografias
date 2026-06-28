import pydicom
from utils import in_file, out_file

def tira_nome(img_dicom):
    dicomfile = pydicom.dcmread(img_dicom)

    # futuramente deixar as atribuição num formato aleatório
    dicomfile.PatientID = "Anonimo123"
    dicomfile.PatientName = "Anonimo123"

    # mudar o caminho de salvamento depois que alterar os diretórios
    dicomfile.save_as(out_file(dicomfile.PatientName, ".dcm"))