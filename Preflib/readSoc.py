from collections import Counter
import random

def readPreflibString(file, n, m):

	# Given a preflib file name, #voters, #alts, reads that file,
	# and samples a profile from it with #voters and #alts
	# (if n is smaller than the voters in the profile of file, we randomly sample
	# n preference orders, proportionally to the number of voters expressing that order.
	# for alterantives, we do a random sample)

	A = set()
	with open(file) as f:
		m_p = int(f.readline())
		for _ in range(m_p):
			f.readline()

		voters = int(f.readline().split(',')[0])
		data = []
		for _ in range(voters):
			line = f.readline()[:-1].split(',')
			if line == ['']:
				continue
			count = int(line[0])
			ballot = tuple(map(lambda x: int(x), line[1:]))
			if not A:
				A = set(ballot)
				if len(A) < m:
					raise Exception("Not enough alternatives.")
			for c in range(count):
				data.append(ballot)

	if n < len(data):
		profile = []
		for _ in range(n):
			profile.append(random.choice(data))
		profile = Counter(profile)
	elif n == len(data):
		profile = Counter(data)
	else:
		raise Exception("Not enough voters.")

	while len(A) > m:
		remove = random.choice(list(A))
		A = {a for a in A if a != remove}

	A_map = dict(zip(sorted(A), list(range(len(A)))))

	new = {}
	for b, c in profile.items():
		b = tuple(A_map[a] for a in b if a in A)
		if b in new:
			new[b] += c
		else:
			new[b] = c
	profile = new

	return ','.join(f"{c}:{''.join(map(str, b))}" for b, c in profile.items())