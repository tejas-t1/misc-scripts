
import keyring

from ngaapi.NgaDataClasses.ResponseTestLine import Parameter
from ngaapi.RestApi import Credentials, RestInterface
SERVICE_NAME = "ngaapi"
def get_credential_from_keyring(key: str) -> str:
    credential = keyring.get_password(SERVICE_NAME, key)
    return credential



from suite_definition.tws.aggregators import ClassDependencyAggregator
from suite_definition.tcdef_suite_generator import TcdefSuiteGenerator
from rails_core.integration.tws.CustomCaseBuilder import CustomCaseBuilder
from suite_definition.metadata.discovery import MetadataDiscovery
from suite_definition.decorators import CaseMetaDataDecorator


class InspectToolDependency:
    """
    Example Usage
    handler = TestSuiteHandler(scanModuleNames=['rails.nga_cases'])
    handler.discoverCases()
    print(handler.getToolDependenciesFromCaseId("HSD_2201143024_M"))

    """

    def __init__(self, scanModuleNames):
        self.scanModuleNames = scanModuleNames
        self.suiteGen = TcdefSuiteGenerator(
            module_paths=self.scanModuleNames,
            case_builder=CustomCaseBuilder(),
        )
        self.metadataDiscovery = MetadataDiscovery("", CaseMetaDataDecorator)
        self.aggregator = ClassDependencyAggregator()

    def discoverCases(self):
        self.suiteGen._discover_cases_modules()

    def getClassFromCaseId(self, moduleName):
        return self.suiteGen._get_case_from_module(moduleName, self.metadataDiscovery)

    def aggregateDependencies(self, case):
        return self.aggregator.recurse_class_dependencies(case)

    def getToolDependenciesFromCaseId(self, caseId):
        className = self.getClassFromCaseId(caseId)
        toolDeps, _ = self.aggregateDependencies(className)
        return toolDeps




client_secret = get_credential_from_keyring("client_secret")
client_id = get_credential_from_keyring("client_id")
creds = Credentials(client_secret=client_secret, client_id=client_id)
api = RestInterface(credentials=creds)
a = api.get_test_lines_by_suite("ad85bc7b-fe77-42ba-b301-06eb4e9cc6fe")

paramName = "suiteDependencySet"
allParams = api.get_all_parameters()

paramId = None
for i in allParams.Records:
    if i.Name == paramName:
        paramId = i.Id
assert allParams is not None, "Failed to retrieve parameters from API"


# print(len(a))
for i in a:
    
    if i.Name == "test-testline":
        print(i.Name)
        print(i.Parameters)
        print(i.GoalName)
        
        if paramId in i.Parameters:
            for param in i.Parameters:
                if param == paramId:
                    param.Value=r"{'xyz123','4444'}"
        else:
            i.Parameters.append(Parameter(Id=paramId, Value="{'qwe'}"))

        print(i.Parameters)
        print(i.to_json())
        api.update_testline(i)
        break

"""
Suite = ad85bc7b-fe77-42ba-b301-06eb4e9cc6fe

Test Line = b7f5a5c1-31e0-426b-bbe9-16017bf1f628

"""
