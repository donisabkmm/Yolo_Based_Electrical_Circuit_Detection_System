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
# SAME YOUR PIPELINE
# -----------------------------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bw = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY_INV,
    15, 2
)

kernel_connect = np.ones((3,3), np.uint8)
bw = cv2.dilate(bw, kernel_connect, iterations=1)

kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
horizontal = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_h)

kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
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
# Extract segments
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

            if len(path) > 10:
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

    orientation = "horizontal" if (x_max - x_min) > (y_max - y_min) else "vertical"

    # Draw line (green)
    for (x, y) in seg:
        output[y, x] = (0, 255, 0)

    # Put label (line number)
    cx = int(sum(xs) / len(xs))
    cy = int(sum(ys) / len(ys))

    cv2.putText(
        output,
        f"{i}",
        (cx, cy),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        1,
        cv2.LINE_AA
    )

    line_data.append({
        "id": f"line_{i}",
        "orientation": orientation,
        "bbox": {
            "x": int(x_min),
            "y": int(y_min),
            "width": int(x_max - x_min),
            "height": int(y_max - y_min)
        },
        "points": {
            "start": [int(xs[0]), int(ys[0])],
            "end": [int(xs[-1]), int(ys[-1])]
        },
        "length": len(seg)
    })

# -----------------------------
# Save outputs
# -----------------------------
cv2.imwrite("annotated_lines.png", output)

output_json = {
    "image": os.path.basename(img_path),
    "image_size": {"width": w, "height": h},
    "num_lines": len(line_data),
    "lines": line_data
}

with open("lines_output.json", "w") as f:
    json.dump(output_json, f, indent=4)

print(f"✅ Done: {len(line_data)} lines")
print("🖼️ Image saved: annotated_lines.png")
print("📄 JSON saved: lines_output.json")