import pandas as pd

df= pd.read_excel("./data/BĐQT_ Ô tô quân sự 258.xlsx", header=None)
row_text = None

for _, row in df.iterrows():

        values = [
            str(x).strip()
            for x in row
            if pd.notna(x)
        ]

        row_text = " ".join(values)
        print(row_text)

