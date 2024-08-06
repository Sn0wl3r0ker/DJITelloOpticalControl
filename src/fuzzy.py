import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyControl(object):
    def __init__(self):
        # 定義輸入和輸出的論域
        self.error = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'error')
        self.delta_error = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'delta_error')
        self.output = ctrl.Consequent(np.arange(-20, 20, 0.1), 'output')
        
        # 定義 error 的模糊集合
        self.error['negative_large'] = fuzz.trapmf(self.error.universe, [-20, -20, -10, -5])
        self.error['negative_small'] = fuzz.trimf(self.error.universe, [-10, -5, 0])
        self.error['zero'] = fuzz.trimf(self.error.universe, [-5, 0, 5])
        self.error['positive_small'] = fuzz.trimf(self.error.universe, [0, 5, 10])
        self.error['positive_large'] = fuzz.trapmf(self.error.universe, [5, 10, 20, 20])
        
        # 定義 delta_error 的模糊集合
        self.delta_error['negative_large'] = fuzz.trapmf(self.delta_error.universe, [-20, -20, -10, -5])
        self.delta_error['negative_small'] = fuzz.trimf(self.delta_error.universe, [-10, -5, 0])
        self.delta_error['zero'] = fuzz.trimf(self.delta_error.universe, [-5, 0, 5])
        self.delta_error['positive_small'] = fuzz.trimf(self.delta_error.universe, [0, 5, 10])
        self.delta_error['positive_large'] = fuzz.trapmf(self.delta_error.universe, [5, 10, 20, 20])
        
        # 定義 output 的模糊集合
        self.output['negative_large'] = fuzz.trapmf(self.output.universe, [-20, -20, -10, -5])
        self.output['negative_small'] = fuzz.trimf(self.output.universe, [-10, -5, 0])
        self.output['zero'] = fuzz.trimf(self.output.universe, [-5, 0, 5])
        self.output['positive_small'] = fuzz.trimf(self.output.universe, [0, 5, 10])
        self.output['positive_large'] = fuzz.trapmf(self.output.universe, [5, 10, 20, 20])
        
        # 定義模糊規則
        rule1 = ctrl.Rule(self.error['negative_large'] & self.delta_error['negative_large'], self.output['negative_large'])
        rule2 = ctrl.Rule(self.error['negative_large'] & self.delta_error['negative_small'], self.output['negative_large'])
        rule3 = ctrl.Rule(self.error['negative_large'] & self.delta_error['zero'], self.output['negative_small'])
        rule4 = ctrl.Rule(self.error['negative_large'] & self.delta_error['positive_small'], self.output['zero'])
        rule5 = ctrl.Rule(self.error['negative_large'] & self.delta_error['positive_large'], self.output['positive_small'])

        rule6 = ctrl.Rule(self.error['negative_small'] & self.delta_error['negative_large'], self.output['negative_large'])
        rule7 = ctrl.Rule(self.error['negative_small'] & self.delta_error['negative_small'], self.output['negative_small'])
        rule8 = ctrl.Rule(self.error['negative_small'] & self.delta_error['zero'], self.output['negative_small'])
        rule9 = ctrl.Rule(self.error['negative_small'] & self.delta_error['positive_small'], self.output['zero'])
        rule10 = ctrl.Rule(self.error['negative_small'] & self.delta_error['positive_large'], self.output['positive_small'])

        rule11 = ctrl.Rule(self.error['zero'] & self.delta_error['negative_large'], self.output['negative_small'])
        rule12 = ctrl.Rule(self.error['zero'] & self.delta_error['negative_small'], self.output['negative_small'])
        rule13 = ctrl.Rule(self.error['zero'] & self.delta_error['zero'], self.output['zero'])
        rule14 = ctrl.Rule(self.error['zero'] & self.delta_error['positive_small'], self.output['positive_small'])
        rule15 = ctrl.Rule(self.error['zero'] & self.delta_error['positive_large'], self.output['positive_small'])

        rule16 = ctrl.Rule(self.error['positive_small'] & self.delta_error['negative_large'], self.output['zero'])
        rule17 = ctrl.Rule(self.error['positive_small'] & self.delta_error['negative_small'], self.output['zero'])
        rule18 = ctrl.Rule(self.error['positive_small'] & self.delta_error['zero'], self.output['positive_small'])
        rule19 = ctrl.Rule(self.error['positive_small'] & self.delta_error['positive_small'], self.output['positive_small'])
        rule20 = ctrl.Rule(self.error['positive_small'] & self.delta_error['positive_large'], self.output['positive_large'])

        rule21 = ctrl.Rule(self.error['positive_large'] & self.delta_error['negative_large'], self.output['positive_small'])
        rule22 = ctrl.Rule(self.error['positive_large'] & self.delta_error['negative_small'], self.output['positive_small'])
        rule23 = ctrl.Rule(self.error['positive_large'] & self.delta_error['zero'], self.output['positive_large'])
        rule24 = ctrl.Rule(self.error['positive_large'] & self.delta_error['positive_small'], self.output['positive_large'])
        rule25 = ctrl.Rule(self.error['positive_large'] & self.delta_error['positive_large'], self.output['positive_large'])
        
        # 創建控制系統
        self.control_system = ctrl.ControlSystem([
            rule1, rule2, rule3, rule4, rule5,
            rule6, rule7, rule8, rule9, rule10,
            rule11, rule12, rule13, rule14, rule15,
            rule16, rule17, rule18, rule19, rule20,
            rule21, rule22, rule23, rule24, rule25
        ])
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)
        
        # 儲存前一次誤差
        self.previous_error = None

    def control(self, current_error):
        self.previous_error=previous_error
        # 如果是第一次調用，初始化前一次誤差
        if self.previous_error is None:
            print("Initializing previous_error")
            self.previous_error = current_error

        # 計算誤差變化率
        delta_error = current_error - self.previous_error

        # 設置輸入值並計算輸出
        self.simulation.input['error'] = current_error
        self.simulation.input['delta_error'] = delta_error
        self.simulation.compute()

        # 更新前一次誤差
        self.previous_error = current_error

        # 獲取控制輸出
        output_value = self.simulation.output['output']
        return output_value

    def reset(self):
        self.previous_error = None

# test!
# fuzzy_controller = FuzzyControl()
# error_input = 7.0
# previous_error=-4.0
# output = fuzzy_controller.control(error_input,previous_error)
# print(f"Control output: {output}")
