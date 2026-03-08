from security.encryption import EncryptionManager

def test_encrypt_decrypt():

    enc = EncryptionManager()

    data = b"hello"

    encrypted = enc.encrypt(data)

    decrypted = enc.decrypt(encrypted)

    assert decrypted == data
