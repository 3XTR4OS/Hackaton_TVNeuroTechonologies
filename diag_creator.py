import random
import string
from diagrams import Diagram, Cluster
from diagrams.aws.network import ELB
from diagrams.oci.connectivity import CustomerPremises
from diagrams.oci.security import Encryption
from diagrams.onprem.client import User


class DataDiagrammer:
    def __init__(self):
        self.save_folder: str = 'results_storage/'
        self.img_output_format: str = 'png'

    # Assigns a random name to the schema
    def generate_random_name(self, symbols_count=10) -> str:
        return ''.join([i for i in random.choices(string.ascii_letters, k=symbols_count)])

    def create_diagram(self, data: dict, diag_direction='TB') -> None:
        user_role: None | str = data['user_role']
        state: None | str = data['state']
        allowed_actions: None | list = data['allowed_actions']
        allowed_blocks: None | list = data['allowed_blocks']

        '''
        The diagram gets a name from random characters each time.
        show (the argument responsible for opening the created schema)
        outformat (the argument responsible for the format in which the schema will be saved)
        direction (the method by which the schema will be created)
        LR (left-to-right), RL (right-to-left), TB(top-to-bottom), BT(bottom-to-bottom up)
        '''

        with Diagram(
                show=False,  # do not open generated image
                direction=diag_direction,
                outformat=self.img_output_format,
                filename=f"{self.save_folder}{str(user_role) + '_' + self.generate_random_name()}",
        ):
            user: User = self.__create_user_node(user=user_role, status=state)
            actions_balancer: ELB = ELB('Возможные действия')
            blocks_balancer: ELB = ELB('Доступные блоки')

            with Cluster('Доступные действия'):
                actions_group: list[CustomerPremises | Encryption] = self.__create_allowed_actions_node(allowed_actions)  # objects to draw

            with Cluster('Доступные блоки'):
                blocks_group: list[CustomerPremises | Encryption] = self.__create_allowed_blocks_node(allowed_blocks)  # objects to draw

            user >> actions_balancer
            user >> blocks_balancer
            actions_balancer >> actions_group
            blocks_balancer >> blocks_group

    def __create_user_node(self, user: str, status: str) -> User:
        user_node = User(f'Уровень пользователя: {user} \nСтатус: {status}')
        return user_node

    def __create_allowed_actions_node(self, actions: list) -> list[CustomerPremises | Encryption]:
        """Adding all list elements inside cluster (with Cluster()...)"""
        if actions:
            allowed_actions = [CustomerPremises(action) for action in actions]
        else:
            allowed_actions = [Encryption('Нет')]

        return allowed_actions

    def __create_allowed_blocks_node(self, allowed_blocks: list) -> list[CustomerPremises | Encryption]:
        """Adding all list elements inside cluster (with Cluster()...)"""
        if allowed_blocks:
            allowed_blocks = [CustomerPremises(block) for block in allowed_blocks]
        else:
            allowed_blocks = [Encryption('Нет')]

        return allowed_blocks
