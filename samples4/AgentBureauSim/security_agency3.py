import hashlib

class Security_Agency:
    def __init__(self):
        self.__encoding = 'utf-8'
        def tmp_encode(txt):
            m = hashlib.sha256()
            m.update(bytes(str(txt),self.__encoding))
            txt_encoded = m.digest()
            return txt_encoded
        self.__encode = tmp_encode
    def get_encode(self):
        return self.__encode
