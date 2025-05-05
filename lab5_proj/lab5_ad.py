import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import iirfilter, lfilter

# Побудова графіку
def update_plot(val=None):
    A = amp_slider.get()
    omega = freq_slider.get()
    phi = phase_slider.get()
    noise_mean = noise_mean_slider.get()
    noise_covariance = noise_covariance_slider.get()


    t = np.linspace(0, 4*np.pi, 1000)
    y = A * np.sin(omega * t + phi)
    if add_noise.get():
        noise = np.random.normal(noise_mean, noise_covariance, size=t.shape)
        y += noise

    if add_filter.get():
        k = fs_slider.get()
        z = Wn_slider.get()
        fs = 1000 / (4 * np.pi) * k
        Wn = omega * 2 * z
        b, a = iirfilter(N=4, Wn=Wn, fs=fs, btype='low', ftype='butter')
        y_filtered = lfilter(b, a, y)

        ax2.clear()
        ax2.plot(t, y_filtered, color='green')
        ax2.set_title("Відфільтрований сигнал")
        ax2.set_xlabel("Час")
        ax2.set_ylabel("y(t)")
        ax2.set_visible(True)  # Показуємо
    else:
        ax2.clear()
        ax2.set_visible(False)
    ax1.clear()
    ax1.plot(t, y)
    ax1.set_title("Зашумлений сигнал")
    ax1.set_xlabel("Час")
    ax1.set_ylabel("y(t)")

    canvas.draw()

def reset_parameters():
    amp_slider.set(1)
    freq_slider.set(2)
    phase_slider.set(0)
    add_noise.set(False)
    update_plot()

# Вікно
root = tk.Tk()
root.title("Гармоніка з параметрами")

add_noise = tk.BooleanVar()
add_filter = tk.BooleanVar()

# Фрейм для слайдерів
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

label = tk.Label(control_frame, text="Налаштування гармоніки", font=("Arial", 12, "bold"))
label.pack(pady=5)

# Слайдер амплітуди
amp_slider = tk.Scale(control_frame, from_=0, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Амплітуда", command=update_plot)
amp_slider.set(1)
amp_slider.pack()

# Слайдер частоти
freq_slider = tk.Scale(control_frame, from_=0.5, to=10, resolution=0.1, orient=tk.HORIZONTAL, label="Частота", command=update_plot)
freq_slider.set(2)
freq_slider.pack()

# Слайдер фази
phase_slider = tk.Scale(control_frame, from_=-np.pi, to=np.pi, resolution=0.1, orient=tk.HORIZONTAL, label="Фаза", command=update_plot)
phase_slider.set(0)
phase_slider.pack()

# Слайдер сер знач шуму
noise_mean_slider = tk.Scale(control_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="сер знач шуму", command=update_plot)
noise_mean_slider.set(0)
noise_mean_slider.pack()

# Слайдер дисперсії шуму
noise_covariance_slider = tk.Scale(control_frame, from_=0, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="дисперсія шуму", command=update_plot)
noise_covariance_slider.set(0)
noise_covariance_slider.pack()

#Чекбокс шуму
noise_checkbox = tk.Checkbutton(control_frame, text="Додати шум", variable=add_noise, command=update_plot)
noise_checkbox.pack()

#кнопка скидання значень
reset_button = ttk.Button(control_frame, text="Скинути", command=reset_parameters)
reset_button.pack(pady=10)

label = tk.Label(control_frame, text="Налаштування фільтру", font=("Arial", 12, "bold"))
label.pack(pady=5)

#Чекбокс фільтру
filter_checkbox = tk.Checkbutton(control_frame, text="Додати фільтр", variable=add_filter, command=update_plot)
filter_checkbox.pack()

# Слайдер множника Wm
Wn_slider = tk.Scale(control_frame, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="множник Wn", command=update_plot)
Wn_slider.set(1)
Wn_slider.pack()

# Слайдер множника fs
fs_slider = tk.Scale(control_frame, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="множник fs", command=update_plot)
fs_slider.set(1)
fs_slider.pack()

# Площа під графік
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
fig.tight_layout(pad=3)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



# Початковий графік
update_plot()

root.mainloop()