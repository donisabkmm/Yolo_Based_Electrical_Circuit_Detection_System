import os
import xml.etree.ElementTree as ET
import yaml

# 📁 Paths
xml_folder = "data"
dataset_path = "./dataset"

# 🔥 Use SET first (to avoid duplicates)
classes_set = set([
    "AND_Operation",
    "Alarm",
    "Annotation",
    "Cause",
    "Circle_common",
    "Connector",
    "Cross_Connector",
    "Decision",
    "Explanatory_Note",
    "Flow_Line",
    "Indication_Lamp",
    "Manual_Input",
    "Manual_Operation",
    "OR_Operation",
    "Predefined_Process",
    "Preparation",
    "Process",
    "Rect_common",
    "Table",
    "Terminal",
    "Triangle_Connector"
])

# 🔍 Extract classes from XML (optional but safe)
for file in os.listdir(xml_folder):
    if file.endswith(".xml"):
        xml_path = os.path.join(xml_folder, file)

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.findall("object"):
            name = obj.find("name").text.strip()
            classes_set.add(name)

# 🔄 Convert to sorted list (IMPORTANT for YOLO consistency)
classes = sorted(list(classes_set))

# 📄 Create YAML data
data_yaml = {
    "path": dataset_path,
    "train": "images/train",
    "val": "images/val",
    "nc": len(classes),
    "names": classes
}

# 💾 Save YAML
with open("../model/dataset/data.yaml", "w") as f:
    yaml.dump(data_yaml, f, sort_keys=False)

print("✅ data.yaml created successfully!")
print("📊 Total classes:", len(classes))
print("📌 Classes:", classes)