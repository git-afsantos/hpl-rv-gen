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

def globally_some():
    text = 'globally: some b {len(xs) > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([
        new_spam('b', EMPTY_ARRAY),
        new_timer(),
        new_spam('b', EMPTY_ARRAY),
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_spam('b', ARRAY_123),
    ])
    # invalid
    # none, lol
    return (text, traces)

###############################################################################
# Global Scope With Timeout
###############################################################################

def globally_some_within():
    text = 'globally: some b {exists i in xs: xs[@i] > 0} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_behaviour(ARRAY_010, STATE_TRUE) ])
    traces.append([
        new_spam('b', Array(())),
        new_behaviour(ARRAY_010, STATE_TRUE),
        new_timer(),
        new_spam('b', ARRAY_010),
    ])
    # invalid
    traces.append([
        new_spam('b', ARRAY_000),
        new_timer(),
        new_spam('b', ARRAY_010, state=STATE_FALSE),
    ])
    traces.append([
        new_timer(),
        new_timer(),
        new_timer(state=STATE_FALSE),
    ])
    return (text, traces)

###############################################################################
# After Scope No Timeout
###############################################################################

def after_some():
    text = 'after p as P {xs[1] > 0}: some b {xs[1] > @P.xs[1]}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', ARRAY_010) ])
    traces.append([ new_activator(ARRAY_010, STATE_ACTIVE) ])
    traces.append([
        new_spam('b', ARRAY_123),
        new_activator(ARRAY_010, STATE_ACTIVE),
        new_timer(),
        new_spam('b', ARRAY_010),
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_spam('b', ARRAY_123),
    ])
    # invalid
    # none, lol
    return (text, traces)

###############################################################################
# After Scope With Timeout
###############################################################################

def after_some_within():
    text = 'after p as P {xs[1] > 0}: some b {xs[1] > @P.xs[1]} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_activator(ARRAY_010, STATE_ACTIVE) ])
    traces.append([
        new_activator(ARRAY_010, STATE_ACTIVE),
        new_behaviour(ARRAY_123, STATE_TRUE)
    ])
    traces.append([
        new_spam('b', ARRAY_010),
        new_timer(),
        new_activator(ARRAY_010, STATE_ACTIVE),
        new_spam('b', ARRAY_010),
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_timer(),
        new_spam('b', ARRAY_123),
    ])
    # invalid
    traces.append([
        new_spam('b', ARRAY_010),
        new_activator(ARRAY_010, STATE_ACTIVE),
        new_timer(),
        new_spam('b', ARRAY_010),
        new_spam('b', ARRAY_123, state=STATE_FALSE),
        new_spam('b', ARRAY_123),
    ])
    return (text, traces)

###############################################################################
# Until Scope No Timeout
###############################################################################

def until_some():
    text = 'until q {forall i in xs: xs[@i] = 0}: some b {sum(xs) > 3}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_spam('q', ARRAY_010) ])
    traces.append([ new_behaviour(ARRAY_123, STATE_TRUE) ])
    traces.append([
        new_spam('b', ARRAY_000),
        new_timer(),
        new_spam('q', ARRAY_010),
    ])
    traces.append([
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_spam('q', ARRAY_000),
    ])
    traces.append([
        new_spam('b', EMPTY_ARRAY),
        new_timer(),
        new_spam('b', ARRAY_111),
        new_spam('q', ARRAY_111),
        new_timer(),
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_timer(),
        new_spam('b', ARRAY_123),
    ])
    # invalid
    traces.append([ new_terminator(EMPTY_ARRAY, STATE_FALSE) ])
    traces.append([
        new_spam('b', ARRAY_111),
        new_spam('q', ARRAY_111),
        new_timer(),
        new_terminator(ARRAY_000, STATE_FALSE),
        new_spam('b', ARRAY_123),
    ])
    return (text, traces)

###############################################################################
# Until Scope With Timeout
###############################################################################

def until_some_within():
    text = 'until q {forall i in xs: xs[@i] = 0}: some b {sum(xs) > 3} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_spam('q', ARRAY_010) ])
    traces.append([ new_behaviour(ARRAY_123, STATE_TRUE) ])
    traces.append([
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_spam('q', ARRAY_000),
    ])
    traces.append([
        new_spam('b', EMPTY_ARRAY),
        new_behaviour(ARRAY_123, STATE_TRUE),
        new_timer(),
        new_spam('b', ARRAY_111),
        new_spam('q', ARRAY_111),
        new_timer(),
        new_spam('b', ARRAY_123),
    ])
    # invalid
    traces.append([ new_terminator(EMPTY_ARRAY, STATE_FALSE) ])
    traces.append([
        new_spam('b', ARRAY_000),
        new_timer(),
        new_spam('q', ARRAY_010, state=STATE_FALSE),
        new_spam('b', ARRAY_123),
    ])
    traces.append([
        new_timer(),
        new_terminator(ARRAY_000, STATE_FALSE),
        new_spam('b', ARRAY_123),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope No Timeout
###############################################################################

def after_until_some():
    text = 'after p as P {prod(xs) = 1} until q {max(xs) < min(@P.xs)}: some b {prod(xs) >= prod(@P.xs)}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', ARRAY_010) ])
    traces.append([ new_spam('q', EMPTY_ARRAY) ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_activator(EMPTY_ARRAY, STATE_ACTIVE) ])
    traces.append([
        new_spam('b', EMPTY_ARRAY),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_timer(),
        new_spam('b', ARRAY_010),
    ])
    traces.append([
        new_spam('p', ARRAY_010),
        new_spam('q', ARRAY_000),
        new_spam('b', ARRAY_111),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_000),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_spam('q', ARRAY_123),
        new_terminator(ARRAY_000, STATE_INACTIVE),
        new_spam('b', ARRAY_123),
        new_spam('q', ARRAY_000),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('q', ARRAY_010),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_spam('b', ARRAY_123),
        new_terminator(ARRAY_000, STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_terminator(ARRAY_000, STATE_FALSE)
    ])
    traces.append([
        new_spam('p', ARRAY_010),
        new_spam('q', ARRAY_000),
        new_spam('b', ARRAY_111),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_000),
        new_spam('q', ARRAY_123),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_terminator(ARRAY_000, STATE_INACTIVE),
        new_spam('b', ARRAY_123),
        new_spam('q', ARRAY_000),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_010),
        new_spam('q', ARRAY_010),
        new_terminator(ARRAY_000, STATE_FALSE),
    ])
    return (text, traces)

###############################################################################
# After-Until Scope With Timeout
###############################################################################

def after_until_some_within():
    text = 'after p as P {prod(xs) = 1} until q {max(xs) < min(@P.xs)}: some b {prod(xs) >= prod(@P.xs)} within 3 s'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer() ])
    traces.append([ new_spam('p', ARRAY_010) ])
    traces.append([ new_spam('q', EMPTY_ARRAY) ])
    traces.append([ new_spam('b', EMPTY_ARRAY) ])
    traces.append([ new_activator(EMPTY_ARRAY, STATE_ACTIVE) ])
    traces.append([
        new_spam('b', EMPTY_ARRAY),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_timer(),
        new_spam('b', ARRAY_010),
    ])
    traces.append([
        new_spam('p', ARRAY_010),
        new_spam('q', ARRAY_000),
        new_spam('b', ARRAY_111),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_000),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_spam('q', ARRAY_123),
        new_terminator(ARRAY_000, STATE_INACTIVE),
        new_spam('b', ARRAY_123),
        new_spam('q', ARRAY_000),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('q', ARRAY_010),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_spam('b', ARRAY_123),
        new_terminator(ARRAY_000, STATE_INACTIVE),
    ])
    # invalid
    traces.append([
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_terminator(ARRAY_000, STATE_FALSE)
    ])
    traces.append([
        new_spam('p', ARRAY_010),
        new_spam('q', ARRAY_000),
        new_spam('b', ARRAY_111),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_000),
        new_behaviour(ARRAY_123, STATE_SAFE),
        new_spam('q', ARRAY_123),
        new_terminator(ARRAY_000, STATE_INACTIVE),
        new_spam('b', ARRAY_123),
        new_spam('q', ARRAY_000),
        new_activator(ARRAY_111, STATE_ACTIVE),
        new_spam('b', ARRAY_010),
        new_spam('q', ARRAY_010),
        new_spam('b', ARRAY_123, state=STATE_FALSE),
        new_spam('q', ARRAY_000),
    ])
    return (text, traces)
