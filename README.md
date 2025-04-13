In-Memory Graph Database

Overview:
This is an in-memory graph database that supports CRUD operations for nodes and relationships, graph traversal with filtering conditions, and pattern matching for subgraph queries. It uses Python's built-in libraries and is intended to run entirely in memory, with optional export/import to/from a JSON file for basic persistence.

-------------------------------------------------------------------

Features:
- Node CRUD Operations: Create and modify nodes with properties.
- Relationship CRUD Operations: Create, modify, and query relationships between nodes.
- Graph Traversal: Perform pathfinding and traversals with filtering conditions.
- Pattern Matching: Execute subgraph queries to find matching patterns in the graph.
- Persistence: Export and import graph data to/from JSON files.

-------------------------------------------------------------------

Setup Instructions
1. Clone the repository:
   git clone *https://github.com/yourusername/graph-database.git*
   cd graph-database

2. Install Python 3.x: Ensure you have Python 3.6 or later installed. You can check your Python version with:

-------------------------------------------------------------------

Query Syntax
The database supports a simple command-line interface to create nodes, relationships, perform traversals, and execute pattern matching. The query syntax follows these patterns:

Create Node:
To create a new node with properties:
Example : CREATE NODE <NodeType> {<property1>: <value1>, <property2>: <value2>, ...}

Create Relationship:
To create a relationship between two nodes:
Example : CREATE RELATIONSHIP <RelType> FROM <NodeType1>(<id1>) TO <NodeType2>(<id2>) {<property1>: <value1>, <property2>: <value2>, ...}

Traverse:
To traverse the graph:
Example : TRAVERSE <NodeType>(<id>) -[<RelType>]-> <NodeType2>
WHERE <condition>

Match (Pattern Matching):
To find subgraphs that match a given pattern:
MATCH (<node1>:<Type1>)-[<rel1>:<RelType1>]->(<node2>:<Type2>)
WHERE <condition>

-------------------------------------------------------------------

Supported Operations
1. Create Node:
Command: CREATE NODE <NodeType> {<properties>}
Example: CREATE NODE Person {id: 1, name: "Alice", age: 30}

2. Create Relationship:
Command: CREATE RELATIONSHIP <RelType> FROM <NodeType1>(<id1>) TO <NodeType2>(<id2>) {<properties>}
Example: CREATE RELATIONSHIP WORKS_AT FROM Person(id=1) TO Company(id=101) {since: 2018, role: "Engineer"}

3. Get Node by ID:
Command: GET NODE <NodeType> <NodeID>
Example: GET NODE Person 1

4. Get Neighbors:
Command: GET NEIGHBORS <NodeType> <NodeID> WITH RELATIONSHIP <RelType> DIRECTION <direction>
Example: GET NEIGHBORS Person 1 WITH RELATIONSHIP WORKS_AT DIRECTION OUTGOING

5. Traverse:
Command: TRAVERSE <NodeType>(<NodeID>) -[<RelType>]-> <NodeType2> WHERE <condition>
Example: TRAVERSE Person(id=1) -[WORKS_AT]-> Company WHERE Person.age < 35

6. Pattern Matching:
Command: MATCH (<node1>:<Type1>)-[<rel1>:<RelType1>]->(<node2>:<Type2>) WHERE <condition>
Example: MATCH (a:Person)-[r:KNOWS]->(b:Person)-[w:WORKS_AT]->(c:Company) WHERE a.age > 25 AND c.name = "Acme Inc."

7. Export to JSON:
Command: EXPORT TO JSON <filename>
Example: EXPORT TO JSON graph_data.json

8. Import from JSON:
Command: IMPORT FROM JSON <filename>
Example: IMPORT FROM JSON graph_data.json

-------------------------------------------------------------------

Example Usage
Example 1: Create Nodes and Relationships
CREATE NODE Person {id: 1, name: "Alice", age: 30}
CREATE NODE Person {id: 2, name: "Bob", age: 28}
CREATE NODE Company {id: 101, name: "Acme Inc.", founded: 2010}

CREATE RELATIONSHIP WORKS_AT FROM Person(id=1) TO Company(id=101) {since: 2018, role: "Engineer"}
CREATE RELATIONSHIP KNOWS FROM Person(id=1) TO Person(id=2) {since: 2015}

Example 2: Perform Traversal Query
TRAVERSE Person(id=1) -[WORKS_AT]-> Company
WHERE Person.age < 35


Output:
[
  {
    "path": ["Person:1", "WORKS_AT", "Company:101"],
    "nodes": [
      {"id": 1, "type": "Person", "name": "Alice", "age": 30},
      {"id": 101, "type": "Company", "name": "Acme Inc.", "founded": 2010}
    ],
    "relationships": [
      {"type": "WORKS_AT", "from": 1, "to": 101, "since": 2018, "role": "Engineer"}
    ]
  }
]
