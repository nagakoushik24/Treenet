class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def delete(self, word: str):
        def _delete(node, word, depth):
            if not node:
                return False

            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0

            char = word[depth]
            if char in node.children:
                should_delete_child = _delete(node.children[char], word, depth + 1)

                if should_delete_child:
                    del node.children[char]
                    return not node.is_end_of_word and len(node.children) == 0

            return False

        _delete(self.root, word, 0)

    def get_words(self):
        result = []

        def _dfs(node, prefix):
            if node.is_end_of_word:
                result.append(prefix)
            for char, child in node.children.items():
                _dfs(child, prefix + char)

        _dfs(self.root, "")
        return result
