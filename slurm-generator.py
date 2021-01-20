import json
import random
import ipaddress
import sys
from pprint import pprint

# roa length from command line in numbers of 100,000s
v4len = 100000 * int(sys.argv[1])
v6len = 100000 * int(sys.argv[2])

# Chunks of the file
head = """
{
  "slurmVersion": 1,
  "validationOutputFilters": {
    "prefixFilters": [],
    "bgpsecFilters": []
  },
  "locallyAddedAssertions": {
    "prefixAssertions":"""
middle = """
      {
        "asn": 64496,
        "prefix": "198.51.100.0/24",
        "comment": "My other important route"
      },
      {
        "asn": 64496,
        "prefix": "2001:DB8::/32",
        "maxPrefixLength": 48,
        "comment": "My other important de-aggregated routes"
      }
"""
tail = """
    ,
    "bgpsecAssertions": []
  }
} """

# dictionary to hold the info
mdict = {}
# list to go inside the dictionary
prefixAssertions = []

# stuff to generate random ASNs and IPv4 and IPv6 addrs
MAX_ASN = 2**16
MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1


def random_asn():
    return random.randint(0, MAX_ASN)

def random_ipv4():
    return  ipaddress.IPv4Address._string_from_ip_int(
        random.randint(0, MAX_IPV4)
    )

def random_ipv6():
    return ipaddress.IPv6Address._string_from_ip_int(
        random.randint(0, MAX_IPV6)
    )

def random_ipv4_cidr():
    # Random prefix length for IPv4 from /8 to /24
    mask = random.randint(8,24)
    n = random.randint(0, (2**mask))
    m = str(bin(n))[2::].ljust(((len(str(bin(n)))-2)+(32-mask)),"0")
    return str(ipaddress.IPv4Address(int(m,2)))+"/"+str(mask)

def random_ipv6_cidr():
    # Random prefix length for IPv6 from /20 to /64
    mask = random.randint(20,64)
    n = random.randint(0, (2**mask))
    m = str(n).ljust((128-mask),"0")
    m = str(bin(n))[2::].ljust(((len(str(bin(n)))-2)+(128-mask)),"0")
    return str(ipaddress.IPv6Address(int(m,2)))+"/"+str(mask)

# build a random ROA
def build_roas(v4,v6):
   for i in range(v4):
       roa = {}
       roa['asn'] = random_asn()
       roa['prefix'] = random_ipv4() + "/" + str(random.randrange(10,32))
       prefixAssertions.append(roa)
   for i in range(v6):
       roa = {}
       roa['asn'] = random_asn()
       roa['prefix'] = random_ipv6() + "/" + str(random.randrange(32,128))
       prefixAssertions.append(roa)
   j = json.dumps(prefixAssertions)
   return j


# build the SLURM file
def build_slurm_file(v4len,v6len):
	print(f"Building SLURM file of {v4len} v4 and {v6len} v6 prefixes ")
	#print(fname)
	roas = build_roas(v4len,v6len)
	#exit()
	fname = "slurm-" + str(v4len) + "-" + str(v6len) + "k.json"
	f = open(fname,'w')
	f.write(head)
	f.write(roas)
	f.write(tail)

build_slurm_file(v4len,v6len)

import random
import ipaddress
mask = random.randint(8,24)
n = random.randint(0, (2**mask))
m = str(bin(n))[2::].ljust(((len(str(bin(n)))-2)+(32-mask)),"0")
ipaddress.IPv4Address(int(m,2))
