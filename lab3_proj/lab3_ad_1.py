import streamlit as st
import urllib.request
import os
import pandas as pd
from datetime import datetime
import glob
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import sys

st.title('lab3')
area_names = {
    0: "Empty",
    1: "Вінницька",
    2: "Волинська",
    3: "Дніпропетровська",
    4: "Донецька",
    5: "Житомирська",
    6: "Закарпатська",
    7: "Запорізька",
    8: "Івано-Франківська",
    9: "Київська",
    10: "Кіровоградська",
    11: "Луганська",
    12: "Львівська",
    13: "Миколаївська",
    14: "Одеська",
    15: "Полтавська",
    16: "Рівненська",
    17: "Сумська",
    18: "Тернопільська",
    19: "Харківська",
    20: "Херсонська",
    21: "Хмельницька",
    22: "Черкаська",
    23: "Чернівецька",
    24: "Чернігівська",
    25: "Республіка Крим"
}



DATA_DIR = "noaa_data"
os.makedirs(DATA_DIR, exist_ok=True)

@st.cache_data
def download_vhi(province_id):
    # Формуємо URL для запиту
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean"

    try:
        # Завантажуємо нові дані
        wp = urllib.request.urlopen(url)
        text = wp.read().decode("utf-8")
        # Конвертуємо у DataFrame
        from io import StringIO
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        new_data = pd.read_csv(StringIO(text), header = 1,  names = headers, sep=",")

        # Шукаємо існуючий файл у папці
        existing_files = glob.glob(os.path.join(DATA_DIR, f"obl_{province_id}_*.csv"))
        if existing_files:
            existing_file = existing_files[0]  # Беремо будь-який (бо буде заміна)
            old_data = pd.read_csv(existing_file, header = 1, names = headers)

            # Якщо нові дані такі ж, як старі, виходимо
            if new_data.equals(old_data):
                print(f" Дані для області {province_id} не змінилися. Файл залишився без змін.")
                return

            # Видаляємо старий файл
            os.remove(existing_file)

        # Формуємо нову назву файлу
        current_datetime = datetime.now().strftime("%d%m%Y%H%M%S")
        new_file_path = os.path.join(DATA_DIR, f"obl_{province_id}_{current_datetime}.csv")

        # Зберігаємо нові дані
        new_data.to_csv(new_file_path, index=False)
        print(f" Дані оновлені. Новий файл: {new_file_path}")

    except Exception as e:
        print(f" Помилка при завантаженні області {province_id}: {e}")

@st.cache_data
def getting_data():
    for i in range(1, 29):
        province_id = i
        download_vhi(province_id)
getting_data()

@st.cache_data
def load_vhi_data(directory):
    all_files = [f for f in os.listdir(directory) if f.startswith("obl_") and f.endswith(".csv")]

    if not all_files:
        print("Немає файлів для завантаження!")
        return None

    dataframes = []

    for file in all_files:
        file_path = os.path.join(directory, file)
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        df = pd.read_csv(file_path, header=1, names=headers)

        province_id = int(file.split("_")[1])
        df.insert(0, "Province_ID", province_id)

        dataframes.append(df)

    final_df = pd.concat(dataframes, ignore_index=True)
    print("Завантажено", len(all_files), "файлів.")
    return final_df


DATA_DIR = "noaa_data"
df_vhi = load_vhi_data(DATA_DIR)
if df_vhi is not None:
    print(df_vhi.head())

@st.cache_data
def rename_province_ids(df):
    province_mapping = {
        1: 13, 2: 14, 3: 15, 4: 16, 5: 17, 6: 18, 7: 19, 8: 20,
        9: 21, 10: 22, 11: 23, 12: 24, 13: 1, 14: 2, 15: 3, 16: 4,
        17: 5, 18: 6, 19: 7, 20: 8, 21: 9, 22: 10, 23: 11, 24: 12,
        25: 25
    }

    # Використовуємо .replace() для всієї колонки без циклу
    df["Province_ID"] = df["Province_ID"].replace(province_mapping)

    print("Готово!\n", df.head())  # Вивід перших 5 рядків для перевірки
    return df


df_vhi = rename_province_ids(df_vhi)

def get_vhi_by_year(df, province_id, year):
    return df[(df["Province_ID"] == province_id) & (df["Year"] == year)]
def get_extremes(df, province_ids, years):
    subset = df[(df["Province_ID"].isin(province_ids)) & (df["Year"].isin(years))]
    return {
        "min": subset["VHI"].min(),
        "max": subset["VHI"].max(),
        "mean": subset["VHI"].mean(),
        "median": subset["VHI"].median()
    }
def get_vhi_by_year_range(df, province_ids, start_year, end_year):
    df_vhi["Year"] = pd.to_numeric(df_vhi["Year"], errors="coerce").astype("Int64")
    return df[(df["Province_ID"].isin(province_ids)) & (df["Year"].between(start_year, end_year))]

def find_drought_years(df, threshold=5):
    drought_years = []
    for year in df["Year"].unique():
        yearly_data = df[df["Year"] == year]
        drought_regions = yearly_data[yearly_data["VHI"] < 15]["Province_ID"].unique()
        if len(drought_regions) >= threshold:
            drought_years.append((year, drought_regions))
    return drought_years

def sort_func1(df):
    df.sort_values(by=st.session_state.selected_index, ascending=True, inplace=True)


def sort_func2(df):
    df.sort_values(by=st.session_state.selected_index, ascending=False, inplace=True)


col1, col2 = st.columns([1, 2])
with col1:
    options_for_dropbox1 = ["VCI", "TCI", "VHI"]
    if "selected_index" not in st.session_state:
        st.session_state.selected_index = options_for_dropbox1[0]
    st.session_state.selected_index = st.selectbox("Оберіть часовий ряд:", options=options_for_dropbox1,
                                                   index=options_for_dropbox1.index(st.session_state.selected_index))

    if "selected_area" not in st.session_state:
        st.session_state.selected_area = list(area_names.values())[1]
    st.session_state.selected_area = st.selectbox(
        "Оберіть область", options=list(area_names.values()),
        index=list(area_names.values()).index(st.session_state.selected_area)
    )

        if "week_range" not in st.session_state:
        st.session_state.week_range = 1
    if "week_range_2" not in st.session_state:
        st.session_state.week_range_2 = 5
    st.session_state.week_range, st.session_state.week_range_2 = st.slider(
        "Виберіть інтервал тижнів", 1, 52, (st.session_state.week_range, st.session_state.week_range_2)
    )

    if "year_range" not in st.session_state:
        st.session_state.year_range = 1982
    if "year_range_2" not in st.session_state:
        st.session_state.year_range_2 = 2000
    st.session_state.year_range, st.session_state.year_range_2 = st.slider(
        "Виберіть інтервал років", 1982, 2025, (st.session_state.year_range, st.session_state.year_range_2)

    if st.button("Скинути фільтри"):
        st.session_state.selected_index = options_for_dropbox1[0]
        st.session_state.selected_area = list(area_names.values())[1]
        st.session_state.week_range = 1
        st.session_state.year_range = 1982

    df_vhi["Year"] = pd.to_numeric(df_vhi["Year"], errors="coerce").astype("Int64")
    filtered_df_vhi = df_vhi[
        (df_vhi["Province_ID"] == list(area_names.values()).index(st.session_state.selected_area)) &
        (df_vhi["Year"].between(int(st.session_state.year_range), int(st.session_state.year_range_2))) &
        (df_vhi["Week"].between(float(st.session_state.week_range), float(st.session_state.week_range_2)))]

    if "ascending_order" not in st.session_state:
        st.session_state["ascending_order"] = False
    ascending_order = st.checkbox(
        "Сортувати за зростанням",
        value=st.session_state["ascending_order"],
        key="ascending_order"
    )

    if "descending_order" not in st.session_state:
        st.session_state["descending_order"] = False
    descending_order = st.checkbox(
        "Сортувати за спаданням",
        value=st.session_state["descending_order"],
        key="descending_order"
    )

    if ascending_order and descending_order:
        st.warning("Вибрані обидва варіанти! Використовується сортування за зростанням.")
        filtered_df_vhi = filtered_df_vhi.sort_values(by=st.session_state.selected_index, ascending=True)
    elif ascending_order:
        filtered_df_vhi = filtered_df_vhi.sort_values(by=st.session_state.selected_index, ascending=True)
    elif descending_order:
        filtered_df_vhi = filtered_df_vhi.sort_values(by=st.session_state.selected_index, ascending=False)
    else:
        filtered_df_vhi = filtered_df_vhi

with col2:

    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік 1", "Графік 2"])
    with tab1:
        st.subheader("Відфільтровані дані в таблицю")
        st.write(filtered_df_vhi.loc[:, ["Province_ID", "Year", "Week", "SMN", "SMT", st.session_state.selected_index]])
    with tab2:
        st.subheader("Графік 1")
        filtered_df_vhi["Week"] = pd.to_numeric(filtered_df_vhi["Week"], errors="coerce")
        fig, ax = plt.subplots(figsize=(12, 6))
        filtered_df_vhi["Year"] = filtered_df_vhi["Year"].astype(str)

        sns.lineplot(data=filtered_df_vhi, x="Week", y=st.session_state.selected_index, hue="Year", ax=ax)

        ax.set_title(f"Графік {st.session_state.selected_index} за обраний діапазон років та тижнів")
        ax.set_xlabel("Тиждень")
        ax.set_ylabel(st.session_state.selected_index)
        ax.legend(title="Рік")

        st.pyplot(fig)
    with tab3:
        st.subheader("Графік 2")
        fig, ax = plt.subplots(figsize=(12, 6))

        selected_area_data = filtered_df_vhi[filtered_df_vhi["Province_ID"] == st.session_state.selected_area]

        all_areas_data = df_vhi[(df_vhi["Year"].between(1, int(st.session_state.year_range))) & (df_vhi["Week"].between(1.0, float(st.session_state.week_range)))]

        sns.regplot(data=all_areas_data, x="Week", y=st.session_state.selected_index, scatter=False, ax=ax)

        sns.lineplot(data=filtered_df_vhi, x="Week", y=st.session_state.selected_index,
                    marker="o", linewidth=2.5, ci=None, ax=ax)

        ax.set_title(
            f"Порівняння {st.session_state.selected_index} для {st.session_state.selected_area} з іншими областями")
        ax.set_xlabel("Тиждень")
        ax.set_ylabel(st.session_state.selected_index)
        ax.legend(title="Рік")

        st.pyplot(fig)
