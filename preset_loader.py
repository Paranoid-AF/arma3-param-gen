import xml.etree.ElementTree as ET

def load(preset_path):
  xml_file = open(preset_path, "r", encoding="utf-8")
  xml_content = ET.parse(xml_file).getroot()
  xml_file.close()
  
  addon_list = xml_content.find("published-ids")
  addon_nodes = addon_list.findall("id")
  addons = []

  for item in addon_nodes:
    addons.append(item.text)

  return addons
