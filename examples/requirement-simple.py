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
    HPL_PROPERTY = r'''globally: /b { True } requires /a { True }'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
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
    HPL_PROPERTY = r'''globally: /b { True } requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
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
    HPL_PROPERTY = r'''globally: /b { (data > 0) } requires /a { (data < 0) }'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/a', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
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
    HPL_PROPERTY = r'''globally: /b { (data > 0) } requires /a { (data < 0) } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))
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
    HPL_PROPERTY = r'''globally: (/b1 { (data > 0) } or /b2 { (data < 0) }) requires /a { True }'''

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

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
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
    HPL_PROPERTY = r'''globally: (/b1 { (data > 0) } or /b2 { (data < 0) }) requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b1', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
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
    HPL_PROPERTY = r'''globally: /b { True } requires (/a1 { (data > 0) } or /a2 { (data < 0) })'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/a1', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_success(stamp, self.witness)
                    return True
        return False

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/a2', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
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
    HPL_PROPERTY = r'''globally: /b { True } requires (/a1 { (data > 0) } or /a2 { (data < 0) }) within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a1', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a1', stamp, msg))
                    return True
        return False

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a2', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a2', stamp, msg))
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
    HPL_PROPERTY = r'''globally: /b { True } requires /b { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
                self._pool.append(MsgRecord('/b', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/b', stamp, msg))
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
    HPL_PROPERTY = r'''globally: /b { True } requires /b { (data > 0) } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/b', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/b', stamp, msg))
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
    HPL_PROPERTY = r'''globally: /b { (data > 0) } requires /b { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
                self._pool.append(MsgRecord('/b', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/b', stamp, msg))
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
    HPL_PROPERTY = r'''after /p { True }: /b { True } requires /a { True }'''

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
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
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
    HPL_PROPERTY = r'''after /p { True }: /b { True } requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
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
    HPL_PROPERTY = r'''after /p { (phi implies psi) }: /b { (data > 0) } requires /a { (data < 0) }'''

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
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/a', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_success(stamp, self.witness)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                if (not msg.phi or msg.psi):
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
    HPL_PROPERTY = r'''after /p { (phi iff psi) }: /b { (data > 0) } requires /a { (data < 0) } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                if (msg.phi is msg.psi):
                    self.witness.append(MsgRecord('/p', stamp, msg))
                    self._state = 2
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
    HPL_PROPERTY = r'''after /p { True }: (/b1 { (data > 0) } or /b2 { (data < 0) }) requires /a { True }'''

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

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b1', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
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
    HPL_PROPERTY = r'''after /p { True }: (/b1 { (data > 0) } or /b2 { (data < 0) }) requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/b1', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
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
    HPL_PROPERTY = r'''after /p { True }: /b { True } requires (/a1 { (data > 0) } or /a2 { (data < 0) })'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/a2': self.on_msg__a2,
            '/b': self.on_msg__b,
            '/a1': self.on_msg__a1,
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

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data < 0):
                    self.witness.append(MsgRecord('/a2', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_success(stamp, self.witness)
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if (msg.data > 0):
                    self.witness.append(MsgRecord('/a1', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_success(stamp, self.witness)
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
    HPL_PROPERTY = r'''after /p { True }: /b { True } requires (/a1 { (data > 0) } or /a2 { (data < 0) }) within 0.1s'''

    def __init__(self):
        self._lock = Lock()
        self._reset()
        self.on_enter_scope = self._noop
        self.on_exit_scope = self._noop
        self.on_violation = self._noop
        self.on_success = self._noop
        self._state = 0
        self.cb_map = {
            '/a2': self.on_msg__a2,
            '/b': self.on_msg__b,
            '/a1': self.on_msg__a1,
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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a2', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data < 0):
                    self._pool.append(MsgRecord('/a2', stamp, msg))
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a1', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if (msg.data > 0):
                    self._pool.append(MsgRecord('/a1', stamp, msg))
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
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
    HPL_PROPERTY = r'''after (/p1 { (x in {1, 2, 3}) } or /p2 { (y in ![0 to 10]!) }): /b { True } requires /a { True }'''

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
            '/p1': self.on_msg__p1,
            '/p2': self.on_msg__p2,
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

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__p1(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                if (msg.x in (1, 2, 3)):
                    self.witness.append(MsgRecord('/p1', stamp, msg))
                    self._state = 2
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def on_msg__p2(self, msg, stamp):
        with self._lock:
            if self._state == 1:
                if (msg.y in range(int(0)+1, int(10))):
                    self.witness.append(MsgRecord('/p2', stamp, msg))
                    self._state = 2
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
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
    HPL_PROPERTY = r'''after (/p1 { (x in {1, 2, 3}) } or /p2 { (y in ![0 to 10]!) }): /b { True } requires /a { True } within 0.1s'''

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
            '/p1': self.on_msg__p1,
            '/p2': self.on_msg__p2,
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
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def on_msg__p1(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                if (msg.x in (1, 2, 3)):
                    self.witness.append(MsgRecord('/p1', stamp, msg))
                    self._state = 2
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def on_msg__p2(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                if (msg.y in range(int(0)+1, int(10))):
                    self.witness.append(MsgRecord('/p2', stamp, msg))
                    self._state = 2
                    self.time_state = stamp
                    self.on_enter_scope(stamp)
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
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
    HPL_PROPERTY = r'''after /b { True }: /b { True } requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
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
    HPL_PROPERTY = r'''after /a { True }: /b { True } requires /a { True } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/a', stamp, msg))
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
    HPL_PROPERTY = r'''after /b { True }: /b { True } requires /b { True } within 0.1s'''

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
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = 2
                self.time_state = stamp
                self.on_enter_scope(stamp)
                return True
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
                self._pool.append(MsgRecord('/b', stamp, msg))
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                self._pool.append(MsgRecord('/b', stamp, msg))
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
    HPL_PROPERTY = r'''until /q { phi }: /b { psi } requires /a { omega }'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.psi:
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
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

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.omega:
                    self.witness.append(MsgRecord('/a', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
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
    HPL_PROPERTY = r'''until /q { phi }: /b { psi } requires /a { omega } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if msg.psi:
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if msg.phi:
                    self._pool.clear()
                    self.witness.append(MsgRecord('/q', stamp, msg))
                    self._state = -1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    self.on_success(stamp, self.witness)
                    return True
            if self._state == 3:
                if msg.phi:
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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if msg.omega:
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if msg.omega:
                    self._pool.append(MsgRecord('/a', stamp, msg))
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
    HPL_PROPERTY = r'''until /q { True }: (/b1 { phi } or /b2 { psi }) requires /a { True }'''

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
            '/q': self.on_msg__q,
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
        return True

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.psi:
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness.append(MsgRecord('/q', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.phi:
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
    HPL_PROPERTY = r'''until (/q1 { True } or /q2 { True }): /b { True } requires /a { True }'''

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
            '/q2': self.on_msg__q2,
            '/q1': self.on_msg__q1,
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

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__q2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness.append(MsgRecord('/q2', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__q1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness.append(MsgRecord('/q1', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
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
    HPL_PROPERTY = r'''until /b { True }: /b { True } requires /a { True }'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
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
    HPL_PROPERTY = r'''until /a { True }: /b { True } requires /a { True }'''

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

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                self.on_success(stamp, self.witness)
                return True
                self.witness.append(MsgRecord('/a', stamp, msg))
                self._state = -1
                self.time_state = stamp
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
    HPL_PROPERTY = r'''after /p { phi } until /q { psi }: /b { beta } requires /a { alpha }'''

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
            if self._state == 2:
                if msg.alpha:
                    # there is no pool to add this message to
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if msg.alpha:
                    # there is no pool to add this message to
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.beta:
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.psi:
                    # there is no record pool to clear
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
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
    HPL_PROPERTY = r'''after /p { phi } until /q { psi }: /b { beta } requires /a { alpha } within 0.1s'''

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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
        return True

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if msg.alpha:
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    self._state = 3
                    self.time_state = stamp
                    return True
            if self._state == 3:
                if msg.alpha:
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                assert not self._pool, 'unexpected trigger'
                if msg.beta:
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 2:
                if msg.psi:
                    self._pool.clear()
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
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
            if self._state == 3:
                assert len(self._pool) == 1, 'missing trigger event'
                rec = self._pool[0]
                if (stamp - rec.timestamp) >= 0.1:
                    self._pool.pop()
                    self._state = 2
                    self.time_state = stamp
            if self._state == 1:
                if msg.phi:
                    self.witness.append(MsgRecord('/p', stamp, msg))
                    self._state = 2
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
    HPL_PROPERTY = r'''after /p { True } until /q { True }: (/b1 { beta } or /b2 { beta }) requires /a { True }'''

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
        return True

    def on_msg__b1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.beta:
                    self.witness.append(MsgRecord('/b1', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__b2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                if msg.beta:
                    self.witness.append(MsgRecord('/b2', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no pool to add this message to
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                # there is no pool to add this message to
                return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
            if self._state == 3:
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
    HPL_PROPERTY = r'''after /p { True } until (/q1 { True } or /q2 { True }): /b { True } requires /a { True }'''

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
            '/q2': self.on_msg__q2,
            '/q1': self.on_msg__q1,
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
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no pool to add this message to
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                # there is no pool to add this message to
                return True
        return False

    def on_msg__q2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
            if self._state == 3:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
        return False

    def on_msg__q1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
            if self._state == 3:
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
    HPL_PROPERTY = r'''after (/p { True } or /q { True }) until /q { True }: /b { True } requires /a { True }'''

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
            if self._state == 2:
                # there is no pool to add this message to
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                # there is no pool to add this message to
                return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
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
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
            if self._state == 3:
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
    HPL_PROPERTY = r'''after /b { True } until /q { True }: /b { True } requires /a { True }'''

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
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
            if self._state == 3:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no pool to add this message to
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                # there is no pool to add this message to
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
    HPL_PROPERTY = r'''after /p { True } until /a { True }: /b { True } requires /a { True }'''

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
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                self.witness.append(MsgRecord('/b', stamp, msg))
                self._state = -2
                self.time_state = stamp
                self.on_violation(stamp, self.witness)
                return True
        return False

    def on_msg__a(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
                # there is no pool to add this message to
                self._state = 3
                self.time_state = stamp
                return True
            if self._state == 3:
                # there is no record pool to clear
                self.witness = []
                self._state = 1
                self.time_state = stamp
                self.on_exit_scope(stamp)
                return True
                # there is no pool to add this message to
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
