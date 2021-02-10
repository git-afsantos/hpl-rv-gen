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

# MsgRecord = namedtuple("MsgRecord", ('topic', 'timestamp', 'msg'))

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

def new_timer(state, drops=0):
    # state: int (target state)
    # drops: int (triggers dropped)
    return TimerEvent(E_TIMER, state, drops)


###############################################################################
# Test Case Generation
###############################################################################

def absence_properties():

def existence_properties():

def precedence_properties():

def response_properties():

def prevention_properties():

def all_types_of_property():
    for test_case in absence_properties():
        yield test_case
    for test_case in existence_properties():
        yield test_case
    for test_case in precedence_properties():
        yield test_case
    for test_case in response_properties():
        yield test_case
    for test_case in prevention_properties():
        yield test_case


###############################################################################
# Test Loop
###############################################################################

class MonitorTester(object):
    def __init__(self):
        self._reset()

    def test():
        n = 0
        p = property_parser()
        r = TemplateRenderer()
        for text, traces in all_types_of_property():
            hp = p.parse(text)
            py = r.render_monitor(hp)
            m = self._make_monitor(py)
            for trace in traces:
                n += 1
                self._update_debug_string(text, trace, n)
                self._launch(hp, m)
                for i in range(len(trace)):
                    time = i + 1
                    event = trace[i]
                    self._dispatch(m, event, time)
                self._shutdown(m)
                self._reset()
        print('Tested {} examples.'.format(self._examples))

    def _reset(self):
        self.debug_string = ''
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
        assert m._state == STATE_OFF, self.debug_string
        assert m.verdict is None, self.debug_string
        assert not m.witness, self.debug_string
        assert m.time_launch < 0, self.debug_string
        assert m.time_state < 0, self.debug_string
        assert m.time_shutdown < 0, self.debug_string
        return m

    def _launch(self, hp, m):
        m.on_launch(0)
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
        assert consumed, self.debug_string
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        self._check_verdict(m, event, time)

    def _dispatch_trigger(self, m, event, time):
        a = len(self.entered_scope)
        b = len(self.exited_scope)
        k = -1 if not hasattr(m, '_pool') else len(m._pool)
        consumed = self._dispatch_msg(m, event.topic, event.msg, time)
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
        m.on_timer(time)
        assert len(self.entered_scope) == a, self.debug_string
        assert len(self.exited_scope) == b, self.debug_string
        assert len(getattr(m, '_pool', ())) <= k, self.debug_string
        assert m._state == event.state, self.debug_string
        if event.state == STATE_TRUE:
            assert len(self.found_success) == 1, self.debug_string
            assert self.found_success[0][0] == time, self.debug_string
            assert self.found_success[0][1] == m.witness, self.debug_string
            assert m.verdict is True, self.debug_string
            assert m.time_state == time, self.debug_string
        elif event.state == STATE_FALSE:
            assert len(self.found_failure) == 1, self.debug_string
            assert self.found_failure[0][0] == time, self.debug_string
            assert self.found_failure[0][1] == m.witness, self.debug_string
            assert m.verdict is False, self.debug_string
            assert m.time_state == time, self.debug_string
        else:
            assert not self.found_success, self.debug_string
            assert not self.found_failure, self.debug_string
            assert m.verdict is None, self.debug_string
            assert not m.witness, self.debug_string

    def _shutdown(self, m):
        m.on_shutdown(1000)
        assert m._state == STATE_OFF, self.debug_string
        assert m.time_launch == 0, self.debug_string
        assert m.time_state >= 0, self.debug_string
        assert m.time_shutdown == 1000, self.debug_string
        try:
            m.on_shutdown(2000)
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

    def _update_debug_string(self, text, trace, n):
        self.debug_string = ('failed for the following test'
            '\n  [HPL]: {}'
            '\n  [Example #{}]: {}'
        ).format(text, n, trace)
