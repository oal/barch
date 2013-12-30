import subprocess
import os
from procedures import BaseProcedure


class Procedure(BaseProcedure):
    def backup(self, config):
        filename = '%s.sql.gz' % config.replace('/', '_')[1:]
        backup_path = self.get_tmp_path(filename)

        cmd = 'sqlite3 %s .dump | gzip > %s' % (config, backup_path)
        subprocess.check_call(cmd, shell=True)

        existing_backup = self.get_existing_backup(filename)

        if existing_backup and abs(os.stat(backup_path).st_size - existing_backup.get('size')) <= 2:
            print('Backup has not changed. Skipping.')
            return

        self.upload(backup_path)
        print('Backed up %s ' % filename)