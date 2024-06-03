# encoding: utf-8
#-------------------------------------------------------------------------------
# Name:        contextgenerator.py
# Purpose:
#
# Author:      Nikita Romashkin
#
# Created:     27.01.2010
# Copyright:   (c) Nikita Romashkin 2010
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys

from random import random

import fca

def generate_random_context(objects_len, attributes_len, prob=0.3):
    cross_table = []
    for i in range(objects_len):
        cross_table.append([random() < prob for i in range(attributes_len)])
    attributes = ["".join(["attr", str(i)]) for i in range(attributes_len)]
    objects = ["".join(["obj", str(i)]) for i in range(objects_len)]
    return fcatng.Context(cross_table, objects, attributes)

def main():
    print("*******************************")
    print("* contextgenerator 2010-01-27 *")
    print("*******************************")

    if len(sys.argv) == 1:
        return

    path = sys.argv[1]
    objects_len = int(sys.argv[2])
    attributes_len = int(sys.argv[3])
    prob = float(sys.argv[4])

    context = generate_random_context(objects_len, attributes_len, prob)
    fcatng.write_cxt(context, path)

    print("done")

if __name__ == '__main__':
    main()