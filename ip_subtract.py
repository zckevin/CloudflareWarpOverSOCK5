from ipaddress import ip_network
import socket

def getIP(d):
    """
    This method returns the first IP address string
    that responds as the given domain name
    """
    try:
        data = socket.gethostbyname(d)
        return data
    except Exception:
        return False

exclude_socks_server = getIP("hkhe01.clashcloud.club")

start = '0.0.0.0/0'
exclude = ['172.16.0.0/12', '192.168.0.0/16', '10.0.0.0/8', exclude_socks_server+'/32']

result = [ip_network(start)]
for x in exclude:
    n = ip_network(x)
    new = []
    for y in result:
        if y.overlaps(n):
            new.extend(y.address_exclude(n))
        else:
            new.append(y)
    result = new

print(','.join(str(x) for x in sorted(result)))

