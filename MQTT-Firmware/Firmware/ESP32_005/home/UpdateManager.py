import os
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

    def disconnect(self):
        """
        Disconnects from the FTP server if a connection is established.
        """
        if self.ftp:
            self.ftp.quit()

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
        except IOError as e:
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

    def list_directory(self):
        """
        Lists the contents of the current directory on the FTP server.

        :return: A list of the names of the files and directories in the current directory.
        """
        return self.ftp.nlst()


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
        local_dir = '/'.join(local_file_path.split('/')[:-1])
        self.makedirs(local_dir)
        self.ftp_client.download_file(self.update_path + remote_file_path, local_file_path)
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


class UpdateManager:
    """
    UpdateManager class handles the firmware updates for the device.
    """

    def __init__(self, host, user, password, unit_id):
        """
        Initializes UpdateManager with provided parameters.

        :param host (str): The FTP host address.
        :param user (str): The username for the FTP host.
        :param password (str): The password for the FTP host.
        :param unit_id (str): The unit id of the device.
        """
        self.firmware_updater = FirmwareUpdater(host, user, password, unit_id)

    def download_and_update(self, file_path):
        """
        Downloads the firmware update and applies it.

        :param file_path: The file path on the FTP server for the firmware update.
        """
        self.firmware_updater.download_and_update(file_path)

