import time
import matplotlib.pyplot as plt

def NOD(a,b):
	r = a % b
	while not(r == 0):
		a = b
		b = r
		r = a % b
		
	return b

def power(a,n):
	m = []
	while n > 0:
		m.append(n%2)
		n = n // 2
	s = 1
	q = len(m)
	for i in range(q):
		if m[q - i - 1] == 0:
			s = s*s
		else:
			s=s*s*a
	return s
	
class frac:
	def __init__(self,up,down=1):
		if down == 0:
			print('blue screen of  death(we can\'t div 0)')
			return None
		hup = float(up).as_integer_ratio()[0] * float(down).as_integer_ratio()[1]
		hdown = float(up).as_integer_ratio()[1] * float(down).as_integer_ratio()[0]
		c = NOD(int(hup),int(hdown))
		self.up = hup // c
		self.down = hdown // c
		
		
	def __str__(self):
		if self.down == 1:
			return '{}'.format(self.up)
		else:
			return ('{}/{}'.format(self.up,self.down))
			
			
	def __add__(self,other):
		if type(other) == frac:
			return frac(self.up*other.down+self.down*other.up,self.down*other.down)
		else:
			return self+frac(other)
			
	def __radd__(self,other):
		return self + other
			
	
	def __sub__(self,other):
		if type(other) == frac:
			return self + frac(-1*other.up,other.down)
		else:
			return self + frac(-1*other)
			
	def __rsub__(self,other):
		return -self + other		
			
			
	def __mul__(self,other):
		if type(other) == frac:
			return frac(self.up*other.up,self.down*other.down)
		else:
			return self*frac(other)
			
	def __rmul__(self,other):
		return self * other
		
			
	def __neg__(self):
		return frac(-self.up,self.down)
		
		
	def __truediv__(self,other):
		if type(other) == frac:
			return frac(self.up*other.down,self.down*other.up)
		else:
			return self / frac(other)
			
	def __rtruediv__(self,other):
		return frac(self.down,self.up)*frac(other)
			
			
	def __pow__(self,p):
		return frac(power(self.up,p),power(self.down,p))
	
	
	def __eq__(self,other):
		if type(other) == frac:
			if self.up == other.up and self.down == other.down:
				return True
			else:
				return False
		else:
			return self == frac(other)
	
	def __ne__(self,other):
		return not(self == other)
	
	def __lt__(self,other):
		if type(other) == frac:
			if (self - other).up < 0:
				return True
			else:
				return False
		else:
			return self<frac(other)
	
	def __gt__(self,other):
		if type(other) == frac:
			if (self - other).up > 0:
				return True
			else:
				return False
		else:
			return self>frac(other)
	
	def __le__(self,other):
		if type(other) == frac:
			if (self - other).up <= 0:
				return True
			else:
				return False
		else:
			return self<=frac(other)
			
	def __ge__(self,other):
		if type(other) == frac:
			if (self - other).up >= 0:
				return True
			else:
				return False
		else:
			return self>=frac(other)
			
		
	def __float__(self):
		return self.up/self.down
		
	def __abs__(self):
		return frac(abs(self.up),abs(self.down))



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
			res += str(abs(self[i] if not self[i].is_integer() else int(self[i])) ) if abs(self[i]) != 1 or i == 0 else ''
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
			for j in range((i.start if i.start != None else 0),(i.stop if i.stop != None else len(self)),(i.step if i.step != None else 1)):
				res.append(self[j])
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
		
	def __call__(self,x):
		res = 0
		h = 1
		for i in self:
			res += h*i
			h*=x
		return res
	
	def interval_with_all_roots(self):
		return 1+(max([abs(i) for i in self[1:]])/abs(self[self.deg()]))
	
	def Sturm_system(self):
		res = [self,self.derivative()]
		i = 1
		while res[-1] != 0:
			res.append(res[i-1]%res[i] * (-1))
			i+=1
		return res[:-1]

def W(Sturm_system,c):
	h = []
	for i in Sturm_system:
		if i(c) == 0:
			continue
		else:
			h.append(i(c))
	res = 0
	for i in range(1,len(h)):
		if (h[i] > 0 and h[i-1] < 0) or (h[i] < 0 and h[i-1] > 0):
			res+=1
	return res

def get_intervals_with_roots(f):
	'''
	Возвращает список интервалов, содержащих по одному корню
	многочлена [(a0, b0), (a1, b1), ..., (am, bm)]
	'''
	# 1й шаг: строим систему Штурма
	# 2й шаг: находим K
	# 3й шаг: находим интервалы половинным делением, используя функцию W
	syst = f.Sturm_system()
	k = f.interval_with_all_roots()
	intrs = [-k,k]
	WK = W(syst,-k)-W(syst,k)
	t = 1
	tail=0
	while len(intrs)-1 < WK or t > 0:
		t-=1
		for i in range(1,len(intrs)-tail):
			if W(syst,intrs[i-1]) - W(syst,intrs[i]) > 1:
				intrs.append((intrs[i-1]+intrs[i])/2)
				intrs.sort()
				t += 1
			elif W(syst,intrs[i-1]) - W(syst,intrs[i]) == 0:
				intrs[i-1] = k+1
				tail +=1
	return intrs[:-tail] if tail != 0 else intrs

def calculate_root_on_interval(f, a, b):
	'''
	Возвращает корень x0 на интервале (a, b)
	'''
	# Находим корень половинным делением, выбирая половину,
	# на которой различаются знаки
	a = frac(a)
	b = frac(b)
	while abs(b-a)>0.0001:
		c = (a+b)/2
		if f(c) == 0:
			return float(c) if f(round(float(c))) != 0 else round(float(c))
		if f(a)*f(c) < 0:
			b = c
		else:
			a = c
	return float((a+b)/2) if f(round(float((a+b)/2))) != 0 else round(float((a+b)/2))

def get_all_roots(f):
	'''
	Возвращает список корней [x1, x2, ..., xm]
	'''
	res =[]
	intrs = get_intervals_with_roots(f)
	for i in range(len(intrs)-1):
		if f(intrs[i]) == 0:
			res.append(intrs[i])
		elif f(intrs[i+1]) == 0:
			res.append(intrs[i+1])
		res.append(calculate_root_on_interval(f,intrs[i],intrs[i+1]))
	res = list(set(res))
	res.sort()
	return res

a = polynom([0,-6,-1,1])
print(0.0)
print(get_all_roots(a))
