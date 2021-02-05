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
                assert not self._pool, 'unexpected trigger'
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
                assert not self._pool, 'unexpected trigger'
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
