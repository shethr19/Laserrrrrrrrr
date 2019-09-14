import random

# Q1
capital = 100
f=0.5


for i in range(45):
	capital -= f*capital

for i in range(55):
	capital += f*capital

print('a: ' + str(capital))


# ten thousand iters
max = 0
capital = 100

f = 0.1
count = 0
while(True):
	count += 1
	capital += capital*f
	if(capital >= 1000000):
		break

