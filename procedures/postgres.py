import subprocess
import os
import pexpect
from procedures import BaseProcedure


class Procedure(BaseProcedure):
    def backup(self, config):
        filename = '%s.sql.gz' % config
        backup_path = self.get_tmp_path(filename)

        cmd = 'su postgres -c "pg_dump %s -Z 5 -f %s"' % (config, backup_path)
        p = pexpect.spawn(cmd)
        p.expect(pexpect.EOF)

        existing_backup = self.get_existing_backup(filename)

        if existing_backup and abs(os.stat(backup_path).st_size - existing_backup.get('size')) <= 2:
            print('Backup has not changed. Skipping.')
            return

        self.upload(backup_path)
        print('Backed up %s ' % filename)

    def get_tmp_dir(self):
        tmp_dir = '/tmp/barch/postgres/'
        try:
            os.mkdir(tmp_dir)
            print('Changing owner of %s to postgres.' % tmp_dir)
            subprocess.check_call('chown -R postgres %s' % tmp_dir, shell=True)
        except (OSError, IOError):
            pass

        return tmp_dir