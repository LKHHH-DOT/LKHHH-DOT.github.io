# Python 编程小技巧

## 列表推导式
```python
squares = [x**2 for x in range(10)]
```

## 字典合并
```python
a = {'x': 1}; b = {'y': 2}
merged = {**a, **b}  # Python 3.5+
```

## 多变量赋值
```python
a, b, *rest = [1, 2, 3, 4, 5]
# a=1, b=2, rest=[3,4,5]
```
