import re
import numpy as np

def cleaning(cellcontent):
    p = re.compile('\.+')
    if(isinstance(cellcontent, str)):
        m = p.match(cellcontent)
        if m:
            return np.NaN
    return cellcontent




print( cleaning('...'))
print( cleaning('Marta'))
print( cleaning(1.5))
