import time

def NOD(a,b):
	r = a % b
	while not(r == 0):
		a = b
		b = r
		r = a % b
		
	return b

class polynom():
	def __init__(self,c=[]):
		self.c = c
		self.check()
	def check(self):
		res = self
		while res[res.deg()]==0 and res.deg() > 0:
			res.c.pop()
		self = res
		return res
		
	def __str__(self):
		if self == 0:
			return '0'
		res=''
		for i in range(len(self)):
			if self[i] == 0:
				continue
			res += '-' if self[i] < 0 else '' if i == 0 else '+'
			res += str(abs(self[i])) if abs(self[i]) != 1 or i == 0 else ''
			res += 'x' if i != 0 else ''
			res += '^'+str(i) if i != 0 and i != 1 else '' 
		return res
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
			return polynom(res).check()	
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
			return polynom(res).check()
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
	def __divmod__(self,other):		
		if type(other) != polynom:
			return self*(1/other)
		else:
			if other.deg() > self.deg():
				res,mod = [0],self.check()
			else:
				mod = polynom(self.c.copy())
				res = [0 for i in range(len(self)-len(other)+1)]
				for step in range(len(self) - len(other),-1,-1):
					res[step] = mod[other.deg()+step] / other[other.deg()]
					mod = mod - other*res[step]*polynom([0 if i != step else 1 for i in range(step+1)])
		return polynom(res).check(),mod.check()
	def __truediv__(self,other):
		return self.__divmod__(other)[0]
	def __mod__(self,other):
		return self.__divmod__(other)[1]
	
	def derivative(self):
		res = []
		for i in range(1,len(self)):
			res.append(self[i]*i)
		return polynom(res).check()
	def del_smth(self):
		hf = polynom(self.c.copy())
		hd = hf.derivative()
		return hf/NOD(hf,hd)
	
	def __eq__(self,other):
		h = other
		if type(h) != polynom:
			h = polynom([h])
		if len(self) != len(h):
			return False
		for i in range(len(self)):
			if self[i] != h[i]:
				return False
		return True
	
a = polynom([1,0,-2,0,1])
print(a.del_smth())
