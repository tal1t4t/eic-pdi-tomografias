import pydicom
from utils import in_file, out_file

dicomfile = pydicom.dcmread(in_file("com_nome.dcm"))
dicomfile.PatientName = "Anonimo123"
dicomfile.PatientID = "Anonimo123"

dicomfile.save_as(out_file("anonimo.dcm"))
print(pydicom.dcmread(out_file("anonimo.dcm")))