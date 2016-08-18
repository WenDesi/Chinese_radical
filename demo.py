# encoding=utf-8

from radical import Radical

if __name__ == '__main__':
    radical = Radical()

    # 如果需要查找的字在字典中，则直接返回其偏旁部首
    print radical.get_radical('好')

    # 本地词典查不到，则从百度汉语中查找
    print radical.get_radical('淥')

    # 可通过下面操作保存新加入的字
    # radical.save()