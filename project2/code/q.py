import matplotlib.pyplot as plt
import pandas as pd
fopen = open("2023.AS-rel.txt", encoding="utf-8")

relationships = {}

for line in fopen:
    if line[0] != "#":
        line_split = line.split("|")
        as1 = line_split[0].strip("\n")
        as2 = line_split[1].strip("\n")
        reltype = int(line_split[2].strip("\n"))
        if as1 not in relationships:
            # [Global Node Degree, Customer Degree, Peer Degree, Provider Degree, [Connections]]
            relationships[as1] = [0, 0, 0, 0, []]
        if as2 not in relationships:
            # [Global Node Degree, Customer Degree, Peer Degree, Provider Degree, [Connections]]
            relationships[as2] = [0, 0, 0, 0, []]
        # If p2c
        if reltype == -1:
            # as1 has customer
            relationships[as1][1] += 1
            relationships[as1][0] += 1
            # as2 has provider
            relationships[as2][3] += 1
            relationships[as2][0] += 1
        # If p2p
        elif reltype == 0:
            # as1 has peer
            relationships[as1][2] += 1
            relationships[as1][0] += 1
            # as2 has
            relationships[as2][2] += 1
            relationships[as2][0] += 1
        else:
            print("Unknown reltype")
        relationships[as1][4].append(as2)
        relationships[as2][4].append(as1)
        arr1 = relationships[as1]
        arr2 = relationships[as2]
        assert (arr1[0] == arr1[1] + arr1[2] + arr1[3])
        assert (arr2[0] == arr2[1] + arr2[2] + arr2[3])
sorted_relationships = sorted(relationships.items(), key=lambda x:x[1][0], reverse=True)
# print(sorted_relationships)
s = []
for as_name in sorted_relationships:
    if len(s) == 0:
        s.append(as_name)
    else:
        # print(as_name[0])
        can_continue = False
        for s_name in s:
            can_continue = False
            for link in s_name[1][4]:
                if as_name[0] == link and as_name[0] != s_name[0]:
                    if s_name[0] == s[-1][0]:
                        s.append(as_name)
                    can_continue = True
                    break
            if can_continue is False:
                break
        if can_continue is False and len(s) >= 50:
            break
fopen.close()
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
as_numbers = []
num_links = []
organizations = []
for as_name in s[:10]:
    as_numbers.append(as_name[0])
    organizations.append(org_to_name[as_to_org[as_name[0]]])
    num_links.append(as_name[1][0])
table_dict = {"AS Number": as_numbers, "Organization": organizations, "Number of Incident Links": num_links}
df = pd.DataFrame(table_dict, index=list(range(1, 11)))
print(df)