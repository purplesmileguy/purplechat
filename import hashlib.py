import hashlib

def ip_to_code(ip_address):
    # Convert IP address to bytes
    ip_bytes = ip_address.encode('utf-8')

    # Calculate the MD5 hash of the IP address
    md5_hash = hashlib.md5(ip_bytes).hexdigest()

    # Take the first 6-12 characters of the MD5 hash
    code = md5_hash[:6]  # or md5_hash[:12] for a longer code

    return code

ip_address = "192.168.1.1"
code = ip_to_code(ip_address)
print(code)