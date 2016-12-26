from threading import Lock
from timeit import default_timer as timer


class KeyTable(object):
    _keys = {}
    _write = Lock()  # Required to edit keys
    _table = {}
    _time = 0
    _elapsed = 0  # Maximum time that has elapsed so far in the sequence
    _read = Lock()  # Required to edit table

    def is_allowed(self, key, advance=True):
        """
        The goal of this function is to be very fast. This is accomplished
        through the table structure, which ensures that we only need to
        check whether `key is in self._table` and change what variable
        is referenced by `self._table`.

        Unfortunately, handling timeouts properly has added significantly to
        the logic required, but the function should still be well within required
        time limits.
        """
        time = timer()
        if self._elapsed == -1:
            elapsed = 0
        else:
            elapsed = time - self._time
            if self._elapsed > elapsed:
                elapsed = self._elapsed

        in_sequence = key in self._table and elapsed < self._table[key][0]
        suppress = in_sequence or key in self._keys
        if advance:
            self._read.acquire()
            if in_sequence and self._table[key][1]:
                self._table = self._table[key][1]
                self._time = time
                self._elapsed = elapsed
            else:
                self._table = self._keys
                self._time = 0
                self._elapsed = -1
            self._read.release()

        return not suppress

    def _refresh(self):
        self._read.acquire()
        self._table = self._keys
        self._read.release()

    def _acquire_table(self, sequence, table, timeout):
        """
        Returns a flat (single level) dictionary
        :param sequence:
        :param table:
        :return:
        """
        el = sequence.pop(0)
        if el not in table:
            table[el] = (timeout, {})
        if table[el][0] < timeout:
            table[el][0] = timeout

        if sequence:
            return self._acquire_table(sequence, table[el][1], timeout)
        else:
            return table

    def suppress_sequence(self, sequence, timeout):
        """
        Adds keys to the suppress_keys table
        :param sequence: List of scan codes
        :param timeout: Time allowed to elapse before resetting
        """

        # the suppress_keys table is organized
        # as a dict of dicts so that the critical
        # path is only checking whether the
        # scan code is 'in current_dict'
        self._write.acquire()
        self._acquire_table(sequence, self._keys, timeout)
        self._refresh()
        self._write.release()

    def suppress_none(self):
        """
        Clears the suppress_keys table and disables
        key suppression
        :return:
        """
        self._write.acquire()
        self._keys = {}
        self._refresh()
        self._write.release()
