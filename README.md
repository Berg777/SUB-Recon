# Subdomain Search Tool in Python

SubRecon is a command-line tool to discover subdomains of a target domain using a wordlist and crt.sh records. It also resolves the found subdomains to obtain their respective IP addresses.

<br>

<div align="center">
<img src="static/subrecon.png">
</div>

---

# Features

```txt
- Subdomain search using a wordlist
- Subdomain search using crt.sh records
- Displays a progress bar during the search.
- Provides real-time updates of found subdomains.
- Resolves subdomains to IP addresses
- Option to save found subdomains to a file
- Option to save found subdomains and their IPs to a file
```

---

# Requirements

- Python 3.x
- Required libraries: dnspython, fade, argparse

<br>

You can install the required libraries using the following command:

```python
pip install dnspython fade argparse
```

---

# Usage

Basic Usage:

The script can be executed from the command line by specifying the path to the wordlist and the target domain. Here is an example of usage:

```sh
python subrecon.py -w wordlist.txt -t targetdomain.com
```

In this example, the script will use the wordlist.txt file to search for subdomains of targetdomain.com.

# Parameters

```txt
-w or --wordlist: Path to the wordlist for subdomain search
-t or --target: Target domain
-c or --crt: Use subdomain search via crt.sh
-oS or --output-subs: Output file for found subdomains
-oSIP or --output-subs-ips: Output file for found subdomains and their respective IPs
```

## Examples

```txt
python subrecon.py -w wordlist.txt -t domain.com

python subrecon.py -c -t domain.com

python subrecon.py -w wordlist.txt -t domain.com -oS subdomains.txt

python subrecon.py -w wordlist.txt -t domain.com -oSIP subdomains_ips.txt
```

