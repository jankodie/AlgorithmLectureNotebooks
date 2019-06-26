print("Rekursive Version 1:")

def fibr(n):
    if n == 1:
      return 1
    if n == 2:
      return 1
    return fibr(n-1) + fibr(n-2)
   
for x in range(1,15):
  print(f'  Fib({x}): {fibr(x)}')

print("Iterative Version 1:")

def fibi(n):
    if n > 2:
     a = 1
     b = 1
     for i in range(2,n):
        tmp = a
        a = b
        b = a + tmp
     return b
    else:
      return 1

for x in range(1,15):
  print(f'  Fib({x}): {fibi(x)}')

print("Iterative Version 2:")
def fibi2(n):
    f = [1,1,1]
    if n > 2:
     for i in range(3,n+1):
        f[i%3] = f[(i-1)%3] + f[(i-2)%3]
    return f[n%3]

for x in range(1,15):
  print(f' Fib({x}): {fibi2(x)}')
