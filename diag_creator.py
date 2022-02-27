from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.aws.network import ELB
from diagrams.oci.connectivity import CustomerPremise
from diagrams.oci.security import Encryption
import random
import string


# Присваивает схеме случайное имя
def random_name():
    return ''.join([i for i in random.choices(string.ascii_letters, k=35)])


def create_diagram(*args, p_direction='TB', p_outformat='png'):
    user_role = args[0][0]  # Уровень доступа пользователя
    status = args[0][1]  # Статус ИО
    allowed_actions = args[0][2]
    allowed_blocks = args[0][3]

    '''
    Диаграмма каждый раз получает имя из случайных символов
    show (аргумент, отвечающий за открытие созданной схемы)
    outformat (аргумент, отвечающий за то, в каком формате будет сохранена схема)
    direction (метод, по которому будет создаваться схема)
    LR (слева-направо), RL (справа-налево), TB(сверху-вниз), BT(снизу-вверх)'''
    with Diagram(f"{str(user_role) + '_' + random_name()}", show=False, direction=p_direction, outformat=p_outformat):
        d_user = create_diag_user(user_role, status)
        actions_balancer = ELB('Возможные действия')
        blocks_balancer = ELB('Доступные блоки')

        with Cluster('Доступные действия'):
            actions_group = create_diag_actions(allowed_actions)  # список объектов на создание

        with Cluster('Доступные блоки'):
            blocks_group = create_diag_allowed_blocks(allowed_blocks)  # список объектов на создание

        d_user >> actions_balancer
        d_user >> blocks_balancer
        actions_balancer >> actions_group
        blocks_balancer >> blocks_group


def create_diag_user(user, status):
    complete_user = User(f'Уровень пользователя: {user} \n'
                         f'Статус: {status}')

    return complete_user


def create_diag_actions(action_list):
    if action_list == 'Пуст':
        return [Encryption('Пуст')]

    else:
        actions_group = [CustomerPremise(i) for i in action_list]

    return actions_group


def create_diag_allowed_blocks(allowed_list):
    if allowed_list == 'Пуст':
        return [Encryption('Пуст')]

    else:
        actions_group = [CustomerPremise(i) for i in allowed_list]
        return actions_group
