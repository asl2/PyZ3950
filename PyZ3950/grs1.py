#!/usr/bin/env python

"""Utility functions for GRS-1 data"""

from __future__ import nested_scopes
# XXX still need to tag non-leaf nodes w/ (tagType, tagValue)
# XXX tagType can be omitted.  If so, default either supplied
# dynamically by tagSet-M or statically spec'd by schema

# from TAG (Z39.50-1995 App 12): tagType 1 is tagSet-M, 2 tagSet-G,
# 3 locally defined.

class Node:
    """Defined members are:
    tag      - tag (always present, except for top node)
    metadata - metadata (opt, seriesOrder only for nonleaf - v. RET.3.2.3 )
    children - list of Node
    leaf     - leaf data (children and leaf are mutually exclusive)
    """
    def __init__ (self, **kw):
        self.__dict__.update (kw)
        self.tab_size = 3 # controls str() indentation width
    def str_depth (self, depth):
        l = []
        children = getattr (self, 'children', [])
        leaf = getattr (self, 'leaf', None)
        tag  = getattr (self, 'tag', None)
        indent = " " * (self.tab_size * depth)
        if leaf <> None:
            l.append ("%s%s %s" % (
                indent, str (tag), leaf.content))
        else:
            if tag <> None:
                l.append (indent + str (tag))
        meta = getattr (self, 'metadata', None)
        if meta <> None:
            l.append (indent + 'metadata: ' + str (meta))
        l.append ("".join (map (
            lambda n: n.str_depth (depth + 1), children)))
        return "\n".join (l)
    def __str__ (self):
        return "\n" + self.str_depth (-1)


def preproc (raw):
    """Transform the raw output of the asn.1 decoder into something
    a bit more programmer-friendly.  (This is automatically called
    by the ZOOM API, so you don't need to worry about it unless you're
    using the raw z3950 API.)
    """
    if isinstance (raw, type ([])):
        return Node (children = map (preproc, raw))
    else: # TaggedElement
        kw = {}
        tag = (raw.tagType, raw.tagValue [1])
        # Value [0] is str vs. num indicator
        kw ['tag'] = tag
        meta = getattr (raw, 'metaData', None)
        if meta <> None:
            kw ['metadata'] = meta
        if raw.content[0] == 'subtree':
            return Node (children = map (preproc, raw.content [1]), **kw)
        else:
            # tag and metadata are here redundantly encoded as
            # both attributes of leaf and of Node.  Use the Node
            # attribs, I'll try to clean this up sometime.
            return Node (leaf = raw, **kw)
        



