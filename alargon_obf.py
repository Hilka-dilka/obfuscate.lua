import binascii
import os

def get_unique_filename(directory, base_name, extension):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{base_name}{extension}"
    path = os.path.join(directory, filename)
    
    counter = 1
    while os.path.exists(path):
        filename = f"{base_name}_{counter}{extension}"
        path = os.path.join(directory, filename)
        counter += 1
    return path

def obfuscate():
    print("--- Alargon's Ultimate Obfuscator V3 (Hex-Base) ---")
    print("Вставьте ваш Lua код. После вставки нажмите Enter, затем Ctrl+Z (Win) или Ctrl+D (Unix):")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    source = "\n".join(lines)
    if not source.strip():
        print("Ошибка: Код не введен!")
        return

    # Переводим в HEX
    hex_data = binascii.hexlify(source.encode()).decode()

    header = "--[[ Obfuscated by Alargon's Obfuscator ]]"
    loader = (
        f"local l1lI = '{hex_data}'; "
        "local Ill1 = ''; "
        "for i = 1, #l1lI, 2 do "
        "Ill1 = Ill1 .. string.char(tonumber(l1lI:sub(i, i + 1), 16)) "
        "end; "
        "local success, result = pcall(function() return loadstring(Ill1) end); "
        "if success and result then task.spawn(result) else warn('Alargon Obf Error: ' .. tostring(result)) end"
    )

    final_script = f"{header} {loader}"

    # Сохранение в папку obfuscated
    output_path = get_unique_filename("obfuscated", "alargon_obfuscated", ".lua")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_script)
    
    print("\n" + "="*40)
    print(f"ГОТОВО! Файл сохранен в: {output_path}")
    print("="*40)

if __name__ == "__main__":
    obfuscate()