import keyring
import logging
import os
from datetime import datetime
from termcolor import colored, cprint

from ngaapi.NgaDataClasses.ResponseTestLine import Parameter, TestDetails
from ngaapi.NgaDataClasses.ResponseTestStep import ResponseTestStep
from ngaapi.RestApi import Credentials, RestInterface

from suite_definition.tws.aggregators import ClassDependencyAggregator
from suite_definition.tcdef_suite_generator import TcdefSuiteGenerator
from rails_core.integration.tws.CustomCaseBuilder import CustomCaseBuilder
from suite_definition.metadata.discovery import MetadataDiscovery
from suite_definition.decorators import CaseMetaDataDecorator
from dataclasses import asdict, dataclass
from typing import List, Optional
import json
import time

SERVICE_NAME = "ngaapi"

class Logger:
    """Handles logging setup and provides logging functionality."""
    
    def __init__(self):
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
        self.logger = logging.getLogger('rails_tool')
    
    def info(self, message):
        self.logger.info(message)
        # cprint(message, "cyan")
        
    def debug(self, message):
        self.logger.debug(message)
        
    def error(self, message):
        self.logger.error(message)
        # cprint(message, "red")
        
    def warning(self, message):
        self.logger.warning(message)
        # cprint(message, "yellow")
        
    def success(self, message):
        self.logger.info(message)
        # cprint(message, "green")
        
    def highlight(self, message):
        self.logger.info(message)
        # cprint(message, "yellow", attrs=["bold"])


class CredentialManager:
    """Manages API credentials retrieval from the keyring."""
    
    def __init__(self, service_name, logger):
        self.service_name = service_name
        self.logger = logger
    
    def get_credential(self, key):
        self.logger.info(f"Retrieving credential for key: {key}")
        credential = keyring.get_password(self.service_name, key)
        if credential:
            self.logger.success(f"Successfully retrieved credential for {key}")
        else:
            self.logger.error(f"Failed to retrieve credential for {key}")
        return credential


class InspectToolDependency:
    """Handles tool dependency discovery and management."""
    
    def __init__(self, scanModuleName, logger):
        self.logger = logger
        self.logger.info(f"Initializing InspectToolDependency with scan module: {scanModuleName}")
        self.scanModuleNames = [scanModuleName]
        self.suiteGen = TcdefSuiteGenerator(
            module_paths=self.scanModuleNames,
            case_builder=CustomCaseBuilder(),
        )
        self.metadataDiscovery = MetadataDiscovery(scanModuleName, CaseMetaDataDecorator)
        self.aggregator = ClassDependencyAggregator()
        self.logger.success("InspectToolDependency initialization complete")
    
    def get_all_classes(self):
        self.logger.info("Retrieving all classes")
        classes = self.metadataDiscovery.find_all()
        self.logger.success(f"Found {len(classes)} classes")
        return classes

    def discoverCases(self):
        self.logger.info("Discovering cases")
        self.suiteGen._discover_cases_modules()
        self.logger.info("Case discovery completed")
    
    def getCaseObj(self, case_id):
        self.logger.info(f"Getting case object for ID: {case_id}")
        return self.suiteGen._get_case(case_id)

    def getClassFromCaseId(self, moduleName):
        self.logger.info(f"Getting class from module name: {moduleName}")
        return self.suiteGen._get_case_from_module(moduleName, self.metadataDiscovery)

    def aggregateDependencies(self, case):
        self.logger.info(f"Aggregating dependencies for case: {case}")
        return self.aggregator.recurse_class_dependencies(case)

    def getToolDependenciesFromCaseId(self, caseId):
        self.logger.info(f"Getting tool dependencies for case ID: {caseId}")
        className = self.getClassFromCaseId(caseId)
        toolDeps, _ = self.aggregateDependencies(className)
        self.logger.success(f"Found {len(toolDeps)} tool dependencies")
        return toolDeps


class NGAApiHandler:
    """Handles NGA API operations and parameter management."""
    
    def __init__(self, credentials, logger):
        self.logger = logger
        self.api = RestInterface(credentials=credentials)
        self.logger.info("API interface initialized")
    
    def get_test_lines_by_suite(self, suite_id):
        self.logger.info(f"Fetching test lines for suite: {suite_id}")
        suite_test_lines = self.api.get_test_lines_by_suite(suite_id)
        self.logger.info(f"Retrieved {len(suite_test_lines)} test lines")
        return suite_test_lines
    
    def create_test_line_mapping(self, test_lines):
        self.logger.info("Creating suite test line mapping")
        mapping = {}
        for line in test_lines:
            if line.GoalName is not None and line.GoalName.strip() != "":
                mapping[line.GoalName] = line
        self.logger.info(f"Created mapping with {len(mapping)} entries")
        return mapping
    
    def get_parameter_ids(self, param_names):
        self.logger.info(f"Fetching parameter IDs for: {param_names}")
        all_params = self.api.get_all_parameters()
        param_id_map = {}
        
        for param in all_params.Records:
            if param.Name in param_names:
                param_id_map[param.Name] = param.Id
                self.logger.debug(f"Found parameter ID for {param.Name}: {param.Id}")
        
        if len(param_id_map.keys()) == len(param_names):
            self.logger.success(f"Successfully fetched all {len(param_names)} required parameters")
        else:
            self.logger.error(f"Not able to fetch all params. Found {len(param_id_map.keys())}/{len(param_names)}")
            assert len(param_id_map.keys()) == len(param_names), "Not able to fetch all params"
            
        return param_id_map
    
    def update_testline(self, test_line):
        self.logger.info(f"Updating test line: {test_line.GoalName}")
        self.api.update_testline(test_line)
        self.logger.success("Test line updated successfully")
    
    @staticmethod
    def add_to_params(param, param_id, value, logger):
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


class TestLineUpdater:
    """Handles the process of updating test lines with case metadata."""
    
    def __init__(self, nga_handler, logger):
        self.nga_handler = nga_handler
        self.logger = logger
    
    def update_test_lines(self, rails_cases, test_line_mapping, param_id_map):
        self.logger.highlight(f"Processing {len(rails_cases)} Rails cases")
        tool_dep_handler = InspectToolDependency(scanModuleName='rails.nga_cases', logger=self.logger)
        tool_dep_handler.discoverCases()
        for idx, case in enumerate(rails_cases):
            metadata = case.metadata
            self.logger.debug(f"Case metadata: {metadata}")
            
            case_id = metadata.case_id
            self.logger.info(f"Case ID: {case_id}")
            
            title = metadata.description
            self.logger.info(f"Case title: {title}")
            
            domain = metadata.domain
            self.logger.info(f"Case domain: {domain}")
            
            tooldeps = tool_dep_handler.getToolDependenciesFromCaseId(case_id)
            self.logger.info(f"Tool dependencies: {tooldeps}")
            
            self.logger.info(f"Processing case {idx+1}/{len(rails_cases)}: {case_id}")
            # break
            test_line = test_line_mapping.get(case_id, None)
            


            if test_line:

                self.logger.success(f"Found test line for case ID: {case_id}")
                self.logger.info(f"Before update - Parameters: {test_line.Parameters}")
                
                case_identifier_param_id = param_id_map['case_identifier']
                case_domain_param_id = param_id_map['case_domain']
                case_name_param_id = param_id_map['case_name']
                tool_deps_id = param_id_map['suiteDependencySet']
                
                testline_param = test_line.Parameters
                testline_param = self.nga_handler.add_to_params(testline_param, case_identifier_param_id, case_id, self.logger)
                testline_param = self.nga_handler.add_to_params(testline_param, case_domain_param_id, domain, self.logger)
                testline_param = self.nga_handler.add_to_params(testline_param, case_name_param_id, title, self.logger)
                testline_param = self.nga_handler.add_to_params(testline_param, tool_deps_id, str(tooldeps), self.logger)

                self.logger.info(f"After update - Parameters: {test_line.Parameters}")
                self.logger.info(f"Updating test line for case ID: {case_id}")
                
                self.nga_handler.update_testline(test_line)
            else:
                self.logger.warning(f"No test line found for case ID: {case_id}")

    def enable_stdout_TS_disable_stream_TL(self, test_line_mapping):
        api:RestInterface = self.nga_handler.api
        
        for name, test_line in test_line_mapping.items():
            test_line: TestDetails
            print("######")
            print(f"Updating stdout steps for testline id {test_line.Id}/{test_line.GoalName}")
            test_line = api.get_test_line_details(test_line.Id)
            teststeps = test_line.TestStepIds
            # Remove duplicates from teststeps while preserving order
            teststeps = list(dict.fromkeys(teststeps))
            print(f"Processing {len(teststeps)} unique test steps")
            import concurrent.futures
            if test_line.StreamTestLogs is True:
                test_line.StreamTestLogs = False
            def process_test_step(api, teststep):
                test_step_obj = api.get_test_step_by_id(teststep)
                if test_step_obj:
                    if test_step_obj.CollectStepLogs is True:
                        return f"Already updated: {teststep}"
                    test_step_obj: ResponseTestStep
                    test_step_obj.CollectStepLogs = True
                    
                    api.update_test_step(test_step_obj)
                    return f"Updated test step: {teststep}"
                return f"Failed to get test step: {teststep}"

            # Using ThreadPoolExecutor to process test steps concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(process_test_step, api, teststep) for teststep in teststeps]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        print(result)
                    except Exception as exc:
                        print(f"Test step processing generated an exception: {exc}")
            print("######")

def enable_stdout_TS_disable_stream_TL(suiteid):
    logger_instance = Logger()
    logger = logger_instance.logger
    
    # Initialize credential manager and get credentials
    logger_instance.highlight("Starting stdout bulk update process")
    cred_manager = CredentialManager(SERVICE_NAME, logger_instance)
    client_secret = cred_manager.get_credential("client_secret")
    client_id = cred_manager.get_credential("client_id")
    creds = Credentials(client_secret=client_secret, client_id=client_id)
    nga_handler = NGAApiHandler(creds, logger_instance)

    testlines = nga_handler.get_test_lines_by_suite(suite_id=suiteid)
    suite_test_line_mapping = nga_handler.create_test_line_mapping(testlines)

    updater = TestLineUpdater(nga_handler, logger_instance)
    updater.enable_stdout_TS_disable_stream_TL(suite_test_line_mapping)


def main(suite_id):
    # Initialize logger
    logger_instance = Logger()
    logger = logger_instance.logger
    
    # Initialize credential manager and get credentials
    logger_instance.highlight("Starting tool dependency handling process")
    cred_manager = CredentialManager(SERVICE_NAME, logger_instance)
    client_secret = cred_manager.get_credential("client_secret")
    client_id = cred_manager.get_credential("client_id")
    creds = Credentials(client_secret=client_secret, client_id=client_id)
    
    # Initialize tool dependency handler
    tool_dep_handler = InspectToolDependency(scanModuleName='rails.nga_cases', logger=logger_instance)
    rails_cases = tool_dep_handler.get_all_classes()
    
    # Initialize NGA API handler
    nga_handler = NGAApiHandler(creds, logger_instance)
    
    # Get test lines and create mapping
    
    suite_test_lines = nga_handler.get_test_lines_by_suite(suite_id)
    suite_test_line_mapping = nga_handler.create_test_line_mapping(suite_test_lines)
    
    # Get parameter IDs
    params = ('case_identifier', 'case_domain', 'case_name', 'suiteDependencySet')
    param_id_map = nga_handler.get_parameter_ids(params)
    print(param_id_map)
    # exit()
    # Update test lines with case metadata
    updater = TestLineUpdater(nga_handler, logger_instance)
    updater.update_test_lines(rails_cases, suite_test_line_mapping, param_id_map)
    
    logger_instance.highlight("Process completed successfully")

def disableStream(suiteid):
    logger_instance = Logger()
    logger = logger_instance.logger
    
    # Initialize credential manager and get credentials
    logger_instance.highlight("Starting stdout bulk update process")
    cred_manager = CredentialManager(SERVICE_NAME, logger_instance)
    client_secret = cred_manager.get_credential("client_secret")
    client_id = cred_manager.get_credential("client_id")
    creds = Credentials(client_secret=client_secret, client_id=client_id)
    nga_handler = NGAApiHandler(creds, logger_instance)

    testlines = nga_handler.get_test_lines_by_suite(suite_id=suiteid)
    suite_test_line_mapping = nga_handler.create_test_line_mapping(testlines)

    for goal, testline in suite_test_line_mapping.items():
        if testline.StreamTestLogs is False:
            continue
        testline.StreamTestLogs = False
        nga_handler.update_testline(testline)

if __name__ == "__main__":
    """
    This scipt will sync ('case_identifier', 'case_domain', 'case_name', 'suiteDependencySet'),
    between the Python File in Rails and the Test Line in NGA

    How to use?
    1) copy this file to rails repo root
    2) Update suite id below
    3) run - python metadata-updater-nga.py
    """

    suite_id = "9080eb92-61d3-4a80-95fc-d2696c560590"
    # main(suite_id=suite_id)

    start_time = time.time()
    print(f"Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    enable_stdout_TS_disable_stream_TL(suite_id)
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time taken: {total_time:.2f} seconds")
    
    # tool_dep_handler = InspectToolDependency(scanModuleName='rails.nga_cases', logger=Logger())
    # tool_dep_handler.discoverCases()
    # deps = tool_dep_handler.getToolDependenciesFromCaseId("HSD_2007321350")
    # cred_manager = CredentialManager(SERVICE_NAME, Logger())
    # client_secret = cred_manager.get_credential("client_secret")
    # client_id = cred_manager.get_credential("client_id")
    # creds = Credentials(client_secret=client_secret, client_id=client_id)
    # a = RestInterface(creds)
    # ts = a.get_test_step_by_id("6649bcc6-9766-4db5-93dd-1596dc737708")
    # print(ts)
    # ts.CollectStepLogs = True
    # a.update_test_step(ts)