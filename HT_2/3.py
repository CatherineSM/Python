#3. Написати скрипт, який видалить пусті елементи із списка. Список можна #"захардкодити".
 #       Sample data: [(), (), ('',), ('a', 'b'), {}, ('a', 'b', 'c'), ('d'), #'', []]
 #       Expected output: [('',), ('a', 'b'), ('a', 'b', 'c'), 'd']

 list1 = [(), (), ('',), ('a', 'b'), {}, ('a', 'b', 'c'), ('d'), '', []]
 itemsToRemove = set([(), [], ''])
 b = filter(lambda x: x not in itemsToRemove, list1)
 print(b)