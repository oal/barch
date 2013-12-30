import subprocess
import os
from procedures import BaseProcedure


class Procedure(BaseProcedure):
    def backup(self, config):
        directory = config.get('directory')
        if config.get('recursive'):
            for root, dirs, files in os.walk(directory):
                if root.endswith('.git'):
                    self.git_backup(directory, root.replace(directory, ''))
        else:
            dirs = os.listdir(directory)
            for d in dirs:
                if d.endswith('.git'):
                    self.git_backup(directory, d)

        print('Backed up %s.' % directory)

    def git_backup(self, root, git_dir):
        if git_dir[0] == '/':
            git_dir = git_dir[1:]

        absolute_path = os.path.join(root, git_dir, 'objects')

        if not os.path.isdir(absolute_path):
            print('Not a directory. Skipping.')

        git_dir_info = os.stat(absolute_path)

        filename = '%s.tar.gz' % git_dir.replace('/', '_')
        backup_path = self.get_tmp_path(filename)

        existing_backup = self.get_existing_backup(filename)

        if existing_backup and git_dir_info.st_mtime - existing_backup.get('mtime') < 30:
            print('Git repository "%s" has not changed. Skipping.' % git_dir)
            return

        cmd = 'tar -C %s -zcf %s %s && mv %s %s' % (root, filename, git_dir, filename, self.tmp_dir)
        subprocess.check_call(cmd, shell=True)

        self.upload(backup_path)

        print('Backed up "%s".' % git_dir)