import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["tkinter", 
                                                      "PyPDF2", 
                                                      "json",
                                                      "requests",
                                                      "langchain",
                                                      ]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="LocatePDF",
    version="0.1",
    description="Localizador de informaçoes no PDF via IA",
    options={"build_exe": build_exe_options},
    executables=[Executable("WindowsLocale.py", base=base)]
)