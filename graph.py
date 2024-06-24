import matplotlib.pyplot as plt
import numpy as np

def time_to_seconds(time_str):
    minutes, seconds = time_str.split(':')
    seconds = float(seconds)
    return int(minutes) * 60 + seconds

old_times_str = ['01:28.147', '00:07.831', '01:46.243', '00:14.991', '02:30.394', 
                 '00:00.093', '01:44.000', '00:20.000', '01:30.00', '05:56.000']
new_times_str = ['00:00.241', '00:00.006', '00:00.045', '00:00.084', '00:00.142', 
                 '00:00.093', '00:00.17', '00:01.35', '00:01.65', '00:00.102']

old_times = [time_to_seconds(t) for t in old_times_str]
new_times = [time_to_seconds(t) for t in new_times_str]

num_queries = len(old_times)

queries = np.arange(num_queries)

bar_width = 0.35

fig, ax = plt.subplots()

bars1 = ax.bar(queries - bar_width/2, old_times, bar_width, label='Before optimization')

bars2 = ax.bar(queries + bar_width/2, new_times, bar_width, label='After optimization')

ax.set_xlabel('Query')
ax.set_ylabel('Execution Time (s)')
ax.set_title('Execution Time Comparison Before and After Optimization')
ax.set_xticks(queries)
ax.set_xticklabels([f'Query {i+1}' for i in queries])
ax.legend()

def seconds_to_time(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f'{minutes:02}:{seconds:06.3f}'

def add_labels(bars, times):
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax.annotate(seconds_to_time(time),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bars1, old_times)
add_labels(bars2, new_times)

plt.tight_layout()
plt.show()
