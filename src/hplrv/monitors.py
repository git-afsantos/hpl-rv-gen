# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

from __future__ import unicode_literals
from builtins import object, str
from collections import defaultdict, namedtuple

from hpl.ast import HplVacuousTruth

from .constants import *


###############################################################################
# Data Structures
###############################################################################

ActivatorEvent = namedtuple('ActivatorEvent',
    ('event_type', 'predicate'))

def new_activator(phi):
    # phi: HplPredicate
    return ActivatorEvent(EVENT_ACTIVATOR, phi)


TerminatorEvent = namedtuple('TerminatorEvent',
    ('event_type', 'predicate', 'activator', 'verdict'))

def new_terminator(phi, activator, verdict):
    # predicate: HplPredicate
    # activator: str|None
    # verdict: bool|None
    return TerminatorEvent(EVENT_TERMINATOR, phi, activator, verdict)


BehaviourEvent = namedtuple('BehaviourEvent',
    ('event_type', 'predicate', 'activator', 'trigger'))

def new_behaviour(phi, activator, trigger):
    # predicate: HplPredicate
    # activator: str|None
    # trigger: str|None
    return BehaviourEvent(EVENT_BEHAVIOUR, phi, activator, trigger)


TriggerEvent = namedtuple('TriggerEvent',
    ('event_type', 'predicate', 'activator'))

def new_trigger(phi, activator):
    # predicate: HplPredicate
    # activator: str|None
    return TriggerEvent(EVENT_TRIGGER, phi, activator)


def _default_dict_of_lists():
    return defaultdict(list)

###############################################################################
# State Machine Builder
###############################################################################

class PatternBasedBuilder(object):
    def __init__(self, hpl_property):
        self.property_id = hpl_property.metadata.get('id')
        self.property_title = hpl_property.metadata.get('title')
        self.property_desc = hpl_property.metadata.get('description')
        self.property_text = str(hpl_property)
        self.class_name = 'PropertyMonitor'


###############################################################################
# Absence State Machine
###############################################################################

class AbsenceBuilder(PatternBasedBuilder):
    #initial_state: int
    #timeout: float
    #reentrant_scope: bool
    #pool_size: -1|0|int
    #on_msg:
    #    <topic>:
    #        <state>:
    #            - <event>

    def __init__(self, hpl_property):
        super(AbsenceBuilder, self).__init__(hpl_property)
        self._activator = None
        self.reentrant_scope = False
        self.timeout = hpl_property.pattern.max_time
        if self.timeout == INF:
            self.timeout = -1
        self.pool_size = 0
        self.on_msg = defaultdict(_default_dict_of_lists)
        if hpl_property.scope.is_global:
            self.initial_state = STATE_ACTIVE
        elif hpl_property.scope.is_after:
            self.initial_state = STATE_INACTIVE
            self.add_activator(hpl_property.scope.activator)
        elif hpl_property.scope.is_until:
            self.initial_state = STATE_ACTIVE
            self.add_terminator(hpl_property.scope.terminator)
        elif hpl_property.scope.is_after_until:
            self.initial_state = STATE_INACTIVE
            self.reentrant_scope = True
            self.add_activator(hpl_property.scope.activator)
            self.add_terminator(hpl_property.scope.terminator)
        else:
            raise ValueError('unknown scope: ' + str(hpl_property.scope))
        self.add_behaviour(hpl_property.pattern.behaviour)

    @property
    def has_safe_state(self):
        return (self.timeout >= 0 and self.timeout < INF
                and self.reentrant_scope)

    def add_activator(self, event):
        # must be called before all others
        # assuming only disjunctions or simple events
        if event.is_simple_event:
            self._activator = event.alias
            datum = new_activator(event.predicate)
            self.on_msg[event.topic][STATE_INACTIVE].append(datum)
        else:
            for e in event.simple_events():
                datum = new_activator(e.predicate)
                self.on_msg[e.topic][STATE_INACTIVE].append(datum)

    def add_terminator(self, event):
        # must be called before pattern events
        v = None if self.reentrant_scope else True
        for e in event.simple_events():
            alias = None
            if self._activator and e.contains_reference(self._activator):
                alias = self._activator
            datum = new_terminator(e.predicate, alias, v)
            states = self.on_msg[e.topic]
            states[STATE_ACTIVE].append(datum)
            if self.has_safe_state:
                states[STATE_SAFE].append(datum)

    def add_behaviour(self, event):
        for e in event.simple_events():
            alias = None
            if self._activator and e.contains_reference(self._activator):
                alias = self._activator
            datum = new_behaviour(e.predicate, alias, None)
            self.on_msg[e.topic][STATE_ACTIVE].append(datum)


class ExistenceBuilder(object):
    pass

class RequirementBuilder(object):
    pass

class ResponseBuilder(object):
    pass

class PreventionBuilder(object):
    pass
