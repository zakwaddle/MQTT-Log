import json
import machine


class MessageError(Exception):
    pass


class Message:

    def __init__(self, raw_message):
        self.raw_message = raw_message
        self.message = None
        self.instructions = None
        self.command = None

        self.parse_message()
        self.parse_command()
        self.execute_command()

    def parse_message(self):
        if isinstance(self.raw_message, dict):
            self.instructions = self.raw_message
            return

        self.message = self.raw_message.decode('utf-8')
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

    def execute_command(self):
        if hasattr(self, self.command):
            command_func = self.__getattribute__(self.command)
            command_func()

    def poo_boy(self):
        stuff = self.instructions.get('info')
        print(stuff)

    def restart(self):
        machine.reset()


if __name__ == "__main__":
    msg = {
        "command": "poo_boy",
        "info": "well well well"
    }
    Message(msg)
