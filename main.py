import logging
import aiohttp
import asyncio
from collections import defaultdict
import traceback
from colorama import Fore


def print_header():
    header = r"""
 ██▓███   ██▀███   ▒█████  ▒██   ██▒▓██   ██▓    ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒▒ █ █ ▒░ ▒██  ██▒   ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░░  █   ░  ▒██ ██░   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ █ █ ▒   ░ ▐██▓░   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██▒ ▒██▒  ░ ██▒▓░   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ██▒▒▒    ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░░   ░▒ ░ ▓██ ░▒░      ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░         ░░   ░ ░ ░ ░ ▒   ░    ░   ▒ ▒ ░░     ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
            ░         ░ ░   ░    ░   ░ ░        ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                     ░ ░        ░                       ░                               
                                    
                                            ||   Autor: dEEpEst              ||                                    
                                            ||   Version: 1.0                ||
                                            ||   Home: level23hacktools.com  ||
""" 
    print(Fore.RED + header + Fore.GREEN)
print_header()



# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Semaphore to limit concurrent tasks
sem = asyncio.Semaphore(5000)

# Lock to handle shared resource
lock = asyncio.Lock()

# A dictionary to store the counts of working proxies for each protocol
working_proxies_count = defaultdict(int)

# A dictionary to store the working proxies for each protocol
working_proxies = defaultdict(list)

# A dictionary to store the counts of non-working proxies for each protocol
non_working_proxies_count = defaultdict(int)

async def check_proxy(session, proxies, protocol_type, total_proxies):
    while proxies:
        proxy = proxies.pop(0)
        if protocol_type.lower() in ['http', 'https', 'socks4', 'socks5']:
            try:
                async with sem, session.get('https://www.google.com', proxy=f'{protocol_type}://{proxy}', timeout=5) as response:
                    async with lock:
                        if response.status == 200:
                            working_proxies_count[protocol_type] += 1
                            working_proxies[protocol_type].append(proxy)
                        else:
                            non_working_proxies_count[protocol_type] += 1
            except Exception as e:
                logging.error(f'Error with proxy {proxy} and protocol {protocol_type}: {e}', exc_info=True)
                async with lock:
                    non_working_proxies_count[protocol_type] += 1
            finally:
                print(f'Checked: {total_proxies-len(proxies)}/{total_proxies} proxies. Valid: {working_proxies_count[protocol_type]}. Unvalid: {non_working_proxies_count[protocol_type]}', end='\r')

async def check_proxies(session, protocol_type, proxies):
    print(f"\nChecking proxies for protocol: {protocol_type}")
    await check_proxy(session, proxies, protocol_type, len(proxies))
    print(f'\n{protocol_type}: Valid: {working_proxies_count[protocol_type]}, Unvalid: {non_working_proxies_count[protocol_type]}')

def write_proxies_to_file(protocol_type):
    file_name = f'{protocol_type}_working_proxies.txt'
    with open(file_name, 'w') as file:
        for proxy in working_proxies[protocol_type]:
            file.write(proxy + '\n')

def load_proxies():
    file_name = 'proxies.txt'
    proxies = []
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                proxy = line.strip()
                proxies.append(proxy)
    except FileNotFoundError:
        print("File not found.")
    return proxies

async def menu():
    protocol_types = ['https', 'http', 'socks5', 'socks4']
    options_text = "\n".join([f"{i+1}. {protocol_type.upper()}" for i, protocol_type in enumerate(protocol_types)])
    print("Please select an option:")
    print(options_text)
    print("5. All protocols")
    option = input("Choose an option: ")
    proxies = load_proxies()

    tasks = []
    async with aiohttp.ClientSession() as session:
        if option in [str(i+1) for i in range(4)]:
            protocol_type = protocol_types[int(option)-1]
            tasks.append(asyncio.create_task(check_proxies(session, protocol_type, proxies.copy())))
            await asyncio.gather(*tasks)
            write_proxies_to_file(protocol_type)
        elif option == '5':
            for i in range(4):
                protocol_type = protocol_types[i]
                tasks.append(asyncio.create_task(check_proxies(session, protocol_type, proxies.copy())))
            await asyncio.gather(*tasks)
            for protocol_type in protocol_types:
                write_proxies_to_file(protocol_type)
        else:
            print("Invalid option. Please select a number between 1 and 5.")

if __name__ == "__main__":
    asyncio.run(menu())
