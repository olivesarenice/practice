# Topological Sort (Kahn's Algorithm) Explained

## Overview
Topological Sort determines if a directed acyclic graph (DAG) exists and can produce a linear ordering of vertices. For job dependencies, this tells us if all jobs can be completed and in what order.

## Algorithm Steps Breakdown

### Step 1: Build Graph and Calculate In-Degrees
```python
# Build adjacency list and in-degree count
graph = defaultdict(list)
in_degree = defaultdict(int)

# Initialize all jobs
for job in jobs:
    in_degree[job] = 0

# Build graph
for job, dependencies in jobs.items():
    for dep in dependencies:
        graph[dep].append(job)  # dep -> job edge
        in_degree[job] += 1     # job has one more dependency
```

**What this does:**
- Creates a graph where edges point from dependencies to jobs that depend on them
- Counts how many dependencies each job has (in-degree)

### Step 2: Find Starting Points
```python
queue = deque([job for job in jobs if in_degree[job] == 0])
```

**What this does:**
- Jobs with in-degree 0 have no dependencies and can start immediately
- These become our starting points

### Step 3: Process Jobs and Update Dependencies
```python
while queue:
    current = queue.popleft()
    processed += 1
    
    # Remove current job and update dependents
    for dependent in graph[current]:
        in_degree[dependent] -= 1
        if in_degree[dependent] == 0:
            queue.append(dependent)
```

**What this does:**
- Process a job that has no remaining dependencies
- "Remove" this job by decreasing the in-degree of all jobs that depend on it
- If any dependent job now has in-degree 0, it can be processed next

### Step 4: Check Completeness
```python
return processed == len(jobs)
```

**What this does:**
- If we processed all jobs, the workflow can complete
- If we processed fewer jobs, there's a cycle (deadlock)

## Sample Case 1: Valid Workflow

**Input:**
```python
jobs = {
    "a": [],           # No dependencies
    "b": ["a"],        # Depends on a
    "c": ["a"],        # Depends on a  
    "d": ["b"],        # Depends on b
    "e": ["d", "c"]    # Depends on d and c
}
```

**Step-by-step execution:**

### Initial State:
```
Graph:
a -> [b, c]
b -> [d]
c -> [e]
d -> [e]
e -> []

In-degrees:
a: 0, b: 1, c: 1, d: 1, e: 2

Queue: [a]  (only 'a' has in-degree 0)
```

### Iteration 1: Process 'a'
```
Remove 'a' from queue
processed = 1

Update dependents of 'a': b, c
- b: in-degree 1 -> 0  (add to queue)
- c: in-degree 1 -> 0  (add to queue)

Queue: [b, c]
In-degrees: a: 0, b: 0, c: 0, d: 1, e: 2
```

### Iteration 2: Process 'b'
```
Remove 'b' from queue  
processed = 2

Update dependents of 'b': d
- d: in-degree 1 -> 0  (add to queue)

Queue: [c, d]
In-degrees: a: 0, b: 0, c: 0, d: 0, e: 2
```

### Iteration 3: Process 'c'
```
Remove 'c' from queue
processed = 3

Update dependents of 'c': e
- e: in-degree 2 -> 1  (still has dependencies)

Queue: [d]
In-degrees: a: 0, b: 0, c: 0, d: 0, e: 1
```

### Iteration 4: Process 'd'
```
Remove 'd' from queue
processed = 4

Update dependents of 'd': e
- e: in-degree 1 -> 0  (add to queue)

Queue: [e]
In-degrees: a: 0, b: 0, c: 0, d: 0, e: 0
```

### Iteration 5: Process 'e'
```
Remove 'e' from queue
processed = 5

No dependents to update

Queue: []
```

**Result:** `processed (5) == len(jobs) (5)` → **TRUE** (workflow can complete)

**Execution order:** a → b → c → d → e

## Sample Case 2: Cyclic Dependency (Deadlock)

**Input:**
```python
jobs = {
    "a": ["c"],        # Depends on c
    "b": ["a"],        # Depends on a
    "c": ["b"]         # Depends on b  (creates cycle: a->c->b->a)
}
```

**Step-by-step execution:**

### Initial State:
```
Graph:
c -> [a]
a -> [b]
b -> [c]

In-degrees:
a: 1, b: 1, c: 1

Queue: []  (no job has in-degree 0!)
```

### Processing:
```
Queue is empty, so while loop never executes
processed = 0
```

**Result:** `processed (0) != len(jobs) (3)` → **FALSE** (deadlock detected)

## Sample Case 3: Mixed Dependencies

**Input:**
```python
jobs = {
    "extract": [],
    "transform": ["extract"],
    "load": ["transform"],
    "validate": ["extract"],
    "report": ["load", "validate"]
}
```

**Execution trace:**
1. **Initial:** extract (in-degree 0) → Queue: [extract]
2. **Process extract:** transform, validate become available → Queue: [transform, validate]  
3. **Process transform:** load becomes available → Queue: [validate, load]
4. **Process validate:** report gets one dependency satisfied → Queue: [load]
5. **Process load:** report gets final dependency satisfied → Queue: [report]
6. **Process report:** Done → Queue: []

**Result:** All 5 jobs processed → **TRUE** (workflow can complete)

## Why This Algorithm Works

1. **Cycle Detection:** If there's a cycle, no job in the cycle will ever have in-degree 0, so they'll never be processed
2. **Dependency Respect:** Jobs are only processed when all their dependencies are complete
3. **Completeness Check:** Comparing processed count with total jobs reveals if any jobs were stuck
4. **Efficiency:** O(V + E) time complexity where V = jobs, E = dependencies

## Key Insights

- **Queue represents "ready to run" jobs** - those with no remaining dependencies
- **In-degree tracks remaining dependencies** - decreases as dependencies complete  
- **Graph represents "unlocks relationship"** - completing a job may unlock others
- **Algorithm naturally handles complex dependency chains** without explicit recursion
