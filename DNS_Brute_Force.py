# requirements 
# pip install dnspython && pip install fade

import dns.resolver
import fade

print(fade.fire("""▓█████▄  ███▄    █   ██████     ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓▓█████ 
▒██▀ ██▌ ██ ▀█   █ ▒██    ▒    ▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▓█   ▀ 
░██   █▌▓██  ▀█ ██▒░ ▓██▄      ▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒███   
░▓█▄   ▌▓██▒  ▐▌██▒  ▒   ██▒   ▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄ 
░▒████▓ ▒██░   ▓██░▒██████▒▒   ░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░ ░▒████▒
 ▒▒▓  ▒ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░   ░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░
 ░ ▒  ▒ ░ ░░   ░ ▒░░ ░▒  ░ ░   ▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░     ░ ░  ░
 ░ ░  ░    ░   ░ ░ ░  ░  ░      ░    ░   ░░   ░  ░░░ ░ ░   ░         ░   
   ░             ░       ░      ░         ░        ░                 ░  ░
 ░                                   ░ by Berg, 2022"""))

res = dns.resolver.Resolver()
caminho = input(fade.fire("Digite o caminho da wordlist desejada para o ataque: "))
arquivo = open(caminho)
subdominios = arquivo.read().splitlines()
count  = 0

alvo = input(fade.fire("Digite o alvo desejado: "))

for sub in subdominios:

    try:
        
        sub_alvo = sub + "." + alvo
        resultado = res.resolve(sub_alvo, "A")

        for ip in resultado:

            print(fade.fire(f"{sub_alvo.strip():-<50}->  {ip}"))
            count += 1

    except:
        pass

print(fade.fire(f"No total foram encontrados {count} subdomínios para {alvo}"))
