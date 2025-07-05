from trees.binary_tree import BinarySearchTree
from trees.avl_tree import AVLTree

def rearrange_binary_tree(tree):
    values = tree.inorder()
    if not values:
        return tree

    def build_balanced_tree(sorted_vals, tree_class):
        if not sorted_vals:
            return None

        new_tree = tree_class()
        def insert_balanced(vals):
            if not vals:
                return
            mid = len(vals) // 2
            new_tree.insert(vals[mid])
            insert_balanced(vals[:mid])
            insert_balanced(vals[mid+1:])
        insert_balanced(sorted_vals)
        return new_tree

    tree_class = type(tree)  # Keep same class (BinarySearchTree or AVLTree)
    return build_balanced_tree(values, tree_class)
