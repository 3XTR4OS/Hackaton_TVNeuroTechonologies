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


def diagram_creator(user_role, status, allowed_actions, allowed_blocks):
    # Дать диаграмме случайное имя. Show=False отключает автоматическое открытие схемы после создания

    with Diagram(f"{random_name()}", show=False):
        d_user = create_diag_user(user_role, status)
        actions_balancer = ELB('Возможные действия')
        blocks_balancer = ELB('Доступные блоки')

        with Cluster('Доступные действия'):
            actions_group = create_diag_actions(allowed_actions)

        with Cluster('Доступные блоки'):
            blocks_group = create_diag_allowed_blocks(allowed_blocks)

        d_user >> actions_balancer
        d_user >> blocks_balancer
        actions_balancer >> actions_group
        blocks_balancer >> blocks_group


def create_diag_user(user, status):
    complete_user = User(f'Пользователь: {user} \n'
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
