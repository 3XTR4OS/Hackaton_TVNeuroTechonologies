import json
import constants
from diag_creator import DataDiagrammer

datafile_path = 'static/Пример входного JSON.txt'


def params_handler(row: dict) -> dict:
    user_role: None | str = row['role']  # user_role = user rights
    state: None | dict = row['state']['status'] if row['state'] else None  # state - object status
    allowed_actions: None | list = [action['name'] for action in row['allowedActions']]  # available actions
    allowed_blocks: None | list = row['allowedBlocks']  # allowedBlocks - blocks available for display

    if allowed_blocks:  # translate to RU using constant BLOCKS: dict
        allowed_blocks: list = [constants.BLOCKS.get(block_name) for block_name in allowed_blocks]

    if state:  # translate to RU using constant STATES: dict
        state: str = constants.STATES.get(state)
    else:
        state: str = 'Удалён'

    return {'user_role': user_role,
            'state': state,
            'allowed_actions': allowed_actions,
            'allowed_blocks': allowed_blocks}


if __name__ == '__main__':
    with open(datafile_path, 'r', encoding='utf-8') as file:
        diagrammer: DataDiagrammer = DataDiagrammer()
        for row in json.load(file):
            params_of_object: dict = params_handler(row)
            diagrammer.create_diagram(data=params_of_object)
