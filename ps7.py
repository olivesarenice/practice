# Assume the data scope only contains these primitive types:
tracker = {}
ref_count = 0


# each top level key is key=...;value=...
# delimiter is _
# types:

# reserved characters are : `,` for lists delimiters | `;` for key-to-value mapping | `_` for dict items

#value = 
# int::123
# float::123
# list::item1,item2,item3
# map::{a:b}
# nested map --> map::{a:map::{b:c}}
def escape(s:str)->str:
    reserved_chars = [";", ":", ":", "{", "}", ",", "\\"]
    escaped_string = ""
    # print("--ESCAPED--")
    # print(s)
    
    for c in s:
        if c in reserved_chars:
            c = "\\" + c
        escaped_string += c
            
    # print(escaped_string)
    return escaped_string

def ser_int(i:int)->str:
    return f"int::{str(i)}"

def ser_f(f:float)->str:
    return f"float::{str(f)}"

def ser_s(s:str)->str:
    s = escape(s)
    return f"string::{s}"

def ser_b(b:bool)->str:
    if b is True:
        return f"bool::true"
    elif b is False:
        return f"bool::false"

def ser_null()->str:
    return "null"

def ser_ls(l:list)->str:
    global tracker
    global ref_count
    seen = tracker.get(id(l), None)
    if seen:
        return f"ref::{seen}"
    else:
        ref_count += 1
        tracker[id(l)] = ref_count
        
    ser = ""
    for item in l:
        if isinstance(item, list): # handle nested lists
            ser_item = ser_ls(item)
        elif isinstance(item, float):
            ser_item = ser_f(item)
        elif isinstance(item, bool):
            ser_item = ser_b(item)
        elif isinstance(item, int):
            ser_item = ser_int(item)
        elif isinstance(item, str):
            ser_item = ser_s(item)
        elif item is None:
            ser_item = ser_null()
       
        # We assume that the list may not contain nested maps for simplicity, but if it does, we have to recursively call the ser_map from here.
        
        ser += ser_item
        ser += ","
    
    ser = ser[0:-1] # Drop the last ,
    return f"list::[{ser}]"

def ser_map(object:dict)->str:
    global tracker
    global ref_count
    ser = ""
    seen = tracker.get(id(object), None)
    if seen:
        return f"ref::{seen}"
    else:
        ref_count += 1
        tracker[id(object)] = ref_count
        
    for key, item in object.items():
        print(key, item)
        # key is always a string
        if isinstance(item, dict):
            ser_item = ser_map(item)
        elif isinstance(item, list):
            ser_item = ser_ls(item)
        elif isinstance(item, float):
            ser_item = ser_f(item)
        elif isinstance(item, str):
            ser_item = ser_s(item)
        elif isinstance(item, bool):
            ser_item = ser_b(item)
        elif isinstance(item, int): # int has to come after the bool check bc bool is a subclass of int in python!
            ser_item = ser_int(item)
        elif item is None:
            ser_item = ser_null()
        
        ser_key = escape(key)
        ser_term = f"{ser_key}:{ser_item}"
        ser += ser_term
        ser += ","
        
    ser = ser[0:-1] # drop the last ,
    return f"map::{{{ser}}}"



print("---"*20)
test_object = {
    "user_id": 123,
    "user_name": "Alice",
    "is_active": True,
    "courses": ["math", "history"],
    "profile": {
        "details": "A user with ; and , in their bio.",
        "rating": 4.5,
        "metadata": None
    },
    "version:0.1.0":True
}
print(test_object)
print(">>>")
s = ser_map(test_object)
print(s)

# ref_map = {f"ref::{v}":k for k,v in tracker.items()}
# print(ref_map)

# implement cyclic referencing


cyclic_list = ["a", "b"]
cyclic_list2 = ["d", "e"]
cyclic_list.append(cyclic_list)
cyclic_list.append(cyclic_list)
cyclic_list.append(cyclic_list2)
cyclic_list.append(cyclic_list2)

cl = ser_ls(cyclic_list)

print("---"*20)
print(cyclic_list)
print(">>>")
print(cl)
# print(ref_map)
    
    
    
### REVIEW
# This was not super challenging with the prompts from Gemini and Q&A, but very tedious because of all the cases that need to be considered
# The main idea here is recursion
# It was also easier to stick with a simple solution rather than a complex one with lots of detail
# For example, I should have stuck with a simple typed system like int:: float:: map:: list:: bool:, and avoided fancy delimiter systems

# Some cool functions I learned
# - using id(object) to get the memory address of an object. this is useful for tracking objects which CANNOT be .__hash__() such as dicts and list
# - implementation of string escaping where you loop through each character, check if its in reserved_chars and then adding \\ to it.
# - python booleans are a SUBCLASS of int, which means we should always check for isinstance(bool) before isinstance(int)


"""
::: GEMINI REVIEW:::

JS SWE Interview Mentor
Custom Gem

Show thinking
Of course. Here is a summary of our mock interview session.

Part 1: Basic Serialization
You were tasked with creating a custom string format to serialize a nested data object.

Initial Proposal & Weaknesses: Your first idea was a delimited string (e.g., key=value;key2=value2). We quickly identified two main weaknesses:

Delimiter Collision: The format would break if a string value contained one of your special characters (;, =, _, ,).

Lack of Nesting: The flat structure could not represent nested dictionaries or lists.

Solutions & Refinements: You addressed these issues effectively:

To solve delimiter collision, you correctly proposed using an escape character (\).

To handle nesting, you redesigned the format to use braces for dictionaries and brackets for lists (e.g., map::{...} and list::[...]), creating a fully recursive and robust structure.

Implementation Bugs: In your first coding attempt, we found and fixed three subtle bugs:

You corrected the isinstance check order to handle booleans before integers, as bool is a subclass of int in Python.

You rewrote the escape function to be more robust by iterating character-by-character.

You applied the escape() function to dictionary keys to make the format fully safe.

======

Part 2: Handling Cyclical References
The next challenge was to make your serializer handle objects that refer back to themselves.

Initial Proposal & Weakness: Your instinct to track already-seen objects in a map was correct. However, your proposal to use the object's hash() as the key was flawed, because mutable objects like lists and dictionaries are not hashable.

Solution: I guided you toward using an object's unique memory address, which you accessed with the id() function. You correctly determined that this ID could be mapped to a simple, incrementing reference counter (e.g., ref::1, ref::2) for the string output.

Design Improvement: Your implementation correctly handled cycles but initially used global variables for the tracker and counter. We discussed how this was not a re-entrant design and concluded that a better pattern is a main wrapper function that initializes state and passes it down to a recursive helper function.

======

Part 3: Forward & Backward Compatibility
The final task was a high-level design discussion on making the format evolve safely over time.

QUESTION:

>>>
Your serializer is now robust and handles cycles. It's been running in production for a year, and we have millions of objects stored in our database in the format you designed.

Now we face a new challenge: the program is evolving. The developers need to change the structure of the data objects over time.

A new field might be added (e.g., adding an email field to a user profile).

An existing field might be renamed (e.g., user_name becomes full_name).

An existing field might be removed.

The problem is that your current format is very brittle. If an old version of the program tries to read data saved by a new version, it might crash. If a new version tries to read old data, it won't find the new fields it expects. We need a format that is both forward and backward compatible.

Backward Compatibility: An old program can read new data (and safely ignore fields it doesn't recognize).

Forward Compatibility: A new program can read old data (and handle missing fields with sensible defaults).
>>>

Initial Proposal & Weakness: You suggested embedding a version number in the string and maintaining a central map of transformation rules to migrate data from one version to another. We discussed that while logical, this approach would become extremely complex and hard to maintain as the number of versions grew.

Solution: I introduced an alternative, industry-standard approach. You quickly understood and articulated the benefits of using permanent, unique numeric tags for each field instead of string names. You correctly explained how this would work:

THIS IS CALLED A SCHEMA REGISTRY

Backward Compatibility: Old parsers would simply ignore unknown tags.

Forward Compatibility: New parsers would apply a default value for any expected tags that were missing from old data

"""