class PID(object):
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_int = 0
        self.error_prev = None

    def control(self, error):
        self.error_int += error
        if self.error_prev is None:
            self.error_prev = error
        error_deriv = error - self.error_prev
        self.error_prev = error
        return self.kp*error + self.ki*self.error_int + self.kd*error_deriv

    def reset(self):
        self.error_prev = None
        self.error_int = 0
#test
# fuzzy_controller = PID(0.8, 0.00001, 0.0001)
# error_input = 7.0
# previous_error=-4.0
# output = fuzzy_controller.control(error_input,previous_error)
# print(f"Control output: {output}")