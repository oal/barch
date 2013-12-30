from api import Seafile
import os


class BaseProcedure:
    def __init__(self, api: Seafile, repo_id: str, config):
        self.name = self.__class__.__module__.split('.')[-1]

        self.api = api
        self.repo_id = repo_id
        self.config = config

        self.tmp_dir = self.get_tmp_dir()
        self.existing_backups = None

        if type(config) == dict:
            self.backup(config)
        elif type(config) == list:
            self.backup_all(config)
        else:
            raise NotImplementedError('Backup procedures only defined for dict and list configs.')

    def get_tmp_dir(self):
        tmp_dir = '/tmp/barch/%s/' % self.name
        try:
            os.mkdir(tmp_dir)
        except (OSError, IOError):
            pass

        return tmp_dir

    def get_tmp_path(self, filename):
        return '%s%s' % (self.tmp_dir, filename)

    def get_existing_backups(self):
        try:
            existing_backups = self.api.repo_dir(self.repo_id, '/%s' % self.name)
        except Exception:
            self.api.repo_create_dir(self.repo_id, '/%s' % self.name)
            existing_backups = {}

        return existing_backups

    def get_existing_backup(self, filename) -> dict:
        if not self.existing_backups:
            self.existing_backups = self.get_existing_backups()

        for backup in self.existing_backups:
            if backup.get('name') == filename:
                return backup

        return None

    def upload(self, file, force_new=False) -> str:
        if type(file) == str:
            file = open(file, 'rb')

        filename = file.name.split('/')[-1]
        existing_backup = self.get_existing_backup(filename)

        if existing_backup and not force_new:
            file_id = self.api.repo_update(self.repo_id, file, '/%s/%s' % (self.name, filename))
        else:
            file_id = self.api.repo_upload(self.repo_id, file, filename, parent_dir='/%s' % self.name)

        file.close()

        return file_id

    def backup(self, config):
        raise NotImplementedError('Create your own implementation.')

    def backup_all(self, configs):
        for config in configs:
            self.backup(config)