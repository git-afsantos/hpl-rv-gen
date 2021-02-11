# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

from __future__ import print_function, unicode_literals
from builtins import object, range
from collections import deque, namedtuple
from threading import Lock
import unittest

from hpl.parser import property_parser

from hplrv.constants import *
from hplrv.rendering import TemplateRenderer


###############################################################################
# Data Structures
###############################################################################

E_TIMER = 0
E_ACTIVATOR = 1
E_TERMINATOR = 2
E_BEHAVIOUR = 3
E_TRIGGER = 4
E_SPAM = 5

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
    ('event', 'topic', 'msg'))

def new_spam(topic, msg):
    # topic: str
    # msg: object
    return SpamEvent(E_SPAM, topic, msg)

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


###############################################################################
# Test Case Generation
###############################################################################

def openings_globally():
    valid = [
        [],
        [new_spam('p', p2d())],
        [new_spam('q', p2d())],
        [new_spam('a', p2d())],
        [new_spam('b', p2d())],
        [
            new_spam('p', p2d()),
            new_spam('p', p2d())
        ],
    ]
    invalid = ()
    return valid, invalid

def openings_after(s0):
    valid = [
        [new_activator(p2d(x=1), s0)],
        [
            new_spam('p', p2d()),
            new_activator(p2d(x=1), s0)
        ],
        [
            new_spam('q', p2d()),
            new_activator(p2d(x=1), s0)
        ],
        [
            new_spam('a', p2d()),
            new_activator(p2d(x=1), s0)
        ],
        [
            new_spam('b', p2d()),
            new_activator(p2d(x=1), s0)
        ],
    ]
    invalid = [
        [],
        [],
        [new_spam('q', p2d())],
        [new_spam('a', p2d())],
        [new_spam('b', p2d())],
        [
            new_spam('p', p2d(x=-1)),
            new_spam('p', p2d())
        ],
    ]
    return valid, invalid

SCOPES = (
    'globally',
    'after p as P {x > 0}',
    'until q {x > 0}',
    'after p as P {x > 0} until q {x > @P.x}',
)

def absence_properties():
    text = 'globally: no b {x > 0}'
    traces = []
    # valid
    traces.append([])
    traces.append([ new_timer(STATE_ACTIVE) ])
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
        new_spam('b', p2d()),
    ])
    yield (text, traces)

def existence_properties():
    return ()

def precedence_properties():
    return ()

def response_properties():
    return ()

def prevention_properties():
    return ()

def all_types_of_property():
    # example = text, traces
    for example in absence_properties():
        yield example
    for example in existence_properties():
        yield example
    for example in precedence_properties():
        yield example
    for example in response_properties():
        yield example
    for example in prevention_properties():
        yield example


###############################################################################
# Test Loop
###############################################################################

def state_name(s):
    if s == STATE_FALSE:
        return 'FALSE'
    if s == STATE_TRUE:
        return 'TRUE'
    if s == STATE_OFF:
        return 'OFF'
    if s == STATE_INACTIVE:
        return 'INACTIVE'
    if s == STATE_ACTIVE:
        return 'ACTIVE'
    if s == STATE_SAFE:
        return 'SAFE'
    return 'STATE {}'.format(s)

def pretty_trace(trace):
    s = []
    t = 0
    for e in trace:
        t += 1
        etype = e[0]
        if etype == E_TIMER:
            s.append('@ {}: (Timer, -{}) -> {}'.format(
                t, e.drops, state_name(e.state)))
        elif etype == E_ACTIVATOR:
            s.append("@ {}: (Activator) '{}' {} -> {}".format(
                t, e.topic, e.msg, state_name(e.state)))
        elif etype == E_TERMINATOR:
            s.append("@ {}: (Terminator) '{}' {} -> {}".format(
                t, e.topic, e.msg, state_name(e.state)))
        elif etype == E_BEHAVIOUR:
            s.append("@ {}: (Behaviour) '{}' {} -> {}".format(
                t, e.topic, e.msg, state_name(e.state)))
        elif etype == E_TRIGGER:
            s.append("@ {}: (Trigger) '{}' {} -> {}".format(
                t, e.topic, e.msg, state_name(e.state)))
        else:
            s.append("@ {}: (Spam) '{}' {}".format(
                t, e.topic, e.msg))
    return "\n".join(s)

def pretty_monitor(m):
    return "\n".join((
        'm._state = {}'.format(m._state),
        'm.time_launch = {}'.format(m.time_launch),
        'm.time_shutdown = {}'.format(m.time_shutdown),
        'm.time_state = {}'.format(m.time_state),
        'm.witness = {}'.format(m.witness),
        'm._pool = {}'.format(getattr(m, '_pool', None)),
    ))


class TestMonitorClasses(unittest.TestCase):
    #def __init__(self):
    def setUp(self):
        self._reset()

    def test_examples(self):
        n = 0
        p = property_parser()
        r = TemplateRenderer()
        for text, traces in all_types_of_property():
            hp = p.parse(text)
            py = r.render_monitor(hp)
            m = self._make_monitor(py)
            for trace in traces:
                n += 1
                self.hpl_string = text
                self._set_trace_string(trace, n)
                self._launch(hp, m)
                time = 0
                for event in trace:
                    time += 1
                    self._dispatch(m, event, time)
                self._shutdown(m)
                self._reset()
        print('Tested {} examples.'.format(n))

    def _reset(self):
        self.debug_string = ''
        self.trace_string = ''
        self.hpl_string = ''
        self.entered_scope = []
        self.exited_scope = []
        self.found_success = []
        self.found_failure = []

    def _make_monitor(self, py):
        exec(py)
        m = PropertyMonitor()
        m.on_enter_scope = self._on_enter
        m.on_exit_scope = self._on_exit
        m.on_success = self._on_success
        m.on_violation = self._on_failure
        self._update_debug_string(m, -1)
        assert m._state == STATE_OFF, self.debug_string
        assert m.verdict is None, self.debug_string
        assert not m.witness, self.debug_string
        assert m.time_launch < 0, self.debug_string
        assert m.time_state < 0, self.debug_string
        assert m.time_shutdown < 0, self.debug_string
        return m

    def _launch(self, hp, m):
        m.on_launch(0)
        self._update_debug_string(m, 0)
        if hp.scope.is_global or hp.scope.is_until:
            assert len(self.entered_scope) == 1, self.debug_string
            assert self.entered_scope[0] == 0, self.debug_string
        else:
            assert not self.entered_scope, self.debug_string
        assert not self.exited_scope, self.debug_string
        assert not self.found_success, self.debug_string
        assert not self.found_failure, self.debug_string
        assert m._state != STATE_OFF, self.debug_string
        assert m.verdict is None, self.debug_string
        assert not m.witness, self.debug_string
        assert m.time_launch == 0, self.debug_string
        assert m.time_state == 0, self.debug_string
        assert m.time_shutdown < 0, self.debug_string
        try:
            m.on_launch(0)
            self._update_debug_string(m, 0)
            assert False, self.debug_string
        except RuntimeError:
            pass # expected

    def _dispatch(self, m, event, time):
        etype = event[0]
        if etype == E_TIMER:
            self._dispatch_timer(m, event, time)
        elif etype == E_ACTIVATOR:
            self._dispatch_activator(m, event, time)
        elif etype == E_TERMINATOR:
            self._dispatch_terminator(m, event, time)
        elif etype == E_BEHAVIOUR:
            self._dispatch_behaviour(m, event, time)
        elif etype == E_TRIGGER:
            self._dispatch_trigger(m, event, time)
        else:
            self._dispatch_spam(m, event, time)

    def _dispatch_activator(self, m, event, time):
        n = len(self.entered_scope)
        assert m._state == STATE_INACTIVE, self.debug_string
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
        self._update_debug_string(m, time)
        assert consumed, self.debug_string
        assert len(self.entered_scope) == n + 1, self.debug_string
        assert self.entered_scope[-1] == time, self.debug_string
        assert not self.exited_scope, self.debug_string
        assert not self.found_success, self.debug_string
        assert not self.found_failure, self.debug_string
        assert m._state == event.state, self.debug_string
        assert m.verdict is None, self.debug_string
        assert len(m.witness) == 1, self.debug_string
        assert m.witness[-1].topic == event.topic, self.debug_string
        assert m.witness[-1].timestamp == time, self.debug_string
        assert m.witness[-1].msg == event.msg, self.debug_string
        assert m.time_state == time, self.debug_string

    def _dispatch_terminator(self, m, event, time):
        n = len(self.exited_scope)
        assert m._state > STATE_INACTIVE, self.debug_string
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
        self._update_debug_string(m, time)
        assert consumed, self.debug_string
        assert len(self.exited_scope) == n + 1, self.debug_string
        assert self.exited_scope[-1] == time, self.debug_string
        assert len(self.entered_scope) == n + 1, self.debug_string
        self._check_verdict(m, event, time)
        if event.state == STATE_INACTIVE:
            assert not m.witness, self.debug_string
            assert not getattr(m, '_pool', None), self.debug_string

    def _dispatch_behaviour(self, m, event, time):
        a = len(self.entered_scope)
        b = len(self.exited_scope)
        assert m._state == STATE_ACTIVE, self.debug_string
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
        self._update_debug_string(m, time)
        assert consumed, self.debug_string
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        self._check_verdict(m, event, time)

    def _dispatch_trigger(self, m, event, time):
        a = len(self.entered_scope)
        b = len(self.exited_scope)
        k = -1 if not hasattr(m, '_pool') else len(m._pool)
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
        self._update_debug_string(m, time)
        assert consumed, self.debug_string
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        self._check_verdict(m, event, time)
        if k >= 0:
            assert len(m._pool) >= k, self.debug_string
            assert m._pool[-1].topic == event.topic, self.debug_string
            assert m._pool[-1].timestamp == time, self.debug_string
            assert m._pool[-1].msg == event.msg, self.debug_string

    def _dispatch_spam(self, m, event, time):
        a = len(self.entered_scope)
        b = len(self.exited_scope)
        c = len(self.found_success)
        d = len(self.found_failure)
        k = len(getattr(m, '_pool', ()))
        n = len(m.witness)
        s = m._state
        t = m.time_state
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
        self._update_debug_string(m, time)
        assert not consumed, self.debug_string
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        assert len(self.found_success) == c, self.debug_string
        assert len(self.found_failure) == d, self.debug_string
        assert len(getattr(m, '_pool', ())) == k, self.debug_string
        assert len(m.witness) == n, self.debug_string
        assert m._state == s, self.debug_string
        assert m.time_state == t, self.debug_string

    def _dispatch_msg(self, m, topic, msg, time):
        cb = getattr(m, 'on_msg_' + topic)
        return cb(msg, time)

    def _dispatch_timer(self, m, event, time):
        a = len(self.entered_scope)
        b = len(self.exited_scope)
        k = len(getattr(m, '_pool', ()))
        s = m._state
        m.on_timer(time)
        self._update_debug_string(m, time)
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        assert len(getattr(m, '_pool', ())) <= k, self.debug_string
        if event.state == STATE_TRUE:
            assert len(self.found_success) == 1, self.debug_string
            assert self.found_success[0][0] == time, self.debug_string
            assert self.found_success[0][1] == m.witness, self.debug_string
            assert m.verdict is True, self.debug_string
            assert m.time_state == time, self.debug_string
            assert m._state == event.state, self.debug_string
        elif event.state == STATE_FALSE:
            assert len(self.found_failure) == 1, self.debug_string
            assert self.found_failure[0][0] == time, self.debug_string
            assert self.found_failure[0][1] == m.witness, self.debug_string
            assert m.verdict is False, self.debug_string
            assert m.time_state == time, self.debug_string
            assert m._state == event.state, self.debug_string
        elif event.state is not None:
            assert not self.found_success, self.debug_string
            assert not self.found_failure, self.debug_string
            assert m.verdict is None, self.debug_string
            assert not m.witness, self.debug_string
            assert m._state == event.state, self.debug_string
        else:
            assert m._state == s, self.debug_string

    def _shutdown(self, m):
        m.on_shutdown(1000)
        self._update_debug_string(m, 1000)
        assert m._state == STATE_OFF, self.debug_string
        assert m.time_launch == 0, self.debug_string
        assert m.time_state >= 0, self.debug_string
        assert m.time_shutdown == 1000, self.debug_string
        try:
            m.on_shutdown(2000)
            self._update_debug_string(m, 2000)
            assert False, self.debug_string
        except RuntimeError:
            pass # expected

    def _check_verdict(self, m, event, time):
        assert m._state == event.state, self.debug_string
        if event.state == STATE_TRUE:
            assert len(self.found_success) == 1, self.debug_string
            assert self.found_success[0][0] == time, self.debug_string
            assert self.found_success[0][1] == m.witness, self.debug_string
            assert m.verdict is True, self.debug_string
            assert len(m.witness) >= 1, self.debug_string
            assert m.witness[-1].topic == event.topic, self.debug_string
            assert m.witness[-1].timestamp == time, self.debug_string
            assert m.witness[-1].msg == event.msg, self.debug_string
            assert m.time_state == time, self.debug_string
        elif event.state == STATE_FALSE:
            assert len(self.found_failure) == 1, self.debug_string
            assert self.found_failure[0][0] == time, self.debug_string
            assert self.found_failure[0][1] == m.witness, self.debug_string
            assert m.verdict is False, self.debug_string
            assert len(m.witness) >= 1, self.debug_string
            assert m.witness[-1].topic == event.topic, self.debug_string
            assert m.witness[-1].timestamp == time, self.debug_string
            assert m.witness[-1].msg == event.msg, self.debug_string
            assert m.time_state == time, self.debug_string
        else:
            assert not self.found_success, self.debug_string
            assert not self.found_failure, self.debug_string
            assert m.verdict is None, self.debug_string

    def _on_enter(self, stamp):
        self.entered_scope.append(stamp)

    def _on_exit(self, stamp):
        self.exited_scope.append(stamp)

    def _on_success(self, stamp, witness):
        self.found_success.append((stamp, witness))

    def _on_failure(self, stamp, witness):
        self.found_failure.append((stamp, witness))

    def _set_trace_string(self, trace, n):
        self.trace_string = '[Example #{}]:\n{}'.format(n, pretty_trace(trace))

    def _update_debug_string(self, m, time):
        self.debug_string = ('failed for the following test'
            '\n  [HPL]: {}'
            '\n  {}'
            '\n  [Timestamp]: {}'
            '\n  [Monitor]:'
            '\n{}'
        ).format(self.hpl_string, self.trace_string, time, pretty_monitor(m))


if __name__ == '__main__':
    unittest.main()
