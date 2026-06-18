import binascii
import os
import re

def get_unique_filename(directory, base_name, extension):
    # Create the folder if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{base_name}{extension}"
    path = os.path.join(directory, filename)
    
    # If file already exists, add a number (1, 2, 3...)
    counter = 1
    while os.path.exists(path):
        filename = f"{base_name}_{counter}{extension}"
        path = os.path.join(directory, filename)
        counter += 1
    return path

def deobfuscate():
    print("--- Alargon's Deobfuscator (Input Text Mode) ---")
    print("Paste your OBFUSCATED code. After pasting, press Enter, then Ctrl+Z (Win) or Ctrl+D (Unix):")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    content = "\n".join(lines)
    if not content.strip():
        print("Error: No code entered!")
        return

    # Look for HEX string inside quotes: local l1lI = '...'
    # We're looking specifically for the pattern that your obfuscator creates
    match = re.search(r"local l1lI\s*=\s*'([a-fA-F0-9]+)'", content)
    
    if not match:
        print("\n[!] Error: Could not find encrypted data.")
        print("Make sure you pasted the full script containing: local l1lI = '...'")
        return

    try:
        hex_data = match.group(1)
        # Decode from HEX back to text (Lua source)
        decoded_source = binascii.unhexlify(hex_data).decode('utf-8')

        # Save to deobfuscated folder
        output_path = get_unique_filename("deobfuscated", "restored_script", ".lua")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decoded_source)

        print("\n" + "="*40)
        print(f"SUCCESS! Script decrypted.")
        print(f"Saved to: {output_path}")
        print("="*40)

    except Exception as e:
        print(f"\n[!] Error processing data: {e}")

if __name__ == "__main__":
    deobfuscate()