import json

class Option:
    def __init__(self, option_filename) -> None:
        option_file = open(f"modules/option/{option_filename}", "r")
        self.list_choix = json.loads(str(option_file.read()))
        option_file.close()

    def run(self):
        info_choix = "Veillez choisir parmi la liste suivante \n\n"
        for choix in self.list_choix:
            info_choix += f"\t[{self.list_choix.index(choix) + 1}] {choix['option_name']} \n"
        print(f"{info_choix}\n")
        while True:
            try:
                choix = int(input("==> "))
                if not choix or choix > len(self.list_choix):
                    raise Exception()
                del info_choix
                return choix
            except:
                print("Votre choix n'est pas dans la liste")
                continue

    def __del__(self):
        del self.list_choix
        
if __name__ == "__main__":
    print("Vous ne pouvez pas lancer dans le module")