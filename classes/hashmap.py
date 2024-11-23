from copy import deepcopy

class HashMap:
	def __init__(self, initial_capacity=10):
		self.capacity = initial_capacity
		self.size = 0
		self.buckets = [[] for _ in range(self.capacity)]
		self.load_threshold = 0.7

	def rehash(self):
		old = self.buckets
		self.capacity *= 2
		self.buckets = [[] for _ in range(self.capacity)]
		self.size = 0
		for bucket in old:
			for k, v in bucket:
				self.put(k, v)


	def put(self, key, value):
		if self.size / self.capacity > self.load_threshold:
			self.rehash()

		index = hash(key) % self.capacity
		bucket = self.buckets[index]

		for i, (k, v) in enumerate(bucket):
			if k == key:
				bucket[i] = (key, value)
				return

		bucket.append((key, value))
		self.size += 1


	def get(self, key):
		index = hash(key) % self.capacity
		bucket = self.buckets[index]

		for k, v in bucket:
			if k == key:
				return v

		return None


	def __len__(self):
		return self.size


	def __iter__(self):
		for bucket in self.buckets:
			for key, val in bucket:
				yield key, val


	def __setitem__(self, a, b):
		self.put(a, b)


	def __getitem__(self, a):
		return self.get(a)


	def keys(self):
		lst = []
		for bucket in self.buckets:
			for key, _ in bucket:
				lst.append(key)
		
		return lst
