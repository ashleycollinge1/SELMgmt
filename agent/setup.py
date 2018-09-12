#setup.py
from cx_Freeze import setup, Executable

setup(
    name = "SELAgent",
    version = "0.0.3",
    options = {"build_exe": {
        'include_files': ['connected.ico', 'disconnected.ico'],
        'include_msvcr': True,},
        "bdist_msi": {'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',}},
    executables = [Executable("run_agent.py",base="Win32GUI", shortcutName="SELAgent", shortcutDir="StartupFolder")]
    )