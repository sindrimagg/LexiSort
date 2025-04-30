= LexiSort

Renames files so that when files are lexicographically ordered their numbers are also numerically ordered.

Before we run the program in the directory /School/:
```bash
School
├── Week 1
├── Week 10
├── Week 11
├── Week 12
├── Week 13
├── Week 2
├── Week 3
├── Week 4
├── Week 5
├── Week 6
├── Week 7
├── Week 8
│   ├── Lecture 10
│   ├── Lecture 11
│   ├── Lecture 12
│   ├── Lecture 13
│   ├── Lecture 14
│   ├── Lecture 15
│   ├── Lecture 4
│   ├── Lecture 5
│   ├── Lecture 6
│   ├── Lecture 7
│   ├── Lecture 8
│   └── Lecture 9
└── Week 9
```

After we run the program with the recursive flag:
```bash
School
├── Week 01
├── Week 02
├── Week 03
├── Week 04
├── Week 05
├── Week 06
├── Week 07
├── Week 08
│   ├── Lecture 04
│   ├── Lecture 05
│   ├── Lecture 06
│   ├── Lecture 07
│   ├── Lecture 08
│   ├── Lecture 09
│   ├── Lecture 10
│   ├── Lecture 11
│   ├── Lecture 12
│   ├── Lecture 13
│   ├── Lecture 14
│   └── Lecture 15
├── Week 09
├── Week 10
├── Week 11
├── Week 12
└── Week 13
```

== Usage

LexiSort [-h] [-f] [-r] [-d] [--dry] [path]

Renames files so that when they are ordered lexicographically their numbers are also numerically ordered, e.g. if you have two files "Week 9"
and "Week 10" this program will change the former to "Week 09"

positional arguments:
  path             Path to the directory which should have its entries renamed, defaults to '.'

options:
  -h, --help       show this help message and exit
  -f, --fill       If there are two files a and a1 then the former becomes a0
  -r, --recursive  Recursively renames entries in all subfolders
  -d, --hidden     Changes hidden files and directories
  --dry            See which files would change
