from ttyutility import Command


class DatabaseCommand(Command):
    """
    Database command
    """
    root: str
    create: str
    delete: str
    
    def __init__(self):
        super(DatabaseCommand, self).__init__()

        self.root = ''
        self.create = ''
        self.delete = ''

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        super(DatabaseCommand, self).configure(name, parser, prog, help)

        self.add_argument('-p', 0, str, 'Root password')
        self.add_argument('-c', 1, str, 'Create a database name')
        self.add_argument('-d', 1, str, 'Delete a database name')

    def execute(self, args: dict):
        if args['p']:
            self.root = args['p']

        if args['c'] and args['d']:
            print('-c and -d options are mutually excluded')
        elif args['c']:
            self.create = args['c']
        elif args['d']:
            self.delete = args['d']
