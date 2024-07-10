allPipelines = """
af2_suite_model-pr
analytics-logprocessor-pr
analytics-logprocessor-release
analytics-parser-pr
analytics-parser-release
analytics-tws-to-splunk-pr
analytics-tws-to-splunk-release
Analytics_Failure_Category_Prediction_Model
audacity-automation-pr
audacity-automation-release
audio-quality-classifier
audio-quality-classifier-release
audio-tools-automation-pr
audio-tools-automation-release
automation-architecture
automation-data-models-pr
automation-data-models-release
autostress-pr
autostress-release
awesome-automation-libraries-sync
azure-auth-lib-pr
azure-auth-lib-release
best-known-ifwi-preprod-pr
best-known-ifwi-prod-pr
camera-driver-automation-pr
camera-driver-automation-release
campaign-assigner-pr
campaign-assigner-release
campaign-builder-pr
campaign-builder-release
campaign-catalog-integration-test-temp
campaign-catalog-pr
campaign-catalog-release
campaign-dispatcher-pr
campaign-query-pr
campaign-query-release
cicd-tasks-pr
cicd-tasks-release
cloud-client-automation-pr
cloud-client-automation-release
cmaas-pr
cmaas-release
command-wrapper-pr
command-wrapper-release
connectivity-tools-automation-pr
connectivity-tools-automation-release
rails-release
core-lib-pr
core-lib-release
cps-dtt-test-content-pr
cps-dtt-test-content-release
data-ingest-pr
data-ingest-release
debug-tools-automation-pr
debug-tools-automation-release
display-automation-pr
display-automation-release
dpmt-execution
dpmt-execution-pr
dpmt-pr
dpmt-profile-service-release
dpmt-release
dpmt_profile_service-pr
enact-service-pr
enact-service-release
endurance-gaming-pr
endurance-gaming-release
google-meet-automation-pr
google-meet-automation-release
hgs-emulator-validation-Automation-pr
hgs-emulator-validation-automation-release
hgsplus-workload-automation-pr
hgsplus-workload-automation-release
hsd-report-service-pr
hsd-report-service-release
io-margining-automation-pr
io-margining-automation-release
ipf-python-client-pr
ipf-python-client-release
manageability-tools-automation-pr
manageability-tools-automation-release
mep-classifier-service-pr
mep-classifier-service-release
meshcommander-automation-pr
meshcommander-automation-release
microservice-auth-pr
microservice-auth-release
microservice-deploy
microservice-integration-test
microservice-navbar-ui-pr
microservice-pr
microservice-release
microservice-template-pr
microservices-navbar-ui-pr
microsoft-effect-package-automation-pr
microsoft-effect-package-automation-release
moreutils-pr
moreutils-release
oap-microservice-deploy
oap-microservice-integration-test
oap-pr
oap-release
onebox-api-wrapper-pr
onebox-api-wrapper-release
overclocking-tools-automation-pr
overclocking-tools-automation-release
packaging-service-pr
packaging-service-release
plugins-pr
plugins-release
pnputil-powershell-automation-pr
pnputil-powershell-automation-release
power-automation-pr
power-automation-release
pycst-backend-release
pycst-pr
pycst-release
pywevtutil-pr
pywevtutil-release
rails-enact-pr
rails-enact-release
rails-framework-pr
rails-framework-release
rails-init-tc-pr
rails-init-tc-release
rails-pr
rails-recovery-pr
rails-recovery-release
rails-recovery-tc-pr
rails-recovery-tc-release
rails-release
rails-resources-pr
rails-resources-release
rails-sample-tc-pr
rails-sample-tc-release
rails-test-content-template-pr
rails-test-content-template-release
rails-wse-bronze-test-content-pr
rails-wse-bronze-test-content-release
rails_nightly_execution_dit_onsite_cerium
rails_nightly_execution_dit_onsite_wipro
retry-service-pr
retry-service-release
root-configuration-ui-pr
run-automation-dev-locally-pr
run-automation-dev-locally-release
Sample_CD
abi_test
emphemeral_agent_win_hello_world
idoc-helloworld
test-kaniko
test-microservice
test_poetry
test_poetry_2
test_win_containers
sdr-python-pr
sdr-python-release
secret-resource-release
security-ipf-autimation-pr
security-ipf-autimation-release
security-ipf-automation-pr
security-ipf-automation-release
selenium-automation-pr
selenium-automation-release
services-deployments-pr
SL3 Trigger
storage-automation-pr
storage-automation-release
suite-def-siv-docs
suite-definition-pr
suite-definition-release
sync-artifacts-between-ba-and-or
systemscope-python-pr
systemscope-python-release
tcss-debug-tool-pr
tcss-debug-tool-release
teams_automation-pr
teams_automation-release
test-automation-library-template-pr
test-automation-library-template-release
test-batch-builder-pr
test-batch-builder-release
test-batch-catalog-pr
test-batch-catalog-release
test-batch-executor-pr
test-batch-executor-release
test-catalog-pr
test-catalog-release
test-catalog-temp
test-catalog-ui-pr
test-catalog-ui-pr-dummy
test-list-service-pr
test-microservice
test-microservice-pr
test-microservice-release
thermal-tools-automation-pr
thermal-tools-automation-release
three-d-mark-pr
three-d-mark-release
tws-campaign-monitor-pr
tws-campaign-monitor-release
tws-certifier-pr
tws-certifier-release
tws-gateway-service-pr
tws-gateway-service-release
tws-meta-pr
tws-meta-release
tws-toolcase-pr
tws-toolcase-release
twsapi-pr
twsapi-release
upgrade-utility-pr
upgrade-utility-release
vaad-tools-automation-pr
vaad-tools-automation-release
vault-resource-sync
vault-resource-validation
vault-server-pr
winidoc-hello-world
vaultio-pr
vaultio-release
vc2-pr
vc2-release
visual-processing-unit-automation-pr
visual-processing-unit-automation-release
vlab-catalog-pr
vlab-catalog-release
vlab-service-pr
vlab-service-release
watch-dog-timer-automation-pr
watch-dog-timer-automation-release
wdt-automation-pr
wdt-automation-release
wmp_automation-pr
wmp_automation-release
youtube_automation
youtube_automation-release
z-temp-test-catalog-ui
zoom-automation-pr
zoom-automation-release
"""

reposToUpdate = """
suite-definition
enact-service
packaging-service
three-d-mark
command-wrapper
autostress
teams-automation
youtube-automation
display-automation
zoom-automation
meshcommander-automation
connectivity-tools-automation
audacity-automation
storage-automation
thermal-tools-automation
manageability-tools-automation
debug-tools-automation
overclocking-tools-automation
selenium-automation
automation-architecture
cloud-client-automation
rails-shared
google-meet-automation
"""

allPipelnesList = allPipelines.split()
# print(allPipelnesList)
reposToUpdateList = reposToUpdate.split()
# print(reposToUpdateList)
for repos in reposToUpdateList:
    for pipeline in allPipelnesList:
        if repos in pipeline:
            print(pipeline)