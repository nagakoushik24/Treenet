from trees.binary_tree import Node


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _height(self, node):
        return 0 if node is None else node.height

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _balance(self, node):
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _insert(self, node, key):
        if not node:
            new_node = Node(key)
            new_node.height = 1
            return new_node
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        self._update_height(node)
        return self._balance(node)

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
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        self._update_height(node)
        return self._balance(node)

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        return self._inorder(self.root)

    def preorder(self):
        return self._preorder(self.root)

    def postorder(self):
        return self._postorder(self.root)

    def _inorder(self, node):
        return [] if not node else self._inorder(node.left) + [node.key] + self._inorder(node.right)

    def _preorder(self, node):
        return [] if not node else [node.key] + self._preorder(node.left) + self._preorder(node.right)

    def _postorder(self, node):
        return [] if not node else self._postorder(node.left) + self._postorder(node.right) + [node.key]
