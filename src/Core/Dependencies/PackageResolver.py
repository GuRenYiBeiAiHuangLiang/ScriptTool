
import types
import typing

from Common.domain import PackageName


Dependency = typing.Tuple("Dependency", [PackageName, VersionRequirement, FrameworkRestrictions])
DependencySet = typing.Set[Dependency]


PackageDetails = typing.NamedTuple("PackageDetails", [
    ("Name", PackageName),
    ("Source", PackageSource),
    ("DownloadLink", str),
    ("LicenseUrl", str),
    ("Unlisted", bool),
    ("DirectDependencies", DependencySet)
    ])


ResolvedPackage = typing.NamedTuple("ResolvedPackage", [
    ("Name", PackageName),
    ("Version", SemVerInfo),
    ("Dependencies", DependencySet),
    ("Unlisted", bool),
    ("IsRuntimeDependency", bool),
    ("Settings", InstallSettings),
    ("Source", PackageSource)
    ])


class ResolvedPackage(ResolvedPackage):

    def __repr__(self):
        return "%s %s" % (s.Name, s.Version)

    # TODO: needs transfer
    def __format__(self):
        return "%s\nDependencies -\n%s\nSource - %s\nInstall Settings\n%s" % (
            s.Name, s.Dependencies, s.Source, s.Settings)

    HasFrameworkRestrictions = \
        property(lambda s:
                 getExplicitRestriction(s.Settings.FrameworkRestrictions != FrameworkRestriction.NoRestriction
        ))


PackageResolution = typing.Dict[PackageName, ResolvedPackage]


def isIncluded(restriction: FrameworkRestriction, dependency: Dependency) -> bool:
    """
    """
    _, _, dependencyRestrictions = dependency
    dependencyRestrictions = getExplicitRestriction(dependencyRestrictions)
    if dependencyRestrictions == FrameworkRestriction.NoRestriction:
        return True
    else:
        return bool(restriction.RepresentedFrameworks | dependencyRestrictions.RepresentedFrameworks)


def filterByRestrictions(restrictions: FrameworkRestrictions, dependencies: DependencySet) -> DependencySet:
    """
    """
    restrictions = getExplicitRestriction(restrictions)
    if restrictions == FrameworkRestriction.NoRestriction:
        return dependencies
    else:
        return DependencySet(filter(isIncluded(restrictions), dependencies))


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


def cleanupNames(model: PackageResolution) -> PackageResolution:
    PackageResolution(map())