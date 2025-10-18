from src.lsh import LSH
import csv 



with open("topviews-2019_04.csv",) as f:
    reader = csv.DictReader(f, delimiter=',')
    rows = (list(reader))

page_names = [row['Page'] for row in rows]

lsh = LSH(band_size=10)

lsh.fit(page_names)

result = lsh.find_candidates()

print(result)

for x_id,y_id in result:
    print("-"*50)
    print(page_names[x_id])
    print(page_names[y_id])
    print("-"*50)
