#!/usr/bin/env python
# This file should be available from
# http://www.pobox.com/~asl2/software/PyZ3950/
# and is licensed under the X Consortium license:
# Copyright (c) 2001, Aaron S. Lav, asl2@pobox.com
# All rights reserved. 

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, provided that the above
# copyright notice(s) and this permission notice appear in all copies of
# the Software and that both the above copyright notice(s) and this
# permission notice appear in supporting documentation. 

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 

# Except as contained in this notice, the name of a copyright holder
# shall not be used in advertising or otherwise to promote the sale, use
# or other dealings in this Software without prior written authorization
# of the copyright holder. 
# Change history:
# 2001/9/22 - fix test code to be slightly more elegant and fix test
# comments to be correct.  Due to Roy Smith, roy.smith@micromuse.com

# 2002/05/23 - fix handling of ANY.  Needed for handling of SUTRS records
# by Z3950.


"""<p>asn1 is a relatively general-purpose ASN.1 BER encoder and decoder.
Encoding and
decoding functions  (asn1.encode and asn1.decode) take an ASN.1 spec, and
transform back and forth between a byte stream and what I consider a natural
Python representation of the data.  (Decoding applications where the length of
the BER is not provided externally and indefinite-length encodings are allowed
will have to instantiate their own decoding context: see the comments near
and source of decode.)
<p>Separating the ASN.1 specification from the code allows me to,
if it becomes desirable, compile the specification to inline Python or C
code, or to a specification for a C-based engine.
<p>I support the following ASN.1 types:
<ul>
<li>BOOLEAN - encoder takes any Python value, decoder produces 0 or 1</li>
<li>INTEGER - as in Python</li>
<li>BITSTRING - asn1.BitStringVal</li>
<li>OCTSTRING - Python string</li>
<li>NULL - ignore value on encoding, return None on decoding</li>
<li>OID - OidVal</li>
<li>EXTERNAL - as SEQUENCE, see below (or read the source)</li>
<li>all string types - Python string (no validity checking is done)</li>
</ul>
<p>For all the above types, the ASN.1 spec is just the name of the type.
Inherently constructed types:
<ul>
<li>SEQUENCE_OF (ASN1.spec) - Python representation is a list of values.</li>
<li>
SEQUENCE, CHOICE - the ASN.1 spec is a list of tuples, either (name, tag, type)
or, for SEQUENCE, (name, tag, type, optionalflag), where:
tag can be None, asn1.EXPLICIT(tag), asn1.IMPLICIT(tag), or an integer
interpreted as either an explicit or an implicit tag according to the setting
of asn1.implicit_default; type is recursively an ASN.1 spec.</li>
</ul>
<p>For CHOICE, the Python representation is (name, val).  For SEQUENCE, on
decoding,
the Python representation is an instance of an asn1-synthesized class.
On encoding, any class with the appropriate attributes is acceptable, but you
can obtain a fresh instance of the synthesized class by calling the SEQUENCE
specification: this class overrides setattr to provide attribute-name error
checking.  (The rationale for the seemingly unPythonic errorchecking is that
misspelled optional attributes would otherwise be hard to detect.  If you don't
like it, it should be easy to turn off.)
<p>
For examples, see the test code at the end of this file, or the
Z39.50 code that should be distributed with this file.
<p>
There is not yet support for:
<ul>
<li>Constructed encodings for BITSTRINGs</li>
<li>REAL, UTCTime, ENUM, SET, SET OF, or some more obscure types</li>
<li>APPLICATION or PRIVATE class tags</li>
<li>Symbolic names for enumerated values</li>
</ul>
<p>Useful ASN.1 references:
<ul>
<li><a href="ftp://ftp.rsasecurity.com/pub/pkcs/ascii/layman.asc">
Burton S. Kaliski's "A Layman's guide to a Subset of ASN.1, BER, and DER"
</a></li>
<li><a href="http://www.oss.com/asn1/booksintro.html">Olivier Dubuisson's
_ASN.1: Communication between Heterogeneous Systems_</a>
(or available in book form)</li>
</ul>
"""
vers = "0.83"

import array
import string
import copy

# - elements should expose a list of possible tags, instead of just one tag
#    bringing CHOICE into line with other elements
# - make test cases more comprehensive
# - Decoder should be resumable rather than blocking in readproc until
#    entire PDU is delivered.  Then we can plug into asyncore.
#   (If PEP XXX on coroutines were part of the language, this would be easier:
#   as it is, we'd need to maintain an explicit stack of constructed encodings
#   we're in the middle of decoding, and explicit info about whether we're
#   decoding tag, len, or value.  Is it true that only constructed encodings
#   can be indef-len?  That makes it easier.)
# - Should we check to make sure that lengths of sub-objects of a
#    constructed encoding don't overrun the length of the outer constructed
#    encoding?  (Robustness issue, not correctness)
# - Eventually it would be nice to have an ASN.1 compiler which took the
#    official ASN.1 definition and spat out the ASN descriptors we use.

# Parameters you can tweak

implicit_default = 1
# Treat bare numeric tags as IMPLICIT if 1, EXPLICIT if 0.  Set at
# definition time.  This requires that all ASN.1 definitions be done
# single-threadedly - no big deal.  It'd be somewhat more modular to
# look this up in the caller's module dictionary.  We could also have it
# be a parameter to every def'n, but that's syntactically a little unwieldy.
# The abovementioned compiler would fix that.

indef_len_encodings = 0
# Generate indefinite-length encodings whenever we'd otherwise have to
# go back and fix up the length bytes if 1.  Set at encoding time.

cons_encoding = 0
# Generate constructed encodings for string types.  Useful only for
# testing the decoding of such encodings, I think.

# In theory, indef_len_encodings and cons_encoding are designed for
# cases where the length of the data isn't known ahead of time, and
# one doesn't want to have to buffer the entire thing.  It is possible
# to pass lazy sequences into the appropriate functions, but ...


# For debugging the asn.1 code only
trace_seq = 0
trace_choice = 0
trace_tag = 0
trace_seq_of = 0
trace_int = 0
trace_external = 0

# Note: BERError is only for decoding errors (either input data is illegal
# BER, or input data is legal BER but we don't support it.)

class BERError (Exception):
    def __init__ ( *args):
        apply (Exception.__init__, args)

class EncodingError (Exception):
    def __init__ ( *args):
        apply (Exception.__init__, args)


def encode (spec, data):
    ctx = Ctx (Ctx.dir_write)
    spec.encode (ctx, data)
    return ctx.get_data ()

# Note: in order to handle leftover data, many decoding applications
# will need to instantiate their own decoding context
def decode (spec, buf, readproc = None):
    ctx = Ctx(Ctx.dir_read)
    ctx.set_data (buf)
    ctx.set_readproc (readproc)
    retval = spec.decode (ctx)
    leftover = ctx.get_len_remaining ()
    if leftover:
        print "Leftover bytes:", leftover
        # Many apps will need to save these for next time
        ctx.dump (min (0x100, leftover))
    return retval

UNIVERSAL_FLAG = 0
APPLICATION_FLAG = 0x40
CONTEXT_FLAG = 0x80
PRIVATE_FLAG = 0xC0

CONS_FLAG = 0x20


ANY_TAG = -1 # pseudotag

BOOL_TAG = 0x1
INT_TAG = 0x2
BITSTRING_TAG = 0x3
OCTSTRING_TAG = 0x4
NULL_TAG = 0x5
OID_TAG = 0x6
OBJECTDESCRIPTOR_TAG = 0x7
EXTERNAL_TAG = 0x8

SEQUENCE_TAG = 0x10
UTF8STRING_TAG = 0xC
NUMERICSTRING_TAG = 0x12
PRINTABLESTRING_TAG = 0x13
T61STRING_TAG = 0x14
VIDEOTEXSTRING_TAG = 0x15
IA5STRING_TAG = 0x16
GENERALIZEDTIME_TAG = 0x18
GRAPHICSTRING_TAG = 0x19
VISIBLESTRING_TAG = 0x1A
GENERALSTRING_TAG = 0x1B
UNIVERSALSTRING_TAG = 0x1C
BMPSTRING_TAG = 0x1E

class StructBase:
    # replace _allowed_attrib_list with __slots__ mechanism
    # once we no longer need to support Python 2.1
    _allowed_attrib_list = []
    def __init__ (self,  **kw):
        self.set_allowed_attribs (self._allowed_attrib_list)
        # we don't just self.__dict__.update (...) b/c
        # we want error-checking in setattr below
        for k, v in kw.items ():
            setattr (self, k, v)
    def __repr__ (self):
        s = 'Struct: [\n'
        i = self.__dict__.items ()
        i.sort ()
        i = filter (lambda it: it[0][0] <> '_', i)
        s = s + string.join (map (lambda it: repr (it[0]) +
                                  ' ' + repr (it[1]), i), '\n')
        s = s + ']\n'
        return s
    def __cmp__ (self, other):
        keys = self.__dict__.keys ()
        keys.sort () # to ensure reproduciblity
        for k in keys:
            c = cmp (getattr (self, k, None), getattr (other, k, None))
            if c <> 0:
                return c
        okeys = other.__dict__.keys ()
        okeys.sort ()
        if okeys <> keys: return 1
        return 0
    def set_allowed_attribs (self, l):
        self._allowed_attribs = {}
        for e in l:
            self._allowed_attribs [e] = 1
    def is_allowed (self, k):
        if self._allowed_attrib_list == []: return 1
        if k == '_allowed_attribs': return 1
        return self._allowed_attribs.has_key (k)
# I implemented setattr b/c otherwise it can be difficult to tell when one
# has mistyped an OPTIONAL element of a SEQUENCE.  This is probably a matter
# of taste, and derived classes should feel welcome to override this.
    def __setattr__ (self, key, val):
        if not self.is_allowed (key):
            raise AttributeError (key)
        self.__dict__ [key] = val

# tags can match if only constructedness of encoding is different.  Not
# quite right, since, e.g., SEQUENCE must always be a constructed type,
# and INTEGER never is.

def match_tag (a, b):
    if trace_tag: print "Match_tag", a, b
    cons_match = (a[0] & ~CONS_FLAG == b[0] & ~CONS_FLAG)
    if (a[1] == ANY_TAG or b[1] == ANY_TAG):
        return cons_match
    return a[1] == b[1] and cons_match

def encode_base128 (val):
    # Only specified for encoding strictly positive vals (OIDs, tags >= 0x1F)
    l = []
    # But UTF-8 OID 1.0.10646.1.0.8 has 0 in middle, so I think that
    # language in X.209 about not ending with 0x80 is to be understood
    # in the context of minimal-length encoding for OID elements,
    # not that 0 is invalid.
    if val == 0:
        return [0x80]
    assert (val > 0)
    while val:
        l.append ((val % 128) | 0x80)
        val = val / 128
    if len (l) > 0:
        l[0] = l[0] & 0x7F
        l.reverse ()
    return l

class Ctx:
    dir_read = 0 
    dir_write = 1 
    def __init__ (self, direction):
        self.direction = direction
        self.cur_tag = None
        if direction == self.dir_write:
            self.buf = array.array ('B')
        else:
            self.buf = ""
        self.readproc = None
    def get_data (self):
        return self.buf
    def set_data (self, buf):
        if type (buf) == type (''):
            self.buf = array.array ('B')
            self.buf.fromstring (buf)
        else:
            self.buf = buf
        self.offset = 0
# set_readproc is required b/c the top-level PDU can be a constructed
# value with the indefinite-length encoding.
    def set_readproc (self, readproc):
        self.readproc = readproc
    def set_implicit_tag (self, tag):
        if self.cur_tag == None:
            self.cur_tag = tag
    def tag_write (self, tag):
        if trace_tag: print "Writing tag", tag
        (orig_flags, orig_tag) = tag
        if self.cur_tag <> None:
            tag = self.cur_tag
            self.cur_tag = None
        (flags, val) = tag
        # Constructed encoding is property of original tag, not of
        # implicit tag override
        flags = flags | (orig_flags & CONS_FLAG)
        extra = 0
        if val >=0x1F:
            extra = val
            val = 0x1F
        self.buf.append (flags | val)
        if extra:
            l = encode_base128 (extra)
            self.bytes_write (l)
    def read_base128 (self):
        val = 0
        while 1:
            b = self.byte_read ()
            val = val * 128 + (b & 0x7F)
            if b & 0x80 == 0:
                break
        return val
    def tag_read (self, exp_tag):
        val = self.byte_read ()
        flags = val & 0xE0
        val = val & 0x1f
        if val == 0x1F:
            val = self.read_base128 ()
        ret_tag = (flags, val)
        if self.cur_tag <> None:
            exp_tag = self.cur_tag
        if exp_tag <> None: # exp_tag of None used in tag_peek
            if not match_tag (ret_tag,exp_tag):
                self.raise_error ("Saw tag " + repr(ret_tag) +
                                  " Expecting " + repr (exp_tag))
        self.cur_tag = None
        return ret_tag
    def get_pos (self):
        if self.direction == Ctx.dir_write: return len (self.buf)
        else: return self.offset
    class LenPlaceHolder:
        def __init__ (self, ctx, estlen = 127):
            if not indef_len_encodings:
                self.ctx = ctx
                self.oldpos = ctx.get_pos ()
                self.estlen = estlen
                self.lenlen = ctx.est_len_write (estlen)
            else:
                self.ctx = ctx
                ctx.bytes_write ([0x80])
        def finish (self):
            if not indef_len_encodings:
                real_len = self.ctx.get_pos() - self.oldpos - 1
                self.ctx._len_write_at (self.ctx.get_pos () - self.oldpos - 1,
                                        self.oldpos, self.lenlen)
            else:
                self.ctx.bytes_write ([0,0])
    def len_write (self, mylen = 0):
        return Ctx.LenPlaceHolder (self, mylen)
    def len_write_known (self, mylen):
        return self.est_len_write (mylen)
    def make_len_list (self, mylen):
        if mylen < 128:
            return [mylen]
        else:
            l = []
            while mylen:
                l.append (mylen % 256)
                mylen = mylen / 256
            assert (len (l) < 0x80)
            l.append (len (l) | 0x80)
            l.reverse ()
            return l
    def est_len_write (self, mylen):
        l = self.make_len_list (mylen)
        self.buf.fromlist (l)
        return len (l)
    def _len_write_at (self, mylen, pos, lenlen):
        l = self.make_len_list (mylen)
        assert (len(l) >= lenlen)
        # array.pop not available in Python 1.5.2.  We could just use a
        # less efficient length encoding (long form w/leading 0 bytes
        # where necessary), but ...
        for i in range (len(l) - lenlen):
            self.buf.insert (pos, 0)
        for i in range(len(l)):
            self.buf[pos + i] = l [i]
    # len_read returns None to indicate indefinite-length encoding,
    # 0 to indicate definite-len zero-length
    def len_read (self):
        len = self.byte_read ()
        if len >= 128:
            extra_bytes = len & 0x7F
            if extra_bytes == 0: return None
            len = 0
            for i in range (extra_bytes):
                len = 256 * len + self.byte_read ()
        return len
    def bytes_write (self, data):
        if type (data) == type ([]):
            self.buf.fromlist (data)
        elif type (data) == type (''):
            self.buf.fromstring (data)
        else:
            raise EncodingError, "Bad type to bytes_write"
    def tag_peek (self):
        oldoff = self.offset
        tag = self.tag_read (None)
        self.offset = oldoff
        return tag
    def check_space (self):
        if self.offset == len (self.buf):
            if self.readproc:
                self.buf.fromstring (self.readproc ())

    def byte_read (self):
        self.check_space ()
        b = self.buf[self.offset]
        self.offset =  self.offset + 1
        return b
    def byte_peek (self):
        self.check_space ()
        return self.buf[self.offset]
    def dump (self, len = 0x10):
        try:
            for i in range (len):
                print hex (self.buf[self.offset + i]),
                if i > 0 and 0 == (i % 8):
                    print
        except IndexError:
            pass
        print
    def get_len_remaining (self):
        return len (self.buf) - self.offset
    def rd_indef_term (self):
        b1 = self.byte_read ()
        b2 = self.byte_read ()
        if b1 <> 0 or b2 <> 0:
            self.raise_error ("Bad indef-len terminator")
    def raise_error (self, descr):
        if self.direction == Ctx.dir_write:
            offset = len (self.buf)
        else:
            offset = self.offset
        raise BERError, (descr, offset)
    def reset_read (self):
        self.buf = self.buf [self.offset:]
        self.offset = 0
    def def_done (self, mylen):
        if mylen == None:
            def done (ctx = self):
                return ctx.tag_peek () == (0,0)
        else:
            oldpos = self.get_pos ()
            def done (ctx = self, oldpos = oldpos, mylen = mylen):
                return ctx.get_pos () - oldpos >= mylen
        return done


# EXPLICIT, IMPLICIT, CHOICE can't derive from eltbase b/c they need to do
# tag manipulation
class ELTBASE:
    # known_len is 1 if len can easily be calculated w/o encoding
    # val (e.g. OCTET STRING),
    # 0 if otherwise and we have to go back and fix up (e.g. SEQUENCE).
    def encode (self, ctx, val):
        ctx.tag_write (self.tag)
        if not self.known_len: lph = ctx.len_write ()
        self.encode_val (ctx, val)
        if not self.known_len: lph.finish ()
    def decode (self, ctx):
        cur_tag = ctx.tag_read (self.tag)
        mylen = ctx.len_read ()
        oldpos = ctx.get_pos ()
        v = self.decode_val (ctx, cur_tag, mylen)
        if mylen == None:
            ctx.rd_indef_term ()
        else:
            assert (mylen == ctx.get_pos () - oldpos)
        return v

class TAG: # base class for IMPLICIT and EXPLICIT
    def __init__ (self, tag, cls=CONTEXT_FLAG):
        if type (tag) == type (0):
            tag = (CONTEXT_FLAG, tag)
        self.tag = (tag[0] | self.flags, tag[1])
    def set_typ (self, typ):
        self.typ = typ
    def __call__ (self):
        return self.typ ()

# Note: IMPLICIT and EXPLICIT have dual use: they can be instantiated by
# users of this module to indicate tagging, but when TAG.set_typ is
# called, they become asn.1 type descriptors themselves.  Maybe these
# two uses should have separate classes, making four classes overall.

class IMPLICIT(TAG):
    flags = 0
    def __repr__ (self):
        return "IMPLICIT: " + repr (self.tag)
    def __cmp__ (self, other):
        if not isinstance (other, IMPLICIT):
            return -1
        return cmp (self.tag, other.tag)
    def encode (self, ctx, val):
        ctx.set_implicit_tag (self.tag)
        self.typ.encode (ctx, val)
    def decode (self, ctx):
        ctx.set_implicit_tag (self.tag)
        return self.typ.decode (ctx)
    
class EXPLICIT (TAG):
    flags = CONS_FLAG  # Explicit tag is always a constructed encoding
    def __repr__ (self):
        return "EXPLICIT: " + repr (self.tag)
    def __cmp__ (self, other):
        if not isinstance (other, EXPLICIT):
            return -1
        return cmp (self.tag, other.tag)
    def encode (self, ctx, val):
        ctx.cur_tag = None
        ctx.tag_write (self.tag)
        lph = ctx.len_write ()
        self.typ.encode (ctx, val)
        lph.finish ()
    def decode (self, ctx):
        tag = ctx.tag_read (self.tag)
        len = ctx.len_read ()
        v = self.typ.decode (ctx)
        if len == None:
            ctx.rd_indef_term ()
        return v

def make_tag (tag):
    if implicit_default:
        return IMPLICIT (tag)
    else:
        return EXPLICIT (tag)

def TYPE (tag, typ):
    if tag == None:
        return typ
    if not isinstance (tag, TAG):
        tag = make_tag (tag)
    tag.set_typ (typ)
    return tag


class SEQUENCE_BASE (ELTBASE):
    tag = (CONS_FLAG, SEQUENCE_TAG)
    known_len = 0
    def __init__ (self, klass, seq):
        self.klass = klass
        self.seq = []
        for e in seq:
            self.seq.append (self.mung (e))
    def __call__ (self, **kw):
        return apply (self.klass, (), kw)
    def mung (self, e):
        if len (e) == 3:
            (name, tag, typ) = e
            optional = 0
        elif len (e) == 4:
            (name, tag, typ, optional) = e
        else: assert (len(e) == 3 or len(e) == 4)
        typ = TYPE (tag, typ)
        return (name, typ, optional)
    def __repr__ (self):
        return  ('SEQUENCE: ' + repr (self.klass) +
                 '\n' + string.join (map (repr, self.seq), '\n'))
    def get_attribs (self):
        return map (lambda e: e[0], self.seq)
    def encode_val (self, ctx, val):
        for (attrname, typ, optional) in self.seq:
            try:
                v = getattr (val, attrname)
            except AttributeError:
                if optional: continue
                else: raise EncodingError, ("Val " +  repr(val) +
                                            " missing attribute: " +
                                            str(attrname))
            if trace_seq: print "Encoding", attrname, v
            typ.encode (ctx, v)
    def decode_val (self, ctx, seq_tag, mylen):
        oldpos = ctx.get_pos ()
        c = self.klass ()
        done = ctx.def_done (mylen)
        for (attrname, typ, optional) in self.seq:
            if done ():
                break
            force = 0
            if not hasattr (typ, 'tag'): # only CHOICE, for now
                force = not optional
                tag = None
            else:
                tag = typ.tag
                pk = ctx.tag_peek ()
            if trace_seq: print "seq tag", seq_tag, "exp tag", tag, \
               "Peeked tag", pk, "typ", typ, "force", force
            if tag <> None and not match_tag (tag, pk):
                if optional:
                    continue
# XXX Do we still need this raise, or will typ.decode below whine?
                ctx.raise_error ("Bogus tag: expecting " + repr (tag) +
                                 " saw " + repr (pk) + repr (self.seq))
            if force:
                v = typ.decode (ctx, 1, so_far = c)
            else:
                if tag == None: # XXX refactor this!
                    v = typ.decode (ctx, 0, so_far = c)
                else:
                    v = typ.decode (ctx)
            if trace_seq:
                print "Setting", attrname, "to", v
            setattr (c, attrname, v)
        return c

import new

# SEQUENCE returns an object which is both 
# XXX I used to have SEQUENCE taking a classname and, using ~8 lines of
# black (OK, grayish) magic (throw an exn, catch it, and futz with the
# caller's locals dicts), bind the klass below in the caller's namespace.
# This meant I could provide bindings for SEQUENCEs nested inside other
# definitions (making my specs look more like the original ASN.1), and
# that I got the correct name for debugging purposes instead of using
# mk_klass_name ().  I took it out b/c I didn't like the magic or the
# funny syntax it used (a mere function call caused an alteration to the
# caller's ns), but I'm still not sure about that.  Ideally we'd compile
# real ASN.1 def'ns to Python specs, and then I could take care of these
# issues in the compiler -- pass the redundant name to SEQUENCE as an arg
# (so klass.__name__ is correct for debugging purposes), and auto-breakout
# SEQUENCE defns nested inside others.  (Generating a name# for those could be:
#  - for SEQUENCE inside SEQUENCE or CHOICE, the name on the left.
#  - for SEQUENCE inside TYPE, the name for the TYPE (and make TYPE callable,
#     so it can be used to instantiate the class.)
#  - for others (e.g SEQUENCE_OF SEQUENCE), annotate asn.1 w/ special comment?

class Ctr:
    def __init__ (self):
        self.count = 0
    def __call__ (self):
        self.count = self.count + 1
        return self.count

class_count = Ctr ()

# This name only appears in debugging displays, so no big deal.
def mk_seq_class_name (): 
    return "seq_class_%d" % class_count ()
    
def SEQUENCE (spec):
    klass = new.classobj (mk_seq_class_name (), (StructBase,), {})
    seq = SEQUENCE_BASE (klass, spec)
    klass._allowed_attrib_list = seq.get_attribs ()
    seq.klass = klass
    return seq
    
class SEQUENCE_OF(ELTBASE):
    tag = (CONS_FLAG, SEQUENCE_TAG)
    known_len = 0
    def __init__ (self, typ):
        self.typ = typ
    def encode_val (self, ctx, val):
        for e in val:
            self.typ.encode (ctx, e)
    def decode_val (self, ctx, cur_tag, mylen):
        l = []
        if trace_seq_of:
            print "Entering SEQUENCE_OF"
        done = ctx.def_done (mylen)
        while not done ():
            if trace_seq_of:
                print "SEQUENCE_OF", l, self.typ, getattr (self.typ,
                                                           'tag', None)
            l.append (self.typ.decode (ctx))
        return l

_oid_to_asn1_map = [] # list b/c OIDs not hashable.

def register_oid (oid, asn):
    tmp = EXPLICIT(0) # b/c ANY is EXPLICIT 0 arm of EXTERNAL CHOICE
    tmp.set_typ (asn)
    _oid_to_asn1_map.append ((oid, tmp))

# XXX It would probably be better to handle EXTERNAL as a specialized
# descendant of SEQUENCE than to have special-case code in CHOICE to
# handle it.

def check_EXTERNAL_ASN (so_far):
    if so_far == None:
        return None
    if so_far.__class__ <> external_class:
        return None
    dir_ref = getattr (so_far, 'direct_reference', None)
    if dir_ref == None:
        return
    if trace_external:
        print so_far, dir_ref
    for (oid, asn) in _oid_to_asn1_map:
        if dir_ref == oid:
            return asn
    return None

class CHOICE:
    choice_type = 1
    # No class.tag, tag derives from chosen arm of CHOICE
    def __init__ (self, c):
        self.choice = []
        for arm in c:
            self.choice.append (self.mung (arm))
    def set_arm (self, i, new_arm):
        self.choice[i] = self.mung (new_arm)
    def mung (self, arm):
        (cname, ctag, ctyp) = arm
        ctyp = TYPE (ctag, ctyp)
        return (cname, ctyp)
    def __repr__ (self):
        return 'CHOICE: ' + string.join (map (repr,self.choice), '\n')
    def encode (self, ctx, val):
        if trace_choice: print val
        (name, val) = val
        for (cname, ctyp) in self.choice:
            if cname == name:
                if trace_choice: print "Encoding typ", ctyp, "Val", val
                ctyp.encode (ctx, val)
                return
        err =  ("Bogus, no arm for " + repr (name) + " val " +
                repr(val) + " in " + repr (self.choice))
        raise EncodingError,err
# Only time we aren't forced is when CHOICE is an OPTIONAL elt. of a SEQUENCE
    def decode (self, ctx, forced = 1, so_far = None):
        pk_tag = ctx.tag_peek ()
        for (cname, ctyp) in self.choice:
            if trace_choice:
                print "Testing", cname,"ctyp", ctyp, "against read tag", \
                      pk_tag, "Val", match_tag (ctyp.tag, pk_tag)
            ltyp = check_EXTERNAL_ASN (so_far)
            if ltyp <> None: # it's an ANY type in EXTERNAL
                if trace_external:
                    print "Returning ANY type for EXTERNAL"
                return ('single-ASN1-type', ltyp.decode (ctx))
            if match_tag (ctyp.tag, pk_tag):
                v = (cname, ctyp.decode (ctx))
                return v
        if forced:
            ctx.raise_error ("No match for " + repr (pk_tag) + " in " +
                             repr (self.choice))
        return None

class BitStringVal:
    def __init__ (self, top, bits = 0):
        self.top_ind = top # 0-based
        self.bits = bits
    def __repr__ (self):
        return "Top: " +  repr(self.top_ind) +  " Bits " + repr(self.bits)
    def __cmp__ (self, other):
        return cmp ((self.top_ind, self.bits), (other.top_ind, other.bits))
    def set (self, bit):
        if bit > self.top_ind: self.top_ind = bit # XXX or error?
        self.bits = self.bits | (1L << (self.top_ind - bit))
    def set_bits (self, bitseq):
        for bit in bitseq:
            self.set (bit)
    def is_set (self, bit):
        if self.top_ind - bit < 0:
            return 0
        return self.bits & (1L << ( self.top_ind - bit))

class BITSTRING_class (ELTBASE):
    tag = (0, BITSTRING_TAG)
    known_len = 1
    def encode_val (self, ctx, val):
        pad_bits = (8 - (val.top_ind + 1 % 8)) % 8 # XXX better way?
        len = ((val.top_ind + 1) / 8) + 1
        # + 1 for count of padding bits, count always 1 byte
        if pad_bits <> 0: len = len + 1
        ctx.len_write_known (len)
        l = []
        to_write = (1L * val.bits) <<  pad_bits
        assert (to_write >= 0)
        for i in range (len - 1):
            l.append (to_write % 256)
            to_write = to_write / 256
        l.append (pad_bits)
        l.reverse ()
        ctx.bytes_write (l)
    def decode_val (self, ctx, tag, mylen):
        if mylen == None: ctx.raise_error ("cons encoding of BITSTRING NYI")
        pad_bits = ctx.byte_read ()
        bits = 0
        for i in range (mylen - 1):
            b = ctx.byte_read ()
            bits = 256L * bits + b
        bits = bits >> pad_bits
        return BitStringVal ((mylen - 1) * 8 - pad_bits - 1, bits)

BITSTRING = BITSTRING_class ()

class OCTSTRING_class (ELTBASE):
    tag = (0, OCTSTRING_TAG)
    known_len = 1
    def __init__ (self, tag = None):
        if tag <> None:
            self.tag = (0, tag)
        if cons_encoding:
            self.tag = (CONS_FLAG, self.tag[1])
            self.known_len = 0
    def __repr__ (self):
        return 'OCTSTRING: ' + repr (self.tag)
    def encode_val (self, ctx, val):
        if cons_encoding:
            tag = (0, OCTSTRING_TAG)
            for i in range (len (val)):
                ctx.tag_write (tag)
                ctx.len_write_known (1)
                ctx.bytes_write ([ord(val[i])])
        else:
            ctx.len_write_known (len (val))
            ctx.bytes_write (val)
    def decode_val (self, ctx, cur_tag, mylen):
        if cur_tag [0] & CONS_FLAG:
            done = ctx.def_done (mylen)
            l = []
            while not done ():
                v = self.decode (ctx)
                l.append (v)
            return string.join (l, '')
        else:
            if mylen == None:
                ctx.raise_error ("Indef noncons encoding for OCTSTRING tag: " +
                                               repr (self.tag))
            l = []
            for i in range (mylen):
                l.append (ctx.byte_read ())
            s = ''.join (map (chr, l))
            return s
    
OCTSTRING = OCTSTRING_class ()

_STRING_TAGS = (UTF8STRING_TAG, NUMERICSTRING_TAG, PRINTABLESTRING_TAG,
                T61STRING_TAG, VIDEOTEXSTRING_TAG, IA5STRING_TAG,
                GRAPHICSTRING_TAG, VISIBLESTRING_TAG, GENERALSTRING_TAG,
                UNIVERSALSTRING_TAG, BMPSTRING_TAG, GENERALIZEDTIME_TAG,
                OBJECTDESCRIPTOR_TAG)

(UTF8String, NumericString, PrintableString, T61String, VideotexString,
 IA5String, GraphicString, VisibleString, GeneralString, UniversalString,
 BMPString, GeneralizedTime, ObjectDescriptor) = \
 map (OCTSTRING_class, _STRING_TAGS)


# XXX kludge, ANY can actually be any asn1.type, and defining it to
# OCTSTRING means that indef-len encoded values will lose.  The ASN.1 spec
# is supposed to indicate an OID or something somewhere which we can use to
# figure out how to encode/decode the ANY type.

class ANY_class (OCTSTRING_class):
    tag = (CONS_FLAG, ANY_TAG)
    # override encode, not encode_val: skip writing tag, len,
    # val is assumed to be BER-encoded already
    def encode (self, ctx, val):
        ctx.bytes_write (val)

ANY = ANY_class ()


def sgn(val):
    if val < 0: return -1
    if val == 0: return 0
    return 1

class BOOLEAN_class (ELTBASE):
    tag = (0, BOOL_TAG)
    known_len = 1
    def encode_val (self, ctx, val):
        ctx.len_write_known (1)
        ctx.bytes_write ([val <> 0])
        # if val is multiple of 256, Python would treat as true, but
        # just writing val would truncate. Thus, write val <> 0
    def decode_val (self, ctx, tag, mylen):
        if mylen <> 1: ctx.raise_error ("Bogus length for bool " +
                                        repr (mylen))
        return ctx.byte_read ()
    
BOOLEAN = BOOLEAN_class ()

class INTEGER_class (ELTBASE):
    tag = (0, INT_TAG)
    known_len = 1 
    def encode_val (self, ctx, val):
        # based on ber.py in pysnmp
        l = []
        if val == 0:
            l = [0]
        elif val == -1:
            l = [0xFF]
        else:
            if sgn (val) == -1:
                term_cond = -1
                last_hi = 1
            else:
                term_cond = 0
                last_hi = 0
            while val <> term_cond:
                val, res = val >> 8, (val & 0xFF)
                l.append (res)
            if (l[-1] & 0x80 <> 0) ^ last_hi:
                l.append (last_hi * 0xFF)
        ctx.len_write_known (len(l))
        l.reverse ()
        ctx.bytes_write (l)
        
    def decode_val (self, ctx, tag, mylen):
        if mylen == None: ctx.raise_error ("Indef-length encoding for INTEGER")
        val = 0
        if ctx.byte_peek () >= 128: sgn = -1
        else: sgn = 1
        for i in range (mylen):
            b = ctx.byte_read ()
            if trace_int: print "Reading INTEGER byte", b
            val = 256 * val + sgn * b
        if sgn == -1:
            val = - (val + pow (2, 8 * mylen))
            # XXX should be much more efficient decoder here
        return val
    
INTEGER = INTEGER_class ()

class OidVal:
    def __init__ (self, lst):
        self.lst = lst
        self.encoded = self.encode (lst)
    def __repr__ (self):
        s = 'OID:'
        for i in self.lst:
            s = s + ' %d' % i
        return s
    def __cmp__ (self, other):
        if not hasattr (other, 'lst'):
            return -1
        return cmp (self.lst, other.lst)
        
    def encode (self, lst):
        encoded = [40 * lst [0] + lst [1]]
        for val in lst [2:]:
            encoded = encoded + encode_base128 (val)
        return encoded
        
class OID_class (ELTBASE):
    tag = (0, OID_TAG)
    known_len = 1
    def encode_val (self, ctx, val):
        ctx.len_write_known (len (val.encoded))
        ctx.bytes_write (val.encoded)
    def decode_val (self, ctx, tag, mylen):
        if mylen == None: ctx.raise_error ("Indef encoding for OID")
        oldpos = ctx.get_pos ()
        b1 = ctx.byte_read ()
        oid = [b1 / 40, b1 % 40]
        while ctx.get_pos () - oldpos < mylen:
            val = ctx.read_base128 ()
            oid.append (val)
        return OidVal (oid)
    
OID = OID_class ()

class NULL_class (ELTBASE):
    tag = (0, NULL_TAG)
    known_len = 1
    def encode_val (self, ctx, val):
        ctx.len_write_known (0)
    def decode_val (self, ctx, tag, mylen):
        if mylen <> 0: ctx.raise_error ("Bad length for NULL" + str (tag) +
                                        ' ' + str (mylen))
        return None
    
NULL = NULL_class ()
    

# This is the pre-1994 def'n.  Note that post-1994 removes the ANY
# and BITSTRING options
EXTERNAL = SEQUENCE ([('direct_reference', None, OID, 1),
                      ('indirect_reference', None, INTEGER, 1),
                      ('data_value_descriptor', None, ObjectDescriptor, 1),
                      ('encoding', None, 
                       CHOICE([('single-ASN1-type', EXPLICIT(0), ANY),
                               ('octet-aligned', 1, OCTSTRING),
                               ('arbitrary', 2, BITSTRING)]))])

external_class = EXTERNAL().__class__ # needed for check_EXTERNAL_ASN above


EXTERNAL.tag = (CONS_FLAG, EXTERNAL_TAG)
# Don't try this at home!  (I.e. frobbing the tag value is unsupported)
                           

class ENUM (INTEGER_class):
    def __init__ (self, **kw):
        self.__dict__.update (kw)
        
OBJECT_IDENTIFIER = lambda x:x
ANY_constr = lambda def_by=None: None

do_print_test = 0
def test (spec, val, assertflag = 1):
    # XXX add an optional correct encoding to check against, and cmpfn
    buf = encode (spec, val)
    if do_print_test:
        for byte in buf:
            print hex (byte)[2:], 
        print
    dec = decode (spec, buf)
    if do_print_test:
        print "Val",val, "Dec", dec
    if assertflag:
        assert (dec == val)

if __name__ == '__main__':
    do_print_test = 1
    int_spec = TYPE (3, INTEGER)
    string_spec = TYPE (5, GeneralString)
    bitstring_spec = TYPE (5, BITSTRING)
    octstring_spec = TYPE (5, OCTSTRING)
    bool_spec = TYPE(100, BOOLEAN)
    test (bool_spec, 0)
    test (bool_spec, 1)
    test (bool_spec, -1, 0)
    test (bool_spec, 1024, 0)
    test (int_spec, 4)
    test (int_spec, 256)
    test (int_spec, -128)
    test (int_spec, -129) # should be 83 02 FF 7F
    test (int_spec, -1)
    test (int_spec, 0)
    test (int_spec, -27066) # should be 83 02 96 46
    test (string_spec, '')
    test (string_spec, 'Lemon curry?')
    test (octstring_spec, '\xFF\x00\x99 Foo')
    bs_test = BitStringVal (17, 0x1B977L) # 011011100101110111
    for i in range (10):
        test (bitstring_spec, bs_test)
        bs_test.top_ind = bs_test.top_ind + 1
    seq_spec = SEQUENCE (
                         [('a',5, INTEGER),
                          ('c', 51, INTEGER, 1),
                          ('b',6, INTEGER)])

    class Foo (seq_spec.klass):
        def __init__ (self, a = 0,b = 0):
            StructBase.__init__ (self)
            self.a = a
            self.b = b

    seq_test = Foo (4,5)
    test (seq_spec, seq_test)
    seq_test.c = 9
    test (seq_spec, seq_test)
    seq_of_spec = SEQUENCE_OF (INTEGER)
    test (seq_of_spec, [1,44,131072])
    oid_spec = TYPE (4, OID)
    oid = OidVal ([1, 2, 840, 10003, 1])
    test (oid_spec, oid)
    null_spec = TYPE (65536, NULL)
    test (null_spec, None)
    v = EXTERNAL ()
    v.direct_reference = oid
    v.data_value_descriptor = "infrequently used field"
    v.encoding = ('octet-aligned', 'foo bar')
    test (EXTERNAL, v)
    

    seq_of_spec2 = TYPE (18, SEQUENCE_OF (TYPE(105,GeneralString)))
    test (seq_of_spec2, ['db'])
    test (seq_of_spec2, ['db1', 'db2', 'db3'])
    big_spec_test = SEQUENCE ([('a', 5, INTEGER),
                                    ('b', 4096, GeneralString)])
    sq = big_spec_test ()
    sq.a = 1
    sq.b = '34' *  8192
    test (big_spec_test, sq)
    sq.b = '35' * (65536 * 2)
    test (big_spec_test, sq)
    try:
        sq.c = 'bogus'
    except AttributeError, exn:
        assert (exn.args == ('c',))
    else: assert (0)

        
