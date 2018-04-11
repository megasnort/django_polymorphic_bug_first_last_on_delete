# README

This repo contains code to trigger a bug in django-polymorphic

- Django 2.0.4
- Python 3.6.4
- Django-polymorphic 2.0.2
- Postgresql and Sqllite


## Bug description

Create two instances of Classes that have the same Base class, using `django-polymorphic`. 
The Class of the first (!) instance has a post_delete signal

In this post_delete signal, you issue a Query to the database to determine what is the 'first' element of all the existing instances of the base class.

If you do it like this, this works

```python
entry = None
for entry in Entry.objects.order_by('pk'):
    print(entry)
    break
```

if you do it like this, it does not work, because the [0] always returns `None`

```python
try:
    print(Entry.objects.order_by('pk')[0])
except IndexError:
    pass
```

if you do it like this, it also does not work, because the first() also always returns `None`. (first() is an easier form of [0] with the try/except)

```python
print(Entry.objects.order_by('pk').first())
```


Note that in all three case, when you issue

```python
print(Entry.objects.order_by('pk'))
```

You do see the Queryset, with the element that was not deleted.

### Notes

- The order in which the instances are created does matter (if create the item with the signal secondly, the bug does not occur)
- The problem also occurs when using 'last()'



## Example

I created some tests to show the bug:

```
pip install -r requirements.txt`
cd django_first_bug
python manage.py test
```

You will see that two tests fail, that should pass. They don't because the first() and [0] method of the queryset return None instead of the first element.
