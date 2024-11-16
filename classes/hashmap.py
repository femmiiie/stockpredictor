# So my idea for the hash map is that each "bucket" inside the array is a stock, then we append a tuple
# with a key which is the date and a value which is a vector with the stock properties like open prize, 
# close prize, volume...
# For example: key = 2013-01-02 and value = [16.6,19.6,19.8,19.34,19.77,56051800] which correspond to 
# Adj close, close, high, low, open and volume.
# Adj close: Adjusted close is the closing price after adjustments for all applicable splits and dividend distributions.

class HashMap:
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity # The hash function works even if the key is a date like 2013-01-13

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return None 

    def __len__(self):
        return self.size

