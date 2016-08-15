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

bucket = {}

def gen_hash(length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))
    
start_time = time.time()
for i in range(C):
    hash = gen_hash(N);
    
    print(hash)
    
    for s in samples:
        name = ''
            
        if ('^' not in s and '*' not in s and '$' not in s):
            continue
        
        if ('^' in s and s['^'] is not None):
            name += '[uh^='+s['^']+']'
            if (not hash.startswith(s['^'])):
                continue
        if ('*' in s and s['*'] is not None):
            contain_val = s['*']
            if type(contain_val) is list:
                skip = False
                for j in contain_val:
                    name += '[uh*='+j+']'
                    if (j not in hash):
                        skip = True
                        break
                if skip:
                    continue
            else:
                name += '[uh*='+contain_val+']'
                if (contain_val not in hash):
                    continue
        if ('$' in s and s['$'] is not None):
            name += '[uh^='+s['$']+']'
            if (not hash.startswith(s['$'])):
                continue
        
        if name not in bucket:
            bucket[name] = 1
        else:
            bucket[name] += 1
end_time = time.time()

print('\nCompleted in ' + str(end_time - start_time) + ' seconds\n')

for key,val in bucket.items():
    print('  ' + key + ': ' + str(val / C * 100.0) + '% ('+str(val)+')')