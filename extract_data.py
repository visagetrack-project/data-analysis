import xml.etree.ElementTree as ET
import os
import re


def extract_number(file_name):
    # Extrai o número do nome do arquivo
    number = re.findall(r'\d+', file_name)
    return int(number[0]) if number else 0


folder = r"C:\Users\wyllg\Desktop\PDI_IA\data_PDI\dataset"
sorted_files = sorted(os.listdir(folder), key=extract_number)

squares = {
    'square 1': (250, 800),
    'square 2': (620, 800),
    'square 3': (990, 800),
    'square 4': (1380, 800),
    'square 5': (1750, 800),
    'square 6': (430, 625),
    'square 7': (710, 625),
    'square 8': (980, 625),
    'square 9': (1260, 625),
    'square 10': (1535, 625),
    'square 11': (590, 510),
    'square 12': (780, 510),
    'square 13': (980, 510),
    'square 14': (1170, 510),
    'square 15': (1370, 510)
}
squares_lists = {name: [] for name in squares}

day = 0
for file in sorted_files:
    if file.endswith(".xml"):
        squares_empty = {name: True for name in squares}
        squares_full = {name: None for name in squares}
        full_path = os.path.join(folder, file)
        xml = ET.parse(full_path)
        root = xml.getroot()

        for obj in root.iter('object'):
            bndbox = obj.find('bndbox')
            blob = obj.find('name').text
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # Verifica se o objeto está dentro de algum quadrado
            for name, coords in squares.items():
                x, y = coords
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    squares_empty[name] = False
                    squares_full[name] = blob
        print()
        print("----------------------------------")
        print("DAY:", day + 1)
        print(f'Processing file: {full_path}')
        print()
        for name, is_empty in squares_empty.items():
            if is_empty:
                print(f'{name} is empty')
                squares_lists[name].append("missing")
            else:
                print(f'{name} is full with {squares_full[name]}')
                squares_lists[name].append(squares_full[name])
        day += 1
