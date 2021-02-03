# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos


###############################################################################
# Imports
###############################################################################

from __future__ import print_function

from .rendering import TemplateRenderer


###############################################################################
# Constants
###############################################################################

EMPTY_DICT = {}

INF = float("inf")


################################################################################
# Parsing
################################################################################

def parse_single_property(arg):
    return

def parse_property_file(text):
    return []


################################################################################
# Generation
################################################################################

def gen_monitor_nodes(props, output_dir):
    pass

def get_imports():
    return set()

def render_rv_common():
    return ""

def render_monitor(prop):
    # depends on stuff from rv_common
    return ""


################################################################################
# Entry Point
################################################################################

# http://wiki.ros.org/rospy_tutorials/Tutorials/Makefile
# https://answers.ros.org/question/323563/ros-1-correct-way-to-declare-python-dependencies/
# https://github.com/ros/rosdistro/blob/master/rosdep/python.yaml

# tool [-o <dir>] [-p] [-s <yaml_file>] [-t <yaml_file>] [-i] <arg1> <arg2> ...

# -o:   output directory for generated files
# -p:   positional args are properties, not HPL files
# -t:   [not needed for RV] type token dict file {msg type name -> {field: type}}
# -s:   signature dict file {ros name -> msg type name}
# -i:   interactive mode, ask for missing ros names
# -r:   allow use of rospy to build type tokens

def main(args):
    output_dir = args.output_dir
    is_property = args.input_property
    if is_property:
        for arg in args.args: # positional args, at least 1
            prop = parse_single_property(arg)
    else: # is file
        for arg in args.args:
            with open(arg, "r") as f:
                text = f.read().strip()
            props = parse_property_file(text)
    gen_monitor_nodes(props, output_dir)



EXAMPLES = [
    '''
    # id: p1
    # title: "My First Property"
    # description: "This is a test property to be transformed into a monitor."
    globally: no /ns/topic {data > 0}
    ''',

    'globally: no /ns/topic {data > 0} within 100 ms',

    'after /p: no /b {data > 0} within 100 ms',

    'after /p as P: no /b {data > @P.data}',

    'until /q {phi}: no /b {data > 0} within 100 ms',

    'after /p as P until /q {phi and (not @P.psi)}: no /b {forall i in array: array[@i] > 0}',
]

def test_me():
    from hpl.parser import property_parser
    p = property_parser()
    r = TemplateRenderer()
    outputs = []
    for text in EXAMPLES:
        hpl_property = p.parse(text)
        code = r.render_monitor(hpl_property)
        outputs.append(code)
    print('\n\n'.join(code for code in outputs))


if __name__ == '__main__':
    test_me()