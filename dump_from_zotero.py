import requests
import time
import os
from acdh_tei_pyutils.tei import TeiReader
from lxml import etree


def parse_and_pretty_save(xml_input_file, xml_output_file):
    """
    Parses an XML file, processes it, and saves it with pretty indentation.
    :param xml_input_file: The path to the input XML file.
    :param xml_output_file: The path where the new XML should be saved.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_input_file, parser)
    root = tree.getroot()

    with open(xml_output_file, "wb") as f:
        f.write(
            etree.tostring(
                root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
            )
        )

    print(f"Formatted XML saved to {xml_output_file}")


API_KEY = os.environ.get("ZOTERO_API_KEY")
USER_ID = os.environ.get("ZOTERO_USER_ID")
COLLECTION_ID = "5701116"
PAGE_SIZE = 1
zotero_url = f"https://api.zotero.org/groups/{COLLECTION_ID}/items?format=tei&limit={PAGE_SIZE}"  # noqa:
headers = {
    "Zotero-API-Key": API_KEY,
}
response = requests.get(zotero_url, headers=headers)
item_count = response.headers["Total-Results"]

dummy = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Tillich Literaturverzeichnis</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Datendump aus Zotero-Collection</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <listBibl></listBibl>
      </body>
  </text>
</TEI>
"""
doc = TeiReader(dummy)
root_node = doc.any_xpath(".//tei:listBibl")[0]

PAGE_SIZE = 50
for i in range(0, int(item_count), PAGE_SIZE):
    zotero_url = f"https://api.zotero.org/groups/{COLLECTION_ID}/items?format=tei&limit={PAGE_SIZE}&start={i}"  # noqa: E501
    print(zotero_url)
    response = requests.get(zotero_url, headers=headers)
    cur_doc = TeiReader(response.text)
    for x in cur_doc.any_xpath(".//tei:biblStruct[@xml:id]"):
        new_xml_id = x.attrib["corresp"].split("/")[-1]
        x.attrib["{http://www.w3.org/XML/1998/namespace}id"] = (
            f"tillich__{new_xml_id}"  # noqa:
        )
        root_node.append(x)
    time.sleep(2)
    doc.tree_to_file("listbibl.xml")

parse_and_pretty_save("listbibl.xml", "listbibl.xml")
