"""
Imagine you're building a system to run data processing jobs. These jobs have dependencies; for example, a 'transform' job can't run until an 'extract' job is finished. You're given a set of these jobs and their dependencies. How would you design a program to determine if this workflow can actually run to completion, or if it's stuck in a deadlock?
"""

jobs = {
    "a": [],
    "b": [],
    "c": ["a"],
    "d": ["b"],
    "e": ["d", "c"],
    "f": ["c"],
    "g": ["e", "f"],
    # "a": ["f"],  # force cyclic
}

job_durations = {
    "a": 5,
    "b": 3,
    "c": 2,
    "d": 1,
    "e": 8,
    "f": 3,
    "g": 4,
    # "a": ["f"],  # force cyclic
}

# Could not solve this question ):
# This is a DAG topological sort

# This is my re-doing of the algorithm

# First create 2 structures:
from collections import (
    defaultdict,
)  # useful data structure which allows you to operate on a dict even if the key hasnt been created. it will auto create the key:default_value for you and then apply to it.


graph = defaultdict(list)
in_degree = defaultdict(int)

# Set in_degree 0 for all first, before we update
for job in jobs.keys():
    in_degree[job] = 0

# Create the graph relations
for job, deps in jobs.items():
    # Create the in-degree counter

    for dep in deps:
        # dep > job
        graph[dep].append(
            job
        )  # add the jobs to the graph list, or create it if it doesnt exist

        # Also track all the incoming edges into each job (node)
        in_degree[job] += 1

print(graph)
print(in_degree)


# Assuming k >> number of parallel nodes for any graph, we can say that the shortest duration to complete the DAG is also the path along the nodes where we select nodes where the duration is minimum whenever we have the choice.

# First create the transition times from node1 --> node2

graph_timed = defaultdict(list)

for job, deps in jobs.items():
    time_to_transition = job_durations[job]
    for dep in deps:
        graph_timed[dep].append((job, time_to_transition))

print(graph_timed)


# Now we start processing each job in sequence, starting from the job with NO dependencies (i.e. no in_degrees)
from collections import deque

process_q = deque([job for job in in_degree.keys() if in_degree[job] == 0])
print(process_q)

processed = 0
processed_log = []
processed_log_fastest = []
while len(process_q) > 0:  # keep processing until we are out
    job = process_q.popleft()
    processed += 1  # "process" the upstream job
    processed_log.append(job)

    for dependant in graph[job]:
        in_degree[dependant] -= 1  # remove the dependency from the next dependent.
        if (
            in_degree[dependant] == 0
        ):  # once the next dependent has no more dependecies, we can treat it as the terminal node

            process_q.append(dependant)  # and add it to the queue for processing

# Once we are done going through all in the queue, check if we have processed ALL jobs.
if processed == len(jobs):
    print("Success")
    print(f"Processed in order: {processed_log}")
else:
    print("Could not finish processing all jobs")

# """
# STAGE 3:
# Let's introduce performance. Each job takes a certain amount of time to run. To speed things up, we can use a cluster of k machines to run jobs in parallel. How would you approach calculating the shortest possible time to finish the entire workflow?
# """
# Critical Path Analysis: https://www.youtube.com/watch?v=4oDLMs11Exs

# Gemini provided Critical Path Algo!n Study this again:

# def find_critical_path(jobs, job_durations):
#     """
#     Calculates the critical path and total duration for a project.

#     Args:
#         jobs (dict): A dictionary where keys are job names and values are lists
#                      of prerequisite job names.
#         job_durations (dict): A dictionary mapping job names to their durations.

#     Returns:
#         tuple: A tuple containing the critical path (list) and the total
#                project duration (int).
#     """

#     # 1. Build the graph structure for easy traversal
#     in_degree = {job: 0 for job in jobs}
#     successors = {job: [] for job in jobs}
#     predecessors = {job: [] for job in jobs}

#     for job, deps in jobs.items():
#         in_degree[job] = len(deps)
#         for dep in deps:
#             successors[dep].append(job)
#             predecessors[job].append(dep)

#     # 2. Perform a topological sort to get a valid processing order
#     queue = [job for job, degree in in_degree.items() if degree == 0]
#     topological_order = []
#     while queue:
#         current_job = queue.pop(0)
#         topological_order.append(current_job)
#         for successor in successors[current_job]:
#             in_degree[successor] -= 1
#             if in_degree[successor] == 0:
#                 queue.append(successor)

#     # 3. Forward Pass: Calculate earliest start (ES) and earliest finish (EF)
#     es = {job: 0 for job in jobs}
#     ef = {job: 0 for job in jobs}
#     for job in topological_order:
#         max_predecessor_ef = 0 # ! This is just so we have a starting value
#         if job in predecessors: # ! Technically redundant
#             for predecessor in predecessors[job]:
#                 max_predecessor_ef = max(max_predecessor_ef, ef[predecessor]) # ! This is the key part, it ensures that we always take the largest EF (earliest finish) across all predecessor nodes leading into the current job. Nice thing is that doesn't matter what order you do the check, it will always recalculate the max anyway.
#         es[job] = max_predecessor_ef # ! Do the "carry forward"
#         ef[job] = es[job] + job_durations[job]

#     project_duration = max(ef.values())

#     # 4. Backward Pass: Calculate latest start (LS) and latest finish (LF)
#     ls = {job: 0 for job in jobs}
#     lf = {job: project_duration for job in jobs} # Initial LF is project duration

#     for job in reversed(topological_order):
#         min_successor_ls = float('inf')
#         if job in successors and successors[job]:
#             for successor in successors[job]:
#                 min_successor_ls = min(min_successor_ls, ls[successor])
#             lf[job] = min_successor_ls

#         ls[job] = lf[job] - job_durations[job]

#     # 5. Identify the critical path by finding jobs with zero slack
#     critical_path = [job for job in topological_order if es[job] == ls[job]]

#     return critical_path, project_duration

# # Example Usage:
# jobs = {
#     "a": [], "b": [], "c": ["a"], "d": ["b"],
#     "e": ["d", "c"], "f": ["c"], "g": ["e", "f"],
# }
# job_durations = {
#     "a": 5, "b": 3, "c": 2, "d": 1,
#     "e": 8, "f": 3, "g": 4,
# }

# path, duration = find_critical_path(jobs, job_durations)
# print(f"The critical path is: {path}")
# print(f"The total project duration is: {duration}")


### REVIEW:

# Need to study more on DAGs and the topological sort algorithm - seems like a key topic in dependency checking
# Also study critical path algorithms. Conceptually is a very intuitive approach, but coding it out requires the appropriate data structures.
