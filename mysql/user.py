import os

from ttyutility import Command
from question import YesNoQuestion, SimpleQuestion


class UserCommand(Command):
    """
    User command
    """
    root: str
    create: str
    delete: str
    user: str

    def __init__(self):
        """
        Initialization
        """
        super(UserCommand, self).__init__()

        self.root = ''
        self.create = ''
        self.delete = ''
        self.user = ''

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        super(UserCommand, self).configure(name, parser, prog, help)

        self.add_argument('-p', 0, str, 'Root password')
        self.add_argument('-c', 1, str, 'Create a user')
        self.add_argument('-d', 1, str, 'Delete a user')

    def fill(self, args: dict):
        """
        Fill properties with the used arguments
        :param args: arguments
        """
        if args['p']:
            self.root = args['p']

        if args['c'] and args['d']:
            print('-c and -d options are mutually excluded')
        elif args['c']:
            self.create = args['c'][0]
        elif args['d']:
            self.delete = args['d'][0]

    def execute(self, args: dict):
        sql: str = ''

        self.fill(args)

        # If root password is not specified in command line
        if not self.root:
            simple = SimpleQuestion()
            self.root = simple.run('Password of root MySQL/MariaDB user', True)

        # If create a new user
        if self.create:
            self.user = self.create
            simple = SimpleQuestion()
            password = simple.run('Password of user', True)

            sql = "CREATE USER '{0}'@localhost IDENTIFIED BY '{1}';\n".format(self.user, password)

            question = YesNoQuestion()
            if question.run('Grant all privileges?', True):

                sql += "GRANT ALL PRIVILEGES ON *.* TO '{0}'@localhost WITH GRANT OPTION;\n".format(self.create)

            if question.run('Create a user database?', True):
                sql += "CREATE DATABASE {0}; GRANT ALL PRIVILEGES ON {0}.* to '{0}'@localhost;".format(
                    self.create
                )
            sql += "FLUSH PRIVILEGES;"

            os.system('mysql -u root --password={0} -e "{1}"'.format(self.root, sql))

            print("The {0} user has been created.".format(self.create))

            if self.user:
                print("The privileges of {0} has been updated.".format(self.create))

        # Else if delete exist user
        elif self.delete:
            sql = "DROP USER IF EXISTS '{0}'@localhost;\n".format(self.delete)

            question = YesNoQuestion()
            if question.run("Delete any database with the same name as the user?", True):

                sql += "DROP DATABASE IF EXISTS {0};\n".format(self.delete)
                self.user = self.delete
            sql += "FLUSH PRIVILEGES;"

            os.system('mysql -u root --password={0} -e "{1}"'.format(self.root, sql))

            print("The {0} user has been deleted".format(self.delete))

            if self.user:
                print("The database {0} has been deleted.".format(self.delete))
