import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi']= 300
mpl.rc("savefig", dpi=300)

def plot_wrapper(df):
    for metric in get_metrics(df):
        plot_metrics(df, metric)
    
    
def plot_metrics(df, metric):
    if metric == 'collisions':
        label_replacement = 'Collisions (num)'
    elif metric == 'a_succ':
        label_replacement = 'Sender A Successes (num)'
    elif metric == 'c_succ':
        label_replacement = 'Sender B Successes (num)'
    elif metric == 'ap_col':
        label_replacement = 'Collisions at AP (num)'
    elif metric == 'a_thruput':
        label_replacement = 'Sender A Throughput (Kib/sec)'
    elif metric == 'c_thruput':
        label_replacement = 'Sender B Throughput (Kib/sec)'
    elif metric == 'fairness_index':
        label_replacement = 'Fairness Index (ratio)'
    if metric != 'fairness_index':
        ax = sns.lineplot(data=df,x="frame_rate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
    else:
        ax = sns.lineplot(data=df,x="frame_rate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate in Scenario B'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
        ax = sns.lineplot(data=df.head(10),x="frame_rate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate in Scenario A'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
    
    
def get_scenarios(df):
    return list(set(df.scenario.values.tolist()))


def get_metrics(df):
    return df.columns.values.tolist()[2:]


def get_x_ticks(df):
    return list(set(df.frame_rate.values.tolist()))