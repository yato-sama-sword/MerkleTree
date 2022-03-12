from hashlib import sha256

if __name__ == '__main__':
    print(sha256('mySecret'.encode()).hexdigest())
