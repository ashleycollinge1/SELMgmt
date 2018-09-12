#setup.py
from cx_Freeze import setup, Executable

shortcut_table = [
    ("Startmenushortcut",        # Shortcut
     "StartMenuFolder",          # Directory_
     "SELAgent",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]run_agent.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),
    ("Startupfoldershortcut",
    	"StartupFolder",
    	"SELAgent",
    	"TARGETDIR",
    	"[TARGETDIR]run_agent.exe",
    	None,
    	None,
    	None,
    	None,
    	None,
    	None,
    	'TARGETDIR')
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data, 'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}'}

setup(
    name = "SELAgent",
    version = "0.0.3",
    options = {"build_exe": {
        'include_msvcr': True,},
        "bdist_msi": bdist_msi_options,},
    executables = [Executable("run_agent.py",base="Win32GUI", icon='connected.ico')]
    )