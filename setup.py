from cx_Freeze import setup, Executable

build_exe_options = {"includes": ["os", 'cryptography', '_cffi_backend', 'idna.idnadata', 'base64', 'sys', 'time']}
setup(name="Password Manager",
      version="1.2",
      description="A simple application to store and encrypt your passwords, creates a file named SECRETSTUFF which can"
                  " be filled with whatever you want to keep safe",
      requires=['cryptography', 'cffi', 'idna'],
      executables=[Executable("final.py", targetName="Password_Manager.exe")],
      options={"build.exe": build_exe_options}
      )
