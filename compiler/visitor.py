# Modeled on Python's Lib/compiler/visitor.py

class BadNode (Exception): pass

class ASTWalk:
    def _default(self, node, *args):
        raise BadNode (str (node))

    def dispatch(self, node, *args):
        methname = 'visit' + node.__class__.__name__
        method = getattr(self.visitor, methname, self.default)
        return method (node, *args)

    def preorder(self, tree, visitor, *args):
        self.visitor = visitor
        self.default = getattr (self.visitor, 'visitdefault', self._default)
        l = self.dispatch(tree, *args)
        if l == None: return
        for n in l:
            self.dispatch (n, *args)
