import pandas as pd
import matplotlib.pyplot as plt

# Correcting the script to handle potential zero division errors

file_path_2022 = '2023.AS-rel.txt'

# Initialize dictionaries to hold AS relationships
customer_relationships = {}
peer_relationships = {}

with open(file_path_2022, 'r') as file:
    for line in file:
        parts = line.strip().split('|')
        if len(parts) < 3:
            continue

        as_number, link_type_str = parts[0], parts[2]
        
        # Ensure that the link type is an integer
        try:
            link_type = int(link_type_str)
        except ValueError:
            continue  # Skip lines where link type is not an integer

        # Transit AS: Any AS with at least one customer (-1)
        if link_type == -1:
            customer_relationships[as_number] = customer_relationships.get(as_number, 0) + 1

        # Content AS: Any AS with no customers and at least one peer (0)
        elif link_type == 0:
            peer_relationships[as_number] = peer_relationships.get(as_number, 0) + 1

# Determine the classification of each AS
transit_as = {as_num for as_num in customer_relationships}
content_as = {as_num for as_num in peer_relationships if as_num not in transit_as}
enterprise_as = {as_num for as_num in set(customer_relationships).union(peer_relationships) if as_num not in transit_as and as_num not in content_as}

# Count the number of ASes in each class
as_counts = {
    'Transit': len(transit_as),
    'Content': len(content_as),
    'Enterprise': len(enterprise_as)
}

# Convert counts to percentages, handling the case where total_as is zero
total_as = sum(as_counts.values())
percentages = {as_class: (count / total_as) * 100 if total_as > 0 else 0 for as_class, count in as_counts.items()}

# Create a DataFrame for plotting
df_as_classes = pd.DataFrame(list(percentages.items()), columns=['Class', 'Percentage'])

# Plotting the distribution of AS classes
ax = df_as_classes.plot(kind='bar', x='Class', y='Percentage', figsize=(10, 6), legend=False, color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Distribution of AS Classes for 2023')
plt.xlabel('AS Class')
plt.ylabel('Percentage of ASes (%)')

# Annotate the percentage on top of each bar
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

plt.tight_layout()
plt.show()

