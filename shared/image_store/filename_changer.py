import os

base_path = r"C:\Users\DakBle\Desktop\Project\yoloCX\shared\image_store\EM-13_AMS"

folder_name = os.path.basename(base_path)

for file_name in os.listdir(base_path):

    if file_name.endswith(".txt"):
        old_path = os.path.join(base_path, file_name)

        # Extract page number
        name_part = file_name.split('.')[0]   # page_1
        page_number = name_part.split('_')[-1]

        # New name
        new_name = f"{folder_name}_page_{page_number}.txt"
        new_path = os.path.join(base_path, new_name)

        os.rename(old_path, new_path)

        print(f"Renamed: {file_name} → {new_name}")