import os
from utils.config_loader import config
from utils.file_loader import load_yaml, write_yaml
from utils.request import Request
from utils.logger import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, config['data']['user_file'])

class User:

    def __init__(self, username, password, data_path=None):
        self.username = username
        self.password = password
        self.data_path = data_path or DATA_DIR

    def login(self):
        logger.info(f"User {self.username} try to login")

        data_list = load_yaml(self.data_path) or {}
        users = data_list.get('users', [])

        for user in users:
            if user['username'] != self.username:
                continue
            if user['password'] == self.password:
                logger.info(f"User {self.username} login successfully")
                return True
            else:
                logger.error(f"Wrong password for user {self.username}")
                return False

        logger.error(f"No existing user with username {self.username}")
        return False

    def register(self):
        logger.info(f"User {self.username} try to register")

        data_list = load_yaml(self.data_path) or {}
        users = data_list.get('users', [])

        for user in users:
            if user['username'] == self.username:
                logger.error(f"User {self.username} already exists")
                return False

        users.append({'username': self.username, 'password': self.password})
        data_list['users'] = users
        write_yaml(self.data_path, data_list)

        logger.info(f"User {self.username} register successfully")
        return True