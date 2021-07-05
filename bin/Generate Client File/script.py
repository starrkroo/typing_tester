
import socket

updated = 'Error'

print("Reading code from template...")
with open('assets_under/base.txt', 'r') as f:
    read_data = f.read()
    hostname = socket.gethostname()
    local_ipv4 = socket.gethostbyname(hostname)
    updated = read_data.replace('<ENTER_NEW_SOCKET_ADDRESS>', "{!r}".format(str(local_ipv4)))
print("Done\n")

print("Writing data into client_side.py file..\n")
with open('client_side.py', 'w') as f:
    f.write(updated)

print('Done.')
