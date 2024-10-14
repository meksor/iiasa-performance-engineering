import matplotlib.pyplot as plt 
import glob
import cProfile
import pstats
import sys
import re

pr = cProfile.Profile()

def get_profiles(prefix=""):
    return glob.glob(f".profiles/{prefix}*.prof")


def get_runtime(profile):
    stats = pstats.Stats(profile)
    stats.sort_stats("cumulative")
    for fcn in stats.fcn_list:
        if fcn[2] == 'bench':
            ftup = stats.stats[fcn]
            # cumtime / ncalls 
            return ftup[3] / ftup[0]
    else:
        ftup = stats.stats[stats.fcn_list[0]]
        return ftup[3]
test_regex = re.compile(r"\.profiles\/(\w+)\[[^\d]+(\d+)\].*")
def plot(prefix):
    data = {}
    for prof in get_profiles(prefix):
        runtime = get_runtime(prof)
        print(prof)
        match = test_regex.match(prof)
        if match is None:
            match = 0
        else:
            match = int(match.groups()[1])
        data[(match, prof)] = runtime

    data = dict(sorted(data.items(), key=lambda x: x[0]))

    profiles = list(k[1] for k in data.keys())
    values = list(data.values())

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(profiles, values, color ='maroon', 
            width = 0.4)

    plt.xlabel("Profile")
    plt.ylabel("Runtime (s)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f'assets/profiles_{prefix}.png')


plot("test")

plot("test_python_mm")
plot("test_tc_get_middle_item")
plot("test_tc_sum")
plot("test_tc_quick_sort")
plot("test_tc_sorted")
