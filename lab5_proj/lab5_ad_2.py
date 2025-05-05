from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Slider, CheckboxGroup
from bokeh.plotting import figure
import numpy as np
from scipy.signal import iirfilter, lfilter
from bokeh.models import Panel, Tabs

def moving_average_filter(x, window_size):
    """Простий ковзний середній фільтр."""
    y = np.zeros_like(x)
    for i in range(len(x)):
        if i < window_size:
            y[i] = np.mean(x[:i+1])
        else:
            y[i] = np.mean(x[i-window_size+1:i+1])
    return y


# Початкові дані
t = np.linspace(0, 4 * np.pi, 1000)

# Функція для створення сигналу
def generate_signal(A, omega, phi, noise_mean, noise_covariance, add_noise_flag):
    y = A * np.sin(omega * t + phi)
    if add_noise_flag:
        noise = np.random.normal(noise_mean, noise_covariance, size=t.shape)
        y += noise
    return y

# Функція для фільтрації сигналу
def filter_signal(y, omega, Wn_mult, fs_mult):
    fs = 1000 / (4 * np.pi) * fs_mult
    Wn = omega * 2 * Wn_mult
    b, a = iirfilter(N=4, Wn=Wn, fs=fs, btype='low', ftype='butter')
    return lfilter(b, a, y)

# Створення фігури
p = figure(title="Сигнал", height=400, width=700)
r = p.line(t, np.zeros_like(t), line_width=2)

p_filtered = figure(title="Відфільтрований сигнал", height=400, width=700)
r_filtered = p_filtered.line(t, np.zeros_like(t), line_width=2, color="green")


# Віджети (слайдери і чекбокси)
amp_slider = Slider(title="Амплітуда", start=0, end=5, value=1, step=0.1)
freq_slider = Slider(title="Частота", start=0.5, end=10, value=2, step=0.1)
phase_slider = Slider(title="Фаза", start=-np.pi, end=np.pi, value=0, step=0.1)
noise_mean_slider = Slider(title="Сер. значення шуму", start=0, end=1, value=0, step=0.1)
noise_cov_slider = Slider(title="Дисперсія шуму", start=0, end=5, value=0, step=0.1)

filter_checkbox = CheckboxGroup(labels=["Додати фільтр"], active=[])
noise_checkbox = CheckboxGroup(labels=["Додати шум"], active=[])

Wn_slider = Slider(title="Множник Wn", start=0.5, end=2, value=1, step=0.1)
fs_slider = Slider(title="Множник fs", start=0.5, end=2, value=1, step=0.1)
filter_type_checkbox = CheckboxGroup(labels=["Використовувати власний фільтр"], active=[])

def filter_signal_custom(y, window_size):
    return moving_average_filter(y, window_size)


# Оновлення графіку
def update(attr, old, new):
    A = amp_slider.value
    omega = freq_slider.value
    phi = phase_slider.value
    noise_mean = noise_mean_slider.value
    noise_covariance = noise_cov_slider.value
    add_noise_flag = 0 in noise_checkbox.active

    y = generate_signal(A, omega, phi, noise_mean, noise_covariance, add_noise_flag)

    r.data_source.data = dict(x=t, y=y)

    if 0 in filter_checkbox.active:
        # Тут вибір типу фільтра
        if 0 in filter_type_checkbox.active:
            # Використовуємо власний фільтр
            y_filtered = filter_signal_custom(y, window_size=10)
        else:
            # Стандартний (Butterworth)
            y_filtered = filter_signal(y, omega, Wn_slider.value, fs_slider.value)

        r_filtered.data_source.data = dict(x=t, y=y_filtered)
    else:
        r_filtered.data_source.data = dict(x=t, y=np.zeros_like(t))


# Прив'язка оновлень до слайдерів і чекбоксів
for widget in [amp_slider, freq_slider, phase_slider, noise_mean_slider, noise_cov_slider, Wn_slider, fs_slider, filter_checkbox, noise_checkbox]:
    widget.on_change('value' if isinstance(widget, Slider) else 'active', update)

# Початковий виклик
update(None, None, None)

# tab1 = Panel(child=p, title="Сигнал")
# tab2 = Panel(child=p_filtered, title="Фільтрований сигнал")
# tabs = Tabs(tabs=[tab1, tab2])
# Розміщення всіх елементів у layout
curdoc().add_root(column(
    amp_slider, freq_slider, phase_slider,
    noise_mean_slider, noise_cov_slider,
    noise_checkbox,
    filter_checkbox,
    Wn_slider, fs_slider,
    filter_type_checkbox,
    p,
    p_filtered
))
curdoc().title = "Гармоніка з параметрами"


