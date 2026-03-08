import secrets

class CertificateManager:

    def generate_certificate(self):

        return secrets.token_hex(32)

    def validate_certificate(self, cert):

        return len(cert) > 20
