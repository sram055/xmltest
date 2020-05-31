import csv
from collections import OrderedDict
import lxml.etree as ET

# BUILD NESTED ID DICTIONARY FROM CSV
with open("input.csv") as f:
    reader = csv.DictReader(f)      

    id_dct = OrderedDict({})
    for dct in reader:      
        if dct["id"] not in id_dct.keys():
            id_dct[dct["id"]] = [OrderedDict({k:v for k,v in dct.items() if k!= "id"})]
        else:
            id_dct[dct["id"]].append(OrderedDict({k:v for k,v in dct.items() if k!= "id"}))         

# INITIALIZING XML FILE WITH ROOT AND NAMESPACE
root = ET.Element('R-Profiles', nsmap={None: "http://WKI/Roughness-Profiles/1"})

# WRITING TO XML NODES
for k,v in id_dct.items():  
    rpNode = ET.SubElement(root, "R-Profile")
    ET.SubElement(rpNode, "id").text = str(k)
    surfacesNode = ET.SubElement(rpNode, "surfaces")

    for dct in v:
        surfaceNode = ET.SubElement(surfacesNode, "surface")
        for k,v in dct.items():         
            ET.SubElement(surfaceNode, k).text = str(v)

# OUTPUT XML CONTENT TO FILE
tree_out = ET.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

with open('Output.xml','wb') as f:
    f.write(tree_out)
