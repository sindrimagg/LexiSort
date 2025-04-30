import re,os,itertools

def weave(*iterable):
    for element in itertools.chain.from_iterable(itertools.zip_longest(*iterable)):
        if element is not None:
            yield element
    
def combine(txt, nums, max_lens):
    padded_nums = (num.rjust(max_len, '0') for num, max_len in zip(nums, max_lens))
    return ''.join(weave(txt, padded_nums))

def add_list_dict(dictionary, key, item):
    try:
        dictionary[key].append(item)
    except KeyError:
        dictionary[key] = [item]

digs = re.compile(r'\d+')
sep = re.compile('0')

def process_entry(entry, dictionary, ignore_ext = False):
    path, ext = os.path.splitext(entry.name)
    name = path if ignore_ext and entry.is_file() else entry.name
    text, nums = re.split(digs, name), re.findall(digs, name)
    if nums:
        key = '0'.join(text)
        add_list_dict(dictionary, key, (nums, entry.path, ext))
        
def get_new_names(path, name_map):
    for key,num_list in name_map.items():
        max_lengths = [max(map(lambda x: len(x), col)) for col in zip(*(nums for nums, _, _ in num_list))]

        txt = re.split(sep, key)
        for num in sorted(num_list):
            out = os.path.join(path, combine(txt, num[0], max_lengths) + num[2])
            if num[1] != out:
                print(f"{'Was':<10}" + num[1])
                print(f"{'Becomes':<10}" + out + '\n')
            else:
                print(f"{'Unchanged':<10}" + num[1] + '\n')

def rename_dir(path = '.', ignore_ext = True, dirs = True, files = True, dir_map = {}, file_map = {}):
    big_list = []
    for entry in os.scandir(path):
        nums = re.findall(digs, entry.name)
        nums.append('')
        big_list.append((re.split(digs, entry.name), nums))

        if entry.is_dir() and dirs:
            process_entry(entry, dir_map)
        elif entry.is_file() and files:
            process_entry(entry, file_map, ignore_ext)

    if dirs:
        print('Changed directories:')
        print(f"{'':-<20}")
        get_new_names(path, dir_map)
    if files:
        print('Changed files:')
        print(f"{'':-<20}")
        get_new_names(path, file_map)

rename_dir(dirs = True, files = True)


