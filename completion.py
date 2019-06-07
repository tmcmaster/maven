#!/usr/bin/env python3

import pathlib
import os
import unittest
import shlex
import sys
import time
import yaml     # pip3 install PyYAML

mavenHome = os.environ["MAVEN_HOME"]
document = open(mavenHome + '/completions.yaml', 'r')
completionTree = yaml.load(document, Loader=yaml.FullLoader)
#print(yaml.dump(parsed))

def getOptions(commandLine):
    # print('Command Line: ', commandLine)

    partial = False if commandLine[-1] == ' ' else True;
    arguments = list(filter(lambda s: len(s) > 0, commandLine.split(' ')))[1:]
    lastArg = arguments[-1] if partial else ''
    arguments = arguments[:-1] if partial else arguments

    # print('Last arg: {' + lastArg + '}')
    # print('arguments', arguments)
    # print('Partial: ', partial)

    pointer = completionTree
    for arg in arguments:
        pointer = pointer[arg];

    options = list(filter(lambda s: not s.startswith('_'),list(pointer.keys())));
    options = list(filter(lambda s: s.startswith(lastArg), options)) if partial else options

    # print('Options: ', options)

    return options,pointer #if len(options) > 1 else list()

def main():
    #commandLine = "./maven yo lit wc"
    commandLine = os.environ["COMP_LINE"]
    results,pointer = getOptions(commandLine)
    if len(results) > 0:
        print("\n".join(results))
    elif '_command' in pointer:
        command = pointer['_command']
        sys.stderr.write("\n")
        os.system(command + " --help")
        sys.stderr.write("\n\n")
        sys.stderr.write(commandLine)


if __name__ == "__main__":
    main()
