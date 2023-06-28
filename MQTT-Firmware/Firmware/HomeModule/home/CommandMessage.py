import json
import home.Home as home
import home.UpdateManager as udm

UpdateError = udm.UpdateError
DownloadError = udm.DownloadError


class MessageError(Exception):
    pass


class CommandMessage:

    def __init__(self, home_client: home.Home, message):
        self.home_client = home_client
        self.message = message
        self.instructions = None
        self.command = None

        self.parse_message()
        self.parse_command()

    def parse_message(self):
        if isinstance(self.message, dict):
            self.instructions = self.message
            return

        self.message = self.message.decode('utf-8')
        try:
            self.instructions = json.loads(self.message)
        except ValueError:
            if isinstance(self.message, dict):
                self.instructions = self.message
            raise MessageError("message not json")
        except OSError:
            raise MessageError("error parsing json")

    def parse_command(self):
        self.command = self.instructions.get("command")
        if self.command is None:
            raise MessageError("no command found in message")
        self.command = self.command.replace('-', '_')

    def execute_command(self):
        try:
            command_func = getattr(self, self.command)
        except AttributeError:
            raise MessageError(f"Unknown command: {self.command}")
        else:
            command_func()

    def restart(self):
        self.home_client.log("Received Restart Command. Restarting", log_type='restart')
        self.home_client.restart_device(delay_seconds=2)

    def check_in(self):
        self.home_client.log('here', log_type='check-in')

    def update_home_package(self):
        remote_root = self.instructions.get("remote_root")
        directories = self.instructions.get("directories")
        if remote_root is not None and directories is not None:
            self.home_client.log("Download home package update", log_type='update')
            try:
                self.home_client.update_manager.download_update(remote_root, directories)
            except DownloadError as e:
                self.home_client.log(e, log_type='error')
            except UpdateError as e:
                self.home_client.log(e, log_type='error')
            else:
                self.home_client.log("Updated home package - restarting to apply update", log_type='update')
                self.home_client.restart_device(delay_seconds=3)

    def update_main(self):
        remote_file_path = self.instructions.get("remote_file_path")
        if remote_file_path is not None:
            self.home_client.log("Downloading main.py update", log_type='update')
            try:
                self.home_client.update_manager.download_main(remote_file_path)
                self.home_client.update_manager.apply_updated_main()
            except DownloadError as e:
                self.home_client.log(e, log_type='error')
            except UpdateError as e:
                self.home_client.log(e, log_type='error')
            else:
                self.home_client.log("Updated main.py - restarting to apply update", log_type='update')
                self.home_client.restart_device(delay_seconds=3)

    def update_host(self):
        new_host = self.instructions.get("host")
        if new_host is not None:
            self.home_client.device_settings.host = new_host
            self.home_client.device_settings.save()
