import os
import json
import xml.etree.ElementTree as ET

# =========================
# 📁 PATH CONFIG
# =========================

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# XML folder (input)
XML_DIR = "./data"

# Output labels folder
LABEL_DIR = os.path.join(BASE_DIR, "../model/dataset/labels")

# Classes JSON path
CLASSES_PATH = os.path.join(BASE_DIR, "../testing/classes.json")

# Create labels folder if not exists
os.makedirs(LABEL_DIR, exist_ok=True)

print("XML_DIR:", XML_DIR)
print("LABEL_DIR:", LABEL_DIR)
print("CLASSES_PATH:", CLASSES_PATH)



if not os.path.exists(CLASSES_PATH):
    raise FileNotFoundError(f"❌ classes.json not found at: {CLASSES_PATH}")

with open(CLASSES_PATH, "r") as f:
    classes = json.load(f)

print("✅ Loaded classes:", len(classes))



def convert(size, box):
    w, h = size
    xmin, xmax, ymin, ymax = box

    x_center = (xmin + xmax) / 2.0 / w
    y_center = (ymin + ymax) / 2.0 / h
    width = (xmax - xmin) / w
    height = (ymax - ymin) / h

    return x_center, y_center, width, height



for xml_file in os.listdir(XML_DIR):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(XML_DIR, xml_file)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"❌ Error parsing {xml_file}: {e}")
        continue

    # Get image size
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    # Output txt file
    txt_file = xml_file.replace(".xml", ".txt")
    txt_path = os.path.join(LABEL_DIR, txt_file)

    with open(txt_path, "w") as f:
        for obj in root.findall("object"):
            cls = obj.find("name").text.strip()

            # Skip unknown classes
            if cls not in classes:
                print(f"⚠️ Skipping unknown class '{cls}' in {xml_file}")
                continue

            cls_id = classes.index(cls)

            bbox = obj.find("bndbox")
            xmin = float(bbox.find("xmin").text)
            ymin = float(bbox.find("ymin").text)
            xmax = float(bbox.find("xmax").text)
            ymax = float(bbox.find("ymax").text)

            x, y, bw, bh = convert((w, h), (xmin, xmax, ymin, ymax))

            f.write(f"{cls_id} {x} {y} {bw} {bh}\n")

    print(f"✅ Converted: {xml_file} → {txt_file}")



print("\n🚀 XML → YOLO conversion completed successfully!")