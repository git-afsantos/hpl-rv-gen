# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

from __future__ import unicode_literals

from hplrv.constants import (
    STATE_OFF, STATE_TRUE, STATE_FALSE,
    STATE_INACTIVE, STATE_ACTIVE, STATE_SAFE
)

from .common_data import *

###############################################################################
# Global Scope No Timeout
###############################################################################

def globally_no():
    text = 'globally: no b {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# Global Scope With Timeout
###############################################################################

def globally_no_within():
    text = 'globally: no b {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2), state=STATE_TRUE),
    ])
    traces.append([
        new_timer(),
        new_timer(),
        new_timer(state=STATE_TRUE),
    ])
    traces.append([
        new_timer(),
        new_timer(),
        new_spam('b', p2d(x=1), state=STATE_TRUE),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# After Scope No Timeout
###############################################################################

def after_no():
    text = 'after p as P {x > 0}: no b {x > @P.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# After Scope With Timeout
###############################################################################

def after_no_within():
    text = 'after p as P {x > 0}: no b {x > @P.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=2), state=STATE_TRUE),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# Until Scope No Timeout
###############################################################################

def until_no():
    text = 'until q {x > 0}: no b {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# Until Scope With Timeout
###############################################################################

def until_no_within():
    text = 'until q {x > 0}: no b {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_spam('b', p2d(x=1), state=STATE_TRUE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope No Timeout
###############################################################################

def after_until_no():
    text = 'after p as P {x + y > 0} until q {x > @P.x}: no b {x > @P.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=-2, y=3), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d()),
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d()),
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope With Timeout
###############################################################################

def after_until_no_within():
    text = 'after p as P {x + y > 0} until q {x > @P.x}: no b {x > @P.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=-2, y=3), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(state=STATE_SAFE),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_timer(state=STATE_SAFE),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d()),
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)
