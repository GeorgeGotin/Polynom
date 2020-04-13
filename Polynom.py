class polynom():
	def __init__(self,c=[]):
		self.c = c
	def __str__(self):
		res=''
		for i in range(len(self)):
			res += (('+' if self[i] > 0 else '') +(str(self[i]) if self[i] != 1 else '') + ('x' if i != 0 else '') +('^'+str(i) if i > 1 else '')) if self[i] != 0 else ''
		return res[1:]
	def deg(self):
		return len(self)-1
	
	def __iter__(self):
		self.counter = 0
		return self
	def __next__(self):
		if self.counter == len(self):
			del self.counter
			raise StopIteration
		else:
			self.counter += 1
			return self[self.counter-1]
	
	def __getitem__(self,i):
		if type(i) != slice:
			return self.c[i] if i <= self.deg() else 0
		else:
			res = []
			for j in range(i.start,i.stop,(i.step if i.step != None else 1)):
				res.append(j)
			return res
	def __len__(self):
		return len(self.c)
		
	def __add__(self,other):
		if type(other) != polynom:
			return polynom([self[0]+other]+self[1:len(self)])
		else:
			res = []
			for i in range(max(len(self),len(other))):
				res.append(self[i]+other[i])
			return polynom(res)		
	def __radd__(self,other):
		return self+other
	
	def __mul__(self,other):
		if type(other) != polynom:
			return polynom([self[i]*other for i in range(len(self))])
		else:
			res = []
			for k in range(self.deg()+other.deg()+1):
				res.append(0)
				for i in range(k+1):
					res[k]+=self[i]*other[k-i]
			return polynom(res)	
	def __rmul__(self,other):
		return self*other
	def __pow__(self,p):
		res=1
		for i in range(p):
			res *=self
		return res
	
	def __sub__(self,other):
		return self+other*(-1)	
	def __rsub__(self,other):
		return (-1)*self+other
	def __neg__(self):
		return self*(-1)
		
	def __floordiv__(self,other):
		if type(other) != polynom:
			return self*(1/other)
		else:
			if other.deg() > self.deg():
				return polynom([1])
			else:
				mod = polynom(self.c.copy())
				res = [0 for i in range(len(self)-len(other)+1)]
				for step in range(len(self) - len(other),-1,-1):
					res[step] = mod[other.deg()+step] / other[other.deg()]
					mod = mod - other*res[step]*polynom([0 if i != step else 1 for i in range(step+1)])
			
				return polynom(res)
	def __mod__(self,other):
		if type(other) != polynom:
			return 0
		else:
			if other.deg() > self.deg():
				return polynom([1])
			else:
				mod = polynom(self.c.copy())
				res = [0 for i in range(len(self)-len(other)+1)]
				for step in range(len(self) - len(other),-1,-1):
					res[step] = mod[other.deg()+step] / other[other.deg()]
					mod = mod - other*res[step]*polynom([0 if i != step else 1 for i in range(step+1)])
			
				return mod
	
a = polynom([0,6,4,8])
b = polynom([4,2])
print(a,a+b,a*b)
for i in a:
	print(i,a.counter)
print(a.counter)
