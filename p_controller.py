import operator

from pidsim import PidSimulator
from utils import almost_equal, fuzz_factor, frange


class PController(PidSimulator):
    PROPORTIONAL_GAIN = 0.01
    STEADY_STATE_THRESHOLD = 50

    def __init__(self, gain=0.01, *args, **kwargs):
        super(PController, self).__init__(*args, **kwargs)
        self.PROPORTIONAL_GAIN = gain

        self.temperature = 20
        self.target_temperature = 25
        self.temperature_delta = 0.0

        self.steady_state_ticks = 0

    def _tick(self):
        super(PController, self)._tick()
        self.temperature += self.temperature_delta * fuzz_factor()

    def _read_sensor(self):
        super(PController, self)._read_sensor()

        reading = self.temperature
        self.print("[{:>5}]Sensor returns {}".format(self.ticks, round(reading, 2)), end="")

        return reading

    def _act(self, sensor_value):
        super(PController, self)._act(sensor_value)

        error = (self.target_temperature - self.temperature)
        self.print(" (error: {})".format(round(error, 5)))

        if almost_equal(error, 0.0, decimals=2):
            self.steady_state_ticks += 1
            if self.steady_state_ticks >= self.STEADY_STATE_THRESHOLD:
                self.running = False
                self.ticks -= self.STEADY_STATE_THRESHOLD  # hack to make run() return the right val
                self.print("Controller reached steady state in {} ticks".format(self.ticks))
        else:
            self.steady_state_ticks = 0

        output = error * self.PROPORTIONAL_GAIN

        self.temperature_delta = output


if __name__ == "__main__":
    # sim = PController(0.01)
    # sim.run()

    results = {}
    start = 0.001
    step = 0.01
    stop = 0.999

    for gain in frange(start, stop, step):
        sim = PController(gain, verbose=False)
        results[gain] = sim.run()

    print("{:<10}|{:>8}".format("Gain", "Ticks"))
    for gain, ticks in sorted(results.items(), key=operator.itemgetter(0)):
        print("{:<10f}|{:>8}".format(gain, ticks))

    gain, ticks = min(results.items(), key=operator.itemgetter(1))
    print("Winner: {:f} at {} ticks".format(gain, ticks))
