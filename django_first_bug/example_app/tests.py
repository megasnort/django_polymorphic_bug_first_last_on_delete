from django.test import TestCase

from .models import EntryWithSignalFirst, EntryWithSignalForloop, \
    EntryWithoutSignal, Entry, Log, EntryWithSignalBrackets


class OrderTests(TestCase):
    def test_getting_first_element_after_manual_deletion_of_last_element(self):
        self.a_first_entry = EntryWithoutSignal(
            name='Jayne'
        )
        self.a_first_entry.save()

        self.entry_without_signal = EntryWithoutSignal(
            name='Summer'
        )
        self.entry_without_signal.save()

        self.entry_without_signal.delete()

        entry = Entry.objects.order_by('pk').first()

        if entry:
            log = Log(
                text=entry.name
            )
            log.save()

        # this works, a log with the first item was created
        self.assertTrue(Log.objects.all().first().text == self.a_first_entry.name)

    def test_getting_first_element_after_signal_deletion_with_forloop(self):
        self.entry_with_signal = EntryWithSignalForloop(
            name='Jayne'
        )
        self.entry_with_signal.save()

        self.another_entry = EntryWithoutSignal(
            name='Inara'
        )
        self.another_entry.save()

        # this will trigger a on_delete signal
        self.entry_with_signal.delete()

        # this works, the log was created by looping over the entries, and breaking
        # after the first
        self.assertTrue(Log.objects.all().first().text == self.another_entry.name)

    def test_getting_first_element_after_signal_deletion_with_first(self):
        self.entry_with_signal = EntryWithSignalFirst(
            name='Jayne'
        )
        self.entry_with_signal.save()

        self.another_entry = EntryWithoutSignal(
            name='Malcolm'
        )
        self.another_entry.save()

        # this will trigger a on_delete signal
        self.entry_with_signal.delete()

        # this fails, because a log was not created, in the post_delete signal
        # the first() method there retursn None, where it should just return the
        # first entry
        self.assertTrue(Log.objects.all().first().text == self.another_entry.name)

    def test_getting_first_element_after_signal_deletion_with_brackets(self):
        self.entry_with_signal = EntryWithSignalBrackets(
            name='Jayne'
        )
        self.entry_with_signal.save()

        self.another_entry = EntryWithoutSignal(
            name='Malcolm'
        )
        self.another_entry.save()

        # this will trigger a on_delete signal
        self.entry_with_signal.delete()

        # this fails, because a log was not created, in the post_delete signal
        # the [0] there returns None, where it should just return the
        # first entry
        self.assertTrue(Log.objects.all().first().text == self.another_entry.name)

    def test_getting_first_element_after_signal_deletion_with_first_reverse(self):
        self.another_entry = EntryWithoutSignal(
            name='Malcolm'
        )
        self.another_entry.save()

        self.entry_with_signal = EntryWithSignalFirst(
            name='Jayne'
        )
        self.entry_with_signal.save()

        # this will trigger a on_delete signal
        self.entry_with_signal.delete()

        # This does work, the instance with the signal is created after the
        # other instance
        self.assertTrue(Log.objects.all().first().text == self.another_entry.name)