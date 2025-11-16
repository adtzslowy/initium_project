# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all modules from requests and its dependencies
requests_datas, requests_binaries, requests_hiddenimports = collect_all('requests')
bs4_datas, bs4_binaries, bs4_hiddenimports = collect_all('bs4')
urllib3_datas, urllib3_binaries, urllib3_hiddenimports = collect_all('urllib3')
certifi_datas, certifi_binaries, certifi_hiddenimports = collect_all('certifi')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=requests_binaries + bs4_binaries + urllib3_binaries + certifi_binaries,
    datas=[
        ('FONT_PATH_PLACEHOLDER', 'pyfiglet/fonts'),
    ] + requests_datas + bs4_datas + urllib3_datas + certifi_datas,
    hiddenimports=[
        'requests',
        'urllib3',
        'bs4',
        'certifi',
        'charset_normalizer',
        'idna',
        'soupsieve',
        'pyfiglet',
    ] + requests_hiddenimports + bs4_hiddenimports + urllib3_hiddenimports + certifi_hiddenimports + collect_submodules('requests') + collect_submodules('urllib3'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='initium',
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
