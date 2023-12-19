# 'Freezing' the Program

You can use the `pyinstaller` package to build a standalone executable for the program (also known as **freezing**). This is useful if you want to distribute the program to non-technical users that may have trouble installing **Python** and the required packages; it is also a better experience for them. This package is included in the [requirements.txt](../requirements.txt) file, but you can also install it manually with:

```bash
pip install pyinstaller
```

After installing the package, you must add the `pyinstaller` folder to the **PATH environment variables**.

Before trying to compile, make sure that you have set up your **API keys** and that you have tested the program to make sure that they work and that you have installed all the required packages. Refer to [studyBot.md](studyBot.md) and [main.md](main.md) for more information.

**Study-Bot** needs to be compiled through a `.spec` file instead of giving a specific script directly to `pyinstaller`.

This is a configuration file that tells `pyinstaller` how to compile the program. You can use the templates provided in [Config/studyBotCLI-template.spec](../Config/studyBotCLI-template.spec) and [Config/studyBotGUI-template.spec](../Config/studyBotGUI-template.spec), depending on which version you wish to compile.

This is required because the script needs to import some additional, temporary files for the `whisper` module that are not automatically bundled by `pyinstaller`. On the `datas` parameter of the `a` object in `.spec` file, you must add the path to where these files are located:

>Note: The specific location of these files depends on your python installation.

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

For the GUI version, an additional modification is needed in the `.spec` file. On the `exe` object, the `console` parameter must be set to `False`, otherwise the program will open an additional console window when it is run, which is unnecessary and may be annoying and confusing to the user:

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

To compile the CLI version, you can run the following command from the root folder of the project:

```bash
pyinstaller Config/studyBotCLI.spec
```

To compile the GUI version, run this command instead:

```bash
pyinstaller Config/studyBotGUI.spec
```

This will create a `dist` folder with the executable and some additional files. You can distribute the executable to users so that they can run it without having to install python or the required libraries. H

However, they will need to have the `ffmpeg` command-line tool installed and added to the **PATH environment variables**, as it isn't bundled with the executable.

After completing these steps you should be able to run the program by double-clicking the executable in the `dist` folder.

Consider that, in Windows at least, the program may take up to a minute to start. This is not because of any potential inefficiencies in program itself, but because the **Antimalware Service Executable** scans the program for malware. This is a common issue with programs compiled with no certificate.