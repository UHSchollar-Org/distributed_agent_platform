import hashlib
from settings import LOGSIZE

def hash(message):
    digest = hashlib.sha256(message.encode()).hexdigest()
    digest = int(digest, 16) % pow(2, LOGSIZE)
    return digest