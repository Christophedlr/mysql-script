from getpass import getpass

from ttycolor import Color


class YesNoQuestion:
    """
    Yes or No question
    """
    color: Color = None

    def __init__(self):
        self.color = Color()

    def execute(self):
        """
        Verify correct input

        :return: Y or N
        """
        stdin = input()

        if len(stdin) > 1 or stdin.upper() != 'Y' and stdin.upper() != 'N':
            print('Invalid option')
            return self.execute()
        else:
            return stdin

    def run(self, msg: str, default: bool = False):
        """
        Run the question

        :param msg: message
        :param default: True if Y default response
        :return: True or False
        """
        if default:
            message = msg + ' [Y/n]'
        else:
            message = msg + ' [y/N]'

        print(self.color.colorrgb(message, 0x00, 0xBF, 0x00)+self.color.color('', self.color.RESET))
        result = self.execute()

        if result.upper() == 'Y':
            return True
        else:
            return False


class SimpleQuestion:
    """Simple Question"""
    color: Color = None

    def __init__(self):
        self.color = Color()

    def run(self, msg: str, mask_input: bool = False):
        """
        Run the question

        :param msg: message displayed in tty
        :param mask_input: True for mask input text
        :return: response
        """
        print(self.color.colorrgb(msg, 0x00, 0xBF, 0x00)+self.color.color('', self.color.RESET))

        if mask_input:
            return getpass()
        else:
            return input()
