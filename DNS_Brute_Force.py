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

alvo = input(fade.fire("Digite o alvo desejado [URL]: "))

for sub in subdominios:

    try:
        
        sub_alvo = sub + "." + alvo
        resultado = res.resolve(sub_alvo, "A")

        for ip in resultado:

            print(fade.fire(f"{sub_alvo.strip():-<50}->  {ip}"))

    except:
        pass
