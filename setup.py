from cx_Freeze import setup, Executable

base = "Win32GUI"   

executables = [Executable("Chess Online.py", base=base)]



setup(
    name = "Chess Online",
    # options = options,
    version = "1.0.0",
    description = 'Simple Chess Game',
    author="Dhananjay Puranik",
    executables = executables
)