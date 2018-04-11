# README

I encountered the following bug when using

- Django 2.0.4
- django-polymorphic 2.0.2
- Python 3.6.4
- Postgresql and sqllite

## Bug description

Create two instances of Classes that have the same Base class, using `django-polymorphic`. 
The Class of the first (!) instance has a post_delete signal

In this post_delete signal, you issue a Query to the database to determine what is the 'first' element of all the existing instances of the base class.

Now, delete the first instance, the one with the signal. 

If you do it like this, it does not work, because the [0] always returns `None`. If should however show the other instance.

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

If you do it like this, it does work!

```python
entry = None
for entry in Entry.objects.order_by('pk'):
    print(entry)
    break
```

Note that in all three case, when you issue

```python
print(Entry.objects.order_by('pk'))
```

You do see the Queryset, with the element that was not deleted.

### Notes

- The order in which the instances are created does matter (if your create the item with the signal secondly, the bug does not occur)
- The problem also occurs when using 'last()'

## Example code

```
pip install -r requirements.txt`
cd django_first_bug
python manage.py test
```
You will see that two tests fail, that should pass. They don't because the first() and [0] method of the queryset return None instead of the first element.
