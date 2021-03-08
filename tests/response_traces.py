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

def globally_causes():
    text = 'globally: a {x > 0} causes b {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('a', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    # none, lol
    return (text, traces)

def globally_causes_ref():
    text = 'globally: a as A {x > 0} causes b {x > 0 and x > @A.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('a', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=2), None),       # response to the first
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE), # response to the remaining two
    ])
    # invalid
    # none, lol
    return (text, traces)

###############################################################################
# Global Scope With Timeout
###############################################################################

def globally_causes_within():
    text = 'globally: a {x > 0} causes b {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_timer(),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d()),
        new_spam('b', p2d()),
        new_spam('b', p2d(), state=STATE_FALSE),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

def globally_causes_ref_within():
    text = 'globally: a as A {x > 0} causes b {x > 0 and x > @A.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_timer(),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1), state=STATE_FALSE),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=2), state=STATE_FALSE),
        new_spam('b', p2d(x=3)),
    ])
    return (text, traces)

###############################################################################
# After Scope No Timeout
###############################################################################

def after_causes():
    text = 'after p as P {x > 0}: a {x > @P.x} causes b {x > @P.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('p', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=2), STATE_SAFE),
    ])
    # invalid
    # none, lol
    return (text, traces)

def after_causes_ref():
    text = 'after p as P {x > 0}: a as A {x > @P.x} causes b {x > @P.x and x > @A.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('p', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=4), STATE_SAFE),
    ])
    # invalid
    # none, lol
    return (text, traces)

###############################################################################
# After Scope With Timeout
###############################################################################

def after_causes_within():
    text = 'after p as P {x > 0}: a {x > @P.x} causes b {x > @P.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_timer(),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

def after_causes_ref_within():
    text = 'after p as P {x > 0}: a as A {x > @P.x} causes b {x > @P.x and x > @A.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_timer(),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_spam('b', p2d(x=4)),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d()),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=2), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=3), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

###############################################################################
# Until Scope No Timeout
###############################################################################

def until_causes():
    text = 'until q {x > 0}: a {x > 0} causes b {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
    ])
    return (text, traces)

def until_causes_ref():
    text = 'until q {x > 0}: a as A {x > 0} causes b {x > 0 and x > @A.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_SAFE),
    ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), None),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
    ])
    return (text, traces)

###############################################################################
# Until Scope With Timeout
###############################################################################

def until_causes_within():
    text = 'until q {x > 0}: a {x > 0} causes b {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d()),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d()),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=0)),
        new_behaviour(p2d(x=2), STATE_SAFE),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d()),
        new_spam('b', p2d(x=2), state=STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=0)),
        new_spam('b', p2d(x=0)),
        new_spam('b', p2d(x=0), state=STATE_FALSE),
    ])
    return (text, traces)

def until_causes_ref_within():
    text = 'until q {x > 0}: a as A {x > 0} causes b {x > 0 and x > @A.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d()),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d()),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=2), None),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('b', p2d(x=4)),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=3), STATE_SAFE),
    ])
    # invalid
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_FALSE),
    ])
    traces.append([
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=1), None),
        new_behaviour(p2d(x=2), None),
        new_spam('b', p2d(x=3), state=STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=3), state=STATE_FALSE),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope No Timeout
###############################################################################

def after_until_causes():
    text = 'after p as P {x > 0} until q {x > @P.x}: a {x > @P.x} causes b {x > @P.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_terminator(p2d(x=2), STATE_FALSE),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_terminator(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_terminator(p2d(x=3), STATE_FALSE),
    ])
    return (text, traces)

def after_until_causes_ref():
    text = 'after p as P {x > 0} until q {x > @P.x}: a as A {x > @P.x} causes b {x > @P.x and x > @A.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_terminator(p2d(x=2), STATE_FALSE),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_terminator(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=4)),
        new_spam('q', p2d(x=4)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_trigger(p2d(x=4), None),
        new_behaviour(p2d(x=4), None),
        new_terminator(p2d(x=3), STATE_FALSE),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope With Timeout
###############################################################################

def after_until_causes_within():
    text = 'after p as P {x > 0} until q {x > @P.x}: a {x > @P.x} causes b {x > @P.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('a', p2d(x=1)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('a', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_timer(),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_FALSE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d(x=2)),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_terminator(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_timer(),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=4), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=2), state=STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)

def after_until_causes_ref_within():
    text = 'after p as P {x > 0} until q {x > @P.x}: a as A {x > @P.x} causes b {x > @P.x and x > @A.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d(x=1)) ])
    traces.append([ new_activator(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('a', p2d(x=1)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_spam('b', p2d(x=4)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_behaviour(p2d(x=4), STATE_SAFE),
        new_spam('b', p2d(x=4)),
        new_timer(),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_FALSE),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    traces.append([
        new_spam('b', p2d(x=2)),
        new_timer(),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_spam('b', p2d(x=2)),
        new_terminator(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_activator(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), STATE_ACTIVE),
        new_terminator(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=4)),
        new_spam('q', p2d(x=4)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_activator(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_timer(),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=4), STATE_ACTIVE),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=4)),
        new_spam('b', p2d(x=5), state=STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)
