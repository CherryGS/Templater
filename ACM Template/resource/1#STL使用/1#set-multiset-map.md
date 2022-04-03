## set

```cpp
set<T> e; // 定义 set
e.clear(); // 清空 set
e.insert(); // 插入 val , 返回指向插入点的迭代器
e.size(); // 返回 set 大小
e.lower_bound(); // iter , 大于等于
e.upper_bound(); // iter , 大于
e.find(); // iter
```

## multiset

```cpp
mlutiset<T> e;
// the same to up
e.equal_range(); // pair<iter,iter>
e.count();
```

## map

```cpp
map<T1, T2> e;
// the same to up
e[T1] = T2;
```

