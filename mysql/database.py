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

        if not self.root:
            simple = SimpleQuestion()
            self.root = simple.run('Password of root MySQL/MariaDB user', True)

        if self.create:
            sql = "CREATE DATABASE IF NOT EXISTS {0};\n".format(self.create)

            question = YesNoQuestion()
            if question.run('Grant all privileges for an user ?', True):
                simple = SimpleQuestion()
                user = simple.run('Name of a valid user :')

                sql += "GRANT ALL PRIVILEGES ON {0}.* TO '{1}'@localhost;\n".format(self.create, user)
            sql += "FLUSH PRIVILEGES;"

            os.system('mysql -u root --password={0} -e "{1}"'.format(self.root, sql))

            print("The {0} database has been created.".format(self.create))

            if user:
                print("The privileges of {0} for {1} database has been updated.".format(user, self.create))
