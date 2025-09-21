# Day 1: Task Scheduler
Imagine you're building a system to run data processing jobs. These jobs have dependencies; for example, a 'transform' job can't run until an 'extract' job is finished. You're given a set of these jobs and their dependencies. How would you design a program to determine if this workflow can actually run to completion, or if it's stuck in a deadlock?

<details>
<summary>Level 2 (The Follow-up)</summary>
Now, your program needs to produce an actual execution plan. Given a valid workflow, how would you determine a sequence of steps to run the jobs one by one?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
Let's introduce performance. Each job takes a certain amount of time to run. To speed things up, we can use a cluster of k machines to run jobs in parallel. How would you approach calculating the shortest possible time to finish the entire workflow?
</details>

# Day 2: Real-Time Leaderboard
We need to build a real-time leaderboard for an online game. The system will receive a continuous stream of scores from players, and we need a way to efficiently query for the top k players at any given moment. How would you design a program to handle this?

<details>
<summary>Level 2 (The Follow-up)</summary>
A new requirement comes in: the leaderboard should rank players by their cumulative score, not just their single best score. How would your design need to change to support this?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
To keep the game exciting, the leaderboard needs to be dynamic. It should only show the top players based on scores achieved in the last five minutes. How can you adapt your system to handle this 'sliding window' of data efficiently?
</details>

# Day 3: Text Autocomplete System
You're tasked with building an autocomplete feature for a search bar. The system will be given a massive corpus of text, like all Wikipedia titles. When a user starts typing, we need to suggest titles that match their input. How would you build a program to provide these suggestions?

<details>
<summary>Level 2 (The Follow-up)</summary>
The initial version is too slow for a real-time application. With millions of potential sentences, searching them live as the user types is not feasible. How would you re-architect your solution to provide suggestions almost instantaneously?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
Not all suggestions are equal. We have data on how popular each sentence (or search query) is. How would you enhance your system to show the most relevant suggestions first, for example, the top 3 most popular matches for what the user has typed?
</details>

# Day 4: Versioned Key-Value Store
We need a simple in-memory configuration service. It should store configuration values by key and allow us to retrieve them. How would you design a program to provide this basic key-value storage?

<details>
<summary>Level 2 (The Follow-up)</summary>
A critical new feature is the ability to audit changes and retrieve historical values. We need to be able to query the value of any key as it was at a specific point in time. How would you modify your design to support this 'time-travel' capability?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
The versioned store has been running in production, and we've noticed its memory footprint is growing uncontrollably. The primary cause seems to be that many keys don't change value for long periods, but we're storing the same value over and over again for each timestamp. How could you re-architect the storage mechanism to be more memory-efficient?
</details>

# Day 5: Arbitrage Calculator
You're building a tool for a currency trading desk. The tool needs to be able to calculate the conversion path between any two currencies, given a set of direct exchange rates (e.g., USD to EUR, EUR to GBP, etc.). How would you write a program to solve this?

<details>
<summary>Level 2 (The Follow-up)</summary>
The real value of this tool would be in automatically spotting profit opportunities. An 'arbitrage' is a cycle of trades that results in a net profit. How could your program analyze the exchange rates to detect if any such opportunities exist?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
In the real world, exchange rates update constantly. A full re-calculation every time a single rate changes is too slow. How would you design your system to handle a high-frequency stream of rate updates and report arbitrage opportunities with very low latency?
</details>

# Day 6: Block Stacking Game
Let's model a simple block stacking game. The game board is a set of columns of a fixed width, and players can add colored blocks to the top of any column. How would you write a program to represent the game board and handle the addition of new blocks?

<details>
<summary>Level 2 (The Follow-up)</summary>
Let's introduce a placement rule: a new block cannot be the same color as any of its adjacent neighbors (up, down, left, right). How would you incorporate this constraint check into your program?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
To make the game more interesting, we're adding a clearing mechanism. When a 2x2 square of same-colored blocks is formed, those four blocks are removed. Any blocks above the cleared space fall down to fill the gap. This can cause chain reactions. How would you implement this game logic?
</details>

# Day 7: Data Serializer
We need a way to save and load the state of a program. The state is represented by a complex data object containing nested dictionaries, lists, and other objects. How would you write a program to convert this in-memory object into a string for storage, and then convert it back into a fully functional object later?

<details>
<summary>Level 2 (The Follow-up)</summary>
We've discovered a bug: if the data object contains cyclical references (e.g., an object that refers to itself), the serialization process enters an infinite loop. How can you make your serialization and deserialization logic robust enough to handle these cycles?
</details>

<details>
<summary>Level 3 (The Extension)</summary>
The program we're saving state for will evolve over time, meaning the structure of the data object will change (e.g., new fields will be added). We need a serialization format that is forward and backward compatible. How would you design such a format? You don't need to write the code, but describe the principles and structure of your proposed format.
</details>