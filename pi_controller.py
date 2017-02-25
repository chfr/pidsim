from collections import defaultdict

from pidsim import PidSimulator
from utils import almost_equal, frange, fuzz_factor


class PIController(PidSimulator):
    PROPORTIONAL_GAIN = 0.01
    INTEGRAL_GAIN = 0.01
    STEADY_STATE_THRESHOLD = 50

    def __init__(self, proportional_gain=0.01, integral_gain=0.01, *args, **kwargs):
        super(PIController, self).__init__(*args, **kwargs)
        self.PROPORTIONAL_GAIN = proportional_gain
        self.INTEGRAL_GAIN = integral_gain

        self.integral = 0
        self.temperature = 20
        self.target_temperature = 100
        self.temperature_delta = 0.0

        self.steady_state_ticks = 0

    def _tick(self):
        super(PIController, self)._tick()
        self.temperature += self.temperature_delta * fuzz_factor()

    def _read_sensor(self):
        super(PIController, self)._read_sensor()

        reading = self.temperature
        self.print("[{:>5}]Sensor returns {}".format(self.ticks, round(reading, 2)), end="")

        return reading

    def _act(self, sensor_value):
        super(PIController, self)._act(sensor_value)

        error = (self.target_temperature - self.temperature)
        self.print(" (error: {})".format(round(error, 5)))

        if almost_equal(error, 0.0, decimals=1):
            self.steady_state_ticks += 1
            if self.steady_state_ticks >= self.STEADY_STATE_THRESHOLD:
                self.running = False
                self.ticks -= self.STEADY_STATE_THRESHOLD  # hack to make run() return the right val
                self.print("Controller reached steady state in {} ticks".format(self.ticks))

        else:
            self.steady_state_ticks = 0

        self.integral += error / self.dt
        self.print("Integral: {}".format(round(self.integral, 5)))

        output = self.PROPORTIONAL_GAIN * error + self.INTEGRAL_GAIN * self.integral

        self.temperature_delta = output


if __name__ == "__main__":
    # sim = PIController(0.01, 0.01)
    # sim.run()

    results = defaultdict(dict)

    pg_args = (0.0, 1.0, 0.05)
    ig_args = (-1.0, 1.0, 0.1)

    total_sims = ((pg_args[1] - pg_args[0]) / pg_args[2]) * ((ig_args[1] - ig_args[0]) / ig_args[2])

    print("Doing {} simulations...".format(total_sims))
    sims = 0
    for proportional_gain in frange(*pg_args):
        for integral_gain in frange(*ig_args):
            sim = PIController(proportional_gain, integral_gain, verbose=False)
            results[proportional_gain][integral_gain] = sim.run()
            sims += 1
            if sims % 100 == 0:
                print("Done {} of {} ({} %)".format(sims, total_sims, round(100 * sims / total_sims, 0)))

    min_ticks = 1E6
    min_pg = 0
    min_ig = 0
    for proportional_gain in results:
        for integral_gain in results[proportional_gain]:
            ticks = results[proportional_gain][integral_gain]
            if ticks < min_ticks:
                min_ticks = ticks
                min_pg = proportional_gain
                min_ig = integral_gain

    print("Winner: ({:f}, {:f}) at {} ticks".format(min_pg, min_ig, min_ticks))
