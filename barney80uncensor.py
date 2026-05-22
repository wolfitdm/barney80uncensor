import UnityPy
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import sys
import os

root = tk.Tk()
root.withdraw()

mosaic_text = "MosaicField"
none_bat_subpath = r"StreamingAssets\XML\none.bat"

file_path = os.path.abspath(__file__)

file_path = os.path.dirname(file_path)

file_path = os.path.join(file_path, "Mad Island_Data", "data.unity3d")

if not os.path.isfile(file_path):
   file_path = filedialog.askopenfilename(
       title="Select File to Patch",
       filetypes=[("Unity Assets", "*.unity3d *.assets *.resource"), ("All Files", "*.*")]
   )

if file_path == "":
   raise SystemExit

print(f"Patching {Path(file_path).name}")
print(f"  Loading {Path(file_path).name} in memory...")
env = UnityPy.load(file_path)
mosaic_text_found = 0
edited_rows = 0
print(f"  Searching for \"{mosaic_text}\" in Shaders...")
for obj in env.objects:
    if obj.type.name != "Shader":
        continue
    data = obj.read()
    if mosaic_text.lower() not in str(data).lower():
        continue
    parsed = getattr(data, "m_ParsedForm", None)
    if not parsed:
        continue

    print(f"  Found \"{mosaic_text}\" in a Shader with PathId: {obj.path_id}.")
    mosaic_text_found = 1
    shader_changed = False
    for sub in parsed.m_SubShaders:
        for pass_ in sub.m_Passes:
            state = pass_.m_State
            for rt in [
                state.rtBlend0, state.rtBlend1, state.rtBlend2,
                state.rtBlend3, state.rtBlend4, state.rtBlend5,
                state.rtBlend6, state.rtBlend7,
            ]:
                if rt and hasattr(rt, "colMask") and rt.colMask.val == 15:
                    rt.colMask.val = 0
                    edited_rows += 1
                    if not shader_changed:
                        shader_changed = True

    if shader_changed:
        obj.save_typetree(data)

if not mosaic_text_found:
    print(f"\033[91m  [ERROR] No {mosaic_text} found in the file. Mosaic patch not applied.\n\033[0m")
else:
    if edited_rows == 0:
        print("\033[93m  [SKIP] No \"val = 15\" entries found. The file may already be patched.\n\033[0m")
    else:
        print(f"  {edited_rows} \"val = 15\" rows patched.\n  Saving & compressing the file... (may take a couple of minutes)")
        patched_bytes = env.file.save(packer="lz4")    #Save with compression
        #patched_bytes = env.file.save()               #Save without compression
        env.objects.clear()
        with open(file_path, "wb") as f:
            f.write(patched_bytes)

        print("\033[92m  [OK] File successfully patched.\n\033[0m") 

# Create an empty none.bat file
none_bat_fullpath = Path(file_path).parent / none_bat_subpath
print(f"Creating none.bat")
if not none_bat_fullpath.exists():
    Path(none_bat_fullpath).touch()
    print("\033[92m  [OK] Empty none.bat file created.\n\033[0m") 
else:
    print("\033[93m  [SKIP] none.bat already exists.\n\033[0m")

print("----------------------------------------")
input("Press Enter to close")