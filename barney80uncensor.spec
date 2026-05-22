# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['barney80uncensor.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\CdemyTeilnehmer\\AppData\\Local\\Python\\pythoncore-3.14-64\\Lib\\site-packages\\UnityPy', 'UnityPy')],
    hiddenimports=['UnityPy.resources', 'UnityPy', 'lzma'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='barney80uncensor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
