# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

from __future__ import print_function, unicode_literals

from hpl.parser import property_parser
from hplrv.rendering import TemplateRenderer


def main():
    p = property_parser()
    r = TemplateRenderer()
    text = [
        '#id: p1 globally: no b {x > 0}',
    ]
    hp = [p.parse(ti) for ti in text]
    topics = {
        'a': 'geometry_msgs/Point',
        'b': 'geometry_msgs/Point',
    }
    py = r.render_rospy_node(hp, topics)
    print(py)

if __name__ == '__main__':
    main()
