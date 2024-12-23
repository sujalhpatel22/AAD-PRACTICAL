from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

# Function to calculate shortest path using Dijkstra's algorithm
def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get number of nodes and create the graph
        num_nodes = int(request.form['num_nodes'])
        nodes = [request.form.get(f'node_{i}') for i in range(num_nodes)]
        
        # Initialize graph as an empty dictionary
        graph = {node: [] for node in nodes}
        
        # Get edges from user input
        num_edges = int(request.form['num_edges'])
        for i in range(num_edges):
            source = request.form.get(f'edge_{i}_source')
            destination = request.form.get(f'edge_{i}_destination')
            weight = request.form.get(f'edge_{i}_weight')
            
            # Validate and convert weight to integer
            try:
                weight = int(weight)
            except (TypeError, ValueError):
                return "Error: All weights must be valid integers.", 400

            # Ensure source and destination nodes are valid
            if source not in graph or destination not in graph:
                return "Error: Source or destination node does not exist in the node list.", 400
            
            graph[source].append((destination, weight))
            graph[destination].append((source, weight))  # Assuming undirected graph

        # Get the source node for shortest path calculation
        source_node = request.form.get('source_node')
        if source_node not in graph:
            return "Error: Source node does not exist in the node list.", 400
        
        shortest_paths = dijkstra(graph, source_node)

        # Render result page with shortest paths
        return render_template('index.html', graph=graph, shortest_paths=shortest_paths, source_node=source_node, nodes=nodes)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
