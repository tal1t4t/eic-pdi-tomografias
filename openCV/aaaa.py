import pydicom
from utils import in_file

ds = pydicom.dcmread(in_file('img2.dcm'))
print(type(ds.WindowCenter))