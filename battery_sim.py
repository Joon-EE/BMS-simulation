import matplotlib.pyplot as plt

# Simulation settings
battery_capacity_ah = 2.0
load_currents = [0.5, 1.0, 1.5, 3.0]
initial_voltage = 4.2
cutoff_voltage = 3.0
time_step_min = 1

internal_resistance = 0.1
max_current_limit = 2.0

results = []

for load_current_a in load_currents:

    time_minutes = []
    voltage_values = []

    elapsed_time = 0
    soc = 1.0

    cutoff_time = None
    cutoff_reason = None

    energy_used = 0

    while True:

        ocv = cutoff_voltage + (initial_voltage - cutoff_voltage) * soc
        terminal_voltage = ocv - load_current_a * internal_resistance

        time_minutes.append(elapsed_time)
        voltage_values.append(terminal_voltage)

        #Energy Calculation
        energy_used += load_current_a * time_step_min

        # Overcurrent protection
        if load_current_a > max_current_limit:
            cutoff_reason = "Overcurrent"
            cutoff_time = elapsed_time
            break

        # Undervoltage protection
        if terminal_voltage <= cutoff_voltage:
            cutoff_reason = "Undervoltage"
            cutoff_time = elapsed_time
            break

        # Decrease in SOC
        soc -= (load_current_a * time_step_min) / (battery_capacity_ah * 60)

        elapsed_time += time_step_min

        if soc <= 0:
            break

    #Efficiency Calculation
    total_energy = battery_capacity_ah * 60
    efficiency = energy_used / total_energy

    results.append((load_current_a, cutoff_time, efficiency, cutoff_reason))

    plt.plot(time_minutes, voltage_values, label=f"{load_current_a}A")

#Print the results
print("\n=== Performance Summary ===")
for load, time, eff, reason in results:
    print(f"{load}A | Time: {time} min | Efficiency: {eff:.2f} | Reason: {reason}")

plt.axhline(y=cutoff_voltage, linestyle='--', label="Cutoff Voltage")

plt.xlabel("Time (minutes)")
plt.ylabel("Voltage (V)")
plt.title("Battery Simulation with Performance Analysis")
plt.grid(True)
plt.legend()

plt.show()