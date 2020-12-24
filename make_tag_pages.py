#!/usr/bin/env python

'''
tag_generator.py
Copyright 2017 Long Qian
Contact: lqian8@jhu.edu
This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os

post_dir = '_questions/'
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*md')

total_tags = []
for filename in filenames:
    f = open(filename, 'r', encoding='utf8')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split()
            if current_tags[0] == 'tags:':
                total_tags.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)

old_tags = glob.glob(tag_dir + '*.md')
for tag in old_tags:
    os.remove(tag)
    
if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

with open("tags.html",'w') as f:
    write_str = f'''---\n
    layout: default\n
    title: "Tags"\n
    robots: noindex\n---
    \n
    \n
    '''
    for tag in sorted(total_tags):
        write_str += f"<h2 style='font-size:30px'><a href='{{{{site.baseurl}}}}/tag/{tag}'>{tag.capitalize()}</a></h2>\n\n"
    f.write(write_str)


for tag in total_tags:
    tag_filename = tag_dir + tag + '.md'
    f = open(tag_filename, 'a')
    write_str = f'''---\n
    layout: tagpage\n
    title: "Tag: {tag}"\n
    tag: {tag} \n
    robots: noindex\n---
    \n
    \n
    '''
    f.write(write_str)
    f.close()
print("Tags generated, count", total_tags.__len__())