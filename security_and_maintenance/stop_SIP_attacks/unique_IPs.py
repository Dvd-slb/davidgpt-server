#!/bin/python3

with open("</.../known_hackers_ips.list>") as file:
    ban_list = file.readlines()
    uniq_list = set(ban_list)

with open("</.../unique_ips.list>", "w") as nf:
    for line in uniq_list:
        nf.write(line)
