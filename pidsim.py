import time

TICK_LENGTH = 0  # Delay (in milliseconds) between each tick
TICKS_PER_READING = 10  # How many ticks pass between sensor readings


class PidSimulator:
    INFINITE_LOOP_CUTOFF = 3000  # number of ticks before we stop automatically

    def __init__(self, tick_length=TICK_LENGTH, ticks_per_reading=TICKS_PER_READING, verbose=True):
        self.tick_length = tick_length
        self.ticks_per_reading = ticks_per_reading
        self.dt = self.ticks_per_reading
        self.ticks = 0
        self.running = False
        self.verbose = verbose

    def run(self):
        self.print("Running")
        self.running = True

        while self.running:
            self._tick()

            if self.ticks % self.ticks_per_reading == 0:
                sensor_value = self._read_sensor()
                self._act(sensor_value)

            time.sleep(self.tick_length / 1000)
            self.ticks += 1

        return self.ticks

    def _tick(self):
        if self.ticks > self.INFINITE_LOOP_CUTOFF:
            self.running = False
            self.print("Controller failed to converge within tolerances")

    def _read_sensor(self):
        pass

    def _act(self, sensor_value):
        pass

    def print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
