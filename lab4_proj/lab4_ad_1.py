
import pandas as pd
from datetime import datetime
import timeit

import numpy as np

#Рівень 1 Pandas

start_time = timeit.default_timer()

headers = ["date", "time", "global_active_power", "global_reactive_power", "voltage", "global_intensity", "sub_metering_1", "sub_metering_2", "sub_metering_3"]
df = pd.read_csv("household_power_consumption.txt", header = 1, names = headers, sep=";", low_memory=False)
# df = df.fillna("?")

df_2 = df.copy()

df_for_1_2_3_task = df.copy()

df_for_1_2_3_task["global_active_power"] = pd.to_numeric(df_for_1_2_3_task["global_active_power"], errors="coerce").fillna(0).astype(int)
df_for_1_2_3_task["voltage"] = pd.to_numeric(df_for_1_2_3_task["voltage"], errors="coerce").fillna(0).astype(int)
df_for_1_2_3_task["global_intensity"] = pd.to_numeric(df_for_1_2_3_task["global_intensity"], errors="coerce").fillna(0).astype(int)
df_for_1_2_3_task["sub_metering_2"] = pd.to_numeric(df_for_1_2_3_task["sub_metering_2"], errors="coerce").fillna(0).astype(int)
df_for_1_2_3_task["sub_metering_3"] = pd.to_numeric(df_for_1_2_3_task["sub_metering_3"], errors="coerce").fillna(0).astype(int)

gap_more_than_5 = df_for_1_2_3_task[df_for_1_2_3_task["global_active_power"] > 5]
voltage_more_than_235 = df_for_1_2_3_task[df_for_1_2_3_task["voltage"] > 235]
intensity_and_sub_metering = df_for_1_2_3_task[df_for_1_2_3_task["global_intensity"].between(19, 20, inclusive='both') &
                                               (df_for_1_2_3_task["sub_metering_2"] > df_for_1_2_3_task["sub_metering_3"])]

pd.set_option('display.max_columns', None)
print(f'Завдання 1 \n{gap_more_than_5}')
print(f'Завдання 2 \n{voltage_more_than_235}')
print(f'Завдання 3 \n{intensity_and_sub_metering}')


df["sub_metering_1"] = pd.to_numeric(df["sub_metering_1"], errors="coerce").fillna(0).astype(float)
df["sub_metering_2"] = pd.to_numeric(df["sub_metering_2"], errors="coerce").fillna(0).astype(float)
df["sub_metering_3"] = pd.to_numeric(df["sub_metering_3"], errors="coerce").fillna(0).astype(float)
df["global_active_power"] = pd.to_numeric(df["global_active_power"], errors="coerce").fillna(0).astype(float)
df["global_reactive_power"] = pd.to_numeric(df["global_reactive_power"], errors="coerce").fillna(0).astype(float)

df_4 = df.sample(n=500000, replace=False)

df_4["df_4_mean"] = df_4[["sub_metering_1", "sub_metering_2", "sub_metering_3"]].mean(axis=1)

print(f'Завдання 4 \n{df_4}')

df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
time_for_comparison = datetime.strptime("18:00:00", "%H:%M:%S").time()

df_sort_by_time_and_other = df[
    (df['time'] > time_for_comparison) &
    ((df["global_active_power"] + df["global_reactive_power"]) > 6) &
    (df[["sub_metering_1", "sub_metering_2", "sub_metering_3"]].max(axis=1) == df["sub_metering_2"])
]
half = len(df_sort_by_time_and_other) // 2

first_half = df_sort_by_time_and_other.iloc[:half].iloc[::3]
second_half = df_sort_by_time_and_other.iloc[half:].iloc[::4]
result = pd.concat([first_half, second_half])

print(f'Завдання 5 \n{result}')
end_time = timeit.default_timer()

print(f"Час виконання: {end_time - start_time:.5f} секунд")




#Рівень 1 Numpy
start_time = timeit.default_timer()

types = [("Date", "U10"), ("Time", "U8"), ("Global_active_power",
"float64"), ("Global_reactive_power", "float64"), ("Voltage",
"float64"), ("Global_intensity", "float64"), ("Sub_metering_1",
"float64"), ("Sub_metering_2", "float64"), ("Sub_metering_3",
"float64")]
df = np.genfromtxt("household_power_consumption.txt", missing_values=["?",np.nan],
delimiter=';', dtype=types, encoding="UTF=8", names=True)

sorted_data = df[df['Global_active_power'] > 5]
print(f'Завдання 1:{sorted_data}')

sorted_data_2 = df[df['Voltage'] > 235]
print(f'Завдання 2:{sorted_data_2}')

sorted_data_3 =  df[(df['Global_intensity'] >= 19) & (df['Global_intensity'] <= 20) & (df['Sub_metering_2'] > df['Sub_metering_3'])]
print(f'Завдання 3:{sorted_data_3}')

num_rows = df.shape[0]
sampled_data = df[np.random.choice(num_rows, size=500000, replace=False)]
sub_metering_values = np.column_stack((
    sampled_data['Sub_metering_1'],
    sampled_data['Sub_metering_2'],
    sampled_data['Sub_metering_3']
))
print(sub_metering_values.dtype)
# Конвертуємо Date і Time в масив
date_time = np.array(sampled_data[['Date', 'Time']].tolist(), dtype=object)

# Конвертуємо числові значення
numeric_sampled_data = np.array(sampled_data[['Global_active_power', 'Global_reactive_power', 'Voltage',
                                              'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']].tolist(), dtype=np.float64)

# Додаємо новий стовпець
numeric_sampled_data = np.column_stack((numeric_sampled_data, np.mean(sub_metering_values, axis=1)))

# Об’єднуємо текстові та числові дані в один масив (dtype=object)
final_data = np.column_stack((date_time, numeric_sampled_data))

print(f'Завдання 4\n{final_data}')


time_values = np.array([datetime.strptime(t, '%H:%M:%S').time() for t in df['Time']])
mask_time = time_values > datetime.strptime('18:00:00', '%H:%M:%S').time()

mask_power = df['Global_active_power'] > 6

mask_group2 = (df['Sub_metering_2'] > df['Sub_metering_1']) & \
              (df['Sub_metering_2'] > df['Sub_metering_3'])

filtered_data = df[mask_time & mask_power & mask_group2]

mid_index = len(filtered_data) // 2
first_half = filtered_data[:mid_index]
second_half = filtered_data[mid_index:]

selected_first_half = first_half[::3]
selected_second_half = second_half[::4]


final_selection = np.concatenate((selected_first_half, selected_second_half))


print(f'завдання 5\n{final_selection}')
end_time = timeit.default_timer()
print(f"Час виконання: {end_time - start_time:.5f} секунд")
