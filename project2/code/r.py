import pandas as pd
fopen = open("2023.AS-rel.txt", encoding="utf-8")

relationships = {}
degree_dict = {}
for line in fopen:
    if line[0] != "#":
        line_split = line.split("|")
        as1 = line_split[0].strip("\n")
        as2 = line_split[1].strip("\n")
        reltype = int(line_split[2].strip("\n"))
        if as1 not in relationships:
            # [customer array, provider array]
            relationships[as1] = [set(), set()]
            degree_dict[as1] = 0
        if as2 not in relationships:
            # [customer array, provider array]
            relationships[as2] = [set(), set()]
            degree_dict[as2] = 0
        # If p2c
        if reltype == -1:
            # as1 has customer
            relationships[as1][0].add(as2)
            # as2 has a provider
            relationships[as2][1].add(as1)
        degree_dict[as1] += 1
        degree_dict[as2] += 1

fopen.close()

# Find all AS's with no children
customers = {}
as_list = set()
for as_name in relationships:
    as_data = relationships[as_name]
    if len(as_data[0]) == 0:
        customers[as_name] = as_data[0]
        as_list.add(as_name)

for as_name in as_list:
    parents = relationships[as_name][1]
    for parent in parents:
        if parent in customers:
            customers[parent].add(as_name)
        else:
            customers[parent] = {as_name}
        as_list.add(as_name)
        for c in customers[as_name]:
            customers[parent].add(c)
            as_list.add(as_name)
sorted_customers = sorted(
    customers.items(), key=lambda key: len(key[1]), reverse=True)
total_as = 0
total_prefix = 0
total_ip = 0
as_stats = {}
for as_num in sorted_customers:
    as_stats[as_num[0]] = {}
    as_stats[as_num[0]]["as_number"] = len(as_num[1])
    total_as += len(as_num[1])

fopen = open("routeviews-rv2-20231116-1400.pfx2as", encoding="utf-8")

ipspace = {}

for line in fopen:
    if line[0] != "#":
        line_split = line.split()
        ip = line_split[0]
        prefix = int(line_split[1])
        as1 = line_split[2].strip("\n")
        if as1 not in ipspace:
            ipspace[as1] = [0, 0]
        ipspace[as1][0] += prefix
        ip_calc = 2 ** (32 - prefix)
        ipspace[as1][1] += ip_calc
        total_prefix += prefix
        total_ip += ip_calc
fopen.close()
for as_num in sorted_customers:
    if as_num[0] in ipspace:
        as_stats[as_num[0]]["prefix"] = ipspace[as_num[0]][0]
        as_stats[as_num[0]]["ip"] = ipspace[as_num[0]][1]
    else:
        as_stats[as_num[0]]["prefix"] = 0
        as_stats[as_num[0]]["ip"] = 0
org_to_name = {}
as_to_org = {}
fopen = open("20230101.as-org2info.txt", encoding="utf-8")
for line in fopen:
    if line[0] != "#":
        line_split = line.split("|")
        org_id = line_split[0]
        name = line_split[2]
        org_to_name[org_id] = name
    elif line.startswith("# format:aut"):
        for line in fopen:
            line_split = line.split("|")
            as_name = line_split[0]
            org_id = line_split[3]
            as_to_org[as_name] = org_id
fopen.close()
top_as = sorted_customers[:15]
top_dict = {}
for as_num in top_as:
    as_stats[as_num[0]]["name"] = org_to_name[as_to_org[as_num[0]]]
    as_stats[as_num[0]]["degree"] = degree_dict[as_num[0]]
    top_dict[as_num[0]] = as_stats[as_num[0]]
as_number = []
as_name = []
as_degree = []
ases = []
prefix = []
ips = []
perc_ases = []
perc_prefix = []
perc_ips = []
for as_num in top_dict:
    as_number.append(as_num)
    as_name.append(top_dict[as_num]["name"])
    as_degree.append(top_dict[as_num]["degree"])
    ases.append(top_dict[as_num]["as_number"])
    prefix.append(top_dict[as_num]["prefix"])
    ips.append(top_dict[as_num]["ip"])
    perc_ases.append(100 * top_dict[as_num]["as_number"] / total_as)
    perc_prefix.append(100 * top_dict[as_num]["prefix"] / total_prefix)
    perc_ips.append(100 * top_dict[as_num]["ip"] / total_ip)
table_dict = {"AS #": as_number, "AS name": as_name, "AS degree": as_degree, "ASes": ases,
              "IP Prefix": prefix, "IPs": ips, "ASes2": perc_ases, "IP Prefix2": perc_prefix, "IPs2": perc_ips}
table = pd.DataFrame(table_dict, index=list(range(1, 16)))
table.columns = [["AS #", "AS name", "AS degree", "customer cone", "customer cone", "customer cone", "customer cone", "customer cone", "customer"],
 ["", "", "", "number of", "number of", "number of", "percentage of", "percentage of", "percentage of"], 
 ["", "", "", "ASes", "IP Prefix", "IPs", "ASes", "IP Prefix", "IPs"]]
print(table)