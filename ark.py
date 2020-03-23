#!/usr/bin/python

import json
import sys
from os.path import basename
from subprocess import getoutput

temp_name = "data"

def place(path, reverse=False):
    global temp_name
    lp = f"./{temp_name}/{basename(path)}"
    return getoutput(f"cp -r {path} {lp} ") if reverse else getoutput(f"cp -r {lp} {path}")

def zip(name, unzip=False):
    getoutput(f"unzip {name}") if unzip else getoutput(f"zip -9 -r {name}.zip {name}")

def add(name, path):
    js = './files.json'
    ex = read(js)
    found = False
    i = 0
    for obj in ex:
        if obj['name'] == name:
            found = True
            ex[i]['paths'].append(path)
        i += 1
    if not found:
        ex.append({ "name": name, "paths": [path] })

    with open(js, 'w') as jf:
        json.dump(ex, jf, indent=4)


def read(path):
    data = None
    with open(path) as f:
        data = json.load(f)
    return data

def parse_args(argv):
    if argv.__len__() == 1:
        return [argv[0]]
    elif argv.__len__() == 2:
        args = argv[1].split("=")
        return [argv[0], args]
    else:
        print("Help")

def main(argv):
    global temp_name

    args = parse_args(argv)
    data = read('./files.json')

    if args[0] == "place":
        print("Inflating objects")
        zip(temp_name, True)
        for obj in data:
            print(f"Placing {obj['name']}")
            for path in obj['paths']:
                place(path)

    elif args[0] == "populate":
        print("Populating storage")
        getoutput(f"mkdir -p ./{temp_name}")
        for obj in data:
            print(f"Placing {obj['name']}")
            for path in obj['paths']:
                place(path, True)
        print("Deflating objects")
        zip(temp_name)
        getoutput(f"rm -rf {temp_name}")

    elif args[0] == "add" and args[1]:
        name = args[1][0]
        path = args[1][1]
        print(f"Adding {name}")
        add(name, path)

if __name__ == "__main__":
    if sys.argv.__len__() == 1: print("Help")
    else: main(sys.argv[1:])
