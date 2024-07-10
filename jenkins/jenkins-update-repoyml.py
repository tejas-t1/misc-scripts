import yaml

reposToUpdate = """
frameworks.validation.platform-automation.suite-definition
frameworks.validation.platform-automation.enact-service
frameworks.validation.platform-automation.packaging-service
frameworks.validation.platform-automation.three-d-mark
frameworks.validation.platform-automation.command-wrapper
frameworks.validation.platform-automation.autostress
frameworks.validation.platform-automation.teams-automation
frameworks.validation.platform-automation.youtube-automation
frameworks.validation.platform-automation.display-automation
frameworks.validation.platform-automation.zoom-automation
frameworks.validation.platform-automation.meshcommander-automation
frameworks.validation.platform-automation.connectivity-tools-automation
frameworks.validation.platform-automation.audacity-automation
frameworks.validation.platform-automation.storage-automation
frameworks.validation.platform-automation.thermal-tools-automation
frameworks.validation.platform-automation.manageability-tools-automation
frameworks.validation.platform-automation.debug-tools-automation
frameworks.validation.platform-automation.overclocking-tools-automation
frameworks.validation.platform-automation.selenium-automation
frameworks.validation.platform-automation.automation-architecture
frameworks.validation.platform-automation.cloud-client-automation
frameworks.validation.platform-automation.rails-shared
frameworks.validation.platform-automation.google-meet-automation
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
