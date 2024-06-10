import dns.resolver
import fade
import argparse
import sys
import time

def print_progress(progress, total, duration, req_per_sec, errors):
    percent = 100 * (progress / float(total))
    progress_msg = (f"-- Progress: [{progress}/{total}] "
                    f"-- {req_per_sec:.0f} req/sec "
                    f"-- Duration: [{duration}] "
                    f"-- Errors: {errors} --")
    sys.stdout.write(f"\33[1;33m" + f"\r{progress_msg}")
    sys.stdout.flush()

def main(wordlist_path, target):
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
                        ░                    ░  by Berg, 2022"""))

    res = dns.resolver.Resolver()

    with open(wordlist_path) as file:
        subdomains = file.read().splitlines()

    total = len(subdomains)
    count = 0
    errors = 0
    start_time = time.time()

    try:
        for i, sub in enumerate(subdomains, start=1):
            try:
                sub_target = f"{sub}.{target}"
                result = res.resolve(sub_target, "A")

                for ip in result:
                    sys.stdout.write('\r' + ' ' * 100 + '\r')  # Clear the progress line
                    print(f"\33[1;32m[+]\33[m Subdomain Found! \33[1;34mSUB: {sub_target:<30} IP: {ip}\33[m")
                    count += 1

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
        print(f"\n\n\33[1;31mKeyboard interrupt (Ctrl+C). Exiting...\n")
    finally:
        sys.stdout.write('\n')  # Ensure the final message is on a new line
        print(fade.fire(f"A total of {count} subdomains were found for {target}"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain search tool.")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist for the attack")
    parser.add_argument("-t", "--target", required=True, help="Target Domain")

    args = parser.parse_args()
    main(args.wordlist, args.target)
