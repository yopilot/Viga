# FILE: main.spec
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.build_main import PYZ, EXE, COLLECT

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('src/assets/*', 'assets'),
        ('src/ui/*', 'ui'),
        ('src/database/*', 'database'),
        ('src/utils/*', 'utils'),
    ],
    hiddenimports=[
        'sqlalchemy', 
        'sqlalchemy.ext.declarative', 
        'sqlalchemy.orm', 
        'sqlalchemy.sql', 
        'sqlalchemy.engine', 
        'sqlalchemy.dialects.sqlite', 
        'sqlalchemy.dialects.mysql', 
        'sqlalchemy.dialects.postgresql', 
        'sqlalchemy.dialects.oracle',
        'pysqlite2',
        'MySQLdb',
        'PyQt6'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Vega',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set this to False to prevent the console window
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Viga',
)