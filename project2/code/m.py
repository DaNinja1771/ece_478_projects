import pandas as pd
import matplotlib.pyplot as plt

# Reading the file and preparing the data
file_path = '2023.AS-rel.txt'
# Function to process the file and calculate unique degrees
def calculate_unique_degrees(file_path):
    # Initialize the dictionaries for degree counts
    global_degree = {}
    customer_degree = {}
    peer_degree = {}
    provider_degree = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue  # Skip lines that don't have enough data
            
            as1, as2, link_type = int(parts[0]), int(parts[1]), int(parts[2])

            # Update global degree for both ASes
            global_degree[as1] = global_degree.get(as1, set())
            global_degree[as2] = global_degree.get(as2, set())
            global_degree[as1].add(as2)
            global_degree[as2].add(as1)

            # Update customer and provider degrees
            if link_type == -1:  # p2c link
                customer_degree[as1] = customer_degree.get(as1, set())
                customer_degree[as1].add(as2)
                provider_degree[as2] = provider_degree.get(as2, set())
                provider_degree[as2].add(as1)
            elif link_type == 0:  # p2p link
                peer_degree[as1] = peer_degree.get(as1, set())
                peer_degree[as1].add(as2)
                peer_degree[as2] = peer_degree.get(as2, set())
                peer_degree[as2].add(as1)

    # Convert sets to counts for each AS
    global_degree_counts = {as_num: len(as_set) for as_num, as_set in global_degree.items()}
    customer_degree_counts = {as_num: len(as_set) for as_num, as_set in customer_degree.items()}
    peer_degree_counts = {as_num: len(as_set) for as_num, as_set in peer_degree.items()}
    provider_degree_counts = {as_num: len(as_set) for as_num, as_set in provider_degree.items()}

    return global_degree_counts, customer_degree_counts, peer_degree_counts, provider_degree_counts

# Calculate the unique degrees
unique_global_degree_counts, unique_customer_degree_counts, unique_peer_degree_counts, unique_provider_degree_counts = calculate_unique_degrees(file_path)

# Create a DataFrame for each category with binned counts
def create_degree_dataframe(degree_counts):
    df = pd.DataFrame.from_dict(degree_counts, orient='index', columns=['Degree'])
    df['Bin'] = pd.cut(df['Degree'], bins=[-1, 0, 1, 5, 100, 200, 1000, float('inf')], labels=['0', '1', '2-5', '6-100', '101-200', '201-1000', '>1000'])
    binned_counts = df['Bin'].value_counts().sort_index()
    return binned_counts

# Create DataFrames for each degree type
df_global = create_degree_dataframe(unique_global_degree_counts)
df_customer = create_degree_dataframe(unique_customer_degree_counts)
df_peer = create_degree_dataframe(unique_peer_degree_counts)
df_provider = create_degree_dataframe(unique_provider_degree_counts)

# Plotting function
# Adjust the plotting function to display percentages instead of raw counts, eliminating the need for a log scale

def plot_degree_distribution_with_percentages(df, title):
    # Calculate the percentage of each bin
    df_percentages = (df / df.sum()) * 100
    ax = df_percentages.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title(title)
    plt.xlabel('Degree')
    plt.ylabel('Percentage of ASes (%)')
    
    # Annotate the percentage on top of each bar
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", (p.get_x() * 1.005, p.get_height() * 1.05))
    
    plt.show()

# Plot histograms with percentages
plot_degree_distribution_with_percentages(df_global, 'Global Node Degree Distribution')
plot_degree_distribution_with_percentages(df_customer, 'Customer Degree Distribution')
plot_degree_distribution_with_percentages(df_peer, 'Peer Degree Distribution')
plot_degree_distribution_with_percentages(df_provider, 'Provider Degree Distribution')

