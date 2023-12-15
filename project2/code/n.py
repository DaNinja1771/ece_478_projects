import matplotlib.pyplot as plt

def process_file(filename):
    # Initialize counters for each AS type
    counts = {'transit/access': 0, 'content': 0, 'enterprise': 0}
    total = 0

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                as_type = parts[2].strip().lower()
                # Check for both 'enterprise' and 'enterpise' (typo)
                if as_type in ['enterprise', 'enterpise']:
                    as_type = 'enterprise'
                if as_type in counts:
                    counts[as_type] += 1
                    total += 1

    # Convert counts to percentages if total is not zero
    if total > 0:
        for key in counts:
            counts[key] = (counts[key] / total) * 100
    
    return counts

# Process the files for each year
data_2015 = process_file('20150801.as2types.txt')
data_2021 = process_file('20210401.as2types.txt')

# Convert to percentages and prepare for plotting
categories = list(data_2015.keys())
percentages_2015 = list(data_2015.values())
percentages_2021 = list(data_2021.values())

# Plotting
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(categories))

bar1 = plt.bar(index, percentages_2015, bar_width, label='2015')
bar2 = plt.bar([i + bar_width for i in index], percentages_2021, bar_width, label='2021')

plt.xlabel('AS Type')
plt.ylabel('Percentage (%)')
plt.title('Percentage Distribution of AS Types for 2015 and 2021')
plt.xticks([i + bar_width / 2 for i in index], categories)
plt.legend()

plt.tight_layout()
plt.show()

