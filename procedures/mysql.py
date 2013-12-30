import os
import pexpect
from procedures import BaseProcedure


class Procedure(BaseProcedure):
    def backup(self, config):
        for db_name in config.get('databases', []):
            cmd = '/bin/bash -c "mysqldump %s -u %s' % (db_name, config.get('username'))
            password = config.get('password')
            if password:
                cmd += ' -p'

            filename = '%s.sql.gz' % db_name
            backup_path = self.get_tmp_path(filename)

            cmd += ' | gzip > %s"' % backup_path
            p = pexpect.spawn(cmd)
            p.expect('Enter password:')
            p.sendline(password)
            p.expect(pexpect.EOF)

            existing_backup = self.get_existing_backup(filename)

            if existing_backup and abs(os.stat(backup_path).st_size - existing_backup.get('size')) <= 2:
                print('Backup has not changed. Skipping.')
                continue

            self.upload(backup_path)
            print('Backed up %s ' % filename)