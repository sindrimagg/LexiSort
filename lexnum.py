import re,os,itertools

def weave(*iterable):
    for element in itertools.chain.from_iterable(itertools.zip_longest(*iterable)):
        if element is not None:
            yield element
    
def combine(txt, nums, max_lens):
    padded_nums = ('0'*(max_len - len(num)) + num for num, max_len in zip(nums, max_lens))
    return ''.join(weave(txt, padded_nums))

filenames = os.listdir()
digs = re.compile(r'\d+')
sep = re.compile(fr'{os.sep}')

hm = {}
for file in filenames:
    text = re.split(digs, file)
    nums = re.findall(digs, file)

    tup_text = f'{os.sep}'.join(text)
    if tup_text in hm:
        hm[tup_text].append(nums)
    else:
        hm[tup_text] = [nums]

for text,num_list in hm.items():
    max_lengths = [max(map(lambda x: len(x), col)) for col in zip(*num_list)]

    txt = re.split(sep, text)
    for num in num_list:
        out = combine(txt, num, max_lengths)
        print('Was: ' + ''.join(weave(txt, num)) + '\nBecomes: ' + out + '\n')
