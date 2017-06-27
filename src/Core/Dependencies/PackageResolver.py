
import types
import typing


Dependency = typing.Tuple("Dependency", [PackageName, VersionRequirement, FrameworkRestrictions])
DependencySet = typing.Set[Dependency]


with typing.NamedTuple("PackageDetails", [
    ("Name", PackageName),
    ("Source", PackageSource),
    ("DownloadLink", str),
    ("LicenseUrl", str),
    ("Unlisted", bool),
    ("DirectDependencies", DependencySet)
    ]) as PackageDetails:
    pass


with typing.NamedTuple("ResolvedPackage", [
    ("Name", PackageName),
    ("Version", SemVerInfo),
    ("Dependencies", DependencySet),
    ("Unlisted", bool),
    ("IsRuntimeDependency", bool),
    ("Settings", InstallSettings),
    ("Source", PackageSource)
    ]) as ResolvedPackage:
    ResolvedPackage.__repr__ = types.MethodType(lambda s: "%s %s" % (s.Name, s.Version))
    # TODO: needs transfer
    ResolvedPackage.__format__ = types.MethodType(lambda s:
            "%s\nDependencies -\n%s\nSource - %s\nInstall Settings\n%s" % (s.Name, s.Dependencies, s.Source, s.Settings)
            )
    ResolvedPackage.HasFrameworkRestrictions = \
        property(lambda s:
                 getExplicitRestriction(s.Settings.FrameworkRestrictions != FrameworkRestriction.NoRestriction
        ))

PackageResolution = typing.Dict[PackageName, ResolvedPackage]


def isIncluded(restriction: FrameworkRestriction, dependency: Dependency) -> bool:
    """
    """
    _, _, dependencyRestrictions = dependency
    dependencyRestrictions = getExplicitRestriction(dependencyRestrictions)
    if dependencyRestrictions == FrameworkRestriction.NoRestriction: return True
    else:
        return bool(
            restriction.RepresentedFrameworks | dependencyRestrictions.RepresentedFrameworks
            )


def filterByRestrictions(restrictions: FrameworkRestrictions, dependencies: DependencySet) -> DependencySet:
    """
    """
    restrictions = getExplicitRestriction(restrictions)
    if restrictions == FrameworkRestriction.NoRestriction: return dependencies
    else:
        return DependencySet(
            filter(isIncluded(restrictions), dependencies)
        )


def isPackageCompatible(dependencies: DependencySet, package: ResolvedPackage) -> bool:
    """
    """
    for name, requirement, restriction in dependencies:
        if name == package.Name and not requirement.IsInRange(package.Version):
            print("Incompatible dependency: %s %s conflicts with resolved version %s" % (name, requirement, package.Version))
            return False
    else:
        return True


class DependencySetFilter:
    isIncluded = isIncluded
    filterByRestrictions = filterByRestrictions
    isPackageCompatible = isPackageCompatible
