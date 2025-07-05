from trees.binary_tree import BinarySearchTree
from trees.avl_tree import AVLTree
from trees.trie import Trie
from utils.graph_drawer import draw_tree_graph
from utils.helpers import rearrange_binary_tree
import os
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = "snk"  # Required for session usage

# Tree Instances
tree_types = {
    "binary": BinarySearchTree(),
    "avl": AVLTree(),
    "trie": Trie()
}

graph_image_path = os.path.join("static", "tree.png")

@app.route('/')
def index():
    tree_type = session.get("tree_type", "binary")

    descriptions = {
        "binary": "A Binary Search Tree (BST) is a hierarchical data structure in which each node has at most two children. Left child nodes contain values less than the parent node, and right child nodes contain values greater than the parent.",
        "avl": "An AVL Tree is a self-balancing Binary Search Tree. It maintains a balance factor for each node and performs rotations to ensure that the height difference between left and right subtrees is no more than one.",
        "trie": "A Trie (Prefix Tree) is a tree-like data structure used for efficient retrieval of strings. Each node represents a character, and paths from root to leaf represent words."
    }

    return render_template(
        'index.html',
        tree_type=tree_type,
        image_path=graph_image_path,
        description=descriptions[tree_type]
    )

@app.route('/set_tree', methods=['POST'])
def set_tree():
    tree_type = request.form['tree_type']
    session["tree_type"] = tree_type
    draw_tree_graph(tree_types[tree_type], tree_type, graph_image_path)
    return redirect(url_for('index'))

@app.route('/insert', methods=['POST'])
def insert():
    tree_type = session.get("tree_type", "binary")
    val = request.form['value']
    if tree_type == "trie":
        tree_types[tree_type].insert(val.lower())
    else:
        if val.isdigit():
            tree_types[tree_type].insert(int(val))
    draw_tree_graph(tree_types[tree_type], tree_type, graph_image_path)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    tree_type = session.get("tree_type", "binary")
    val = request.form['value']
    tree = tree_types[tree_type]
    if tree_type == "trie":
        tree.delete(val.lower())
    else:
        if val.isdigit():
            tree.delete(int(val))
    draw_tree_graph(tree, tree_type, graph_image_path)
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    tree_type = session.get("tree_type", "binary")
    tree_types[tree_type] = {
        "binary": BinarySearchTree(),
        "avl": AVLTree(),
        "trie": Trie()
    }[tree_type]
    draw_tree_graph(tree_types[tree_type], tree_type, graph_image_path)
    return redirect(url_for('index'))

@app.route('/traverse/<order>')
def traverse(order):
    tree_type = session.get("tree_type", "binary")
    tree = tree_types[tree_type]
    if tree_type == "trie":
        return jsonify(tree.get_words())
    if order == "inorder":
        return jsonify(tree.inorder())
    elif order == "preorder":
        return jsonify(tree.preorder())
    else:
        return jsonify(tree.postorder())

@app.route('/rearrange', methods=['POST'])
def rearrange():
    tree_type = session.get("tree_type", "binary")
    if tree_type != "trie":
        tree_types[tree_type] = rearrange_binary_tree(tree_types[tree_type])
        draw_tree_graph(tree_types[tree_type], tree_type, graph_image_path)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
