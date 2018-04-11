from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import EntryWithSignalFirst, \
    EntryWithSignalForloop, Log, Entry, EntryWithSignalBrackets


# this fails, the first() method always returns None
@receiver(post_delete, sender=EntryWithSignalFirst)
def log_the_first_element_with_first(sender, instance, **kwargs):
    # notice the query set is ok
    print('\n\nWITH first()')
    print('------------')
    print('Queryset is ok:', Entry.objects.order_by('pk'))

    entry = Entry.objects.order_by('pk').first()

    print('But the first element is None', entry)

    if entry:
        log = Log(
            text=entry.name
        )
        log.save()


# this fails, the [0] method does not return anything
@receiver(post_delete, sender=EntryWithSignalBrackets)
def log_the_first_element_with_brackets(sender, instance, **kwargs):
    print('\n\nWITH [0]')
    print('--------')
    try:
        # notice the query set is ok
        print('Queryset is ok:', Entry.objects.order_by('pk'))

        entry = Entry.objects.order_by('pk')[0]

        log = Log(
            text=entry.name
        )
        log.save()
    except IndexError:
        print('No index [0]')
        pass


@receiver(post_delete, sender=EntryWithSignalForloop)
def log_the_first_element_with_a_for_loop(sender, instance, **kwargs):
    print('\n\nWITH forloop')
    print('------------')
    print('Queryset is ok:', Entry.objects.order_by('pk'))
    for entry in Entry.objects.order_by('pk'):
        print('First entry is also ok:', entry)
        log = Log(
            text=entry.name
        )
        log.save()
        break

