# -*- mode: python ; coding: utf-8 -*-

from kivymd import hooks_path as kivymd_hooks_path
path = os.path.abspath(".")

a = Analysis(
    ['src/gateway/main.py'],
    pathex=[path],
    binaries=[],
    datas=[
        ('src/gateway/*.py', '.'), 
    ],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    debug=False,
    strip=False,
    upx=True,
    name="app_name",
    console=True,
)
