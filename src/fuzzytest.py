import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 定義輸入和輸出的論域
error = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'error')
delta_error = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'delta_error')
output = ctrl.Consequent(np.arange(-10, 10, 0.1), 'output')

# 定義模糊集合
error['negative_large'] = fuzz.trapmf(error.universe, [-20, -20, -10, -5])
error['negative_small'] = fuzz.trimf(error.universe, [-10, -5, 0])
error['zero'] = fuzz.trimf(error.universe, [-5, 0, 5])
error['positive_small'] = fuzz.trimf(error.universe, [0, 5, 10])
error['positive_large'] = fuzz.trapmf(error.universe, [5, 10, 20, 20])

delta_error['negative_large'] = fuzz.trapmf(delta_error.universe, [-10, -10, -5, -2.5])
delta_error['negative_small'] = fuzz.trimf(delta_error.universe, [-5, -2.5, 0])
delta_error['zero'] = fuzz.trimf(delta_error.universe, [-2.5, 0, 2.5])
delta_error['positive_small'] = fuzz.trimf(delta_error.universe, [0, 2.5, 5])
delta_error['positive_large'] = fuzz.trapmf(delta_error.universe, [2.5, 5, 10, 10])

output['negative_large'] = fuzz.trapmf(output.universe, [-20, -20, -10, -5])
output['negative_small'] = fuzz.trimf(output.universe, [-10, -5, 0])
output['zero'] = fuzz.trimf(output.universe, [-5, 0, 5])
output['positive_small'] = fuzz.trimf(output.universe, [0, 5, 10])
output['positive_large'] = fuzz.trapmf(output.universe, [5, 10, 20, 20])

# 繪製模糊集合
def plot_fuzzy_sets(var, var_name):
    plt.figure()
    for term in var.terms:
        plt.plot(var.universe, var[term].mf, label=term)
    plt.title(f'{var_name} Fuzzy Sets')
    plt.xlabel(var_name)
    plt.ylabel('Membership Degree')
    plt.legend()
    plt.grid(True)
    plt.show()

# 繪製 error, delta_error 和 output 的模糊集合
plot_fuzzy_sets(error, 'error')
plot_fuzzy_sets(delta_error, 'delta_error')
plot_fuzzy_sets(output, 'output')

# 定義模糊規則
rule1 = ctrl.Rule(error['negative_large'] & delta_error['negative'], output['negative'])
rule2 = ctrl.Rule(error['negative'] & delta_error['zero'], output['negative'])
rule3 = ctrl.Rule(error['negative'] & delta_error['positive'], output['zero'])
rule4 = ctrl.Rule(error['zero'] & delta_error['negative'], output['negative'])
rule5 = ctrl.Rule(error['zero'] & delta_error['zero'], output['zero'])
rule6 = ctrl.Rule(error['zero'] & delta_error['positive'], output['positive'])
rule7 = ctrl.Rule(error['positive'] & delta_error['negative'], output['zero'])
rule8 = ctrl.Rule(error['positive'] & delta_error['zero'], output['positive'])
rule9 = ctrl.Rule(error['positive_large'] & delta_error['positive'], output['positive'])

# 創建控制系統並進行模擬
control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulation = ctrl.ControlSystemSimulation(control_system)

# 提供輸入值並計算輸出
error_input = 1.0
delta_error_input = 0.5
simulation.input['error'] = error_input
simulation.input['delta_error'] = delta_error_input
simulation.compute()

# 獲取輸出值
output_value = simulation.output['output']
print(f"Control output: {output_value}")