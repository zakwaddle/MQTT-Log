import os
import uos
import machine
from .lib.ftplib import FTP


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
    updates from a specific directory in the FTP server. It uses an instance of
    the FTPClient class to perform FTP operations.
    """

    def __init__(self, host, user, password, unit_id):
        """
        Constructs a FirmwareUpdater with provided FTP server details and the unit_id
        which corresponds to the directory on the FTP server where firmware updates
        are located.

        :param host: The FTP host address.
        :param user: The username for the FTP host.
        :param password: The password for the FTP host.
        :param unit_id: The directory on the FTP server where firmware updates are located.
        """
        self.ftp_client = FTPClient(host, user, password)
        self.update_path = f"upload/Firmware/{unit_id}"
        self.home_update_path = f"upload/Firmware/HomeModule"

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

    def _download_file(self, remote_file_path):
        """
        Downloads a file from the FTP server and saves it locally.

        :param remote_file_path: The path of the file on the FTP server.
        :return: The local path where the file has been saved.
        """
        self.ftp_client.connect()
        self.ftp_client.ftp.makepasv()
        local_file_path = 'updated_files' + remote_file_path
        # if remote_file_path.startswith('/home'):

        local_dir = '/'.join(local_file_path.split('/')[:-1])
        self.makedirs(local_dir)
        if remote_file_path.startswith('/home'):
            update_path = self.home_update_path + remote_file_path
        else:
            update_path = self.update_path + remote_file_path
        print(f'update_path: {update_path}')
        self.ftp_client.download_file(update_path, local_file_path)
        self.ftp_client.disconnect()
        return local_file_path

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

    @staticmethod
    def _remove_downloaded_files(local_file_path):
        """
        Deletes a file from the local file system.

        :param local_file_path: The path of the file to be deleted.
        """
        try:
            os.remove(local_file_path)
            print("Removed file:", local_file_path)
        except OSError as e:
            print("Error removing file:", local_file_path, "| Error:", e)

    def download_and_update(self, filename):
        """
        Downloads a file from the FTP server, updates a local file with the downloaded
        file's content, and deletes the downloaded file.

        :param filename: The name of the file on the FTP server to be downloaded.
        """
        local_fp = self._download_file(filename)
        self._update_file(filename, local_fp)
        self._remove_downloaded_files(local_fp)
        machine.reset()

    def download(self, filename):
        """
        Downloads a file from the FTP server.

        :param filename: The name of the file on the FTP server to be downloaded.
        :return str: The local path where the file has been saved.
        """

        return self._download_file(filename)

    def update(self, target, source_filepath):
        """
        Updates a local file with the contents of another local file.

        :param target: The path of the file to be updated.
        :param source_filepath: The path of the file that will be used to update.
        """
        self._update_file(target, source_filepath)

    def remove_file(self, target_filepath: str):
        """
        Deletes a file from the local file system.

        :param target_filepath: The path of the file to be deleted.
        """
        self._remove_downloaded_files(target_filepath)

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
        self.current_local_dir = '/update'
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
        self.current_local_dir = '/update'
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

    def __init__(self, host, user, password, unit_id, observer_func=None):
        """
        Initializes UpdateManager with provided parameters.

        :param host (str): The FTP host address.
        :param user (str): The username for the FTP host.
        :param password (str): The password for the FTP host.
        :param unit_id (str): The unit id of the device.
        """
        self.firmware_updater = FirmwareUpdater(host, user, password, unit_id)
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
            path = "{}/{}".format(directory, filename)

            # Check if this is a file or a subdirectory
            if uos.stat(path)[0] == 0x8000:  # this is a file
                uos.remove(path)
            else:  # this is a directory
                self.rmdir(path)

        # Now that the directory is empty, remove the directory itself
        uos.rmdir(directory)

    def download_and_update(self, file_path):
        """
        Downloads the firmware update and applies it.

        :param file_path: The file path on the FTP server for the firmware update.
        """
        self.firmware_updater.download_and_update(file_path)

    def download_main(self, remote_path):
        update_path = '/updated_files/main.py'
        self.firmware_updater.makedirs('/updated_files')
        self.firmware_updater.download_file(remote_path, update_path)
        self.firmware_updater.update('/main.py', '/updated_files/main.py')
        self.remove_update_directory()
        machine.reset()

    def download_all(self, file_list):
        """
        Downloads all files from the FTP server.

        :param file_list: The list of file paths on the FTP server to be downloaded.
        :return list: A list of tuples where each tuple contains the remote file path and the local file path.
        """
        to_update = []
        for f in file_list:
            print(f"downloading:  {f}")
            self.observe(f"downloading:  {f}")
            local_path = self.firmware_updater.download(f"{f}")
            to_update.append((f, local_path))
        return to_update

    def download_update(self, remote_root, directories):
        self.observe('downloading package update')

        downloader = PackageDownloader(self.firmware_updater, observer_func=self.observe)
        for d in directories:
            downloader.download_package(remote_root, d)

        # Remove the existing /home directory
        try:
            self.rmdir('/home')
        except OSError:
            pass  # If the directory doesn't exist, an OSError will be thrown, so we just ignore it

        # Move /update/home to /home
        uos.rename('/update/home', '/home')

        # Optionally, if you want to delete the /update directory after the move
        try:
            uos.rmdir('/update')
        except OSError:
            pass  # If the directory doesn't exist, an OSError will be thrown, so we just ignore it

        machine.reset()

    def update_all(self, update_list):
        """
        Updates all local files with the contents of the corresponding downloaded files.

        :param update_list: A list of tuples where each tuple contains the remote file path and the local file path.
        """
        for file, local_path in update_list:
            self.observe(f"updating:  {file}")
            self.firmware_updater.update(file, local_path)

    def remove_update_directory(self):
        """
        Removes the directory where the downloaded files are stored.
        """
        self.rmdir("/updated_files")
