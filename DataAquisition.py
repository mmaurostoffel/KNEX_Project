#Unpack 7z file
'''
import py7zr
with py7zr.SevenZipFile('dok/warhammer40k_pages_current.xml.7z', mode='r') as z:
    x = z.extractall()
print(x)
'''

#Split file at page tags
import xml.etree.ElementTree as ET


def split_xml_by_page(file_path, output_folder):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find all <page> elements
    pages = root.findall('{http://www.mediawiki.org/xml/export-0.11/}page')

    for i, page in enumerate(pages, start=1):
        # Create a new XML tree with a single <page> element
        page_tree = ET.ElementTree(page)

        # Write the new tree to a file
        output_path = f"{output_folder}/page_{i}.xml"
        page_tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Saved {output_path}")


# Usage example
file_path = 'dok/warhammer40k_pages_current.xml'
output_folder = 'dok/splitFiles'
split_xml_by_page(file_path, output_folder)
