import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#Частина 2

types = [("Date", "U10"), ("Time", "U8"), ("Global_active_power",
"float64"), ("Global_reactive_power", "float64"), ("Voltage",
"float64"), ("Global_intensity", "float64"), ("Sub_metering_1",
"float64"), ("Sub_metering_2", "float64"), ("Sub_metering_3",
"float64")]
df_np = np.genfromtxt("household_power_consumption.txt", missing_values=["?",np.nan],
delimiter=';', dtype=types, encoding="UTF=8", names=True)




headers = ["date", "time", "global_active_power", "global_reactive_power", "voltage", "global_intensity", "sub_metering_1", "sub_metering_2", "sub_metering_3"]
df = pd.read_csv("household_power_consumption.txt", header = 1, names = headers, sep=";", low_memory=False)

df_2 = df.copy()

df_2_1 = df_2.copy()

df_for_1_2_3_task = df.copy()
#Завдання 1 через заповнення середнім значеням (Numpy)

date_time = np.array(df_np[['Date', 'Time']].tolist(), dtype=object)
numeric_mean_values = np.array(df_np[['Global_active_power', 'Global_reactive_power', 'Voltage',
                                              'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']].tolist(), dtype=np.float64)
final_data = np.column_stack((date_time, numeric_mean_values))


df_np_2_1 = np.copy(numeric_mean_values)

#Завдання 1 через видалення (pandas)
df_2_2 = df_2.dropna(axis=0)
print(df_2_2.isna().sum())

df["sub_metering_1"] = pd.to_numeric(df["sub_metering_1"], errors="coerce").fillna(0).astype(float)
df["sub_metering_2"] = pd.to_numeric(df["sub_metering_2"], errors="coerce").fillna(0).astype(float)
df["sub_metering_3"] = pd.to_numeric(df["sub_metering_3"], errors="coerce").fillna(0).astype(float)
df["global_active_power"] = pd.to_numeric(df["global_active_power"], errors="coerce").fillna(0).astype(float)
df["global_reactive_power"] = pd.to_numeric(df["global_reactive_power"], errors="coerce").fillna(0).astype(float)
df["voltage"] = pd.to_numeric(df["voltage"], errors="coerce").fillna(0).astype(float)
df["global_intensity"] = pd.to_numeric(df["global_intensity"], errors="coerce").fillna(0).astype(float)
df.info()

#Нормую датафрейм (pandas)
df_norm = df.copy()
df_norm.iloc[:, 2:] = (df.iloc[:, 2:] - df.iloc[:, 2:].min()) / (df.iloc[:, 2:].max() - df.iloc[:, 2:].min())

print("Нормований датафрейм: ", df_norm)

#Сдандартизую датафрейм (pandas)
df_std = df.copy()
df_std.iloc[:, 2:] = (df.iloc[:, 2:] - df.iloc[:, 2:].mean()) / df.iloc[:, 2:].std()

print("Стандартизований датафрейм: ", df_std)

#гістограма (numpy)
diaps = [230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280]
plt.figure(figsize=(14, 7))
plt.hist(df_np_2_1[:, 2], bins=diaps, edgecolor='green')
plt.title("Гістограма (NumPy масив)")
plt.xlabel("Напруга (V)")
plt.ylabel("Кількість елементів")
plt.grid(True)

plt.show()


#Підготовка даних для побудови графіка залежності "voltage" від "global_intensity" (pandas)
df["voltage"] = pd.to_numeric(df["voltage"], errors="coerce")
df["global_intensity"] = pd.to_numeric(df["global_intensity"], errors="coerce")

df_filtered = df.dropna(subset=["voltage", "global_intensity"])

#Побудова графіка
plt.figure(figsize=(14, 7))
plt.scatter(df_filtered["global_intensity"], df_filtered["voltage"], s=5, alpha=0.3, color="royalblue")
plt.title("Залежність Voltage від Global Intensity")
plt.xlabel("Global Intensity (A)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.tight_layout()
plt.show()


#коефіціент пірсона та спірмена (pandas)
print("Коефіціент пірсона:\n")
print(df_for_1_2_3_task[["voltage", "global_intensity"]].corr(method="pearson"))
print("Коефіціент спірмана:\n")
print(df_for_1_2_3_task[["voltage", "global_intensity"]].corr(method="spearman"))

#One Hot Encoding по даті (pandas)
df_encoded = pd.get_dummies(df, columns=['date'])
print(f'One hot encoding:\n {df_encoded}')

#візуалізація багато вимірних даних (pandas)
plt.figure(figsize=(14, 14))
sns.pairplot(df_for_1_2_3_task)
plt.show()