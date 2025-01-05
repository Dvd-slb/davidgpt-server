#!/bin/python3

with open("</.../banned_IPs/banned_IP_list.txt>") as file:
    ban_list = file.readlines()
    uniq_list = set(ban_list)

with open("</.../banned_IPs/uniq_banned_IP_list.txt>", "w") as nf:
    for line in uniq_list:
        nf.write(line)
