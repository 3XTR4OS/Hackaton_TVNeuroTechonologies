import json

import PySimpleGUI as sg

layout = [
    [sg.Text('File 1'), sg.InputText(), sg.FileBrowse(key="-FILE-"), ],
    [sg.Output(size=(125, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('File Compare', layout)


def weighted(elem):
    if elem is None:
        return 'z'

    else:
        return elem


while True:
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break

    if event == 'Submit':
        file_path = values["-FILE-"]
        print('_' * 100)
        print(f'ПОПЫТКА ОБРАБОТКИ ФАЙЛА {file_path}')
        print('_' * 100)
        try:
            with open(file_path, 'r+', encoding='utf-8') as file:
                file = json.load(file)
                # file = sorted(file, key=lambda x: weighted(x['role'])) # Сортировка по ролям.
                for row in file:
                    print('-' * 100)  # Разделитель (для читаемости)
                    for elem in row:
                        # Условие для обработки строки без вылетов из-за None type'а
                        print(elem, '-', row[elem] if row is not None else None)
        except:
            print('ФАЙЛ НЕ СООТВЕСТВУЕТ ФОРМАТУ/СТРУКТУРЕ JSON ФАЙЛА')

    # print(values[0],values[3])
