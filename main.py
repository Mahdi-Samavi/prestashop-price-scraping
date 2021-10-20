#! venv/Scripts/python

import tables
from configure import Configure

def commands():
    while True:
        command = int(input('''
The first step you should set admin shop then add products and at final you execute run

    [1]: Add admin shop
    [2]: Get all admins
    [3]: Add product
    [4]: Get all products
    [5]: Exit

>>> '''))
        switcher = {
            1: configure.setAdmin,
            2: configure.getAdmins,
            3: configure.setProduct,
            4: configure.getProducts
        }

        if command == 5:
            break

        if len(switcher) < command:
            continue

        switcher.get(command)()

if __name__ == '__main__':
    configure = Configure()
    commands()