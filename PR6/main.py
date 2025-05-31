import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Шлях до гіроскопа ===
GYRO_FILE = 'archive/2021-02-02_10-45-08/Gyroscope.csv'

# === Читання файлу ===
df = pd.read_csv(GYRO_FILE)

# Обчислення часу в секундах від початку
df['Time'] = (df['Milliseconds'] - df['Milliseconds'].iloc[0]) / 1000.0

# Згладжування осі Z
df['Z_smooth'] = df['Z'].rolling(window=10, center=True).mean()

# Порогове значення для виявлення повороту
z_threshold = df['Z_smooth'].std() * 1.5
df['is_turning'] = df['Z_smooth'].abs() > z_threshold

# Групування сегментів поворотів
df['turn_group'] = (df['is_turning'] != df['is_turning'].shift()).cumsum()
turn_segments = df[df['is_turning']].groupby('turn_group')

# === Розрахунок метрик по поворотах ===
turns_info = []

for name, group in turn_segments:
    if len(group) < 5:
        continue  # ігноруємо дуже короткі псевдо-повороти

    t_start = group['Time'].iloc[0]
    t_end = group['Time'].iloc[-1]
    duration = t_end - t_start

    max_angular_speed = group['Z_smooth'].abs().max()

    # Інтегруємо Z для обчислення кута повороту (приблизно)
    angle_change = np.trapz(group['Z_smooth'], group['Time'])  # градуси приблизно

    is_sharp = abs(angle_change) > 30 or max_angular_speed > 50  # умова "різкий поворот"

    turns_info.append({
        'StartTime': t_start,
        'EndTime': t_end,
        'Duration (s)': round(duration, 2),
        'Max Angular Speed (°/s)': round(max_angular_speed, 2),
        'Angle Change (°)': round(angle_change, 2),
        'Sharp Turn': 'Yes' if is_sharp else 'No'
    })

# Збереження в CSV
turns_df = pd.DataFrame(turns_info)
turns_df.to_csv('turn_report.csv', index=False)

# === Візуалізація ===
plt.figure(figsize=(14, 6))
plt.plot(df['Time'], df['Z'], label='Z (гіроскоп)', alpha=0.3)
plt.plot(df['Time'], df['Z_smooth'], label='Z (згладжено)', color='blue')

for name, group in turn_segments:
    if len(group) >= 5:
        plt.axvspan(group['Time'].iloc[0], group['Time'].iloc[-1], color='red', alpha=0.3)

plt.title('Виявлення поворотів за гіроскопом (вісь Z)')
plt.xlabel('Час (сек)')
plt.ylabel('Кутова швидкість (°/s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Консольний вивід ===
print(f"\nВиявлено {len(turns_df)} поворотів:")
print(turns_df.to_string(index=False))
print("\nАналітичний звіт збережено у 'turn_report.csv'")
