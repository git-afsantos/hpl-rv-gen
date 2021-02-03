###############################################################################
# Building a State Machine
###############################################################################

class StateBuilder(object):
    def __init__(self, key, name=None):
        self.key = key
        self.name = name or ('State' + str(key))
        self.tentative_verdict = True
        self.on_enter = EnterStateHandler()
        #self.on_exit = ExitStateHandler()
        self.on_msg = defaultdict(list) # topic -> [MsgEventHandler]
        self.on_timer = TimerUpdateHandler()

    def make_msg_handler(self, topic):
        handler = MsgEventHandler()
        self.on_msg[topic].append(handler)
        return handler

    def via_activator(self, p, to_state):
        cb = self.make_msg_handler(p.topic)
        cb.predicate = p.predicate
        cb.stores_msg = True
        cb.store_alias = p.alias
        cb.enters_scope = True
        cb.jumps_to = to_state

    def via_terminator(self, q, to_state):
        cb = self.make_msg_handler(q.topic)
        cb.predicate = q.predicate
        cb.exits_scope = True
        if to_state == STATE_TRUE or to_state == STATE_FALSE:
            cb.stores_msg = True
            cb.store_alias = q.alias
        else:
            assert to_state == STATE_INACTIVE

    def via_good_behaviour(self, b, to_state):
        # used with Existence
        assert to_state == STATE_TRUE or to_state > STATE_INACTIVE
        cb = self.make_msg_handler(b.topic)
        cb.predicate = b.predicate
        cb.jumps_to = to_state
        cb.stores_msg = True
        cb.store_alias = b.alias

    def via_bad_behaviour_to_false(self, b):
        # used with Absence
        to_state = STATE_FALSE
        cb = self.make_msg_handler(b.topic)
        cb.predicate = b.predicate
        cb.stores_msg = True
        cb.store_alias = b.alias
        cb.jumps_to = to_state

    def via_missing_trigger_to_false(self, b, a):
        # used with Precedence
        to_state = STATE_FALSE
        cb = self.make_msg_handler(b.topic)
        cb.predicate = b.predicate
        cb.stores_msg = True
        cb.store_alias = b.alias
        cb.jumps_to = to_state
        # FIXME jump if predicate not matched
        if a.alias and b.contains_reference(a.alias):
            cb.loads_pool = True
            cb.pool_alias = a.alias
        elif timeout:
            pass # FIXME
        else flag:
            pass # FIXME

    def via_good_response(self, b, to_state, a):
        # used with Response
        assert to_state == STATE_TRUE or to_state > STATE_INACTIVE
        cb = self.make_msg_handler(b.topic)
        cb.predicate = b.predicate
        cb.jumps_to = to_state
        cb.jump_if_pool_empty = True
        if a.alias and b.contains_reference(a.alias):
            cb.loads_pool = True
            cb.pool_alias = a.alias
            cb.pool_matches_all = True
            cb.pool_drops_matched = True
        elif timeout:
            pass # FIXME
        else:
            pass # FIXME
        if to_state == STATE_TRUE:
            cb.stores_msg = True
            cb.store_alias = b.alias

    def via_bad_response_to_false(self, b, a):
        # used with Prevention
        to_state = STATE_FALSE
        cb = self.make_msg_handler(b.topic)
        cb.predicate = b.predicate
        cb.stores_msg = True
        cb.store_alias = b.alias
        cb.jumps_to = to_state
            if a.alias and b.contains_reference(a.alias):
                cb.loads_pool = True
                cb.pool_alias = a.alias
            elif timeout:
                pass # FIXME
            else:
                pass # FIXME

    def via_timeout(self, t, to_state):
        self.on_timer.state_duration = t
        self.on_timer.jumps_to = to_state


class EnterStateHandler(object):
    def __init__(self):
        self.empties_records = False
        self.empties_pool = False

    @property
    def skippable(self):
        # is the call to `enter()` skippable
        return not self.empties_records and not self.empties_pool

#class ExitStateHandler(object):
#    pass


class TimerUpdateHandler(object):
    def __init__(self):
        self.pool_duration = -1 # how long things last in pool; -1 means no drop
        self.state_duration = -1 # state transition via timeout
        self.empties_records = False # if state transition happens
        self.empties_pool = False
        self.jumps_to = 0
        self.jump_if_pool_empty = False
        self.jump_if_pool_not_empty = False

    @property
    def is_noop(self):
        # is the call to `_update()` a noop
        return self.pool_duration < 0 and self.state_duration < 0

class MsgEventHandler(object):
    def __init__(self):
        self.predicate = HplVacuousTruth()
        self.loads_pool = False
        self.pool_alias = None
        self.pool_matches_all = False
        self.pool_drops_matched = False
        self.empties_records = False
        self.empties_pool = False
        self.stores_msg = False
        self.stores_in_pool = False
        self.store_alias = None
        self.enters_scope = False
        self.exits_scope = False
        self.jumps_to = 0
        self.jump_if_pool_empty = False
        self.jump_if_pool_not_empty = False


class LaunchEventHandler(object):
    def __init__(self):
        self.jumps_to = STATE_OFF

    @property
    def enters_scope(self):
        return self.jumps_to > STATE_INACTIVE


# class ShutdownEventHandler(object):
    # def __init__(self):
        # self.verdict = True


class StateMachineMonitor(object):
    def __init__(self):
        self.p_id = None
        self.p_title = None
        self.p_desc = None
        self.p_text = None
        self.class_name = None
        self.on_launch = LaunchEventHandler()
        #self.on_shutdown = ShutdownEventHandler()
        self.topics = set()
        self.aliases = set()
        self.states = {} # int -> StateBuilder

    def add_state(self, key, name=None):
        if key in self.states:
            raise ValueError('state key already in use: ' + str(key))
        state = StateBuilder(key, name=name)
        self.states[key] = state
        return state

    def via_activator(self, event, from_state, to_state):
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        if isinstance(to_state, StateBuilder):
            to_state = self.states.setdefault(to_state.key, to_state).key
        elif to_state not in self.states:
            raise KeyError(to_state)
        self.topics.add(event.topic)
        if event.alias:
            self.aliases.add(event.alias)
        s.via_activator(event, to_state)

    def via_terminator(self, event, from_state, to_state):
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        if isinstance(to_state, StateBuilder):
            to_state = self.states.setdefault(to_state.key, to_state).key
        elif to_state not in self.states:
            raise KeyError(to_state)
        self.topics.add(event.topic)
        if event.alias:
            self.aliases.add(event.alias)
        s.via_terminator(event, to_state)

    def via_good_behaviour(self, event, from_state, to_state):
        # used with Existence
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        if isinstance(to_state, StateBuilder):
            to_state = self.states.setdefault(to_state.key, to_state).key
        elif to_state not in self.states:
            raise KeyError(to_state)
        self.topics.add(event.topic)
        if event.alias:
            self.aliases.add(event.alias)
        s.via_good_behaviour(event, to_state)

    def via_bad_behaviour_to_false(self, event, from_state):
        # used with Absence
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        self.topics.add(event.topic)
        if event.alias:
            self.aliases.add(event.alias)
        s.via_bad_behaviour_to_false(event)

    def via_missing_trigger_to_false(self, event, trigger, from_state):
        # used with Precedence
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        self.topics.add(event.topic)
        self.topics.add(trigger.topic)
        if event.alias:
            self.aliases.add(event.alias)
        if trigger.alias:
            self.aliases.add(trigger.alias)
        s.via_missing_trigger_to_false(event, trigger)

    def via_good_response(self, event, trigger, from_state, to_state):
        # used with Response
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        if isinstance(to_state, StateBuilder):
            to_state = self.states.setdefault(to_state.key, to_state).key
        elif to_state not in self.states:
            raise KeyError(to_state)
        self.topics.add(event.topic)
        self.topics.add(trigger.topic)
        if event.alias:
            self.aliases.add(event.alias)
        if trigger.alias:
            self.aliases.add(trigger.alias)
        s.via_good_response(event, trigger, to_state)

    def via_bad_response_to_false(self, event, trigger, from_state):
        # used with Prevention
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        self.topics.add(event.topic)
        self.topics.add(trigger.topic)
        if event.alias:
            self.aliases.add(event.alias)
        if trigger.alias:
            self.aliases.add(trigger.alias)
        s.via_bad_response_to_false(event, trigger)

    def via_timeout(self, t, from_state, to_state):
        if isinstance(from_state, StateBuilder):
            s = from_state
            self.states[from_state.key] = from_state
        else:
            s = self.states[from_state]
        if isinstance(to_state, StateBuilder):
            to_state = self.states.setdefault(to_state.key, to_state).key
        elif to_state not in self.states:
            raise KeyError(to_state)
        s.via_timeout(t, to_state)




def build_from_property(hpl_property):
    if hpl_property.pattern.is_absence:
        return AbsenceBuilder(hpl_property)
    if hpl_property.pattern.is_existence:
        return ExistenceBuilder(hpl_property)
    if hpl_property.pattern.is_requirement:
        return RequirementBuilder(hpl_property)
    if hpl_property.pattern.is_response:
        return ResponseBuilder(hpl_property)
    if hpl_property.pattern.is_prevention:
        return PreventionBuilder(hpl_property)
    assert False, 'unknown pattern'


class StateMachineBuilder(object):
    def __init__(self, hpl_property, s0):
        # s0: first state after inactive; first 'active' state within scope
        self.sm = StateMachineMonitor()

        # metadata
        self.sm.p_id = hpl_property.metadata.get('id')
        self.sm.p_title = hpl_property.metadata.get('title')
        self.sm.p_desc = hpl_property.metadata.get('description')
        self.sm.p_text = str(hpl_property)

        # main parts and events
        self.scope = hpl_property.scope
        self.pattern = hpl_property.pattern
        self.p = hpl_property.scope.activator
        self.q = hpl_property.scope.terminator
        self.a = hpl_property.pattern.trigger
        self.b = hpl_property.pattern.behaviour

        # default states
        self.active = self.sm.add_state(STATE_ACTIVE, name='Active')
        self.inactive = None
        self.safe = None

        # state initialization
        if self.p is None:
            assert self.scope.is_until or self.scope.is_global
            self.sm.on_launch.jumps_to = s0
        else:
            assert self.scope.is_after or self.scope.is_after_until
            self.inactive = self.sm.add_state(STATE_INACTIVE, name='Inactive')
            self.inactive.on_enter.empties_records = True
            self.inactive.tentative_verdict = True
            self.sm.on_launch.jumps_to = STATE_INACTIVE
            self.sm.via_activator(self.p, STATE_INACTIVE, s0)



class AbsenceBuilder(StateMachineBuilder):
    def __init__(self, hpl_property):
        assert hpl_property.is_absence
        super(AbsenceBuilder, self).__init__(hpl_property, STATE_ACTIVE)
        self._check_timeout()
        self._build_active_state()

    def _check_timeout(self):
        t = self.pattern.max_time
        if t < INF:
            if self.scope.is_after_until:
                assert self.q is not None
                assert self.inactive is not None
                assert self.inactive.on_enter.empties_records
                self.safe = self.sm.add_state(STATE_SAFE, name='Safe')
                self.safe.tentative_verdict = True
                self.sm.via_terminator(self.q, STATE_SAFE, STATE_INACTIVE)
                self.sm.via_timeout(t, STATE_ACTIVE, STATE_SAFE)
            else:
                self.sm.via_timeout(t, STATE_ACTIVE, STATE_TRUE)

    def _build_active_state(self):
        self.active.tentative_verdict = True
        self.sm.via_bad_behaviour_to_false(self.b, STATE_ACTIVE)
        if self.inactive is None:
            self.sm.via_terminator(self.q, STATE_ACTIVE, STATE_TRUE)
        else:
            self.sm.via_terminator(self.q, STATE_ACTIVE, STATE_INACTIVE)


###############################################################################
# Monitor Template
###############################################################################

class Memory(object):
    def __init__(self):
        self.records = []
        self.pools = [deque()] * n
        self.msg_A = None
        self.msg_B = None
        self.msg_C = None

    def iterate(self):
        self.msg_A = self.records[0]
        for i0 in range(len(self.pools[0])):
            self.msg_B = self.pools[0][i0]
            for i1 in range(len(self.pools[1])):
                self.msg_C = self.pools[1][i1]
                yield self


class Monitor(object):
    def __init__(self):
        self.records = []
        self._s0 = StateHandler0()
        self._st = StateHandlerT()
        self._sf = StateHandlerF()
        self._s1 = StateHandler1(1, self.records)
        self._s2 = StateHandler2(2, self.records)
        self._s3 = StateHandler3(3, self.records)
        self._state = self._s0

    def on_launch(self, stamp):
        self._state = self._s1
        self._state.enter(stamp, self._s0)

    def on_timer(self, stamp):
        self._state.update(stamp)

    def on_msg_topic(self, msg, stamp):
        new_state = self._state.on_msg_topic(msg, stamp)
        if new_state:
            self._state.exit()
            prev_state = self._state
            self._state = new_state
            new_state.enter(stamp, prev_state)

class StateHandler(object):
    def __init__(self, number, records):
        self.number = number
        self.records = records
        self.temp = []
        self.time_enter = -1
        self.min_time = -1
        self.max_time = -1

    def enter(self, stamp, prev_state):
        self.min_time = stamp + DELAY
        self.max_time = stamp + DURATION
