import re,os,itertools,stat,sys,argparse

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def is_hidden(filepath):
    # Does maybe not work on Windows
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.')

class Node:
    def __init__(self, value, nums):
        self.value = value
        # Children are stored in a dictionary: {child_value: child_node}
        self.children = {}
        self.nums = len(nums)

    def __repr__(self):
         # Helpful representation for debugging
         return f"Node(value='{self.value}', children_values={list(self.children.keys())})"

    def __str__(self, level=0):
        # Simple string representation for printing the tree structure
        if level == 0:
            ret = ''
        else:
            ret = '  ' * level + f'{self.value} : {self.nums}\n'
        for child_value, child_node in self.children.items():
            ret += child_node.__str__(level + 1)
        return ret

    def update(self, nums):
        self.nums = max(self.nums, len(nums))

def build_forest(list_of_lists):
    """
    Builds a forest of trees from a list of lists.

    Each inner list defines a path in a tree.
    The first element of a list is the root of a tree.
    l_i is the parent of l_{i+1} in a path [l_1, l_2, ..., l_k].
    Lists starting with the same element share the same tree.

    Args:
        list_of_lists: A list where each element is a list representing a path.

    Returns:
        A dictionary representing the forest: {root_value: root_Node_object}.
    """
    string = '*Root*'
    root_node = Node(string, '')

    for alpha, numeric, _ in list_of_lists:
        current_node = root_node
        for alphs, nums in zip(alpha, numeric):
            # Check if the current node already has a child with this value
            if alphs not in current_node.children:
                # If not, create a new node for this element
                new_node = Node(alphs, nums)
                # Add the new node as a child of the current node
                current_node.children[alphs] = new_node
                # Move to the newly created node
                current_node = new_node
            else:
                # If the child node already exists, just move to the existing node
                current_node = current_node.children[alphs]
                current_node.update(nums)

    return root_node

def weave(*iterables):
    for entry in itertools.chain.from_iterable(zip(*iterables)):
        yield entry

digs = re.compile(r'\d+')

def rename_dir(path = '.', ignore_hidden = True, change_empty = True, dry = False):
    if not os.path.isdir(path):
        return

    entry_list = []
    for entry in os.scandir(path):
        if is_hidden(os.path.join(path, entry.name)) and ignore_hidden:
            continue
        # remove the file extension if it exists
        name_no_ext = os.path.splitext(entry.name)[0]

        # get the alphabetical part of name
        alphab = re.split(digs, name_no_ext)

        # get the nuerical part of name
        numeric = re.findall(digs, name_no_ext)
        # need to append empty string since alphab is always 1 longer than numeric (for zip)
        numeric.append('')
        entry_list.append((alphab, numeric, entry.name))

    root_node = build_forest(entry_list)

    new_names = []
    for alphas, nums, name in entry_list:
        name_ext = os.path.splitext(name)[1]
        new_name = ''
        current_node = root_node
        for alpha, num in zip(alphas, nums):
            current_node = current_node.children[alpha]
            new_name += alpha
            if num != '' or change_empty:
                new_name += num.zfill(current_node.nums)
        new_name += name_ext
        new_names.append(new_name)

        if new_name != name:
            if dry:
                print(f'{"Was:":<10}{os.path.join(path, name)}\n{"Becomes:":<10}{os.path.join(path, new_name)}\n')
            else:
                try:
                    os.rename(os.path.join(path, name), os.path.join(path, new_name))
                except OSError:
                    print(f'Could not rename {os.path.join(path, name)} to {os.path.join(path, new_name)}')

    #eprint(root_node, end='')

def walk_rename(path = '.', ignore_hidden = True, change_empty = True, dry = False):
    for entry in os.scandir(path):
        if entry.is_dir() and not (is_hidden(os.path.join(path, entry.name)) and ignore_hidden):
                walk_rename(os.path.join(path, entry.name), ignore_hidden, change_empty, dry)

    rename_dir(path, ignore_hidden, change_empty, dry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = 'lexnum',
            description = 'Renames files so that when they are ordered lexicographically their numbers are also numerically ordered, e.g. if you have two files "Week 9" and "Week 10" this program will change the former to "Week 09"'
            )
    parser.add_argument('path', help = 'Paths to the directories which should have its entries renamed', type = str, nargs = '?')
    parser.add_argument('-f', '--fill', help = 'If there are two files a and a1 then the former becomes a0', action = 'store_true')
    parser.add_argument('-r', '--recursive', help = 'Recursively renames entries in all subfolders', action = 'store_true')
    parser.add_argument('-d', '--hidden', help = 'Changes hidden files and directories', action = 'store_true')
    parser.add_argument('--dry', help = 'See which files would change', action = 'store_true')
    args = parser.parse_args()

    if args.recursive:
        if args.path:
            walk_rename(path = path, ignore_hidden = not args.hidden, change_empty = args.fill, dry = args.dry)
        else:
            walk_rename(path = '.', ignore_hidden = not args.hidden, change_empty = args.fill, dry = args.dry)
    else:
        if args.path:
            rename_dir(path = path, ignore_hidden = not args.hidden, change_empty = args.fill, dry = args.dry)
        else:
            rename_dir(path = '.', ignore_hidden = not args.hidden, change_empty = args.fill, dry = args.dry)
