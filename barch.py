import json
from datetime import datetime
from api import Seafile
import importlib
import os


class Barch:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')

        try:
            with open(self.config_file) as cf:
                connection_config = json.load(cf)
        except (OSError, IOError):
            connection_config = self.create_config()

        host = connection_config.get('host')
        token = connection_config.get('token')
        self.repo_id = connection_config.get('repo_id')
        self.password = connection_config.get('password')

        if not host or not token or not self.repo_id:
            raise KeyError('Need host, token and repo_id in config.json.')

        self.api = Seafile(host, token, verify_cert=False)
        self.log(self.api.auth_ping())

        try:
            os.mkdir('/tmp/barch/')
            self.log('Created /tmp/barch/.')
        except (OSError, IOError):
            self.log('/tmp/barch/ already exists.')

        if self.password:
            self.decrypt(self.repo_id, self.password)

        self.config = self.get_config()
        for procedure in self.config.keys():
            try:
                module = importlib.import_module('procedures.%s' % procedure)
            except (ImportError, NotImplementedError):
                print('Backup procedure "%s" is missing.' % procedure)
                continue
            print('Running %s procedure.' % procedure)
            module.Procedure(self.api, self.repo_id, self.config.get(procedure))

    def log(self, message):
        message = '%s\t%s' % (datetime.now(), message)
        print(message)

    def create_config(self):
        with open(self.config_file, 'w') as config:
            connection_config = {
                'host': input('Seafile URL: '),
                'token': input('Auth token: '),
                'repo_id': input('Repository ID: '),
                'password': input('Password: ')
            }
            json.dump(connection_config, config)
            self.log('Config file created.')

            return connection_config

    def decrypt(self, library, password):
        self.api.decrypt_repo(library, password)

        self.log('Decrypted library.')
        return True

    def get_config(self) -> dict:
        return self.api.repo_file(self.repo_id, '/config.json')


if __name__ == '__main__':
    Barch()


