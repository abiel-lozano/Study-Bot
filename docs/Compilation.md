# 'Freezing' the Program

You can use the `pyinstaller` package to build a standalone executable for the program (also known as freezing). This is useful if you want to distribute the program to non-technical users that may have trouble installing python and the required packages; and it is also a better experience for them.

After installing the package, you must add the `pyinstaller` folder to the PATH environment variable. There are some considerations to take into account before compiling the program. Make sure that you have set up your API keys and that you have tested the program to make sure that they work and that you have installed all the required packages.

This project needs to be compiled through a `.spec` file instead of the script itself.
This file is a configuration file that tells `pyinstaller` how to compile the program. You can use the templates provided in the root directory. This is required because the script needs to import some additional, temporary files from the `whisper` module that are not automatically bundled by `pyinstaller`. On the `datas` parameter of the `a` object in `.spec` file, you must add the path to where these files are located:

```python
a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('{LOCATION OF SITE PACKAGES}/site-packages/whisper/assets/mel_filters.npz', 'whisper/assets'),
    ('{LOCATION OF SITE PACKAGES}/site-packages/whisper/assets/multilingual.tiktoken', 'whisper/assets')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

>Note: The specific location of these files depends on your python installation.

For the GUI version, an additional modification is needed to the `.spec` file. on the `exe` object, the `console` parameter must be set to `False`, otherwise the program will open a console window when it is run:

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='studyBotGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

To compile the CLI version, you can run the following command in the root folder of the project:

```bash
pyinstaller studyBotCLI.spec
```

To compile the GUI version, run this command instead:

```bash
pyinstaller studyBotGUI.spec
```

This will create a `dist` folder with the executable and some additional files. You can distribute the executable to users so that they can run it without having to install python or libraries, however, they will need to have the `ffmpeg` command-line tool installed and added to the PATH environment variable, as it isn't bundled with the executable.

After completing these steps you should be able to run the program by double-clicking the executable in the `dist` folder. Consider that, in Windows at least, the program may take up to a minute to start. This is not because of the program itself, but because the Antimalware Service Executable scans the program for malware. This is a common issue with programs compiled with no certificate.