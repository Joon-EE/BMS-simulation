import matplotlib.pyplot as plt

# Simulation settings
battery_capacity_ah = 2.0
load_currents = [0.5, 1.0, 1.5, 3.0]
initial_voltage = 4.2
cutoff_voltage = 3.0
time_step_min = 1

# Thermal settings
ambient_temp_c = 25.0
initial_temp_c = 25.0
# Considering typical temp limits for lithium ion batteries for EVs
temp_limit_c = 55.0
temp_step_c = 0.5

# Heat equation settings. Heat energy = mass*specific heat*change in temperature
battery_mass_kg = 0.05
specific_heat_J_per_kgC = 1000
time_step_sec = time_step_min*60

# Cooling temperatures
cooling_on_c = 55.0
cooling_off_c = 50.0
cooling_per_min = 1.0
cooling_on = False

internal_resistance = 0.1
max_current_limit = 2.0

results = []
temp_results = []

for load_current_a in load_currents:

    time_minutes = []
    voltage_values = []
    temp_values = []

    elapsed_time = 0
    battery_temp_c = initial_temp_c
    soc = 1.0

    cutoff_time = None
    cutoff_reason = None
    cooling_on = False

    energy_used = 0

    while True:

        ocv = cutoff_voltage + (initial_voltage - cutoff_voltage) * soc
        terminal_voltage = ocv - load_current_a * internal_resistance

        # Thermal model: heat from internal resistance loss
        power_heat_w = (load_current_a ** 2) * internal_resistance
        heat_energy_j = power_heat_w * time_step_sec
        delta_temp_battery = heat_energy_j / (battery_mass_kg * specific_heat_J_per_kgC)
        battery_temp_c += delta_temp_battery

        # Overcurrent protection
        if load_current_a > max_current_limit:
            cutoff_reason = "Overcurrent"
            cutoff_time = elapsed_time
            break

        #Energy Calculation
        energy_used += load_current_a * time_step_min

        # Undervoltage protection
        if terminal_voltage <= cutoff_voltage:
            cutoff_reason = "Undervoltage"
            cutoff_time = elapsed_time
            break

        # Overheating protection
        if battery_temp_c >= temp_limit_c:
            cutoff_reason = "Overheating"
            cutoff_time = elapsed_time
            break
        
        # Cooling
        if cooling_on_c <= battery_temp_c:
            cooling_on = True
        
        if cooling_off_c >= battery_temp_c:
            cooling_on = False

        if cooling_on == True:
            battery_temp_c -= cooling_per_min

        time_minutes.append(elapsed_time)
        voltage_values.append(terminal_voltage)
        temp_values.append(battery_temp_c)
        
        # Decrease in SOC
        soc -= (load_current_a * time_step_min) / (battery_capacity_ah * 60)

        elapsed_time += time_step_min

        if soc <= 0:
            break

    #Efficiency Calculation
    total_energy = battery_capacity_ah * 60
    efficiency = energy_used / total_energy

    #Load current plotting
    results.append((load_current_a, cutoff_time, efficiency, cutoff_reason))
    #Temperature plotting
    temp_results.append((load_current_a, time_minutes, temp_values))
    plt.plot(time_minutes, voltage_values, label=f"{load_current_a}A")

#Print the results for load currents
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

#Print the results for the battery temperatures
plt.figure()

for load_current_a, time_minutes, temp_values in temp_results:
    plt.plot(time_minutes, temp_values, label=f"{load_current_a}A")

plt.axhline(y=temp_limit_c, linestyle='-', label="Temperature Limit")
plt.axhline(y=cooling_on_c, linestyle='--', label="Cooling ON")
plt.axhline(y=cooling_off_c, linestyle=':', label="Cooling OFF")

plt.xlabel("Time (minutes)")
plt.ylabel("Battery Temperature (°C)")
plt.title("Battery Temperature with Cooling Control")
plt.grid(True)
plt.legend()
plt.show()