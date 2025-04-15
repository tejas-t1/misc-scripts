import keyring
import logging
import os
from datetime import datetime
from termcolor import colored, cprint

from ngaapi.NgaDataClasses.ResponseTestLine import Parameter
from ngaapi.RestApi import Credentials, RestInterface
SERVICE_NAME = "ngaapi"

# Set up logging configuration
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'rails_tool_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('rails_tool')

def get_credential_from_keyring(key: str) -> str:
    cprint(f"Retrieving credential for key: {key}", "cyan")
    logger.info(f"Retrieving credential for key: {key}")
    credential = keyring.get_password(SERVICE_NAME, key)
    if credential:
        cprint(f"Successfully retrieved credential for {key}", "green")
        logger.info(f"Successfully retrieved credential for {key}")
    else:
        cprint(f"Failed to retrieve credential for {key}", "red")
        logger.error(f"Failed to retrieve credential for {key}")
    return credential
from ngaapi.NgaDataClasses.ResponseTestLine import TestDetails, Parameter


from suite_definition.tws.aggregators import ClassDependencyAggregator
from suite_definition.tcdef_suite_generator import TcdefSuiteGenerator
from rails_core.integration.tws.CustomCaseBuilder import CustomCaseBuilder
from suite_definition.metadata.discovery import MetadataDiscovery
from suite_definition.decorators import CaseMetaDataDecorator


class InspectToolDependency:
    """
    Example Usage
    handler = InspectToolDependency(scanModuleNames=['rails.nga_cases'])
    handler.discoverCases()
    print(handler.getToolDependenciesFromCaseId("HSD_2201143024_M"))

    """

    def __init__(self, scanModuleName):
        cprint(f"Initializing InspectToolDependency with scan module: {scanModuleName}", "yellow")
        logger.info(f"Initializing InspectToolDependency with scan module: {scanModuleName}")
        self.scanModuleNames = [scanModuleName]
        self.suiteGen = TcdefSuiteGenerator(
            module_paths=self.scanModuleNames,
            case_builder=CustomCaseBuilder(),
        )
        self.metadataDiscovery = MetadataDiscovery(scanModuleName, CaseMetaDataDecorator)
        self.aggregator = ClassDependencyAggregator()
        logger.debug("InspectToolDependency initialization complete")
        cprint("InspectToolDependency initialization complete", "green")
    
    def get_all_classes(self):
        cprint("Retrieving all classes", "cyan")
        logger.info("Retrieving all classes")
        classes = self.metadataDiscovery.find_all()
        logger.info(f"Found {len(classes)} classes")
        cprint(f"Found {len(classes)} classes", "green")
        return classes

    def discoverCases(self):
        logger.info("Discovering cases")
        self.suiteGen._discover_cases_modules()
        logger.info("Case discovery completed")
    
    def getCaseObj(self, case_id):
        logger.info(f"Getting case object for ID: {case_id}")
        return self.suiteGen._get_case(case_id)

    def getClassFromCaseId(self, moduleName):
        logger.info(f"Getting class from module name: {moduleName}")
        return self.suiteGen._get_case_from_module(moduleName, self.metadataDiscovery)

    def aggregateDependencies(self, case):
        logger.info(f"Aggregating dependencies for case: {case}")
        return self.aggregator.recurse_class_dependencies(case)

    def getToolDependenciesFromCaseId(self, caseId):
        cprint(f"Getting tool dependencies for case ID: {caseId}", "cyan")
        logger.info(f"Getting tool dependencies for case ID: {caseId}")
        className = self.getClassFromCaseId(caseId)
        toolDeps, _ = self.aggregateDependencies(className)
        logger.info(f"Found {len(toolDeps)} tool dependencies")
        cprint(f"Found {len(toolDeps)} tool dependencies", "green")
        return toolDeps


cprint("Starting tool dependency handling process", "yellow", attrs=["bold"])
logger.info("Starting tool dependency handling process")
handler = InspectToolDependency(scanModuleName='rails.nga_cases')
# handler.discoverCases()

cprint("Fetching all Rails cases", "cyan")
logger.info("Fetching all Rails cases")
rails_cases = handler.get_all_classes()

cprint("Authenticating with API", "magenta")
logger.info("Authenticating with API")
client_secret = get_credential_from_keyring("client_secret")
client_id = get_credential_from_keyring("client_id")
creds = Credentials(client_secret=client_secret, client_id=client_id)
api = RestInterface(credentials=creds)
logger.info("Fetching test lines by suite")
suite_test_lines = api.get_test_lines_by_suite("67ba941a-038f-4de1-a859-9e5607ba88c5")
logger.info(f"Retrieved {len(suite_test_lines)} test lines")

logger.info("Creating suite test line mapping")
suite_test_line_mapping = {}
for i in suite_test_lines:
    if i.GoalName is not None and i.GoalName.strip() != "":
        suite_test_line_mapping[i.GoalName] = i
logger.info(f"Created mapping with {len(suite_test_line_mapping)} entries")


params = ('case_identifier', 'case_domain', 'case_name')
logger.info("Fetching all parameters")
allParams = api.get_all_parameters()

paramid = {}
for i in allParams.Records:
    if i.Name in params:
        paramid[i.Name] = i.Id
        logger.debug(f"Found parameter ID for {i.Name}: {i.Id}")

if len(paramid.keys()) == 3:
    logger.info("Successfully fetched all required parameters")
else:
    logger.error(f"Not able to fetch all params. Found {len(paramid.keys())}/3")
    assert len(paramid.keys()) == 3, "Not able to fetch all params"


def add_to_params(param, param_id, value):
    logger.debug(f"Adding parameter: ID={param_id}, Value={value}")
    if param_id in param:
        for para in param:
            para: Parameter
            if para.Id == param_id:
                logger.debug(f"Updating existing parameter value from {para.Value} to {value}")
                para.Value = value
    else:
        logger.debug(f"Adding new parameter with ID={param_id}")
        param.append(Parameter(Id=param_id, Value=value))
    return param

logger = logging.getLogger('rails_tool')
cprint(f"Processing {len(rails_cases)} Rails cases", "yellow", attrs=["bold"])
logger.info(f"Processing {len(rails_cases)} Rails cases")
for idx, case in enumerate(rails_cases):
    metadata = case.metadata
    caseId = metadata.case_id
    title = metadata.description
    domain = metadata.domain
    cprint(f"Processing case {idx+1}/{len(rails_cases)}: {caseId}", "cyan")
    logger.info(f"Processing case {idx+1}/{len(rails_cases)}: {caseId}")
    logger.info(f"Parameter IDs: case_identifier={paramid['case_identifier']}, case_domain={paramid['case_domain']}, case_name={paramid['case_name']}")

    test_line:TestDetails = suite_test_line_mapping.get(caseId, None)
    
    if test_line:
        cprint(f"Found test line for case ID: {caseId}", "green")
        logger.info(f"Found test line for case ID: {caseId}")
        logger.info(f"Before update - Parameters: {test_line.Parameters}")
        
        case_identifier_paramid = paramid[params[0]]
        case_domain_paramid = paramid[params[1]]
        case_name_paramid = paramid[params[2]]

        testlineParam = test_line.Parameters
        testlineParam = add_to_params(testlineParam, case_identifier_paramid, caseId)
        testlineParam = add_to_params(testlineParam, case_domain_paramid, domain)
        testlineParam = add_to_params(testlineParam, case_name_paramid, title)
        
        logger.info(f"After update - Parameters: {test_line.Parameters}")
        cprint(f"Updating test line for case ID: {caseId}", "blue")
        logger.info(f"Updating test line for case ID: {caseId}")
        api.update_testline(test_line)
        cprint("Test line updated successfully", "green", attrs=["bold"])
        logger.info("Test line updated successfully")
        # break
    else:
        cprint(f"No test line found for case ID: {caseId}", "red")
        logger.warning(f"No test line found for case ID: {caseId}")

cprint("Process completed successfully", "green", attrs=["bold"])
logger.info("Process completed successfully")

# The commented code below is part of the original file but not currently used
# exit()
# paramName = "suiteDependencySet"
# allParams = api.get_all_parameters()
# paramId = None
# for i in allParams.Records:
#     if i.Name == paramName:
#         paramId = i.Id
# assert allParams is not None, "Failed to retrieve parameters from API"


# # print(len(a))
# for i in a:
#     if i.Name == "test-testline":
#         print(i.Name)
#         print(i.Parameters)
#         print(i.GoalName)
#         
#         if paramId in i.Parameters:
#             for param in i.Parameters:
#                 if param == paramId:
#                     param.Value=r"{'xyz123','4444'}"
#         else:
#             i.Parameters.append(Parameter(Id=paramId, Value="{'qwe'}"))
#
#         print(i.Parameters)
#         print(i.to_json())
#         api.update_testline(i)
#         break

# """
# Suite = ad85bc7b-fe77-42ba-b301-06eb4e9cc6fe
# Test Line = b7f5a5c1-31e0-426b-bbe9-16017bf1f628
# """