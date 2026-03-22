import os
import shutil

def copy_matched_files(src_folder, dst_img_folder, dst_txt_folder):
    # Create destination folders if not exist
    os.makedirs(dst_img_folder, exist_ok=True)
    os.makedirs(dst_txt_folder, exist_ok=True)

    # Get all files
    files = os.listdir(src_folder)

    # Separate png and txt
    png_files = {os.path.splitext(f)[0]: f for f in files if f.endswith(".png")}
    txt_files = {os.path.splitext(f)[0]: f for f in files if f.endswith(".txt")}

    # Find common names
    common_names = set(png_files.keys()) & set(txt_files.keys())

    print(f"Found {len(common_names)} matched pairs")

    # Copy files
    for name in common_names:
        png_src = os.path.join(src_folder, png_files[name])
        txt_src = os.path.join(src_folder, txt_files[name])

        png_dst = os.path.join(dst_img_folder, png_files[name])
        txt_dst = os.path.join(dst_txt_folder, txt_files[name])

        shutil.copy2(png_src, png_dst)
        shutil.copy2(txt_src, txt_dst)

        print(f"Copied: {name}")

    print("✅ Done!")


src_folder= r"C:\Users\DakBle\Desktop\Project\yoloCX\shared\image_store_circuit\EM-05_LOCAL_GROUP_STARTER_INDIVIDUAL_STARTER"
dst_img_folder= r"C:\Users\DakBle\Desktop\Project\yoloCX\model\dataset_circuit\images\train"
dst_txt_folder= r"C:\Users\DakBle\Desktop\Project\yoloCX\model\dataset_circuit\labels\train"


copy_matched_files(src_folder, dst_img_folder, dst_txt_folder)