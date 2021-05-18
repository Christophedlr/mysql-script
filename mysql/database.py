import os

from ttyutility import Command
from question import YesNoQuestion, SimpleQuestion


class DatabaseCommand(Command):
    """
    Database command
    """
    root: str
    create: str
    delete: str
    user: str
    
    def __init__(self):
        """
        Initialization
        """
        super(DatabaseCommand, self).__init__()

        self.root = ''
        self.create = ''
        self.delete = ''
        self.user = ''

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        super(DatabaseCommand, self).configure(name, parser, prog, help)

        self.add_argument('-p', 0, str, 'Root password')
        self.add_argument('-c', 1, str, 'Create a database name')
        self.add_argument('-d', 1, str, 'Delete a database name')

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

        # If create a new database
        if self.create:
            sql = "CREATE DATABASE IF NOT EXISTS {0};\n".format(self.create)

            question = YesNoQuestion()
            if question.run('Grant all privileges for an user ?', True):
                simple = SimpleQuestion()
                self.user = simple.run('Name of a valid user :')

                sql += "GRANT ALL PRIVILEGES ON {0}.* TO '{1}'@localhost;\n".format(self.create, self.user)
            sql += "FLUSH PRIVILEGES;"

            os.system('mysql -u root --password={0} -e "{1}"'.format(self.root, sql))

            print("The {0} database has been created.".format(self.create))

            if self.user:
                print("The privileges of {0} for {1} database has been updated.".format(self.user, self.create))

        # Else if delete exist database
        elif self.delete:
            sql = "DROP DATABASE IF EXISTS {0};\n".format(self.delete)

            question = YesNoQuestion()
            if question.run("Revoke all privileges for an user ?", True):
                simple = SimpleQuestion()
                self.user = simple.run("Name of a valid user :")

                sql += "REVOKE ALL PRIVILEGES ON {0}.* FROM '{1}'@localhost;\n".format(self.delete, self.user)
            sql += "FLUSH PRIVILEGES;"

            os.system('mysql -u root --password={0} -e "{1}"'.format(self.root, sql))

            print("The {0} database has been deleted".format(self.delete))

            if self.user:
                print("The privileges of {0} for {1} database has been revoked.".format(self.user, self.delete))
