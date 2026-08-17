import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================
# 1. УКАЖИТЕ ПРАВИЛЬНЫЙ ПУТЬ К ФАЙЛУ
# ============================================
# Если файл в той же папке что и скрипт:
file_path = "dannye-ce1e2d0f-249c-4782-a612-f0d6eeba56c0.xlsx"

# ЕСЛИ НЕ РАБОТАЕТ — раскомментируйте одну из строк ниже:
# file_path = "../dannye-ce1e2d0f-249c-4782-a612-f0d6eeba56c0.xlsx"
# file_path = "C:/Users/HP/Downloads/матпрак/dannye-ce1e2d0f-249c-4782-a612-f0d6eeba56c0.xlsx"

# Проверяем, существует ли файл
if not os.path.exists(file_path):
    print(f"❌ Файл не найден по пути: {file_path}")
    print(f"Текущая папка: {os.getcwd()}")
    print("Файлы в текущей папке:", os.listdir("."))
    exit()

# ============================================
# 2. ЗАГРУЗКА
# ============================================
df = pd.read_excel(file_path, sheet_name="Данные воронки")
print("✅ Данные загружены")

# Дальше — тот же код, что был ранее
# (агрегация, расчёты, график)

weekly = df.groupby("Неделя").agg({
    "Установки": "sum",
    "Регистрации": "sum",
    "Открыли поиск": "sum",
    "Просмотрели авто": "sum",
    "Забронировали": "sum",
    "Первая поездка": "sum"
}).reset_index()

week_order = [f"Неделя {i}" for i in range(1, 9)]
weekly["Неделя"] = pd.Categorical(weekly["Неделя"], categories=week_order, ordered=True)
weekly = weekly.sort_values("Неделя")

weekly["conv_overall"] = weekly["Первая поездка"] / weekly["Установки"]
weekly["conv_reg_to_search"] = weekly["Открыли поиск"] / weekly["Регистрации"]

# График
fig, ax = plt.subplots(figsize=(10, 5))
weeks = weekly["Неделя"].astype(str)
conv = weekly["conv_overall"] * 100

ax.plot(weeks, conv, marker='o', linewidth=2, markersize=8, color='#2E86AB')
ax.axvspan(5.5, 7.5, alpha=0.2, color='red')
ax.set_ylabel('Конверсия (%)')
ax.set_title('Общая конверсия (установка → первая поездка)')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analytics_report.png', dpi=150)
print("✅ График сохранён как 'analytics_report.png'")
plt.show()

# Вывод потерь
loss_reg_to_search = (1 - weekly[weekly["Неделя"].isin(["Неделя 7", "Неделя 8"])]["conv_reg_to_search"].mean()) * 100
print(f"\n📊 Потери на этапе 'Регистрация → Поиск' за недели 7-8: {loss_reg_to_search:.1f}%")