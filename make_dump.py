# make_dump.py
import os
from datetime import datetime

# ============== НАСТРОЙКИ ==============
# Папки и файлы, которые включить в дамп
INCLUDE_DIRS = ["nobrain_bot"]
INCLUDE_FILES = ["app.py"]

# Исключаемые расширения
EXCLUDE_EXTS = {".pyc", ".pyo", ".log", ".db", ".sqlite", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".env"}

# Куда сохранить дамп
DUMP_DIR = "dumps"  # будет создана папка, если её нет

# ============== ЛОГИКА ==============
def should_exclude(file_path):
    return os.path.splitext(file_path)[1].lower() in EXCLUDE_EXTS

def write_file(dump, file_path, rel_path):
    dump.write(f"\n{'='*80}\n")
    dump.write(f"Файл: {rel_path}\n")
    dump.write(f"{'='*80}\n")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            dump.write(f.read())
    except Exception as e:
        dump.write(f"[Ошибка чтения файла: {e}]")
    dump.write("\n")

def main():
    project_root = os.getcwd()  # Запускаем строго из корня проекта
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(DUMP_DIR, exist_ok=True)
    dump_path = os.path.join(DUMP_DIR, f"project_dump_{now}.txt")

    with open(dump_path, "w", encoding="utf-8") as dump:
        # Файлы из корня
        for fname in INCLUDE_FILES:
            abs_path = os.path.join(project_root, fname)
            if os.path.exists(abs_path) and not should_exclude(abs_path):
                write_file(dump, abs_path, fname)

        # Файлы из папок
        for folder in INCLUDE_DIRS:
            folder_path = os.path.join(project_root, folder)
            if not os.path.exists(folder_path):
                continue
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    if should_exclude(abs_path):
                        continue
                    rel_path = os.path.relpath(abs_path, project_root)
                    write_file(dump, abs_path, rel_path)

    print(f"✅ Дамп сохранён: {dump_path}")

if __name__ == "__main__":
    main()
