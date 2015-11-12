# Copyright (c) 2011, Per Rovegard <per@rovegard.se>
# Licensed under the 3-clause BSD license.
# See the LICENSE file for details.

from struct import unpack
from datetime import datetime, tzinfo, timedelta

# HEADER
#         magic number ("bplist")
#         file format version
#
# OBJECT TABLE
#         variable-sized objects
#
#         Object Formats (marker byte followed by additional info in some cases)
#         null    0000 0000
#         bool    0000 1000                       // false
#         bool    0000 1001                       // true
#         fill    0000 1111                       // fill byte
#         int     0001 nnnn       ...             // # of bytes is 2^nnnn, big-endian bytes
#         real    0010 nnnn       ...             // # of bytes is 2^nnnn, big-endian bytes
#         date    0011 0011       ...             // 8 byte float follows, big-endian bytes
#         data    0100 nnnn       [int]   ...     // nnnn is number of bytes unless 1111 then int count follows, followed by bytes
#         string  0101 nnnn       [int]   ...     // ASCII string, nnnn is # of chars, else 1111 then int count, then bytes
#         string  0110 nnnn       [int]   ...     // Unicode string, nnnn is # of chars, else 1111 then int count, then big-endian 2-byte uint16_t
#                 0111 xxxx                       // unused
#         uid     1000 nnnn       ...             // nnnn+1 is # of bytes
#                 1001 xxxx                       // unused
#         array   1010 nnnn       [int]   objref* // nnnn is count, unless '1111', then int count follows
#                 1011 xxxx                       // unused
#         set     1100 nnnn       [int]   objref* // nnnn is count, unless '1111', then int count follows
#         dict    1101 nnnn       [int]   keyref* objref* // nnnn is count, unless '1111', then int count follows
#                 1110 xxxx                       // unused
#                 1111 xxxx                       // unused
#
# OFFSET TABLE
#         list of ints, byte size of which is given in trailer
#         -- these are the byte offsets into the file
#         -- number of these is in the trailer
#
# TRAILER
#         byte size of offset ints in offset table
#         byte size of object refs in arrays and dicts
#         number of offsets in offset table (also is number of objects)
#         element # in offset table which is top level object
#         offset table offset

try:
    unichr(8364)
except NameError:
    # Python 3
    def unichr(x):
        return chr(x)

# From CFDate Reference: "Absolute time is measured in seconds relative to the
# absolute reference date of Jan 1 2001 00:00:00 GMT".
SECS_EPOCH_TO_2001 = 978307200

MARKER_NULL = 0X00
MARKER_FALSE = 0X08
MARKER_TRUE = 0X09
MARKER_FILL = 0X0F
MARKER_INT = 0X10
MARKER_REAL = 0X20
MARKER_DATE = 0X33
MARKER_DATA = 0X40
MARKER_ASCIISTRING = 0X50
MARKER_UNICODE16STRING = 0X60
MARKER_UID = 0X80
MARKER_ARRAY = 0XA0
MARKER_SET = 0XC0
MARKER_DICT = 0XD0


def read_binary_plist(fd):
    """Read an object from a binary plist.

    The binary plist format is described in CFBinaryPList.c at
    http://opensource.apple.com/source/CF/CF-550/CFBinaryPList.c. Only the top
    level object is returned.

    Raise a PListFormatError or a PListUnhandledError if the input data cannot
    be fully understood.

    Arguments:
    fd -- a file-like object that is seekable

    """
    r = BinaryPListReader(fd)
    return r.read()


class PListFormatError(Exception):
    """Represent a binary plist format error."""
    pass


class PListUnhandledError(Exception):
    """Represent a binary plist error due to an unhandled feature."""
    pass


class ObjectRef(object):
    def __init__(self, index):
        self.index = index

    def resolve(self, lst):
        return lst[self.index]


class BinaryPListReader(object):

    def __init__(self, fd):
        self._fd = fd

    def read(self):
        fd = self._fd

        # start from the beginning to check the signature
        fd.seek(0, 0)
        buf = fd.read(7)

        # verify the signature; the first version digit is always 0
        if buf != b"bplist0":
            raise PListFormatError("Invalid signature: %s" % (buf, ))

        # seek to and read the trailer (validation omitted for now)
        fd.seek(-32, 2)
        buf = fd.read(32)

        _, offsetIntSize, self.objectRefSize, numObjects, topObject, \
                offsetTableOffset = unpack(">5x3B3Q", buf)

        # read the object offsets
        fd.seek(offsetTableOffset, 0)
        self._offsets = [self._read_sized_int(offsetIntSize) for _ in range(0, numObjects)]

        # read the actual objects
        objects = [self._read_object(offs) for offs in self._offsets]

        # resolve lazy values (references to the object list)
        self._resolve_objects(objects)

        return objects[topObject]

    def _resolve_objects(self, objects):
        # all resolutions are in-place, to avoid breaking references to
        # the outer objects!
        for obj in objects:
            if isinstance(obj, list):
                for i in range(0, len(obj)):
                    obj[i] = obj[i].resolve(objects)
            if isinstance(obj, set):
                temp = [item.resolve(objects) for item in obj]
                obj.clear()
                obj.update(temp)
            if isinstance(obj, dict):
                temp = {k.resolve(objects): v.resolve(objects) for k, v in list(obj.items())}
                obj.clear()
                obj.update(temp)

    def _read_object(self, offset=-1):
        if offset >= 0:
            self._fd.seek(offset)
        else:
            offset = self._fd.tell()  # for the error message
        marker = ord(self._fd.read(1))
        nb1 = marker & 0xf0
        nb2 = marker & 0x0f

        if nb1 == MARKER_NULL:
            if marker == MARKER_NULL:
                obj = None
            elif marker == MARKER_FALSE:
                obj = False
            elif marker == MARKER_TRUE:
                obj = True
            #TODO: Fill byte, skip over
        elif nb1 == MARKER_INT:
            count = 1 << nb2
            obj = self._read_sized_int(count)
        elif nb1 == MARKER_REAL:
            obj = self._read_sized_float(nb2)
        elif marker == MARKER_DATE:  # marker!
            secs = self._read_sized_float(3)
            secs += SECS_EPOCH_TO_2001
            obj = datetime.fromtimestamp(secs, UTC())
        elif nb1 == MARKER_DATA:
            # Binary data
            count = self._read_count(nb2)
            obj = self._fd.read(count)
        elif nb1 == MARKER_ASCIISTRING:
            # ASCII string
            count = self._read_count(nb2)
            obj = self._fd.read(count).decode("ascii")
        elif nb1 == MARKER_UNICODE16STRING:
            # UTF-16 string
            count = self._read_count(nb2)
            data = self._fd.read(count * 2)
            chars = unpack(">%dH" % (count, ), data)
            s = u''
            for ch in chars:
                s += unichr(ch)
            obj = s
        elif nb1 == MARKER_UID:
            count = 1 + nb2
            obj = self._read_sized_int(count)
        elif nb1 == MARKER_ARRAY:
            count = self._read_count(nb2)
            # we store lazy references to the object list
            obj = [ObjectRef(self._read_sized_int(self.objectRefSize)) for _ in range(0, count)]
        elif nb1 == MARKER_SET:
            count = self._read_count(nb2)
            # we store lazy references to the object list
            obj = set([ObjectRef(self._read_sized_int(self.objectRefSize)) for _ in range(0, count)])
        elif nb1 == MARKER_DICT:
            count = self._read_count(nb2)
            # first N keys, then N values
            # we store lazy references to the object list
            keys = [ObjectRef(self._read_sized_int(self.objectRefSize)) for _ in range(0, count)]
            values = [ObjectRef(self._read_sized_int(self.objectRefSize)) for _ in range(0, count)]
            obj = dict(list(zip(keys, values)))

        try:
            return obj
        except NameError:
            raise PListFormatError("Unknown marker at position %d: %d" %
                                   (offset, marker))

    def _read_count(self, nb2):
        count = nb2
        if count == 0xf:
            count = self._read_object()
        return count

    def _read_sized_float(self, log2count):
        if log2count == 2:
            # 32 bits
            ret, = unpack(">f", self._fd.read(4))
        elif log2count == 3:
            # 64 bits
            ret, = unpack(">d", self._fd.read(8))
        else:
            raise PListUnhandledError("Unhandled real size: %d" %
                                      (1 << log2count, ))
        return ret

    def _read_sized_int(self, count):
        # in format version '00', 1, 2, and 4-byte integers have to be
        # interpreted as unsigned, whereas 8-byte integers are signed
        # (and 16-byte when available). negative 1, 2, 4-byte integers
        # are always emitted as 8 bytes in format '00'
        buf = self._fd.read(count)
        if count == 1:
            ret = ord(buf)
        elif count == 2:
            ret, = unpack(">H", buf)
        elif count == 4:
            ret, = unpack(">I", buf)
        elif count == 8:
            ret, = unpack(">q", buf)
        else:
            raise PListUnhandledError("Unhandled int size: %d" %
                                      (count, ))
        return ret


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return timedelta(0)


# typedef struct {
#    uint8_t  _unused[5];
#    uint8_t  _sortVersion;
#    uint8_t  _offsetIntSize;
#    uint8_t  _objectRefSize;
#    uint64_t _numObjects;
#    uint64_t _topObject;
#    uint64_t _offsetTableOffset;
# } CFBinaryPlistTrailer;
