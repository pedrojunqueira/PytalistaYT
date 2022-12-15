# List Comprehension

List comprehension is a pythonic way to create a new list from an existing one
In other words you want to tranforma a list for some reason. 
filter lists.

## how a traditional loop works

Loop in python work a little different from "C Like"languages.

What a for loop in python do is to iterate a collection.

For exampla a `list` of items `["One", "Two", "Three"]`

a loop would be 

```python

ages = [24, 23, 45, 60, 11]
filtered_list = []

for i in ages:
    filtered_list.append(i + 1)

```

## from loop to list comprehension

```python

ages = [24, 23, 45, 60, 11]

filtered_list = [i + 1 for i in ages]

``

## In list comprehension with if condition

```python

ages = [24, 23, 45, 60, 11]

filtered_list = [ i for i in ages if i > 25 ]

```

## if else

```python

 [i if i > 25 else 0 for i in ages]

```

