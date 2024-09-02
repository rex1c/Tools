from cryptography import x509
from cryptography.hazmat.backends import default_backend
import re
import ssl
import socket

file = open("certs" , "r")
hosts = file.readlines()

result = []
port = 443

for hostname in hosts:
    hostname = hostname[:-1]
    # Create an SSL context and disable hostname verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        # Connect to the server and retrieve the certificate
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get the server's certificate in DER format and convert it to PEM
                cert = ssock.getpeercert(True)
                pem_cert = ssl.DER_cert_to_PEM_cert(cert)

        # Load the certificate
        cert = x509.load_pem_x509_certificate(pem_cert.encode(), default_backend())

        # Extract the Common Name (CN) from the Subject
        subject_cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        result.append(subject_cn)

        # Extract the Subject Alternative Name (SAN) values
        san_extension = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san_dns_names = san_extension.value.get_values_for_type(x509.DNSName)
        for dns in san_dns_names:
            result.append(dns)
    except:
        pass
result = list(set(result))
f = open("cert.res" , "w")
for res in result:
    f.write(res+"\n")
f.close()
