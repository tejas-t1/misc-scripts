import yaml

reposToUpdate = """
frameworks.validation.platform-automation.rails-enact
frameworks.validation.platform-automation.rails-core
frameworks.validation.platform-automation.rails-tc-template
frameworks.validation.platform-automation.rails-dsl-template
frameworks.validation.platform-automation.presilicon
frameworks.validation.platform-automation.pat
frameworks.validation.platform-automation.pat-content
frameworks.validation.platform-automation.moreutils
frameworks.validation.platform-automation.wmp-automation
frameworks.validation.platform-automation.services-deployments
frameworks.validation.platform-automation.vaultio
frameworks.validation.platform-automation.vault-server
frameworks.validation.platform-automation.twsapi
frameworks.validation.platform-automation.pywevtutil
frameworks.validation.platform-automation.pycst
frameworks.validation.platform-automation.test-automation-library-template
frameworks.validation.platform-automation.pycst-backend
frameworks.validation.platform-automation.awesome-automation-libraries
frameworks.validation.platform-automation.tuning-wizard-automation
frameworks.validation.platform-automation.endurance-gaming
frameworks.validation.platform-automation.hgsplus-workload-automation
frameworks.validation.platform-automation.hgs-emulator-validation-automation
frameworks.validation.platform-automation.camera-driver-automation
frameworks.validation.platform-automation.systemscope-python
frameworks.validation.platform-automation.hammock-harbor-tool-automation
frameworks.validation.platform-automation.watch-dog-timer-automation
frameworks.validation.platform-automation.visual-processing-unit-automation
frameworks.validation.platform-automation.audio-tools-automation
frameworks.validation.platform-automation.sdr-python
frameworks.validation.platform-automation.mep-classifier-service
frameworks.validation.platform-automation.cps-dtt-test-content
frameworks.validation.platform-automation.microsoft-effect-package-automation
frameworks.validation.platform-automation.ipf-python-client
frameworks.validation.platform-automation.rails-test-content-template
frameworks.validation.platform-automation.io-margining-automation
frameworks.validation.platform-automation.vaad-tools-automation
frameworks.validation.platform-automation.pnputil-powershell-automation
frameworks.validation.platform-automation.security-ipf-automation
frameworks.validation.platform-automation.tcss-debug-tool
frameworks.validation.platform-automation.power-automation
frameworks.validation.platform-automation.prst-automation
frameworks.validation.platform-automation.audio-quality-classifier
frameworks.validation.platform-automation.wheel-package-pipeline
frameworks.validation.platform-automation.wse-bronze-test-content
frameworks.validation.platform-automation.recovery
frameworks.validation.platform-automation.rails-init-tc
frameworks.validation.platform-automation.onebox-api-wrapper
frameworks.validation.platform-automation.recovery-tc
frameworks.validation.platform-automation.video-quality-classifier
frameworks.validation.platform-automation.rails
"""

reposToUpdateList = reposToUpdate.split()
print(reposToUpdateList)


# Step 1: Read the YAML file
path = r"C:\workspace\inventory\organizations\intel-innersource\repos\frameworks\validation\platform-automation\repos.yml"
path2 = r"C:\workspace\inventory\organizations\intel-innersource\repos\frameworks\validation\platform-automation\repos2.yml"
with open(path, 'r') as file:
    repos_data = file.readlines()
repos = []
for index,i in enumerate(repos_data):
    if i.startswith("name:"):
        repo =i.split(":")[1].strip()
        repos.append(repo)
        if repo in reposToUpdateList:
            for i in range(index, index+30):
                if i >= len(repos_data):
                    break
                line = repos_data[i].strip()
                if line.startswith("webhooks:"):
                    hooks = repos_data[i].split(":")[1].strip()
                    print(f"{repo} - {hooks}")
                    repos_data[i] = repos_data[i].replace("base-webhooks", "greenfield-webhooks")
                    hooks = repos_data[i].split(":")[1].strip()
                    print(f"{repo} - {hooks}\n")
                    break

print(repos_data)



with open(path2, "w") as file:
    file.writelines(repos_data)
