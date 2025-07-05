import pydot
from PIL import Image

def draw_tree_graph(tree, tree_type, output_path="static/tree.png"):
    # Large canvas and vertical layout
    graph = pydot.Dot(graph_type='digraph', rankdir='TB', dpi=300)

    # Utility to support multiple node value formats
    def get_node_label(node):
        for attr in ['value', 'data', 'key', 'item']:
            if hasattr(node, attr):
                return str(getattr(node, attr))
        return str(node)

    # Unique node ID to allow duplicates in values
    node_id_counter = [0]
    node_map = {}  # Maps actual nodes to unique IDs

    def get_unique_id(node):
        if node not in node_map:
            node_id_counter[0] += 1
            node_map[node] = f"n{node_id_counter[0]}"
        return node_map[node]

    def add_nodes_edges(node):
        if node is None:
            return

        curr_id = get_unique_id(node)
        curr_label = get_node_label(node)
        graph.add_node(pydot.Node(curr_id, label=curr_label, style="filled", fillcolor="#AED6F1", shape="circle", fontsize="14"))

        if hasattr(node, 'left') and node.left:
            left_id = get_unique_id(node.left)
            left_label = get_node_label(node.left)
            graph.add_node(pydot.Node(left_id, label=left_label, style="filled", fillcolor="#ABEBC6", shape="circle", fontsize="14"))
            graph.add_edge(pydot.Edge(curr_id, left_id, color="#1F618D"))
            add_nodes_edges(node.left)

        if hasattr(node, 'right') and node.right:
            right_id = get_unique_id(node.right)
            right_label = get_node_label(node.right)
            graph.add_node(pydot.Node(right_id, label=right_label, style="filled", fillcolor="#F9E79F", shape="circle", fontsize="14"))
            graph.add_edge(pydot.Edge(curr_id, right_id, color="#884EA0"))
            add_nodes_edges(node.right)

    def add_trie_nodes(node, prefix="*"):
        graph.add_node(pydot.Node(prefix, shape="circle", style="filled", fillcolor="#D5F5E3", fontsize="14"))
        for char, child in node.children.items():
            child_label = prefix + char
            graph.add_node(pydot.Node(child_label, shape="circle", style="filled", fillcolor="#FADBD8", fontsize="14"))
            graph.add_edge(pydot.Edge(prefix, child_label, label=char, fontsize="12"))
            add_trie_nodes(child, child_label)

    if tree_type == "trie":
        add_trie_nodes(tree.root)
    else:
        add_nodes_edges(tree.root)

    graph.write_png(output_path)

    # Optionally resize large image (e.g., 1500px width)
    img = Image.open(output_path)
    img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
    img.save(output_path)
