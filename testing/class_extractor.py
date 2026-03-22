import os
import xml.etree.ElementTree as ET
import json

xml_folder = "./data"
classes = set()

for file in os.listdir(xml_folder):
    if file.endswith(".xml"):
        xml_path = os.path.join(xml_folder, file)

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.findall("object"):
            name = obj.find("name").text.strip()
            classes.add(name)

classes_list = sorted(list(classes))

output_file = "classes.json"
with open(output_file, "w") as f:
    json.dump(classes_list, f, indent=4)

print("✅ Classes extracted and saved!")
print(classes_list)