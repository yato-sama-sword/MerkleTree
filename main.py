import random

from MerkleTree import MerkleTree
from MerkleTree import Node
from MerkleTree import my_hash
from MerkleTree import get_key
from MerkleTree import get_val

import ConstVal

if __name__ == '__main__':
    # 数据生成: 随机生成 128 个节点
    val = set()
    number = 7
    for i in range(0, number):
        while True:
            tmp = random.randint(1, 1000)
            if tmp not in val:
                val.add(tmp)
                break
        # val.append(i)
    val = list(val)  # 保证顺序
    data = []
    for i in range(0, number):
        data.append(Node(val[i], my_hash(str(val[i])), ConstVal.LEAF_NODE))
    # 构造
    merkleTree = MerkleTree()
    merkleTree.fit(data)
    root = merkleTree.root
    merkleTree.show_tree()
    # 搜索
    searched = merkleTree.search(27)
    search_result = searched[0]
    print('search result is ' + ('True' if search_result else 'False'))
    search_path = searched[1:]
    path = [get_val(search_path[0])]
    print('search path is ', get_key(search_path[0]))
    if not search_result:
        path.append(get_val(search_path[1]))
        print('search path for bigger one is', get_key(search_path[1]))
    # 检查
    print(path)
    print(merkleTree.check(path))
