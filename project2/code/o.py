import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Let's read the file 'routeviews-rv2-20231116-1400.pfx2as' and calculate the distribution of prefix lengths.

# Path to the file
file_path = 'routeviews-rv2-20231116-1400.pfx2as'

# Function to process the file and calculate the distribution of prefix lengths
def calculate_prefix_length_distribution(file_path):
    prefix_length_counts = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                # Prefix length is the second element in the parts list
                prefix_length = int(parts[1])
                prefix_length_counts[prefix_length] = prefix_length_counts.get(prefix_length, 0) + 1
    
    return prefix_length_counts

# Calculate the prefix length distribution
prefix_length_distribution = calculate_prefix_length_distribution(file_path)

# Convert the distribution to a DataFrame for plotting
df_prefix_lengths = pd.DataFrame(list(prefix_length_distribution.items()), columns=['PrefixLength', 'Count']).sort_values('PrefixLength')

# Calculate percentages for the y-axis
df_prefix_lengths['Percentage'] = (df_prefix_lengths['Count'] / df_prefix_lengths['Count'].sum()) * 100

# Plotting the distribution of prefix lengths
ax = df_prefix_lengths.plot(kind='bar', x='PrefixLength', y='Percentage', figsize=(12, 6), color='skyblue', legend=False)
plt.title('Distribution of Prefix Lengths')
plt.xlabel('Prefix Length')
plt.ylabel('Percentage of Prefixes (%)')

# Annotate the percentage on top of each bar
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() * 1.005, p.get_height() * 1.05))

plt.show()
