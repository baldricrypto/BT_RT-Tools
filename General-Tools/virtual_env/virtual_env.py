import os

directory = input("Input the name for the desired working directory (if you are already in your desired dir a simple . will suffice): ")
os.chdir(f'{directory}')
path=os.getcwd()
print(f"\n\nYour current working directory is {path} \n\nIf this is not correct stop the program here.\n\n")
folder = input("Input folder name for virtual enviroment: ")
os.mkdir(folder)
os.chdir(folder)
os.system(f"python -m venv venv ")
print("\nVirtual Environment created enjoy coding... Don't forget to activate your venv")
