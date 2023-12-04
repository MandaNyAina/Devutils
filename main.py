from modules.modules import Option, Apache

bienvenue_message = "\n\n\t\tBIENVENUE DANS L'APPLICATION D'AUTOMATISATION DE MANDA\n\t\t"
for i in range(0, len(bienvenue_message) - 7):
    bienvenue_message += "_"
print(f"{bienvenue_message}\n\n")

option = Option("main.json")
choix = option.run()
del option

apache_server = Apache()

if choix == 1:
    apache_server.new_site()

if choix == 2:
    apache_server.list_sites()

if choix == 3:
    apache_server.delete_sites()

# if choix == 1:
#     pass

# if choix == 1:
#     pass

del choix
del apache_server