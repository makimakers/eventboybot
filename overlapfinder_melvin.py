from datetime import datetime as dt
from intervaltree import Interval, IntervalTree
#import test_inputs

# one interval
tc_0 = [Interval(1, 3, "aaron")]

# no overlap
tc_1 = [Interval(1, 2, "aaron"), Interval(3, 4, "ben"), Interval(5, 6, "charlotte")]

# separate overlaps
tc_2 = [Interval(1, 3, "aaron"), Interval(2, 4, "ben"),  Interval(3, 5, "charlotte")]

# shared overlap
tc_3 = [Interval(1, 3, "aaron"), Interval(2, 4, "ben"), Interval(2, 5, "charlotte")]

# 4 intervals
tc_4 = [Interval(1, 3, "aaron"), Interval(2, 4, "ben"),
        Interval(3, 5, "charlotte"), Interval(1, 6, "dan")]

# more test cases
#----------------

# input: no overlap
# expected: no common interval
tc_5 = [
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=2, hour=0), "user_1"),
    Interval(dt(year=2018, month=1, day=2, hour=0), dt(year=2018, month=1, day=3, hour=0), "user_2"),
    Interval(dt(year=2018, month=1, day=3, hour=0), dt(year=2018, month=1, day=4, hour=0), "user_3")
]

# input: two overlap
# expected: common interval at 2018,1,2,0 - 2018,1,3,0, for all users
# common interval at 2018,1,2,0 - 2018,1,4,0, for user_1 and user_3.
tc_6 = [
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=4, hour=0), "user_1"),
    Interval(dt(year=2018, month=1, day=2, hour=0), dt(year=2018, month=1, day=3, hour=0), "user_2"),
    Interval(dt(year=2018, month=1, day=2, hour=0), dt(year=2018, month=1, day=5, hour=0), "user_3")
]

# input: complete overlap
# expected: one common interval at 2018,1,1,0 - 2018,1,4,0, for all users
tc_7 = [
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=4, hour=0), "user_1"),
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=4, hour=0), "user_2"),
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=4, hour=0), "user_3")
]

# input: user 1 has 2 different intervals
# expected: two common intervals at [2018,1,1,0 - 2018,1,2,0] and [2018,1,4,0 - 2018,1,5,0] 
tc_8 = [
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=2, hour=0), "user_1"),
    Interval(dt(year=2018, month=1, day=4, hour=0), dt(year=2018, month=1, day=5, hour=0), "user_1"),
    Interval(dt(year=2018, month=1, day=1, hour=0), dt(year=2018, month=1, day=8, hour=0), "user_2"),
]

# input: many users with many intervals each
# expected: many common intervals 
tc_9 = [
    Interval(dt(year=2018, month=1, day=1, hour=10), dt(year=2018, month=1, day=1, hour=12), "user_1"),
    Interval(dt(year=2018, month=1, day=3, hour=10), dt(year=2018, month=1, day=3, hour=12), "user_1"),
    Interval(dt(year=2018, month=1, day=1, hour=11), dt(year=2018, month=1, day=1, hour=13), "user_2"),
    Interval(dt(year=2018, month=1, day=3, hour=11), dt(year=2018, month=1, day=3, hour=13), "user_2"),
    Interval(dt(year=2018, month=1, day=1, hour=8), dt(year=2018, month=1, day=1, hour=18), "user_3"),
    Interval(dt(year=2018, month=1, day=2, hour=8), dt(year=2018, month=1, day=2, hour=18), "user_3"),
    Interval(dt(year=2019, month=1, day=1, hour=8), dt(year=2019, month=1, day=1, hour=18), "user_4"),
    Interval(dt(year=2019, month=1, day=5, hour=0), dt(year=2019, month=1, day=6, hour=0), "user_4"),
    Interval(dt(year=2019, month=1, day=5, hour=0), dt(year=2019, month=1, day=6, hour=0), "user_5"),
    Interval(dt(year=2019, month=1, day=5, hour=0), dt(year=2019, month=1, day=6, hour=0), "user_5"),
    Interval(dt(year=2019, month=1, day=5, hour=0), dt(year=2019, month=1, day=6, hour=0), "user_6")
]        


# Input: An list of Intervals
# Output: A dictionary (key: overlap, value: set of user_ids which share the overlap)
def find_all_common_intervals(interval_list):
    overlap_dict = dict()
    interval_tree = IntervalTree(interval_list)
    
    for interval in interval_tree.items(): # create a copy of the tree to iterate over
        # check interval against overlap_dict
        for overlap in overlap_dict.keys():
            add_overlap_to_dict(overlap, interval, overlap_dict)
            
        # check interval against other intervals in the tree to find overlapping regions
        other_intervals = find_other_intervals_which_overlap(interval_tree, interval)
        for other_interval in other_intervals:
            add_new_overlap_to_dict(interval, other_interval, overlap_dict)         
         
    return overlap_dict


# Input: An IntervalTree and an Interval in the IntervalTree
# Output: A set containing all other Intervals in the IntervalTree that intersect with the given
#  Interval
def find_other_intervals_which_overlap(tree, interval):
    tree.remove(interval)
    result = tree.search(interval.begin, interval.end) # returns a set
    return result


# Input: Two Intervals and a dictionary (key is Interval)
# Output: None
# Pre-condition: interval.data is a user id
def add_new_overlap_to_dict(interval_a, interval_b, overlap_dict):
    overlap = find_overlap(interval_a.begin, interval_a.end, interval_b.begin, interval_b.end) # returns a tuple
    if overlap != None:
        overlap = Interval(overlap[0], overlap[1])
    else: 
        return

    if overlap in overlap_dict:
        overlap_data = overlap_dict[overlap]
        overlap_data |= {interval_a.data, interval_b.data}
    else:
        overlap_dict[overlap] = {interval_a.data, interval_b.data}


# Input: Two Intervals and a dictionary (key is Interval)
# Output: None
# Pre-condition: interval.data is a user id
def add_overlap_to_dict(overlap, current_interval, overlap_dict):

    common_tuple = find_overlap(overlap.begin, overlap.end, current_interval.begin, current_interval.end) # returns a tuple
    if common_tuple != None:
        common = Interval(common_tuple[0], common_tuple[1])
    else: 
        return
    
    if common in overlap_dict:
        overlap_data = overlap_dict[overlap].copy()
        overlap_data |= {current_interval.data} # update set of data
        overlap_dict[common] = overlap_data # update key-value pair


# Pre-condition: all arguments are integers, a and b are comparable
def find_overlap(a1, a2, b1, b2):
    a_begin = min(a1, a2)
    a_end = max(a1, a2)
    b_begin = min(b1, b2)
    b_end = max(b1, b2)

    if b_end < a_begin or a_end < b_begin:
        return None
    common_begin = max(a_begin, b_begin)
    common_end = min(a_end, b_end)
    return common_begin, common_end


def print_common_dtintervals(overlap_dict):
    print("available common datetime intervals:\n")
    # tup is the tuple representing the common interval, userid_set is set of the user data
    for overlap, userid_set in overlap_dict.items():
        print(overlap.begin.strftime('%Y-%b-%d %H%M') + " - " + overlap.end.strftime('%Y-%b-%d %H%M') + ": ")
        print("\tuserids: " + str(userid_set))
    print()


tc_counter = 1

def test_algo(tc):
    global tc_counter
    print(tc_counter)
    tc_counter = tc_counter + 1
    overlap_dict = find_all_common_intervals(tc)
    for items in overlap_dict.items():
        print(items)
    print()

test_algo(tc_1)
test_algo(tc_2)
test_algo(tc_3)
test_algo(tc_4)
test_algo(tc_5)
test_algo(tc_6)
test_algo(tc_7)
test_algo(tc_8)
test_algo(tc_9)
