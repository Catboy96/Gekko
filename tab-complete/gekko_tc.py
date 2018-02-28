#!/usr/bin/env python3

import os
import yaml

if __name__ == '__main__':
    # Nodes saved in "~/.gekko".
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    # Nodes file not exist. Return empty string.
    if not os.path.exists(svrfile):
        print("")
        exit(0)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        datas = yaml.load(f)
    # No nodes saved. Return empty string
    if not datas:
        print("")
        exit(0)
    # Print all node remarks
    for data in datas:
        print('%s' % data['remark'])
