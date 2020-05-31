import csv
import lxml.etree as etree

# INITIALIZING XML FILE WITH ROOT IN PROPER NAMESPACE
nsmap = {None: "http://WKI/Roughness-Profiles/1"}
root = etree.Element('Roughness-Profiles', nsmap=nsmap)

# READING CSV FILE
with open("test.csv") as f:
    reader = csv.DictReader(f)

    # WRITE INITIAL XML NODES
    for row in reader:
        surface_elem = etree.SubElement(root, "surface", nsmap=nsmap)
        for elem_name, elem_value in row.items():
            etree.SubElement(surface_elem, elem_name.strip(), nsmap=nsmap).text = str(elem_value)

# PARSE XSLT AND CREATE TRANSFORMER
xslt_root = etree.parse("test.xsl")
transform = etree.XSLT(xslt_root)

# TRANSFORM
#  (Note the weird use of tostring/fromstring. This was used so
#   namespaces in the XSLT would work the way they're supposed to.)
final_xml = transform(etree.fromstring(etree.tostring(root)))

# WRITE OUTPUT TO FILE
final_xml.write_output("test.xml")
