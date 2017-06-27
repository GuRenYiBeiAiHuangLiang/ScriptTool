
import types
import typing

PackageName = typing.NamedTuple("PackageName", [
    ("Name", str),
    ("CompareString", str)
    ])
PackageName.__repr__ = types.MethodType(lambda s: s.Name)
PackageName.__eq__ = types.MethodType(lambda this, that: isinstance(that, PackageName) and this.CompareString == that.CompareString)
PackageName.__hash__ = types.MethodType(lambda s: s.CompareString.__hash__())
# TODO: missing CompareMethods
# PackageName.__init__ = type.MethodType(lambda s, n: s.Name = )

if __name__ == '__main__':
    packageName = PackageName("Guwei", "guwei")
    print(packageName)

    import re
    re.compile("^(\S+)\s*$")
