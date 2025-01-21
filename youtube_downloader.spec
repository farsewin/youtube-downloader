# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import tkinter as tk

# Add paths to tcl and tk libraries
tcl_dir = os.path.join(sys.base_prefix, 'tcl', 'tcl8.6')
tk_dir = os.path.join(sys.base_prefix, 'tcl', 'tk8.6')

block_cipher = None

# Get TCL/TK paths
tcl_files = [(os.path.join(tcl_dir, x), 'tcl') for x in os.listdir(tcl_dir) if x.endswith('.tcl')]
tk_files = [(os.path.join(tcl_dir, x), 'tk') for x in os.listdir(tcl_dir) if x.endswith('.tcl')]

a = Analysis(
    ['youtube_downloader.py'],
    pathex=[],
    binaries=[('ffmpe.exe', '.')],  # Include FFmpeg
    datas=[
        (tcl_dir, 'tcl'),
        (tk_dir, 'tk'),
        *tcl_files,  # Include TCL files
        *tk_files,   # Include TK files
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.ttk',
        'tkinter.messagebox',
        '_tkinter',
        'yt_dlp.utils',
        'tcl_tk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTube Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI only
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add this line to include the icon
)
