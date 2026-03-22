import pandas as pd

file_path = "Symbols_classes.csv"
df = pd.read_csv(file_path)

column_name = "Symbol Name "

classes = sorted(df[column_name].dropna().unique())
with open("classes.txt", "w") as f:
    for c in classes:
        f.write(str(c).strip() + "\n")

print("classes.txt created successfully!")