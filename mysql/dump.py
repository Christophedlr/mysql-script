import os

from ttyutility import Command
from question import SimpleQuestion


class DumpCommand(Command):
    """
    Dump command
    """
    dbname: str
    dest: str
    root: str

    def __init__(self):
        """
        Initialization
        """
        super(DumpCommand, self).__init__()

        self.dbname = ''
        self.dest = ''
        self.root = ''

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        super(DumpCommand, self).configure(name, parser, prog, help)

        self.add_argument('-p', 0, str, 'Root password')
        self.add_argument('-n', 1, str, 'Name of database')
        self.add_argument('-l', 1, str, 'Location for saved dump database')

    def fill(self, args: dict):
        """
        Fill properties with the used arguments
        :param args: arguments
        """
        if args['p']:
            self.root = args['p']

        if args['n']:
            self.dbname = args['n'][0]

        if args['l']:
            self.dest = args['l'][0]

    def execute(self, args: dict):
        self.fill(args)
        simple = SimpleQuestion()

        # If root password is not specified in command line
        if not self.root:
            self.root = simple.run('Password of root MySQL/MariaDB user', True)

        if not self.dbname:
            self.dbname = simple.run('Name of database to saved')

        params = "--add-drop-table --add-drop-trigger --add-locks --allow-keywords -c -a -i -K -e -l " \
                 "--no-autocommit -B -R {0} -u root --password={1}".format(self.dbname , self.root)

        if not self.dest:
            self.dest = simple.run('Location & name of dump to saved')

        os.system('mysqldump {0} > {1}'.format(params, self.dest))

        print("The {0} database has been saved.".format(self.dbname))
