import json
import diag_creator

file_path = 'Пример входного JSON.txt'

states = {
    'PUBLISHED': 'Опубликовать',
    'UNPUBLISHED': 'Завершить',
    'NEW': 'Редактировать',
    'DELETED': 'Удалить',
    'FINISHED': 'Завершить',
    'ARCHIVE': 'В архив'
}
blocks = {
    'DISCUSSION': 'Обсудить',
    'LIBRARY': 'Библиотека',
    'MANAGEMENT': 'Управление'
}


def params_handler(row):
    # user_role - права пользователя
    user_role = row['role']

    # state - статус ИО
    if row['state'] is None:
        state = 'Пуст'
    else:
        state = states[row['state']['status']]

    # allowed_actions - Доступные действия
    if len(row['allowedActions']) == 0:
        allowed_actions = 'Пуст'
    else:
        allowed_actions = [i['name'] for i in row['allowedActions']]

    # allowedBlocks - Доступные к отображению блоки
    if len(row['allowedBlocks']) == 0:
        allowed_blocks = 'Пуст'
    else:
        allowed_blocks = [blocks[i] for i in row['allowedBlocks']]

    # СОЗДАТЬ ДИАГРАММУ ПО ПОЛУЧЕННЫМ ПАРАМЕТРАМ
    diag_creator.diagram_creator(user_role, state, allowed_actions, allowed_blocks)


with open(file_path, 'r+', encoding='utf-8') as file:
    file = json.load(file)

    for row in file:
        params_handler(row)
