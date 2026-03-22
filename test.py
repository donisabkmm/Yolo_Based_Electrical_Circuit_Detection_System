from ultralytics import YOLO
import cv2
import json

model_path = r"C:\Users\DakBle\Desktop\Project\yoloCX\model\runs\detect\runs\detect\circuit_model4\weights\best.pt"

print("Using model:", model_path)

model = YOLO(model_path)

image_path = r"C:\Users\DakBle\Desktop\Project\yoloCX\shared\image_store_circuit\EM-02_MAIN SWITCHBOARD\EM-02_MAIN SWITCHBOARD_page_87.png"

img = cv2.imread(image_path)

results = model(image_path, conf=0.25, imgsz=1024)

class_names = model.names

detections_json = []

for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label_name = class_names[cls_id]

        detections_json.append({
            "class_id": cls_id,
            "class_name": label_name,
            "confidence": round(conf, 4),
            "bbox": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
        })

        label = f"{label_name} {conf:.2f}"

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1)

        cv2.putText(img, label, (x1, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

output_path = "output_detected.png"
cv2.imwrite(output_path, img)

print("Saved output to:", output_path)

json_path = "detections.json"
with open(json_path, "w") as f:
    json.dump(detections_json, f, indent=4)

print("Saved JSON to:", json_path)

cv2.imshow("Detection Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()