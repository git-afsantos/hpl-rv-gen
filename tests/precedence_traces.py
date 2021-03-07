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

def globally_requires():
    text = 'globally: b {x > 0} requires a {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_trigger(p2d(x=1), STATE_TRUE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('a', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_TRUE),
        new_spam('b', p2d(x=1)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

def globally_requires_ref():
    text = 'globally: b as B {x > 0} requires a {x > 0 and x > @B.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_trigger(p2d(x=1), None) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('a', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_trigger(p2d(x=1), None),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# Global Scope With Timeout
###############################################################################

def globally_requires_within():
    text = 'globally: b {x > 0} requires a {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(state=STATE_ACTIVE),
        new_trigger(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(state=STATE_ACTIVE),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(state=STATE_ACTIVE),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=1)),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

def globally_requires_ref_within():
    text = 'globally: b as B {x > 0} requires a {x > 0 and x > @B.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    traces.append([
        new_trigger(p2d(x=2), None),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_trigger(p2d(x=2), None),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    # invalid
    traces.append([ new_behaviour(p2d(x=1), STATE_FALSE) ])
    traces.append([
        new_spam('b', p2d()),
        new_trigger(p2d(x=1), None),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=2), None),
        new_timer(),
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('a', p2d(x=2)),
        new_timer(),
        new_spam('b', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# After Scope No Timeout
###############################################################################

def after_requires():
    text = 'after p as P {x > 0}: b {x > @P.x} requires a {x > @P.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('p', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_TRUE),
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
        new_spam('a', p2d(x=2)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

def after_requires_ref():
    text = 'after p as P {x > 0}: b as B {x > @P.x} requires a {x > @P.x and x > @B.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_timer(),
        new_spam('p', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), None),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_spam('a', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_timer(),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

###############################################################################
# After Scope With Timeout
###############################################################################

def after_requires_within():
    text = 'after p as P {x > 0}: b {x > @P.x} requires a {x > @P.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_timer(state=STATE_ACTIVE),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_timer(),
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
        new_trigger(p2d(x=2), STATE_SAFE),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

def after_requires_ref_within():
    text = 'after p as P {x > 0}: b as B {x > @P.x} requires a {x > @P.x and x > @B.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', p2d()) ])
    traces.append([ new_spam('a', p2d()) ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_activator(p2d(x=1), STATE_ACTIVE) ])
    traces.append([
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_trigger(p2d(x=3), None),
        new_timer(),
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
        new_trigger(p2d(x=3), None),
        new_timer(),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
    ])
    return (text, traces)

###############################################################################
# Until Scope No Timeout
###############################################################################

def until_requires():
    text = 'until q {x > 0}: b {x > 0} requires a {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_TRUE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_trigger(p2d(x=1), STATE_TRUE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
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
        new_spam('a', p2d()),
        new_spam('q', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    return (text, traces)

def until_requires_ref():
    text = 'until q {x > 0}: b as B {x > 0} requires a {x > 0 and x > @B.x}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), None) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
    ])
    traces.append([
        new_spam('a', p2d()),
        new_timer(),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=1), None),
        new_spam('b', p2d()),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=3)),
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
        new_trigger(p2d(x=1), None),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    return (text, traces)

###############################################################################
# Until Scope With Timeout
###############################################################################

def until_requires_within():
    text = 'until q {x > 0}: b {x > 0} requires a {x > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), STATE_SAFE) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
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
        new_trigger(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_timer(state=STATE_ACTIVE),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_trigger(p2d(x=1), STATE_SAFE),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('b', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
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
        new_trigger(p2d(x=1), STATE_SAFE),
        new_spam('a', p2d()),
        new_spam('q', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), STATE_SAFE),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=1), STATE_FALSE),
    ])
    return (text, traces)

def until_requires_ref_within():
    text = 'until q {x > 0}: b as B {x > 0} requires a {x > 0 and x > @B.x} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', p2d()) ])
    traces.append([ new_terminator(p2d(x=1), STATE_TRUE) ])
    traces.append([ new_trigger(p2d(x=1), None) ])
    traces.append([
        new_spam('b', p2d(x=-1)),
        new_timer(),
        new_spam('b', p2d(x=-2)),
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
        new_trigger(p2d(x=1), None),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_timer(),
        new_terminator(p2d(x=1), STATE_TRUE),
    ])
    traces.append([
        new_spam('b', p2d()),
        new_timer(),
        new_trigger(p2d(x=1), None),
        new_terminator(p2d(x=1), STATE_TRUE),
        new_spam('b', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('q', p2d(x=2)),
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
        new_trigger(p2d(x=1), None),
        new_spam('a', p2d()),
        new_spam('q', p2d()),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('q', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=2), None),
        new_trigger(p2d(x=1), None),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=1), STATE_FALSE),
        new_spam('b', p2d(x=1)),
    ])
    traces.append([
        new_trigger(p2d(x=1), None),
        new_trigger(p2d(x=2), None),
        new_spam('b', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=1), STATE_FALSE),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope No Timeout
###############################################################################

def after_until_requires():
    text = 'after p as P {x > 0} until q {x > @P.x}: b {x > @P.x} requires a {x > @P.x}'
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
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
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
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d()),
        new_spam('a', p2d()),
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)

def after_until_requires_ref():
    text = 'after p as P {x > 0} until q {x > @P.x}: b as B {x > @P.x} requires a {x > @P.x and x > @B.x}'
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
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
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
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d()),
        new_spam('a', p2d()),
        new_spam('b', p2d()),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=3), None),
        new_trigger(p2d(x=4), None),
        new_behaviour(p2d(x=4), STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope With Timeout
###############################################################################

def after_until_requires_within():
    text = 'after p as P {x > 0} until q {x > @P.x}: b {x > @P.x} requires a {x > @P.x} within 3 s'
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
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=1), state=STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_timer(state=STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d(x=2)),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_trigger(p2d(x=2), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_timer(state=STATE_ACTIVE),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_trigger(p2d(x=4), STATE_SAFE),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    return (text, traces)

def after_until_requires_ref_within():
    text = 'after p as P {x > 0} until q {x > @P.x}: b as B {x > @P.x} requires a {x > @P.x and x > @B.x} within 3 s'
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
        new_terminator(p2d(x=3), STATE_INACTIVE),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=4), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=4), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_behaviour(p2d(x=2), STATE_FALSE)
    ])
    traces.append([
        new_spam('b', p2d(x=2)),
        new_timer(),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_behaviour(p2d(x=2), STATE_FALSE),
        new_timer(),
        new_spam('b', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=2)),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('a', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=2)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=2)),
        new_activator(p2d(x=2), STATE_ACTIVE),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=4), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=4), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('q', p2d(x=2)),
    ])
    traces.append([
        new_spam('p', p2d()),
        new_spam('q', p2d(x=1)),
        new_spam('b', p2d(x=1)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=4), None),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=3)),
        new_spam('b', p2d(x=2)),
        new_spam('q', p2d(x=1)),
        new_terminator(p2d(x=2), STATE_INACTIVE),
        new_spam('a', p2d(x=3)),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=3)),
        new_activator(p2d(x=1), STATE_ACTIVE),
        new_spam('b', p2d(x=1)),
        new_trigger(p2d(x=3), None),
        new_spam('b', p2d(x=2)),
        new_behaviour(p2d(x=3), STATE_FALSE),
        new_spam('b', p2d(x=3)),
        new_spam('q', p2d(x=2)),
    ])
    return (text, traces)
