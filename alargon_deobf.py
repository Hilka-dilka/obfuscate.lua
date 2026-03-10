import binascii
import os
import re

def get_unique_filename(directory, base_name, extension):
    # Создаем папку, если её нет
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{base_name}{extension}"
    path = os.path.join(directory, filename)
    
    # Если файл уже есть, добавляем цифру (1, 2, 3...)
    counter = 1
    while os.path.exists(path):
        filename = f"{base_name}_{counter}{extension}"
        path = os.path.join(directory, filename)
        counter += 1
    return path

def deobfuscate():
    print("--- Alargon's Deobfuscator (Input Text Mode) ---")
    print("Вставьте ваш ОБФУСЦИРОВАННЫЙ код. После вставки нажмите Enter, затем Ctrl+Z (Win) или Ctrl+D (Unix):")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    content = "\n".join(lines)
    if not content.strip():
        print("Ошибка: Код не введен!")
        return

    # Ищем HEX-строку внутри кавычек: local l1lI = '...'
    # Мы ищем именно тот паттерн, который создает твой обфускатор
    match = re.search(r"local l1lI\s*=\s*'([a-fA-F0-9]+)'", content)
    
    if not match:
        print("\n[!] Ошибка: Не удалось найти зашифрованные данные.")
        print("Убедитесь, что вы вставили полный скрипт, содержащий: local l1lI = '...'")
        return

    try:
        hex_data = match.group(1)
        # Декодируем из HEX обратно в текст (Lua исходник)
        decoded_source = binascii.unhexlify(hex_data).decode('utf-8')

        # Сохранение в папку deobfuscated
        output_path = get_unique_filename("deobfuscated", "restored_script", ".lua")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decoded_source)

        print("\n" + "="*40)
        print(f"УСПЕХ! Скрипт расшифрован.")
        print(f"Сохранено в: {output_path}")
        print("="*40)

    except Exception as e:
        print(f"\n[!] Ошибка при обработке данных: {e}")

if __name__ == "__main__":
    deobfuscate()