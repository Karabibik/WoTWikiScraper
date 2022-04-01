from tqdm import tqdm
from glob import glob

files = glob(".\\Randland\\*.md")

total = 0
for each_file in tqdm(files):
    with open(each_file, "r", encoding="utf-8") as f:
        cont = f.read()

    links = cont.count("[[")
    total += links

print(total)