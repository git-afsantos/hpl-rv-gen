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
    #initial_state: int
    #timeout: float
    #reentrant_scope: bool
    #pool_size: -1|0|int
    #on_msg:
    #    <topic>:
    #        <state>:
    #            - <event>

    def __init__(self, hpl_property, s0):
        self.property_id = hpl_property.metadata.get('id')
        self.property_title = hpl_property.metadata.get('title')
        self.property_desc = hpl_property.metadata.get('description')
        self.property_text = str(hpl_property)
        self.class_name = 'PropertyMonitor'
        self._activator = None
        self._trigger = None
        self.reentrant_scope = False
        self.timeout = hpl_property.pattern.max_time
        if self.timeout == INF:
            self.timeout = -1
        event = hpl_property.scope.activator
        if event is not None and event.is_simple_event:
            self._activator = event.alias
        event = hpl_property.pattern.trigger
        if event is not None and event.is_simple_event:
            self._trigger = event.alias
        self.pool_size = self.calc_pool_size(hpl_property)
        self.on_msg = defaultdict(_default_dict_of_lists)
        if hpl_property.scope.is_global:
            self.initial_state = s0
        elif hpl_property.scope.is_after:
            self.initial_state = STATE_INACTIVE
            self.add_activator(hpl_property.scope.activator)
        elif hpl_property.scope.is_until:
            self.initial_state = s0
            self.add_terminator(hpl_property.scope.terminator)
        elif hpl_property.scope.is_after_until:
            self.initial_state = STATE_INACTIVE
            self.reentrant_scope = True
            self.add_activator(hpl_property.scope.activator)
            self.add_terminator(hpl_property.scope.terminator)
        else:
            raise ValueError('unknown scope: ' + str(hpl_property.scope))
        self.add_behaviour(hpl_property.pattern.behaviour)
        if hpl_property.pattern.trigger is not None:
            self.add_trigger(hpl_property.pattern.trigger)

    def add_activator(self, event):
        # must be called before all others
        # assuming only disjunctions or simple events
        for e in event.simple_events():
            datum = new_activator(e.predicate)
            self.on_msg[e.topic][STATE_INACTIVE].append(datum)

    def add_terminator(self, event):
        raise NotImplementedError()

    def add_trigger(self, event):
        raise NotImplementedError()

    def add_behaviour(self, event):
        raise NotImplementedError()

    def calc_pool_size(self, hpl_property):
        raise NotImplementedError()


###############################################################################
# Absence State Machine
###############################################################################

class AbsenceBuilder(PatternBasedBuilder):
    def __init__(self, hpl_property):
        super(AbsenceBuilder, self).__init__(hpl_property, STATE_ACTIVE)

    @property
    def has_safe_state(self):
        return (self.timeout >= 0 and self.timeout < INF
                and self.reentrant_scope)

    def calc_pool_size(self, hpl_property):
        return 0

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


###############################################################################
# Existence State Machine
###############################################################################

class ExistenceBuilder(PatternBasedBuilder):
    def __init__(self, hpl_property):
        super(ExistenceBuilder, self).__init__(hpl_property, STATE_ACTIVE)

    def calc_pool_size(self, hpl_property):
        return 0

    def add_terminator(self, event):
        # must be called before pattern events
        self.has_safe_state = True
        for e in event.simple_events():
            alias = None
            if self._activator and e.contains_reference(self._activator):
                alias = self._activator
            states = self.on_msg[e.topic]
            datum = new_terminator(e.predicate, alias, False)
            states[STATE_ACTIVE].append(datum)
            if self.reentrant_scope:
                datum = new_terminator(e.predicate, alias, None)
                states[STATE_SAFE].append(datum)

    def add_behaviour(self, event):
        for e in event.simple_events():
            alias = None
            if self._activator and e.contains_reference(self._activator):
                alias = self._activator
            datum = new_behaviour(e.predicate, alias, None)
            self.on_msg[e.topic][STATE_ACTIVE].append(datum)


###############################################################################
# Requirement State Machine
###############################################################################

class RequirementBuilder(PatternBasedBuilder):
    def __init__(self, hpl_property):
        self.has_trigger_refs = False
        b = hpl_property.pattern.behaviour
        for alias in hpl_property.pattern.trigger.aliases():
            if b.contains_reference(alias):
                self.has_trigger_refs = True
                break
        super(RequirementBuilder, self).__init__(hpl_property, STATE_ACTIVE)

    @property
    def has_safe_state(self):
        return self.timeout > 0 and not self.has_trigger_refs

    def calc_pool_size(self, hpl_property):
        if not self.has_trigger_refs:
            if self.timeout > 0:
                return 1
            else:
                return 0
        return -1

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
            activator = None
            if self._activator and e.contains_reference(self._activator):
                activator = self._activator
            trigger = None
            if self._trigger and e.contains_reference(self._trigger):
                trigger = self._trigger
            datum = new_behaviour(e.predicate, activator, trigger)
            self.on_msg[e.topic][STATE_ACTIVE].append(datum)

    def add_trigger(self, event):
        for e in event.simple_events():
            alias = None
            if self._activator and e.contains_reference(self._activator):
                alias = self._activator
            datum = new_trigger(e.predicate, alias)
            states = self.on_msg[e.topic]
            states[STATE_ACTIVE].append(datum)
            if self.has_safe_state:
                states[STATE_SAFE].append(datum)


###############################################################################
# Response State Machine
###############################################################################

class ResponseBuilder(PatternBasedBuilder):
    pass


###############################################################################
# Prevention State Machine
###############################################################################

class PreventionBuilder(PatternBasedBuilder):
    pass