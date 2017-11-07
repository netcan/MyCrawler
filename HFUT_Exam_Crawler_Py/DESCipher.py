from Crypto.Cipher import DES


class DESCipher:
    def __init__(self, key):
        if len(key) != 8:
            raise ValueError('Key must be 8 bytes long')
        self.cipher = DES.new(key, DES.MODE_ECB)

    def encrypt(self, content):
        if not isinstance(content, str):
            raise TypeError
        while len(content.encode()) % 8 != 0:
            content += chr(23)

        return self.cipher.encrypt(content)

    def decrypt(self, raw):
        if not isinstance(raw, bytes):
            raise TypeError
        content = self.cipher.decrypt(raw)
        length = len(raw)
        for c in content[::-1]:
            if c == 23:
                length -= 1
            else:
                break
        return content[:length].decode('utf8')

