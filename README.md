# misc
import networkx as nx
import matplotlib.pyplot as plt

# Sample skill matrix data
data = {
    'Employee 1': {'Java': 3, 'Python': 2, 'Scala': 1, 'Data Stage': 2, 'Teradata': 4},
    'Employee 2': {'Java': 2, 'Python': 3, 'Scala': 2, 'Data Stage': 1, 'Teradata': 3},
    # ... Add more employees and their skills and proficiencies
}

# Create a graph
G = nx.Graph()

# Add nodes for employees
for employee in data:
    G.add_node(employee)

# Add edges for skills with proficiency levels as weights
for employee, skills in data.items():
    for skill, proficiency in skills.items():
        G.add_edge(employee, skill, weight=proficiency)

# Create positions for nodes
pos = nx.spring_layout(G)

# Draw nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

# Set edge labels as proficiency levels
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Employee Skill Network Graph")
plt.axis('off')
plt.show()
