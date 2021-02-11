# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

from __future__ import unicode_literals
from collections import namedtuple

###############################################################################
# Constants
###############################################################################

E_TIMER = 0
E_ACTIVATOR = 1
E_TERMINATOR = 2
E_BEHAVIOUR = 3
E_TRIGGER = 4
E_SPAM = 5

###############################################################################
# Data Structures
###############################################################################

MsgRecord = namedtuple("MsgRecord", ('topic', 'timestamp', 'msg'))

ActivatorEvent = namedtuple('ActivatorEvent',
    ('event', 'topic', 'msg', 'state'))

def new_activator(msg, state, topic='p'):
    # topic: str
    # msg: object
    # state: int (target state)
    return ActivatorEvent(E_ACTIVATOR, topic, msg, state)


TerminatorEvent = namedtuple('TerminatorEvent',
    ('event', 'topic', 'msg', 'state'))

def new_terminator(msg, state, topic='q'):
    # topic: str
    # msg: object
    # state: int (target state)
    return TerminatorEvent(E_TERMINATOR, topic, msg, state)


BehaviourEvent = namedtuple('BehaviourEvent',
    ('event', 'topic', 'msg', 'state'))

def new_behaviour(msg, state, topic='b'):
    # topic: str
    # msg: object
    # state: int (target state)
    return BehaviourEvent(E_BEHAVIOUR, topic, msg, state)


TriggerEvent = namedtuple('TriggerEvent',
    ('event', 'topic', 'msg', 'state'))

def new_trigger(msg, state, topic='a'):
    # topic: str
    # msg: object
    # state: int (target state)
    return TriggerEvent(E_TRIGGER, topic, msg, state)


SpamEvent = namedtuple('SpamEvent',
    ('event', 'topic', 'msg', 'state'))

def new_spam(topic, msg, state=None):
    # topic: str
    # msg: object
    # state: int (target state)
    return SpamEvent(E_SPAM, topic, msg, state)


TimerEvent = namedtuple('TimerEvent',
    ('event', 'state', 'drops'))

def new_timer(state=None, drops=0):
    # state: int (target state)
    # drops: int (triggers dropped)
    return TimerEvent(E_TIMER, state, drops)


Point2D = namedtuple('Point2D', ('x', 'y'))

def p2d(x=0, y=0):
    return Point2D(x, y)

Array = namedtuple('Vectors', ('array',))
