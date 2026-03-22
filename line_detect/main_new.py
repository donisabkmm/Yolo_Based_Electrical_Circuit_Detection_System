import cv2
import numpy as np
import os
import json

# -----------------------------
# Load Image
# -----------------------------
img_path = r"C:\Users\DakBle\Desktop\Project\yoloCX\model\dataset\images\train\EM-02_MAIN SWITCHBOARD_page_19.png"

img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -----------------------------
# Edge Detection (IMPORTANT)
# -----------------------------
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# -----------------------------
# Hough Line Detection
# -----------------------------
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi/180,
    threshold=100,
    minLineLength=50,
    maxLineGap=10
)

output = img.copy()
line_data = []

if lines is not None:
    for i, line in enumerate(lines):
        x1, y1, x2, y2 = line[0]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # 🔥 Keep ONLY straight lines
        if dx > dy * 3:
            orientation = "horizontal"
        elif dy > dx * 3:
            orientation = "vertical"
        else:
            continue  # skip diagonal

        # Draw line
        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2

        cv2.putText(output, f"L{i}", (mx, my),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)

        # Save JSON
        line_data.append({
            "id": f"line_{i}",
            "orientation": orientation,
            "points": {
                "start": [x1, y1],
                "end": [x2, y2]
            },
            "length": int(np.hypot(x2-x1, y2-y1))
        })

# -----------------------------
# Save
# -----------------------------
cv2.imwrite("HOUGH_LINES.png", output)

with open("lines_output.json", "w") as f:
    json.dump({
        "num_lines": len(line_data),
        "lines": line_data
    }, f, indent=4)

print(f"✅ Detected {len(line_data)} lines")