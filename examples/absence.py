class P1Monitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'p1'
    PROP_TITLE = '''"My First Property"'''
    PROP_DESC = '''"This is a test property to be transformed into a monitor."'''
    HPL_PROPERTY = r'''globally: no /ns/topic { (data > 0) }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/ns/topic': self.on_msg__ns_topic,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 2
            self.time_state = stamp
            self.on_enter_scope(stamp)
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        return True

    def on_msg__ns_topic(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/ns/topic', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''globally: no /ns/topic { (data > 0) } within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/ns/topic': self.on_msg__ns_topic,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 2
            self.time_state = stamp
            self.on_enter_scope(stamp)
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
        return True

    def on_msg__ns_topic(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/ns/topic', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after /p { True }: no /b { (data > 0) } within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/p': self.on_msg__p,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after /p as P { True }: no /b { (data > @P.data) }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/p': self.on_msg__p,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator'
                v_P = self.witness[0].msg
                if (msg.data > v_P.data):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''until /q { phi }: no /b { (data > 0) } within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/q': self.on_msg__q,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 2
            self.time_state = stamp
            self.on_enter_scope(stamp)
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if msg.phi:
                    # there is no record pool to clear
                    self.witness.append(MsgRecord('/q', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    self.on_success(stamp, self.witness)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after /p as P { True } until /q { (phi and (not @P.psi)) }: no /b { (forall i in array: (array[@i] > 0)) }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/q': self.on_msg__q,
            '/p': self.on_msg__p,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if all((msg.array[v_i] > 0) for v_i in range(len(msg.array))):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                if (msg.phi and (not v_P.psi)):
                    # there is no record pool to clear
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after /p as P { True } until /q { (phi and (not @P.psi)) }: no /b { (exists i in [1 to 4]: (array[@i] > 0)) } within 1.0s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/q': self.on_msg__q,
            '/p': self.on_msg__p,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 1.0:
                self._state = 3
                self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 1.0:
                self._state = 3
                self.time_state = stamp
            if self._state == 2:
                if any((msg.array[v_i] > 0) for v_i in range(int(1), int(4)+1)):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 1.0:
                self._state = 3
                self.time_state = stamp
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                if (msg.phi and (not v_P.psi)):
                    # there is no record pool to clear
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
            if self._state == 3:
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                if (msg.phi and (not v_P.psi)):
                    # there is no record pool to clear
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 1.0:
                self._state = 3
                self.time_state = stamp
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''globally: no (/b1 { (data > 0) } or /b2 { (data < 0) }) within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b2': self.on_msg__b2,
            '/b1': self.on_msg__b1,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 2
            self.time_state = stamp
            self.on_enter_scope(stamp)
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
        return True

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2 and (stamp - self.time_state) >= 0.1:
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b1', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after /b { True }: no /b { ((3 * (data ** 2)) > 0) }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
            if self._state == 2:
                if ((3 * (msg.data ** 2)) > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        'witness',        # MsgRecord list of observed events
        'on_enter_scope', # callback upon entering the scope
        'on_exit_scope',  # callback upon exiting the scope
        'on_violation',   # callback upon verdict of False
        'on_success',     # callback upon verdict of True
        'time_launch',    # when was the monitor launched
        'time_shutdown',  # when was the monitor shutdown
        'time_state',     # when did the last state transition occur
        'cb_map',         # mapping of topic names to callback functions
    )

    PROP_ID = 'None'
    PROP_TITLE = '''None'''
    PROP_DESC = '''None'''
    HPL_PROPERTY = r'''after (/p { True } or (/q { True } or /b { True })): no /b { (data in {1, 2, 3}) }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b': self.on_msg__b,
            '/q': self.on_msg__q,
            '/p': self.on_msg__p,
        }

    @property
    def verdict(self):
        with self._lock:
            if self._state == -1:
                return True
            if self._state == -2:
                return False
        return None

    def on_launch(self, stamp):
        with self._lock:
            if self._state != 0:
                raise RuntimeError('monitor is already turned on')
            self._reset()
            self.time_launch = stamp
            self._state = 1
            self.time_state = stamp
        return True

    def on_shutdown(self, stamp):
        with self._lock:
            if self._state == 0:
                raise RuntimeError('monitor is already turned off')
            self.time_shutdown = stamp
            self._state = 0
            self.time_state = stamp
        return True

    def on_timer(self, stamp):
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
            if self._state == 2:
                if (msg.data in (1, 2, 3)):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/q', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass
