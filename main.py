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
    # user_role
    user_role = row['role']

    # state
    if row['state'] is None:
        state = 'Пуст'
    else:
        state = states[row['state']['status']]

    # allowed_actions
    if len(row['allowedActions']) == 0:
        allowed_actions = 'Пуст'
    else:
        allowed_actions = [i['name'] for i in row['allowedActions']]

    # allowedBlocks
    if len(row['allowedBlocks']) == 0:
        allowed_blocks = 'Пуст'
    else:
        allowed_blocks = [blocks[i] for i in row['allowedBlocks']]

    diag_creator.diagram_creator(user_role, state, allowed_actions, allowed_blocks)


with open(file_path, 'r+', encoding='utf-8') as file:
    file = json.load(file)
    # for i in range(4):
    #     params_handler(file[i])

    for row in file:
        params_handler(row)
