import matplotlib.pyplot as plt

# Simulation settings
battery_capacity_ah = 2.0
load_currents = [0.5, 1.0, 1.5, 3.0]  # 일부러 큰 값 포함
initial_voltage = 4.2
cutoff_voltage = 3.0
time_step_min = 1

# 🔴 Internal resistance (Ohms)
internal_resistance = 0.1

# 🔴 Overcurrent limit
max_current_limit = 2.0

for load_current_a in load_currents:

    time_minutes = []
    voltage_values = []

    elapsed_time = 0
    soc = 1.0  # state of charge (1 = 100%)

    cutoff_reason = None
    cutoff_time = None

    while True:

        # 🔴 OCV 간단 모델 (SOC 기반)
        ocv = cutoff_voltage + (initial_voltage - cutoff_voltage) * soc

        # 🔴 실제 전압 (IR drop 포함)
        terminal_voltage = ocv - load_current_a * internal_resistance

        time_minutes.append(elapsed_time)
        voltage_values.append(terminal_voltage)

        # 🔴 Overcurrent protection
        if load_current_a > max_current_limit:
            cutoff_reason = "Overcurrent"
            cutoff_time = elapsed_time
            print(f"[{load_current_a}A] Overcurrent cutoff at {cutoff_time} min")
            break

        # 🔴 Undervoltage protection
        if terminal_voltage <= cutoff_voltage:
            cutoff_reason = "Undervoltage"
            cutoff_time = elapsed_time
            print(f"[{load_current_a}A] Undervoltage cutoff at {cutoff_time} min")
            break

        # 🔴 SOC 감소 (에너지 소모)
        soc -= (load_current_a * time_step_min) / (battery_capacity_ah * 60)

        elapsed_time += time_step_min

        # 안전장치
        if soc <= 0:
            break

    # 그래프
    plt.plot(time_minutes, voltage_values, label=f"{load_current_a}A ({cutoff_reason})")

# cutoff 기준선
plt.axhline(y=cutoff_voltage, linestyle='--', label="Cutoff Voltage")

plt.xlabel("Time (minutes)")
plt.ylabel("Voltage (V)")
plt.title("Battery Simulation with Protection & IR Model")
plt.grid(True)
plt.legend()

plt.show()