from datetime import datetime
import requests


class Seafile:
    def __init__(self, host, token=None, verify_cert=True, verbose=False):
        """

        @param host: https://cloud.seafile.com/
        @param token: str
        @param verify_cert: bool
        @param verbose: bool
        """

        self.host = host
        self.token = token if token else None
        self.verify_cert = verify_cert
        self.verbose = verbose

    def _url(self, path):
        return '%sapi2/%s/' % (self.host, path)

    def _log(self, message):
        if self.verbose:
            print('%s\t%s' % (datetime.now(), message))

    def __auth_get(self, path, headers=None, params=None):
        if headers:
            headers['Authorization'] = 'Token %s' % self.token
        else:
            headers = {
                'Authorization': 'Token %s' % self.token
            }

        if path.startswith('http'):
            url = path
        else:
            url = self._url(path)

        return requests.get(
            url,
            headers=headers,
            params=params,
            verify=self.verify_cert
        )

    def __auth_post(self, path, headers=None, params=None, data=None, files=None):
        if headers:
            headers['Authorization'] = 'Token %s' % self.token
        else:
            headers = {
                'Authorization': 'Token %s' % self.token
            }

        if path.startswith('http'):
            url = path
        else:
            url = self._url(path)

        return requests.post(
            url,
            headers=headers,
            params=params,
            data=data,
            files=files,
            verify=self.verify_cert
        )

    def auth_token(self, username, password):
        r = requests.post(self._url('auth-token'), data={
            'username': username,
            'password': password
        }, verify=self.verify_cert)

        if r.status_code == 400:
            raise ConnectionRefusedError(r.text)

        self._log('Authentication successful.')

        token = r.json().get('token')
        self.token = token

        return token

    def auth_ping(self):
        r = self.__auth_get('auth/ping')

        if r.status_code != 200:
            raise ConnectionError(r.text)

        return r.text[1:-1]

    def accounts(self):
        r = self.__auth_get('accounts')

        if r.status_code != 200:
            raise ConnectionRefusedError(r.text)

        return r.json()

    def account_info(self):
        raise NotImplementedError

    def create_account(self):
        """
        Create account.

        @raise NotImplementedError:
        """
        raise NotImplementedError

    def update_account(self):
        """
        Update account.

        @raise NotImplementedError:
        """
        raise NotImplementedError

    def delete_account(self):
        """
        Delete account.

        @raise NotImplementedError:
        """
        raise NotImplementedError

    def repos(self):
        """
        List libraries.

        @rtype : json
        """

        r = self.__auth_get('repos')
        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()

    def repo(self, repo_id):
        r = self.__auth_get('repos/%s' % repo_id)
        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()

    def decrypt_repo(self, repo_id, password):
        r = self.__auth_post('repos/%s' % repo_id, data={
            'password': password
        })
        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def repo_download_info(self, repo_id):
        r = self.__auth_get('repos/%s/download-info' % repo_id)
        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()

    def __repo_upload_link(self, repo_id):
        r = self.__auth_get('repos/%s/upload-link' % repo_id)
        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def repo_upload(self, repo_id, file, filename=None, parent_dir='/'):
        upload_link = self.__repo_upload_link(repo_id)

        if filename:
            files = {
                'file': (filename, file)
            }
        else:
            files = {
                'file': file
            }

        r = self.__auth_post(
            upload_link,
            files=files,
            data={
                'parent_dir': parent_dir,
            }
        )

        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def __repo_update_link(self, repo_id):
        r = self.__auth_get('repos/%s/update-link' % repo_id)
        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def repo_update(self, repo_id: str, file, target_file: str):
        upload_link = self.__repo_update_link(repo_id)

        r = self.__auth_post(
            upload_link,
            files={
                'file': file
            },
            data={
                'target_file': target_file
            }
        )

        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def __repo_file_link(self, repo_id, path):
        r = self.__auth_get('repos/%s/file' % repo_id, params={
            'p': path
        })

        if r.status_code != 200:
            raise Exception(r.text)

        return r.text[1:-1]

    def repo_file(self, repo_id, path):
        file_url = self.__repo_file_link(repo_id, path)

        r = self.__auth_get(file_url)

        if r.headers.get('content-type') == 'application/json':
            return r.json()

        return r.raw

    def repo_dir(self, repo_id, path):
        r = self.__auth_get('repos/%s/dir' % repo_id, params={
            'p': path,
        })

        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()

    def repo_create_dir(self, repo_id, path):
        r = self.__auth_post('repos/%s/dir' % repo_id, params={
            'p': path
        }, data={
            'operation': 'mkdir'
        })

        if r.status_code != 201:
            raise Exception(r.text)

        return r.text[1:-1]