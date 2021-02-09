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
    HPL_PROPERTY = r'''globally: /b as B { True } requires /a { (data < @B.data) }'''

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
                for rec in self._pool:
                    v_1 = rec.msg
                    if (v_1.data < msg.data):
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
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
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
    HPL_PROPERTY = r'''globally: /b as B { (data > 0) } requires /a { (data < @B.data) } within 0.1s'''

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
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                if (msg.data > 0):
                    for rec in self._pool:
                        v_1 = rec.msg
                        if (v_1.data < msg.data):
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
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                self._pool.append(MsgRecord('/a', stamp, msg))
                return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
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
    HPL_PROPERTY = r'''globally: /b as B { (x > 0) } requires /a { ((x < 0) and (y < @B.y)) }'''

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
                if (msg.x > 0):
                    for rec in self._pool:
                        v_1 = rec.msg
                        if (v_1.y < msg.y):
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
                if (msg.x < 0):
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
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
    HPL_PROPERTY = r'''globally: /b as B { (x > 0) } requires /a { (forall i in array: ((array[@i] > 0) and (array[@i] < @B.x))) } within 0.1s'''

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
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
        return True

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                if (msg.x > 0):
                    for rec in self._pool:
                        v_1 = rec.msg
                        if all((v_1.array[v_i] < msg.x) for v_i in range(len(v_1.array))):
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
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                if all((msg.array[v_i] > 0) for v_i in range(len(msg.array))):
                    self._pool.append(MsgRecord('/a', stamp, msg))
                    return True
        return False

    def _reset(self):
        self.witness = []
        self._pool = deque()
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
    HPL_PROPERTY = r'''after /p as P { True } until /q { (x > @P.x) }: /b as B { (x = @P.x) } requires (/a1 { (not ((a < 0) or (a > @B.b))) } or /a2 { (a in {0, @B.b}) }) within 0.1s'''

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
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
        return True

    def on_msg__a2(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                self._pool.append(MsgRecord('/a2', stamp, msg))
                return True
        return False

    def on_msg__a1(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                if (not (msg.a < 0)):
                    self._pool.append(MsgRecord('/a1', stamp, msg))
                    return True
        return False

    def on_msg__b(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator'
                v_P = self.witness[0].msg
                if (msg.x == v_P.x):
                    for rec in self._pool:
                        v_1 = rec.msg
                        if rec.topic == '/a2':
                            if (v_1.a in (0, msg.b)):
                                return True
                        if rec.topic == '/a1':
                            if (not (v_1.a > msg.b)):
                                return True
                    self.witness.append(MsgRecord('/b', stamp, msg))
                    self._state = -2
                    self.time_state = stamp
                    self.on_violation(stamp, self.witness)
                    return True
        return False

    def on_msg__q(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 2:
                assert len(self.witness) >= 1, 'missing activator'
                v_P = self.witness[0].msg
                if (msg.x > v_P.x):
                    self._pool = deque()
                    self.witness = []
                    self._state = 1
                    self.time_state = stamp
                    self.on_exit_scope(stamp)
                    return True
        return False

    def on_msg__p(self, msg, stamp):
        with self._lock:
            if self._state == 2:
                while self._pool and (stamp - self._pool[0].timestamp) >= 0.1:
                    self._pool.popleft()
            if self._state == 1:
                self.witness.append(MsgRecord('/p', stamp, msg))
                self._state = 2
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

    def _noop(self, *args):
        pass
