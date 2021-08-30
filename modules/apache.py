from .helpers import execute, generate_tmp, mv_file_in_tmp


class Apache:
    apache_path = "/etc/apache2/sites-available/"
    host_file = "/etc/hosts"
    site_enabled_path = "/etc/apache2/sites-enabled/"

    def __init__(self):
        pass

    def new_site(self):
        while True:
            Site_name = str(input("Nom du site (pas d'espace): "))
            while True:
                try:
                    port = int(input("Port : "))
                    break
                except:
                    print("Le port n'est pas valide")
                    continue
            ServerName = str(input("Nom du domaine : "))
            ServerAdmin = str(input("Admin email : "))
            DocumentRoot = str(input("Repertoire de l'application : "))
            if input("Personnaliser le repertoire du error log ? [O/N] ").lower() == "o":
                errorLog = str(input("Entrer le repertoire"))
            else:
                errorLog = "${APACHE_LOG_DIR}/"+Site_name+"_error.log"
            if input("Personnaliser le repertoire du custom log ? [O/N] ").lower() == "o":
                customLog = str(input("Entrer le repertoire"))
            else:
                customLog = "${APACHE_LOG_DIR}/" + \
                    Site_name+"_access.log combined"

            info = f"""
Nom du site \t: {Site_name}
Port \t\t: {port}
ServerName \t: {ServerName}
ServerAdmin \t: {ServerAdmin}
DocumentRoot \t: {DocumentRoot}
ErrorLog \t: {errorLog}
CustomLog \t: {customLog} \n\n
            """
            print(info)

            if str(input("Voulez-vous continuer ? [O/N] ")).lower() == "o":
                apache_config = f"""
<VirtualHost *:{port}>
    ServerName {ServerName}
    ServerAdmin {ServerAdmin}
    DocumentRoot {DocumentRoot}
    ErrorLog {errorLog}
    CustomLog {customLog}

    <Directory {DocumentRoot}>
        Order allow,deny
        Allow from all
    </Directory>

    <FilesMatch "\.(png|jpg|gif|css|php|html|js)$">
        allow from all
    </FilesMatch>

    <FilesMatch "\.(?<!png|jpg|gif|css|php|html|js)$">
        deny from all
    </FilesMatch>
</VirtualHost>
                """
                filename = f"{Site_name}.conf"
                generate_tmp(filename)
                apache_file = open(f"tmp/{filename}", "w")
                apache_file.write(apache_config)
                apache_file.close()
                mv_file_in_tmp(filename, self.apache_path)
                execute(f"sudo a2ensite {filename}")
                self.reload_service_apache()
                print(
                    f"Ajouter {Site_name} par rapport au host si necessaire sinon vous pouvez fermer gedit")
                execute(f"sudo gedit {self.host_file}")
                break
            else:
                continue

    def reload_service_apache(self):
        execute("sudo service apache2 reload")

    def delete_logs(self, site_name):
        print(f"sudo rm -rf /var/log/apache2/{site_name}_*")
        execute(f"sudo rm -rf /var/log/apache2/{site_name}_*")

    def list_sites(self) -> list:
        list_files = str(
            execute(f"ls {self.site_enabled_path}")).strip().split("\n")
        print(f"\nVous avez {len(list_files)} site(s) :\n")
        for file in list_files:
            site = file.split(".conf")[0]
            print(f"\t- {site} \n")
        return list_files

    def delete_sites(self):
        list_sites = self.list_sites()
        selected_site = str(
            input("Veillez entrer le nom du site que vous voulez supprimer : ")) + ".conf"
        if selected_site in list_sites:
            execute(f"sudo a2dissite {selected_site}")
            execute(f"sudo rm -rf {self.apache_path + selected_site}")
            self.reload_service_apache()
            selected_site = selected_site.split(".conf")[0]
            self.delete_logs(selected_site)
            print(
                f"Enlever {selected_site} dans host sinon vous pouvez fermer gedit")
            execute(f"sudo gedit {self.host_file}")
            print("\nFelicitation")
        else:
            selected_site = selected_site.split(".conf")[0]
            print(f"\nLe site {selected_site} est introuvable")
        del selected_site

    def __del__(self):
        self.host_file = ""
        self.apache_path = ""
        self.site_enabled_path = ""


if __name__ == "__main__":
    print("Vous ne pouvez pas lancer dans le module")
