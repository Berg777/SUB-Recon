#!/usr/bin/env python3

import dns.resolver
import fade
import argparse
import sys
import time
import requests

def print_progress(progress, total, duration, req_per_sec, errors):
    percent = 100 * (progress / float(total))
    progress_msg = (f"-- Progress: [{progress}/{total}] "
                    f"-- {req_per_sec:.0f} req/sec "
                    f"-- Duration: [{duration}] "
                    f"-- Errors: {errors} --")
    sys.stdout.write(f"\33[1;33m" + f"\r{progress_msg}")
    sys.stdout.flush()

def get_subdomains_from_crtsh(target):
    url = f"https://crt.sh/?q=%25.{target}&output=json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"\33[1;31m[!] Error fetching data from crt.sh for {target}\33[m")
        return []

    subdomains = set()
    for entry in response.json():
        common_name = entry['common_name']
        name_value = entry['name_value']
        subdomains.add(common_name)
        subdomains.add(name_value)

    return list(subdomains)

def resolve_subdomains(subdomains, target, res, subs_found, subs_ips_found):
    total = len(subdomains)
    errors = 0
    start_time = time.time()

    try:
        for i, sub in enumerate(subdomains, start=1):
            try:
                sub_target = sub if sub.endswith(target) else f"{sub}.{target}"
                result = res.resolve(sub_target, "A")

                for ip in result:
                    sys.stdout.write('\r' + ' ' * 100 + '\r')  # Clear the progress line
                    print(f"\33[1;32m[+]\33[m \33[1mSubdomain Found!\33[m \33[1;34mSUB:\33[m \33[1;36m{sub_target:<30}\33[m \33[1;34mIP:\33[m \33[1;36m{ip}\33[m")
                    subs_found.append(sub_target)
                    subs_ips_found.append(f"{sub_target} {ip}")

            except dns.resolver.NoAnswer:
                errors += 1

            except dns.resolver.NXDOMAIN:
                errors += 1

            except KeyboardInterrupt:
                raise KeyboardInterrupt

            except Exception:
                errors += 1

            duration = time.time() - start_time
            req_per_sec = i / duration if duration > 0 else 0
            print_progress(i, total, time.strftime("%H:%M:%S", time.gmtime(duration)), req_per_sec, errors)

    except KeyboardInterrupt:
        print(f"\n\n\33[1;31m[!] Keyboard interrupt (Ctrl+C). Exiting...\n")
        sys.exit(0)
    finally:
        sys.stdout.write('\n')  # Ensure the final message is on a new line

def main(wordlist_path, target, output_subs, output_subs_ips, use_crtsh):
    print(fade.fire("""
  ██████  █    ██  ▄▄▄▄       ██▀███  ▓█████  ▄████▄   ▒█████   ███▄    █ 
▒██    ▒  ██  ▓██▒▓█████▄    ▓██ ▒ ██▒▓█   ▀ ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █ 
░ ▓██▄   ▓██  ▒██░▒██▒ ▄██   ▓██ ░▄█ ▒▒███   ▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒
  ▒   ██▒▓▓█  ░██░▒██░█▀     ▒██▀▀█▄  ▒▓█  ▄ ▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒
▒██████▒▒▒▒█████▓ ░▓█  ▀█▓   ░██▓ ▒██▒░▒████▒▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▒▓███▀▒   ░ ▒▓ ░▒▓░░░ ▒░ ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
░ ░▒  ░ ░░░▒░ ░ ░ ▒░▒   ░      ░▒ ░ ▒░ ░ ░  ░  ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒░
░  ░  ░   ░░░ ░ ░  ░    ░      ░░   ░    ░   ░        ░ ░ ░ ▒     ░   ░ ░ 
      ░     ░      ░            ░        ░  ░░ ░          ░ ░           ░ 
                        ░                    ░  by Berg, 2024"""))

    res = dns.resolver.Resolver()

    subs_found = []
    subs_ips_found = []

    if use_crtsh:
        crtsh_subdomains = get_subdomains_from_crtsh(target)
        print(f"\n\33[1;34m[*]\33[m \33[1;34mResolving subdomains from crt.sh for {target}\33[m")
        resolve_subdomains(crtsh_subdomains, target, res, subs_found, subs_ips_found)
    else:
        with open(wordlist_path) as file:
            wordlist_subdomains = file.read().splitlines()
        print(f"\n\33[1;33m[*]\33[m \33[1;34mResolving subdomains from wordlist for {target}\33[m")
        resolve_subdomains(wordlist_subdomains, target, res, subs_found, subs_ips_found)

    print(f"\n\33[1;33m[*]\33[m \33[1;34mA total of\33[m \33[1;36m{len(subs_found)}\33[m \33[1;34msubdomains were found for\33[m \33[1;36m{target}\33[m")

    if output_subs:
        with open(output_subs, 'w') as f:
            for sub in subs_found:
                f.write(f"{sub}\n")

    if output_subs_ips:
        with open(output_subs_ips, 'w') as f:
            for sub_ip in subs_ips_found:
                f.write(f"{sub_ip}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain search tool.")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist for the attack")
    parser.add_argument("-t", "--target", required=True, help="Target Domain")
    parser.add_argument("-oS", "--output-subs", help="Output file for subdomains")
    parser.add_argument("-oSIP", "--output-subs-ips", help="Output file for subdomains and IPs")
    parser.add_argument("-c", "--crt", action="store_true", help="Use crt.sh to find subdomains")

    args = parser.parse_args()

    if args.crt:
        main(None, args.target, args.output_subs, args.output_subs_ips, use_crtsh=True)
    elif args.wordlist:
        main(args.wordlist, args.target, args.output_subs, args.output_subs_ips, use_crtsh=False)
    else:
        parser.error("You must specify either --crt or --wordlist")
