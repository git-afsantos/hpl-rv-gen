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
