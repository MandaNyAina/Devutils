import os

def execute(command_line: str):
    try:
        return os.popen(command_line).read()
    except:
        print("Erreur de commande")

def mv_file_in_tmp(filename, destination):
    try:
        execute(f"sudo mv tmp/{filename} {destination}")
    except:
        print("Erreur de commande")

def generate_tmp(filename):
    try:
        open(f"tmp/{filename}", "x").close()
    except FileExistsError:
        print("Le fichier de configuration existe deja")

def delete_tmp(filename):
    try:
        os.remove(f"tmp/{filename}")
    except:
        print("Erreur du suppression du fichier tmp")