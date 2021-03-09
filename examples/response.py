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
    HPL_PROPERTY = r'''globally: /a { True } causes /b { True }'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # all stimuli have their response
                # there is no record pool to clear
                self._state = 3
                self.time_state = stamp
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                self.witness.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
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
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a { True } causes /b { True } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # all stimuli have their response
                self._pool.clear()
                self._state = 3
                self.time_state = stamp
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
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
    HPL_PROPERTY = r'''globally: /a { (data > 0) } causes /b { (data < 0) }'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    # all stimuli have their response
                    # there is no record pool to clear
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
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
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a { (data > 0) } causes /b { (data < 0) } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (msg.data < 0):
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: (/a1 { (data > 0) } or /a2 { (data < 0) }) causes /b { True } within 0.1s'''

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
            '/a1': self.on_msg__a1,
            '/a2': self.on_msg__a2,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # all stimuli have their response
                self._pool.clear()
                self._state = 3
                self.time_state = stamp
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a1', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a2', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a { True } causes (/b1 { (data > 0) } or /b2 { (data < 0) }) within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (msg.data < 0):
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (msg.data > 0):
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''after /p { True }: /a { True } causes /b { True } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # all stimuli have their response
                self._pool.clear()
                self._state = 3
                self.time_state = stamp
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 3
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''after /p { phi }: /a { (data > 0) } causes /b { (data < 0) } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (msg.data < 0):
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 1:
                if msg.phi:
                    self.witness.append(MsgRecord('/p', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''until /q { True }: /a { phi } causes /b { psi } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if msg.psi:
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                self.witness.extend(self._pool)
                self._pool.clear()
                self.witness.append(MsgRecord('/q', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_violation(stamp, self.witness)
                return True
            if self._state == 3:
                self._pool.clear()
                self.witness.append(MsgRecord('/q', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if msg.phi:
                    self._pool.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''until /b { True }: /a { True } causes /b { True } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                self.witness.extend(self._pool)
                self._pool.clear()
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_violation(stamp, self.witness)
                return True
                assert len(self._pool) >= 1, 'missing trigger event'
                # all stimuli have their response
                self._pool.clear()
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.clear()
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''until /a { True }: /a { True } causes /b { True } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # all stimuli have their response
                self._pool.clear()
                self._state = 3
                self.time_state = stamp
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                self.witness.extend(self._pool)
                self._pool.clear()
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_violation(stamp, self.witness)
                return True
                return False # nothing to do

            if self._state == 3:
                self._pool.clear()
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
                self._pool.append(MsgRecord('/a', stamp, msg))

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
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
    HPL_PROPERTY = r'''after /p { phi } until /q { psi }: /a { alpha } causes /b { beta }'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/a': self.on_msg__a,
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

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                if msg.alpha:
                    self.witness.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.beta:
                    # all stimuli have their response
                    # there is no record pool to clear
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.psi:
                    # there is no record pool to clear
                    self.witness.append(MsgRecord('/q', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    self.on_violation(stamp, self.witness)
                    return True
            if self._state == 3:
                if msg.psi:
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
                if msg.phi:
                    self.witness.append(MsgRecord('/p', stamp, msg))
                    self._state = 3
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
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''after /p { phi } until /q { psi }: /a { alpha } causes /b { beta } within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/a': self.on_msg__a,
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                return False # nothing to do

            if self._state == 3:
                if msg.alpha:
                    self._pool.append(MsgRecord('/a', stamp, msg))

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if msg.beta:
                    # all stimuli have their response
                    self._pool.clear()
                    self._state = 3
                    self.time_state = stamp
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                if msg.psi:
                    self.witness.extend(self._pool)
                    self._pool.clear()
                    self.witness.append(MsgRecord('/q', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    self.on_violation(stamp, self.witness)
                    return True
            if self._state == 3:
                if msg.psi:
                    self._pool.clear()
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 1:
                if msg.phi:
                    self.witness.append(MsgRecord('/p', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque((), 1)
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1


    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a as A { True } causes /b { (x < @A.x) }'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.x < v_A.x)):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                rec = MsgRecord('/a', stamp, msg)
                self._pool_insert(rec)
                return True
            if self._state == 3:
                rec = MsgRecord('/a', stamp, msg)
                self._pool_insert(rec)

                self._state = 2
                self.time_state = stamp
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1

    def _pool_insert(self, rec):
        # this method is only needed to ensure Python 2.7 compatibility
        if not self._pool:
            return self._pool.append(rec)
        stamp = rec.timestamp
        if len(self._pool) == 1:
            if stamp >= self._pool[0].timestamp:
                return self._pool.append(rec)
            return self._pool.appendleft(rec)
        for i in range(len(self._pool), 0, -1):
            if stamp >= self._pool[i-1].timestamp:
                try:
                    self._pool.insert(i, rec) # Python >= 3.5
                except AttributeError as e:
                    tmp = [self._pool.pop() for j in range(i, len(self._pool))]
                    self._pool.append(rec)
                    self._pool.extend(reversed(tmp))
                break
        else:
            self._pool.appendleft(rec)

    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a as A { (x > 0) } causes /b { (x < @A.x) } within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.x < v_A.x)):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                if (msg.x > 0):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)
                    return True
            if self._state == 3:
                if (msg.x > 0):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1

    def _pool_insert(self, rec):
        # this method is only needed to ensure Python 2.7 compatibility
        if not self._pool:
            return self._pool.append(rec)
        stamp = rec.timestamp
        if len(self._pool) == 1:
            if stamp >= self._pool[0].timestamp:
                return self._pool.append(rec)
            return self._pool.appendleft(rec)
        for i in range(len(self._pool), 0, -1):
            if stamp >= self._pool[i-1].timestamp:
                try:
                    self._pool.insert(i, rec) # Python >= 3.5
                except AttributeError as e:
                    tmp = [self._pool.pop() for j in range(i, len(self._pool))]
                    self._pool.append(rec)
                    self._pool.extend(reversed(tmp))
                break
        else:
            self._pool.appendleft(rec)

    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''globally: /a as A { (x > 0) } causes (/b1 { (x < @A.x) } or /b2 { (y < @A.y) }) within 0.1s'''

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
            '/a': self.on_msg__a,
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
            self._state = 3
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.y < v_A.y)):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                if (msg.x > 0):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)
                    return True
            if self._state == 3:
                if (msg.x > 0):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.x < v_A.x)):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1

    def _pool_insert(self, rec):
        # this method is only needed to ensure Python 2.7 compatibility
        if not self._pool:
            return self._pool.append(rec)
        stamp = rec.timestamp
        if len(self._pool) == 1:
            if stamp >= self._pool[0].timestamp:
                return self._pool.append(rec)
            return self._pool.appendleft(rec)
        for i in range(len(self._pool), 0, -1):
            if stamp >= self._pool[i-1].timestamp:
                try:
                    self._pool.insert(i, rec) # Python >= 3.5
                except AttributeError as e:
                    tmp = [self._pool.pop() for j in range(i, len(self._pool))]
                    self._pool.append(rec)
                    self._pool.extend(reversed(tmp))
                break
        else:
            self._pool.appendleft(rec)

    def _noop(self, *args):
        pass

class PropertyMonitor(object):
    __slots__ = (
        '_lock',          # concurrency control
        '_state',         # currently active state
        '_pool',          # MsgRecord deque to hold temporary records
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
    HPL_PROPERTY = r'''after /p as P { True } until /q { (x > @P.x) }: /a as A { (x = @P.x) } causes (/b1 { (x < (@A.x + @P.x)) } or /b2 { (x in {@P.x, @A.x}) }) within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/b1': self.on_msg__b1,
            '/b2': self.on_msg__b2,
            '/a': self.on_msg__a,
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
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
        return True

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.x < (v_A.x + v_P.x))):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                n = len(self._pool)
                pool = deque()
                while self._pool:
                    rec = self._pool.popleft()
                    v_A = rec.msg
                    if not ((msg.x in (v_P.x, v_A.x))):
                        pool.append(rec)
                self._pool = pool
                if not pool:
                    self._state = 3
                    self.time_state = stamp
                    return True
                if len(self._pool) != n:
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator'
                v_P = self.witness[0].msg
                if (msg.x == v_P.x):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)
                    return True
            if self._state == 3:
                assert len(self.witness) >= 1, 'missing activator'
                v_P = self.witness[0].msg
                if (msg.x == v_P.x):
                    rec = MsgRecord('/a', stamp, msg)
                    self._pool_insert(rec)

                    self._state = 2
                    self.time_state = stamp
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                if (msg.x > v_P.x):
                    self.witness.extend(self._pool)
                    self._pool.clear()
                    self.witness.append(MsgRecord('/q', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    self.on_violation(stamp, self.witness)
                    return True
            if self._state == 3:
                assert len(self.witness) >= 1, 'missing activator event'
                v_P = self.witness[0].msg
                if (msg.x > v_P.x):
                    self._pool.clear()
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                assert len(self._pool) >= 1, 'missing trigger event'
                # pool is sorted, it suffices to read the first value
                if (stamp - self._pool[0].timestamp) >= 0.1:
                    self.witness.append(self._pool.popleft())
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 3
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
        self.time_launch = -1
        self.time_shutdown = -1
        self.time_state = -1

    def _pool_insert(self, rec):
        # this method is only needed to ensure Python 2.7 compatibility
        if not self._pool:
            return self._pool.append(rec)
        stamp = rec.timestamp
        if len(self._pool) == 1:
            if stamp >= self._pool[0].timestamp:
                return self._pool.append(rec)
            return self._pool.appendleft(rec)
        for i in range(len(self._pool), 0, -1):
            if stamp >= self._pool[i-1].timestamp:
                try:
                    self._pool.insert(i, rec) # Python >= 3.5
                except AttributeError as e:
                    tmp = [self._pool.pop() for j in range(i, len(self._pool))]
                    self._pool.append(rec)
                    self._pool.extend(reversed(tmp))
                break
        else:
            self._pool.appendleft(rec)

    def _noop(self, *args):
        pass
