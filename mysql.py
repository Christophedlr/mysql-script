#!/usr/bin/env python

from ttyutility import Console

from mysql import DatabaseCommand, UserCommand, DumpCommand

console = Console()
console.register('db', DatabaseCommand())
console.register('user', UserCommand())
console.register('dump', DumpCommand())
console.run()
