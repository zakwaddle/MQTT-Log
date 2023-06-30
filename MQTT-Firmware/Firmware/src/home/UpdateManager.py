import json
import os
import uos
from .lib.ftplib import FTP


class DownloadError(Exception):
    pass


class UpdateError(Exception):
    pass


class FTPClient:
    """
    FTPClient class provides a high-level interface to perform operations
    on an FTP server such as connecting, disconnecting, and transferring files.
    """

    def __init__(self, host, user, password):
        """
        Constructs an FTPClient with provided FTP server details.

        :param host: The FTP host address.
        :param user: The username for the FTP host.
        :param password: The password for the FTP host.
        """
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None

    def connect(self):
        """
        Establishes a connection to the FTP server using the host, user, and password
        provided during the initialization of the FTPClient instance.
        """
        self.ftp = FTP()
        self.ftp.connect(self.host)
        self.ftp.login(self.user, self.password)
        print('connected ftp')

    def disconnect(self):
        """
        Disconnects from the FTP server if a connection is established.
        """
        if self.ftp:
            self.ftp.quit()
            print('disconnected ftp')

    def download_file(self, remote_file_path, local_file_path):
        """
        Downloads a file from the FTP server.

        :param remote_file_path: The path of the file on the FTP server.
        :param local_file_path: The path where the file will be saved locally.
        """
        print(f"Remote file path: {remote_file_path}")
        print(f"Local file path: {local_file_path}")
        try:
            with open(local_file_path, "wb") as local_file:
                self.ftp.retrbinary("RETR " + remote_file_path, local_file.write)
        except Exception as e:
            print("Error downloading file:", e)
            raise

    def upload_file(self, local_path, remote_path):
        """
        Uploads a file to the FTP server.

        :param local_path: The path of the file on the local system.
        :param remote_path: The path where the file will be saved on the FTP server.
        """
        with open(local_path, "rb") as f:
            self.ftp.storbinary("STOR " + remote_path, f)

    def change_directory(self, path):
        """
        Changes the current directory on the FTP server.

        :param path: The path of the directory to change to on the FTP server.
        """
        self.ftp.cwd(path)

    def list_directory(self, **kwargs):
        """
        Lists the contents of the current directory on the FTP server.

        :return: A list of the names of the files and directories in the current directory.
        """
        return self.ftp.dir(**kwargs)


class FirmwareUpdater:
    """
    FirmwareUpdater class provides functionalities to download firmware
    updates. It uses an instance of the FTPClient class to perform FTP operations.
    """

    def __init__(self, host, user, password):
        """
        Constructs a FirmwareUpdater with provided FTP server details.

        :param host: The FTP host address.
        :param user: The username for the FTP host.
        :param password: The password for the FTP host.
        """
        self.ftp_client = FTPClient(host, user, password)

    @staticmethod
    def makedirs(path):
        """
        Recursively creates directories.

        :param path: The path of the directory to be created.
        """
        parts = path.split('/')
        current_path = ''
        for part in parts:
            current_path += '/' + part
            try:
                os.mkdir(current_path)
            except OSError as e:
                if e.args[0] != 17:
                    raise

    @staticmethod
    def _update_file(remote_file_path, local_file_path):
        """
        Overwrites a local file with the contents of another local file.

        :param remote_file_path: The path of the file to be updated.
        :param local_file_path: The path of the file that will be used to update.
        """
        print("Updating file:")
        print("  Source:", local_file_path)
        print("  Destination:", remote_file_path)
        print()
        with open(local_file_path, 'rb') as src, open(remote_file_path, 'wb') as dest:
            dest.write(src.read())

    def update(self, target, source_filepath):
        """
        Updates a local file with the contents of another local file.

        :param target: The path of the file to be updated.
        :param source_filepath: The path of the file that will be used to update.
        """
        self._update_file(target, source_filepath)

    def download_file(self, remote_path, local_path):
        self.ftp_client.connect()
        self.ftp_client.ftp.makepasv()
        self.ftp_client.download_file(remote_path, local_path)
        self.ftp_client.disconnect()


class PackageDownloader:

    def __init__(self, updater: FirmwareUpdater, observer_func=None):
        self.observer_func = observer_func
        self.updater = updater
        self.package_name = ''
        self.package_root = ''
        self.current_remote_dir = ''
        self.current_local_dir = '/updates'
        self.directories = []
        self.files = []

    def log(self, message):
        if self.observer_func is not None:
            self.observer_func(message)

    def sort_item(self, thing):
        i = thing.split(' ')
        isDir = thing[0] == "d"
        name = i[-1]
        if isDir:
            if name == self.package_root:
                return
            self.directories.append(name)
        else:
            self.handle_file(name)

    def handle_file(self, file_name):
        remote_path = f"{self.current_remote_dir}/{file_name}"
        local_path = f"{self.current_local_dir}/{file_name}"
        print(f'handle_file: {file_name}')
        print(f'remote: {remote_path}')
        print(f'local: {local_path}')
        self.files.append((remote_path, local_path))
        # self.updater.ftp_client.download_file(remote_path, local_path)

    def handle_dir(self, dir_name):
        self.current_remote_dir = dir_name
        self.updater.makedirs(self.current_local_dir)
        self.updater.ftp_client.change_directory(self.current_remote_dir)
        self.updater.ftp_client.list_directory(callback=self.sort_item)

    def download_package(self, package_root, folder=None):

        def download_files():
            for i in self.files:
                self.updater.ftp_client.download_file(i[0], i[1])
            self.files = []

        self.package_root = package_root
        self.current_local_dir = '/updates'
        if folder is not None:
            self.package_root = package_root + folder
            self.current_local_dir = f'{self.current_local_dir}{folder}'
        self.log(f'downloading contents of: {self.package_root} - to: {self.current_local_dir}')
        self.updater.ftp_client.connect()
        self.updater.ftp_client.ftp.makepasv()
        try:
            self.handle_dir(self.package_root)
            download_files()

        except Exception as e:
            print(f'Download Package Error: {e}')
            self.log(f'Download Package Error: {e}')
        finally:
            self.updater.ftp_client.disconnect()


class UpdateManager:
    """
    UpdateManager class handles the firmware updates for the device.
    """

    @staticmethod
    def item_is_file(item):
        return uos.stat(f"/{item}")[0] == 0x8000

    def __init__(self, host, user, password, observer_func=None):
        """
        Initializes UpdateManager with provided parameters.

        :param host (str): The FTP host address.
        :param user (str): The username for the FTP host.
        :param password (str): The password for the FTP host.
        :param unit_id (str): The unit id of the device.
        """
        self.firmware_updater = FirmwareUpdater(host, user, password)
        self.observer_func = observer_func

    def observe(self, message):
        if self.observer_func is not None:
            self.observer_func(message, log_type='update')

    def rmdir(self, directory):
        """
        Recursively removes directories.

        :param directory: The path of the directory to be removed.
        """
        # List all files and subdirectories in the directory
        for filename in uos.listdir(directory):
            path = f"{directory}/{filename}"

            # Check if this is a file or a subdirectory
            if self.item_is_file(path):  # this is a file
                uos.remove(path)
            else:  # this is a directory
                self.rmdir(path)

        # Now that the directory is empty, remove the directory itself
        uos.rmdir(directory)

    def download_main(self, remote_path):
        local_path = '/updates/main.py'
        try:
            self.firmware_updater.makedirs('/updates')
            self.firmware_updater.download_file(remote_path, local_path)
        except Exception as e:
            raise DownloadError(f"Error Downloading main.py: {e}")

    def download_manifest(self, remote_path):
        local_path = '/updates/manifest.json'
        try:
            self.firmware_updater.makedirs('/updates')
            self.firmware_updater.download_file(remote_path, local_path)
        except Exception as e:
            raise DownloadError(f"Error Downloading manifest.json: {e}")

    def apply_updated_main(self):
        try:
            self.firmware_updater.update('/main.py', '/updates/main.py')
        except Exception as e:
            raise UpdateError(f"Error updating main.py: {e}")
        else:
            self.remove_update_directory()

    def download_update(self, remote_root, directories):
        try:
            downloader = PackageDownloader(self.firmware_updater, observer_func=self.observe)
            for d in directories:
                downloader.download_package(remote_root, d)
        except Exception as e:
            raise DownloadError(f"Error downloading home package: {e}")

    def download_update_from_manifest(self, remote_path):
        def open_manifest():
            with open("updates/manifest.json", 'r') as f:
                return json.load(f)

        # get update manifest
        self.download_manifest(remote_path)
        manifest = open_manifest()

        directories = manifest.get('directories')
        files = manifest.get('files')
        package_root = manifest.get('package_root')

        can_continue = directories is not None and files is not None and package_root is not None
        if not can_continue:
            raise UpdateError()

        # make directories in updates folder
        for i in directories:
            path = i if i.startswith("/") else f"/{i}"
            self.firmware_updater.makedirs(f"/updates{path}")

        # download files
        self.firmware_updater.ftp_client.connect()
        for i in files:
            remote_path = package_root + i
            local_path = f"/updates{i}"
            self.firmware_updater.ftp_client.download_file(remote_path, local_path)
        self.firmware_updater.ftp_client.disconnect()

        # update files
        for file in uos.listdir('/updates'):
            if file == "manifest.json":
                continue
            if self.item_is_file(f'/updates/{file}'):
                self.firmware_updater.update(f'/{file}', f'/updates/{file}')
                print('updated file: ', file)

            else:
                self.rmdir(f'/{file}')  # Remove the existing directory from root
                uos.rename(f'/updates/{file}', f'/{file}')
                print('updated directory: ', file)

        self.remove_update_directory()

    def apply_updated_home_package(self):
        try:
            self.rmdir('/home')  # Remove the existing /home directory
            uos.rename('/updates/home', '/home')  # Move /update/home to /home
        except Exception as e:
            raise UpdateError(f'Error updating home package: {e}')
        else:
            self.remove_update_directory()

    def remove_update_directory(self):
        """
        Removes the directory where the downloaded files are stored.
        """
        self.rmdir("/updates")
