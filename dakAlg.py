import cv2
import numpy as np
import os
import json

# -----------------------------
# Load Image
# -----------------------------
img_path = r"C:\Users\DakBle\Desktop\Project\yoloCX\model\dataset\images\train\EM-02_MAIN SWITCHBOARD_page_19.png"

if not os.path.exists(img_path):
    raise FileNotFoundError("Image not found")

img = cv2.imread(img_path)
h, w = img.shape[:2]

# -----------------------------
# 🔥 IMPROVED PREPROCESSING
# -----------------------------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bw = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY_INV,
    15, 2
)

# 🔥 Strong connection (fix broken lines)
bw = cv2.dilate(bw, np.ones((5,5), np.uint8), iterations=2)

# 🔥 Close gaps
bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

# -----------------------------
# Line extraction (LESS STRICT)
# -----------------------------
kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
horizontal = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_h)

kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
vertical = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_v)

lines = cv2.bitwise_or(horizontal, vertical)

# -----------------------------
# Skeletonize
# -----------------------------
def skeletonize(img):
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

    while True:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        if cv2.countNonZero(img) == 0:
            break

    return skel

skel = skeletonize(lines)

# -----------------------------
# Helpers
# -----------------------------
def get_neighbors(x, y, img):
    neighbors = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x+dx, y+dy
            if 0 <= nx < img.shape[1] and 0 <= ny < img.shape[0]:
                if img[ny, nx] > 0:
                    neighbors.append((nx, ny))
    return neighbors

visited = np.zeros_like(skel)
segments = []

# -----------------------------
# Extract segments (LESS FILTER)
# -----------------------------
for y in range(h):
    for x in range(w):
        if skel[y, x] > 0 and visited[y, x] == 0:

            stack = [(x, y)]
            path = [(x, y)]
            visited[y, x] = 1

            while stack:
                cx, cy = stack.pop()
                for nx, ny in get_neighbors(cx, cy, skel):
                    if visited[ny, nx] == 0:
                        visited[ny, nx] = 1
                        stack.append((nx, ny))
                        path.append((nx, ny))

            # 🔥 keep smaller segments also
            if len(path) > 5:
                segments.append(path)

# -----------------------------
# Draw + JSON
# -----------------------------
output = img.copy()
line_data = []

for i, seg in enumerate(segments):

    xs = [p[0] for p in seg]
    ys = [p[1] for p in seg]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    width = x_max - x_min
    height = y_max - y_min

    # 🔥 FILTER: ONLY STRAIGHT LINES
    if width > height * 3:
        orientation = "horizontal"
    elif height > width * 3:
        orientation = "vertical"
    else:
        continue  # ❌ reject diagonal / noise

    # 🔥 Draw clean straight line
    if orientation == "horizontal":
        y = int(np.mean(ys))
        cv2.line(output, (x_min, y), (x_max, y), (0, 255, 0), 2)

    else:
        x = int(np.mean(xs))
        cv2.line(output, (x, y_min), (x, y_max), (0, 255, 0), 2)

    # Label
    cx = int(np.mean(xs))
    cy = int(np.mean(ys))

    cv2.putText(output, f"L{i}", (cx, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)

    # Save JSON
    line_data.append({
        "id": f"line_{i}",
        "orientation": orientation,
        "bbox": {
            "x": int(x_min),
            "y": int(y_min),
            "width": int(width),
            "height": int(height)
        },
        "points": {
            "start": [int(x_min), int(y_min)],
            "end": [int(x_max), int(y_max)]
        }
    })
# -----------------------------
# Save outputs
# -----------------------------
cv2.imwrite("FINAL_LINES.png", output)

output_json = {
    "image": os.path.basename(img_path),
    "image_size": {"width": w, "height": h},
    "num_lines": len(line_data),
    "lines": line_data
}

with open("lines_output.json", "w") as f:
    json.dump(output_json, f, indent=4)

print(f"✅ Done: {len(line_data)} lines")
print("🖼️ Image saved: FINAL_LINES.png")
print("📄 JSON saved: lines_output.json")