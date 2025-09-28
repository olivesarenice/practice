"""
We need a simple in-memory configuration service. 
It should store configuration values by key and allow us to retrieve them. 
How would you design a program to provide this basic key-value storage?
"""

import bisect
import time
from collections import OrderedDict, defaultdict


def ts():
    return int(time.time()*10000000)

class Config:
    def __init__(self):
        self.values = defaultdict(list) # versioning will use timestamp of addition for simplicity.
    
    def add(self, key, value):
       
        # Add the incoming value as the hash
        self.values[key].append((ts(), value))

        
    def get(self, key, timestamp: int = None): # unix timestamp
        if timestamp is None:
            # just return the latest value
            return self.values.get(key, [])[-1][1] # since this is a tuple
        else:
            versions = self.values.get(key, [])
            # Search for the latest tuple whose timestamp is < ts
            # example: [ts1, ts2, ts3, ts4] 
            # if my ts provided is between  ts2<>ts3, i want the insertion point that is after ts2 --> bisect_right
            insertion_pt = bisect.bisect_right(versions, timestamp, key=lambda x: x[0]) # ts is the first item in the tuple
            if insertion_pt ==0 : # this means that there was nothing submitted before this time, so i cant return anything
                print("timestamp is before any known version, no values returned")
                return None
            else:
                latest_value_idx = insertion_pt - 1
                
                last_versioned_value = versions[latest_value_idx]
                print(f"found value: {last_versioned_value[1]} at ts: {last_versioned_value[0]}")
                return last_versioned_value[1] # return only the value
    
        

config = Config()

changes = [
    ("abc", "firstval"),
    ("abc", "secondval"),
    ("cba", "thirdval"),
    ("abc", "newval"),
]

# while True:
#     k = str(input("Key: "))
#     v = input("Value: ")

#     config.add(k,v)

times = []
for c in changes:
    config.add(c[0], c[1])
    times.append(ts())
    print(config.get(c[0]))
    print(config.values)
    
# also try to get an older version of `abc`
print(config.get('abc', times[0]))
"""
A critical new feature is the ability to audit changes and retrieve historical values. 
We need to be able to query the value of any key as it was at a specific point in time. 
How would you modify your design to support this 'time-travel' capability?
"""

# First thought is to track the full config for every version, where each new key change produces a new version.
# Alternative method is to have a table of changes, possibly indexed by the key, and some time pointer/ hash of the key:value
# and then when the value of the key at a specific time is requetsed, we can reconstruct the key at that particular time based on all its changes.

# After thinking for some time, this is the best way to version:
# track the latest values (src) as self.values = {a: v1, b: v2. etc}
# track the versioned_values as self.versioned_values = {a: {hash1:v1, hash2:v2, ...}}
# and track the version_log as self.log = {hash1:ts1, hash2, ts2}
# the hash is applied on the ENTIRE self.values set --> since each change to any value changes the entire values object as a whole


"""
The versioned store has been running in production, and we've noticed its memory footprint is growing uncontrollably. 
The primary cause seems to be that many keys don't change value for long periods, but we're storing the same value over and over again for each timestamp. 
How could you re-architect the storage mechanism to be more memory-efficient?

"""

# In my above design, it already accounted for the fact that i do NOT want to copy paste the full config each time any version is changed, i onyl track the hash(values) AND only add a new entry to the key if the value was changed. So this issue shuold be handled by that design. 