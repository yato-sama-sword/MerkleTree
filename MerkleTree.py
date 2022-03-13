import ConstVal
import queue
from hashlib import sha256
from graphviz import Digraph


# Computer A sends a hash of the file to computer B.
# Computer B checks that hash against the root of the Merkle tree.
# If there is no difference, we're done! Otherwise, go to step 4.
# If there is a difference in a single hash, computer B will request the roots of the two subtrees of that hash.
# Computer A creates the necessary hashes and sends them back to computer B.
# Repeat steps 4 and 5 until you've found the data blocks(s) that are inconsistent.
# It's possible to find more than one data block that is wrong because there might be more than one error in the data.

def my_hash(s1, s2=''):
    return sha256((s1 + s2).encode()).hexdigest()


def get_key(my_list):
    keys = []
    for it in my_list:
        keys.append(it.key)
    return keys


def get_val(my_list):
    vals = []
    for it in my_list:
        vals.append(it.val)
    return vals


class Node:
    def __init__(self, _key, _node_val='', _node_type=ConstVal.INNER_NODE):
        self.key = _key
        self.val = _node_val
        self.type = _node_type
        self.left = None
        self.right = None
        self.parent = None

    def __lt__(self, other):
        return self.key < other.key


class MerkleTree:
    def __init__(self):
        self.root = None
        self.level_traversal = []

    def fit(self, data):
        """
        构造二叉树，相当于一颗二叉搜索树
        :param data: 排好序并经过 Hash 映射的 Node 数组
        :return:
        """
        q = queue.Queue()
        for it in data:
            q.put(it)
        while not q.empty():
            left = q.get()
            if q.empty():
                self.root = left
                break
            right = q.get()
            while left.key > right.key:
                q.put(left)
                left = right
                right = q.get()
            node = Node((left.key + right.key) / 2)
            left.parent = node
            node.left = left
            right.parent = node
            node.right = right
            node.val = my_hash(left.val, right.val)
            q.put(node)
        return self.root

    def show_tree(self):
        dot = Digraph(filename=r'result/my_tree')
        if self.root is None:
            return None
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            now = q.get()
            if now is None:
                self.level_traversal.append(None)
                continue
            dot.node(str(now.key))
            if now.parent is not None:
                dot.edge(str(now.parent.key), str(now.key))
            self.level_traversal.append(now.key)
            q.put(now.left)
            q.put(now.right)
        dot.view()

    def check(self, target):
        """
        根据给定的若干 hash 值寻找节点
        :param target: 给定路径 一条/两条路径
        :return: T / F
        """
        root = self.root
        for path in target:
            if root.val == path[0]:
                for val in range(1, len(path)):
                    if root.left is not None and root.left.val == path[val]:
                        root = root.left
                    elif root.right is not None and root.right.val == path[val]:
                        root = root.right
                    elif root.parent is not None and root.parent.val == path[val]:
                        root = root.parent
                    else:
                        return False
            else:
                return False
        return True

    def search(self, target):
        """
        寻找给定目标
        :param target: 给定目标的 key 值
        :return: 存在则返回路径 不存在则返回小于的最大的路径和大于的最小的路径 分开返回两条路径
        """
        result = self.search_tree(target, self.root)
        if not result[-1]:
            smaller = self.search_tree_smaller(target, self.root)
            return [False, smaller,
                    self.search_tree_bigger(target, smaller[-1])]  # 左侧路径； 右侧路径是以左侧路径为起点的路径
        return [True, result]

    def search_tree(self, target, root):
        if root is None:
            return [False]
        now_vals = [root]
        if target == root.key and root.type == ConstVal.LEAF_NODE:
            return now_vals
        if target > root.key:
            res = self.search_tree(target, root.right)
            now_vals.extend(res)
        else:
            res = self.search_tree(target, root.left)
            now_vals.extend(res)
        return now_vals

    def search_tree_smaller(self, target, root):
        """
        找小于target的最大的节点
        方法：
            if now < target:
                find_right
            else:
                find_left

        :param target:
        :param root:
        :return:
        """
        if root is None:
            return []
        now_ans = [root]
        if root.key < target:
            now_ans.extend(self.search_tree_smaller(target, root.right))
        else:
            now_ans.extend(self.search_tree_smaller(target, root.left))
        return now_ans

    def search_tree_bigger(self, target, root):
        return self.find_bigger_neighbor(target, root)

    def find_bigger_neighbor(self, target, root):
        """
        找当前节点的右侧的相邻节点
        如果当前节点是左儿子，就找右儿子
        如果当前节点是右儿子，就找有右儿子的祖先的一直往左的儿子
        :return:
        """
        if root.parent is None:
            return None
        if root.parent.key > root.key:
            return [root, root.parent, root.parent.right]
        else:
            ans = []
            while root.parent.key < target:
                ans.append(root)
                root = root.parent
            root = root.parent
            ans.append(root)
            root = root.right
            ans.append(root)
            while root is not None:
                ans.append(root)
                root = root.left
            return ans
