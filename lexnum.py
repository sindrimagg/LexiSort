import re,os

def combine(txt, nums, max_len):
    res = ''
    t = 0
    n = 0
    start = 2

    if len(txt) > len(nums):
        start = 0
    elif len(txt) < len(nums):
        start = 1
    else:
        if not txt:
            assert(len(nums) == 0)
            return nums
        else:
            assert(nums[0] != txt[0])
            if nums[0]:
                start = 0
            elif txt[0]:
                start = 1

    assert(start != 2)

    last = t + n
    while t < len(txt) or n < len(nums):
        if start == 0:
            res += txt[t]
            t += 1
            start = 1
        else:
            res += '0'*(max_len[n] - len(nums[n])) + nums[n]
            n += 1
            start = 0
    return res

filenames = os.listdir()

hm = {}
for file in filenames:
    text = re.split(r'\d+', file)
    nums = re.split(r'[^\d]+', file)

    tup_text = tuple(text)
    if tup_text in hm:
        hm[tup_text].append(nums)
    else:
        hm[tup_text] = [nums]

for text in hm:
    size = len(hm[text][0])
    max_lengths = [0 for _ in range(size)]
    for nums in hm[text]:
        for (ix,num) in enumerate(nums):
            max_lengths[ix] = max(max_lengths[ix], len(num))
    for nums in hm[text]:
        text = list(text)
        out = combine(text, nums, max_lengths)
        print('Was: ' + combine(text, nums, [0 for _ in nums]) + '\nBecomes: ' + out + '\n')
