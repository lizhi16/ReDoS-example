# ReDoS-example
2 ReDoS 原理
2.1 概述
DFA对于文本串里的每一个字符只需扫描一次，比较快，但特性较少；NFA要翻来覆去吃字符、吐字符，速度慢，但是特性(如:分组、替换、分割)丰富。NFA支持 惰性(lazy)、回溯(backtracking)、反向引用(backreference)，NFA缺省应用greedy模式，NFA可能会陷入递归险境导致性能极差。

2.2 说明
我们定义一个正则表达式^(a+)+$来对字符串aaaaX匹配。使用NFA的正则引擎，必须经历2^4=16次尝试失败后才能否定这个匹配。同理字符串为aaaaaaaaaaX就要经历2^10=1024次尝试。如果我们继续增加a的个数为20个、30个或者更多，那么这里的匹配会变成指数增长。

下面我们以python语言为例子来进行代码的演示:

#!/usr/bin/env python
# coding: utf-8

import re
import time

def exp(target_str):
    """
    """
    s1 = time.time()
    flaw_regex = re.compile('^(a+)+$')
    flaw_regex.match(target_str)
    s2 = time.time()
    print("Consuming time: %.4f" % (s2-s1))


if __name__ == '__main__':
    str_list = (
        'aaaaaaaaaaaaaaaaX',           # 2^16
        'aaaaaaaaaaaaaaaaaaX',         # 2^18
        'aaaaaaaaaaaaaaaaaaaaX',       # 2^20
        'aaaaaaaaaaaaaaaaaaaaaaX',     # 2^22
        'aaaaaaaaaaaaaaaaaaaaaaaaX',   # 2^24
        'aaaaaaaaaaaaaaaaaaaaaaaaaaX', # 2^26
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaX', # 2^36
    )
    for evil_str in str_list:
        print('Current: %s' % evil_str)
        exp(evil_str)
        print('--'*40)
把上面的代码保存成redos.py文件并执行这个 py 脚本文件:

$ python redos.py
Current: aaaaaaaaaaaaaaaaX
Consuming time: 0.0043
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaX
Consuming time: 0.0175
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaaaX
Consuming time: 0.0678
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaaaaaX
Consuming time: 0.2370
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaaaaaaaX
Consuming time: 0.9842
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaaaaaaaaaX
Consuming time: 4.1069
--------------------------------------------------------------------------------
Current: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaX
