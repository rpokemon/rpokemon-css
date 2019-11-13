from collections import Counter
import random
import string
import time

N = 50
C = 10000

samples = [
    {
        '*': ['k'],
        '$': 'j'
    },
    {
        '$': 'j4'
    },
    {
        '*': 'k'
    }

]
bucket = Counter()


def gen_hash(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


start_time = time.time()


for i in range(C):
    hash = gen_hash(N)

    print(hash)

    for s in samples:
        name = ''

        if all(c not in s for c in ['^', '*', '$']):
            continue

        if s.get('^') is not None:
            contain_val = s['^']
            name += f'[uh^={contain_val}]'
            if not hash.startswith(contain_val):
                continue

        if s.get('*') is not None:
            contain_val = s['*']
            if isinstance(contain_val, list):
                try:
                    for j in contain_val:
                        name += f'[uh*={j}]'
                        if j not in hash:
                            raise StopIteration()
                except StopIteration:
                    continue
            else:
                name += f'[uh*={contain_val}]'
                if contain_val not in hash:
                    continue

        if s.get('$') is not None:
            contain_val = s['$']
            name += f'[uh$={contain_val}]'
            if not hash.endswith(contain_val):
                continue

        bucket[name] += 1


end_time = time.time()

print(f'\nCompleted in {end_time - start_time:.2f} seconds\n')

for key, val in bucket.items():
    print(f'\t{key}: {val/C:.2%} ({val})')
