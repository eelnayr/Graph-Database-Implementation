import json   #imports JSON modules
import re     #imports the regular expression module


# It encapsulates the properties and type of a node,
# provides a consistent way to identify and access nodes in the graph.
class Node:
    def __init__(self, node_type, node_id, properties):
        self.id = node_id
        self.type = node_type
        self.properties = properties


# It represents a directed, typed connection from one node to another,
# stores metadata about that relationship (called properties)
class Relationship:
    def __init__(self, rel_type, from_node, to_node, properties):
        self.type = rel_type
        self.from_node = from_node
        self.to_node = to_node
        self.properties = properties


# It handles the storage, creation, retrieval, modification, and 
# traversal of the graph structure (nodes and relationships), entirely in memory.
class Graph:

    # The __init__ method is automatically called when a new instance of a class is created. 
    # It’s primarily used to set up the initial values or properties of the object.
    def __init__(self):
        self.nodes = {} 
        self.relationships = []


    # Responsible for creating and adding a new node to the graph database
    def create_node(self, node_type, properties):
        if node_type not in self.nodes:
            self.nodes[node_type] = []
        self.nodes[node_type].append({"type": node_type, **properties})
        
    
    # Responsible for creating a relationship between two nodes in the graph. 
    # The relationship has a type, connects two specific nodes, and may have properties associated with it.
    def create_relationship(self, rel_type, from_type, from_id, to_type, to_id, properties):
        from_node = self.get_node(from_type, from_id)
        to_node = self.get_node(to_type, to_id)
        
        if from_node and to_node:
            self.relationships.append({
                "type": rel_type,
                "from": from_id,
                "to": to_id,
                **properties
           
            })
   

    # Used to retrieve a specific node from the graph by searching for it based on its type and unique identifier. 
    # Allows the user to query the graph for a node and obtain its properties or perform other operations.
    def get_node(self, node_type, node_id):
        for node in self.nodes.get(node_type, []):
            if node.get("id") == node_id:
                return node
        
        return None


    # Used to retrieve a specific node from the graph based on its unique identifier. 
    # Searches for a node by its ID across all the nodes in the graph, regardless of its type.
    def get_node_by_id(self, id):
        for node_list in self.nodes.values():
            for node in node_list:
                if node["id"] == id:
                    return node
        
        return None


    # Retrieves the connected nodes (neighbors) of a given node in the graph based on certain relationship types and traversal direction. 
    # Used to perform traversal queries in the graph, helping to explore adjacent nodes connected by specific types of relationships.
    def get_neighbors(self, node, rel_type, direction):
        results = []
        for rel in self.relationships:
            if rel["type"] != rel_type:
                continue
            
            if direction == "out" and rel["from"] == node["id"]:
                target_node = self.get_node_by_id(rel["to"])
                results.append((rel, target_node))
            
            elif direction == "in" and rel["to"] == node["id"]:
                source_node = self.get_node_by_id(rel["from"])
                results.append((rel, source_node))
        
        return results


    # Designed to update the properties of an existing relationship in the graph database. 
    # This method modifies the properties of a relationship between two nodes, specified by the relationship type (rel_type), 
    # the IDs of the two nodes (from_id and to_id), and the new properties to be applied.
    def update_relationship_properties(self, rel_type, from_id, to_id, new_properties):
        for rel in self.relationships:
            if rel["type"] == rel_type and rel["from"] == from_id and rel["to"] == to_id:
                rel.update(new_properties)
                return True

        return False


    # Designed to export the current state of the graph database to a JSON file. 
    # This allows the graph's nodes, relationships, and their associated properties to be saved in a format that can be easily shared, 
    # stored, or imported back into the graph database at a later time.
    def export_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump({"nodes": self.nodes, "relationships": self.relationships}, f, indent=2)


    # Designed to import graph data from a JSON file into the graph database. 
    # This allows you to load a previously exported graph from a JSON file and reconstruct the graph’s nodes and relationships, 
    # restoring the graph’s state in memory.
    def import_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.nodes = data["nodes"]
            self.relationships = data["relationships"]


    
# It takes a user-entered command (like CREATE NODE Person {id: 1, name: "Alice"}),
# figures out what the user wants to do, and then calls the appropriate function on the Graph object to perform the action.
def command_parser(graph, command):
    if command.startswith("CREATE NODE"):
        match = re.match(r"CREATE NODE (\w+) \{(.+?)\}", command)
        if match:
            node_type, props = match.groups()
            props = json.loads("{" + props + "}")
            graph.create_node(node_type, props)
    

    elif command.startswith("CREATE RELATIONSHIP"):
        match = re.match(
            r"CREATE RELATIONSHIP (\w+) FROM (\w+)\(id=(\d+)\) TO (\w+)\(id=(\d+)\) \{(.+?)\}",
            command
        )

        if match:
            rel_type, from_type, from_id, to_type, to_id, props = match.groups()
            props = json.loads("{" + props + "}")
            graph.create_relationship(rel_type, from_type, int(from_id), to_type, int(to_id), props)
    
   
    elif command.startswith("UPDATE RELATIONSHIP"):
        match = re.match(
            r"UPDATE RELATIONSHIP (\w+) FROM (\w+)\(id=(\d+)\) TO (\w+)\(id=(\d+)\) \{(.+?)\}",
            command
        )
       
        if match:
            rel_type, from_type, from_id, to_type, to_id, props = match.groups()
            props = json.loads("{" + props + "}")
            success = graph.update_relationship_properties(rel_type, int(from_id), int(to_id), props)  
            if not success:
                print("Relationship not found.")
   
    elif command.startswith("TRAVERSE"):
        handle_traverse(graph, command)


# Responsible for handling a TRAVERSE command within the graph database system. 
# It interprets the command and performs the necessary graph traversal based on the command parameters.
def handle_traverse(graph, command):
    match = re.match(r"TRAVERSE (\w+)\(id=(\d+)\)\s+(.*?)\s+WHERE\s+(.+)", command)
    
    if not match:
        print("Invalid TRAVERSE syntax.")
        return

    start_type, start_id, pattern_str, where_clause = match.groups()
    start_id = int(start_id)

    start_node = graph.get_node(start_type, start_id)
    if not start_node:
        print(f"Start node {start_type}({start_id}) not found.")
        return

    pattern = re.findall(r"-\[(\w+)\]->\s+(\w+)|<-\[(\w+)\]-\s+(\w+)", pattern_str)
    steps = []
    for forward_rel, forward_type, backward_rel, backward_type in pattern:
        if forward_rel:
            steps.append(("out", forward_rel, forward_type))
       
        else:
            steps.append(("in", backward_rel, backward_type))

    results = []

    def dfs(path, current_node, step_idx):
        if step_idx >= len(steps):
            if evaluate_filter_clause(where_clause, path):
                results.append(format_path(path))
            
            return

        direction, rel_type, expected_type = steps[step_idx]
        next_nodes = graph.get_neighbors(current_node, rel_type, direction)

        for rel, next_node in next_nodes:
            if next_node["type"] == expected_type:
                dfs(path + [(rel, next_node)], next_node, step_idx + 1)

    dfs([(None, start_node)], start_node, 0)

    print("Results:")
    
    for result in results:
        print(json.dumps(result, indent=2))


# Responsible for evaluating the conditions specified in a WHERE clause of a graph query. 
# This is part of the process where the graph database applies filtering logic to ensure that only the nodes and 
# relationships that match the criteria in the WHERE clause are included in the result.
def evaluate_filter_clause(where_clause, path):
    for _, node in path:
        for clause in where_clause.split("AND"):
            clause = clause.strip()
            match = re.match(r"(\w+)\.(\w+)\s*([<>=!]+)\s*(.+)", clause)
            
            if not match:
                continue
            
            type_name, prop, op, value = match.groups()
            value = eval(value)
            if node["type"] == type_name:
                actual = node.get(prop)
                if not compare(actual, op, value):
                    return False
    return True


# Designed to perform a comparison between two values, a and b, using a specified operator op. 
# The function takes two operands (a and b) and an operator (op), and based on the operator, it returns the result of the comparison.
def compare(a, op, b):
    if op == "<":
        return a < b
    elif op == "<=":
        return a <= b
    elif op == ">":
        return a > b
    elif op == ">=":
        return a >= b
    elif op == "==":
        return a == b
    elif op == "!=":
        return a != b
    
    return False


# Designed to convert a traversal path (a list of nodes and relationships) into a readable, formatted string representation.
def format_path(path):
    nodes = [node for _, node in path]
    rels = [rel for rel, _ in path if rel]
    
    return {
        "path": [f"{node['type']}:{node['id']}" for node in nodes],
        "nodes": nodes,
        "relationships": rels
    }


# Used to control the execution of code when a script is run directly versus when it is imported as a module in another script.
if __name__ == "__main__":
    graph = Graph()

    command_parser(graph, 'CREATE NODE Person {"id": 1, "name": "Alice", "age": 30}')
    command_parser(graph, 'CREATE NODE Person {"id": 2, "name": "Bob", "age": 28}')
    command_parser(graph, 'CREATE NODE Company {"id": 101, "name": "Acme Inc.", "founded": 2010}')
    command_parser(graph, 'CREATE RELATIONSHIP WORKS_AT FROM Person(id=1) TO Company(id=101) {"since": 2018, "role": "Engineer"}')
    command_parser(graph, 'CREATE RELATIONSHIP WORKS_AT FROM Person(id=2) TO Company(id=101) {"since": 2019, "role": "Designer"}')
    command_parser(graph, 'TRAVERSE Person(id=1) -[WORKS_AT]-> Company <-[WORKS_AT]- Person WHERE Person.age < 35')



