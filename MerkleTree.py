import ConstVal
import queue
from hashlib import sha256


# Computer A sends a hash of the file to computer B.
# Computer B checks that hash against the root of the Merkle tree.
# If there is no difference, we're done! Otherwise, go to step 4.
# If there is a difference in a single hash, computer B will request the roots of the two subtrees of that hash.
# Computer A creates the necessary hashes and sends them back to computer B.
# Repeat steps 4 and 5 until you've found the data blocks(s) that are inconsistent.
# It's possible to find more than one data block that is wrong because there might be more than one error in the data.

def my_hash(s1, s2):
    return sha256((s1 + s2).encode()).hexdigest()


class Node:
    def __init__(self, _key, _node_val='', _node_type=ConstVal.INNER_NODE):
        self.key = _key
        self.node_val = _node_val
        self.node_type = _node_type
        self.left_son = None
        self.right_son = None
        self.parent = None


class MerkleTree:
    def __init__(self):
        self.root = None
        self.min_hash = 0
        self.max_hash = 0

    def fit(self, data):
        """
        构造二叉树，相当于一颗二叉搜索树
        :param data: 排好序并经过 Hash 映射的 Node 数组
        :return:
        """
        q = queue.Queue()
        self.max_hash = len(data) - 1
        for it in data:
            q.put(it)
        while not q.empty():
            left = q.get()
            if q.empty():
                self.root = left
                break
            right = q.get()
            node = Node(my_hash(left.node_val, right.node_val))
            left.parent = node
            node.left_son = left
            right.parent = node
            node.right_son = right
            node.key = (left.key + right.key) / 2
            q.put(node)
        return self.root

    def check(self, target):
        """
        根据给定的若干 hash 值寻找节点
        :param target: 给定路径 前序遍历形式的数组
        :return: T / F
        """
        q = queue.Queue()
        pos = 0
        q.put(self.root)
        while not q.empty():
            now = q.get()
            if target[pos] == now.key:
                pos += 1
            else:
                return False
            q.put()

        # return self.check_tree(target, self.root)

    def search(self, target):
        """
        寻找给定目标
        :param target: 给定目标的 Hash 值
        :return: 存在则返回路径 不存在则返回小于的最大的路径和大于的最小的路径 路径为 DFS序
        """
        result = self.search_tree(target, self.root)
        if not result[-1]:
            min_path = self.search_tree_min(target, self.root)
            return [False, min_path.append(self.find_bigger_neighbor(min_path[-1]))]
        return [True, result]

    def search_tree(self, target, root):
        if root is None:
            return [False]
        now_ans = [root]
        if target == root.key:
            return now_ans
        if target <= root.key:
            now_ans.append(self.search_tree(target, root.left))
        else:
            now_ans.append(self.search_tree(target, root.right))
        now_ans.append(root)
        return now_ans

    def search_tree_min(self, target, root):
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
            return [False]
        now_ans = [root]

    def find_bigger_neighbor(self, root):
        """
        找当前节点的右侧的相邻节点
        如果当前节点是左儿子，就找右儿子
        如果当前节点是右儿子，就找grandfather的右儿子的一直往左的儿子
        如果没有更大的，怎么证明？（老师好像也没讲）
        :return:
        """
        pass
