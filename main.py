from pdf2image import convert_from_path
import os

pdf_path = "shared/store/MM-10 COMPOSITE BOILER.pdf"
output_folder = "shared/image_store/MM-10 COMPOSITE BOILER"

os.makedirs(output_folder, exist_ok=True)

images = convert_from_path(
    pdf_path,
    dpi=400,
    fmt="png",
    thread_count=4,
)

for i, image in enumerate(images):
    output_path = os.path.join(output_folder, f"page_{i + 1}.png")

    image.save(
        output_path,
        "PNG",
        optimize=True
    )

    print(f"Saved: {output_path}")