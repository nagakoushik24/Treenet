class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        return self._traverse(node, "inorder")

    def preorder(self):
        return self._preorder(self.root)

    def _preorder(self, node):
        return self._traverse(node, "preorder")

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, node):
        return self._traverse(node, "postorder")

    def _traverse(self, node, order):
        if not node:
            return []
        if order == "inorder":
            return self._traverse(node.left, order) + [node.key] + self._traverse(node.right, order)
        elif order == "preorder":
            return [node.key] + self._traverse(node.left, order) + self._traverse(node.right, order)
        elif order == "postorder":
            return self._traverse(node.left, order) + self._traverse(node.right, order) + [node.key]
