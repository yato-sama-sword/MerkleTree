import queue

from MerkleTree import MerkleTree
from MerkleTree import Node
from MerkleTree import my_hash
from MerkleTree import get_key
from MerkleTree import get_val

import ConstVal

if __name__ == '__main__':
    # 数据生成：构建一棵有128个节点且去掉了编号28的二叉树
    # 更改为随机生成
    data = []
    for i in range(0, 129):
        if i == 27:
            continue
        data.append(Node(i, my_hash(str(i)), ConstVal.LEAF_NODE))
    # 测试部分
    merkleTree = MerkleTree()
    merkleTree.fit(data)
    root = merkleTree.root
    merkleTree.show_tree()
    searched = merkleTree.search(27)
    search_result = searched[0]
    search_path = searched[1:]
    print(get_key(search_path[0]))
    if not search_result:
        print(get_key(search_path[1]))
