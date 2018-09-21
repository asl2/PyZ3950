#!/usr/bin/env python
"""Quick hack at graphical browser for Zthes data.  Should probably
update to use GtkCList (vs. gtk 1.2) or new fns in gtk2.0"""


import sys
import string

import gtk

import zthes1

def make_tv (term, val):
    return '%s: %s' % (term, val)

def split_tv (s):
    colon_ind = s.find (':')
    return (s[0:colon_ind], s[colon_ind + 2:]) # + 2 to ignore space, also

class App:
    def __init__ (self, host = 'dbiref.kub.nl', port = 1800,
                  db = 'jel', term = ''):
        self.zthes = zthes1.Zthes (host, port, db)
        self.mainwnd = self.mk_wnd ('Zthes browser: %s:%d %s' %
                                    (host, port, db))
        self.lookup ('', term)
    def mk_wnd (self, title):
        wnd = gtk.GtkWindow ()
        wnd.set_title (title)
        self.box = gtk.GtkVBox ()
        self.textbox = gtk.GtkHBox ()
        e = gtk.GtkEntry ()
        self.textentry = e
        e.show ()
        self.textbox.pack_start (e)
        b = gtk.GtkButton ('Lookup')
        def looker (button):
            self.lookup ('', e.get_text ())
        b.connect ('released', looker)
        b.show ()
        self.textbox.pack_start (b)
        self.textbox.show ()
        self.box.pack_start (self.textbox)

        def mk_sel_changed (fn):
            def sel_changed (l, fn = fn):
                sel = l.get_selection ()
                if len (sel) > 0:
                    s = sel[0].children ()[0].get ()
                    (typ, val) = split_tv (s)
                    fn (typ, val)
            return sel_changed

        def make_lb (text, fn, box):
            lb = gtk.GtkList ()
            lb.show ()
            frame = gtk.GtkFrame (text)
            frame.add (lb)
            frame.show ()
            box.pack_start (frame)
            lb.connect ('selection-changed', fn)
            return lb
        self.lb_head = make_lb ('Head terms', mk_sel_changed (self.set_head),
                                self.box)
        self.lb_rel  = make_lb ('Relations', mk_sel_changed (self.lookup),
                                self.box)
        self.box.show ()
        wnd.add (self.box)
        wnd.show ()
        return wnd
    def set_head (self, typ, term):
        self.lb_rel.clear_items (0, -1)
        for e in self.dat:
            if (e[0].typ == typ) and e[0].name == term:
                for x in e[1]:
                    obj = gtk.GtkListItem (make_tv (x.typ, x.name))
                    obj.show ()
                    self.lb_rel.append_items ([obj])
                return
                    
    def lookup (self, typ, term): # takes typ for uniformity only, ignores
        if term == '':
            return
        self.textentry.set_text (term)
        self.lb_head.clear_items (0, -1)
        self.lb_rel.clear_items (0, -1)
        self.dat = self.zthes.lookup (term)
        toplist = [t[0] for t in self.dat]
        for e in toplist:
            obj = gtk.GtkListItem (make_tv (e.typ, e.name))
            obj.show ()
            self.lb_head.append_items ([obj])
        if len (self.dat) > 0:
            self.lb_head.select_item (0)
    def run (self):
        gtk.mainloop ()
                

if __name__ == '__main__':
    if len (sys.argv) < 4:
        App (term = 'time series').run ()
    else:
        App (sys.argv[1], string.atoi(sys.argv[2]), sys.argv [3]).run ()

