

from Typedef import *
from Common.domain import PackageName


Dependency = TTuple[PackageName, VersionRequirement, FrameworkRestrictions]
DependencySet = TSet[Dependency]


PackageDetails = TNTuple("PackageDetails", [
    ("Name", PackageName),
    ("Source", PackageSource),
    ("DownloadLink", str),
    ("LicenseUrl", str),
    ("Unlisted", bool),
    ("DirectDependencies", DependencySet)
    ])


ResolvedPackage = TNTuple("ResolvedPackage", [
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


PackageResolution = TDict[PackageName, ResolvedPackage]


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
    for _, package in PackageResolution.items():
        package.Dependencies = DependencySet(map(lambda name, v, d: model[name].Name, v, d))
    return model


ResolverStep = TNTuple("ResolverStep", [
    ("Relax", bool),
    ("FilteredVersion", TDict[PackageName, TNTuple[TList[SemVerInfo, TList[PackageSource]], bool]]),
    ("CurrentResolution", TDict[PackageName, ResolvedPackage]),
    ("ClosedRequirements", TSet[PackageRequirement]),
    ("OpenRequirements", TSet[PackageRequirement]),
    ])


ConflictInfo = TNTuple("ConflictInfo", [
    ("ResolveStep", ResolverStep),
    ("RequirementSet", TSet[PackageRequirement]),
    ("Requirement", PackageRequirement),
    ])


class ResolutionRaw(object): pass
class OkRaw(ResolutionRaw): pass
class ConflictRaw(ConflictInfo): pass


class ResolutionRaw:

    def getConflicts(res: ResolutionRaw):
        if isinstance(res, OkRaw):
            return set()
        elif isinstance(res, ConflictRaw):
            currentStep, _, lastPackageRequirement = res
            union = currentStep.ClosedRequirements | currentStep.OpenRequirements
            union.add(lastPackageRequirement)
            return filter(lambda x: x.Name == lastPackageRequirement.Name, union)

    getConflicts = staticmethod(getConflicts)

    def buildConflictReport(errorReport: StringBuilder, conflicts: TSet[PackageRequirement]):

        def formatVR(vr: VersionRequirement):
            s = vr.ToString()
            return ">= 0" if s.isspace() else s

        def formatPR(hasPrereleases: bool, vr: VersionRequirement):
            if hasPrereleases and vr.PreReleases == PreReleaseStatus.No:
                return "(not prereleases)"
            else:
                pass
