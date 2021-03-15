class diffieHellman:
    def __init__(self, p = 486377, g = 54321):
        self.p = p
        self.g = g % p
    
    def setValue(self, a):
        return (self.g ** a) % self.p

    def getKey(self, B, a):
        return ((B ** a) % self.p).to_bytes(16, 'big')