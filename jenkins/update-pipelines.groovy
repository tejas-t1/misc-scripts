import hudson.model.*


disableChildren(Hudson.instance.items)
def disableChildren(items) {
def pipelines = [
    "suite-definition-pr",
    "suite-definition-release",
    "enact-service-pr",
    "enact-service-release",
    "packaging-service-pr",
    "packaging-service-release",
    "three-d-mark-pr",
    "three-d-mark-release",
    "command-wrapper-pr",
    "command-wrapper-release",
    "autostress-pr",
    "autostress-release",
    "display-automation-pr",
    "display-automation-release",
    "zoom-automation-pr",
    "zoom-automation-release",
    "meshcommander-automation-pr",
    "meshcommander-automation-release",
    "connectivity-tools-automation-pr",
    "connectivity-tools-automation-release",
    "audacity-automation-pr",
    "audacity-automation-release",
    "storage-automation-pr",
    "storage-automation-release",
    "thermal-tools-automation-pr",
    "thermal-tools-automation-release",
    "manageability-tools-automation-pr",
    "manageability-tools-automation-release",
    "debug-tools-automation-pr",
    "debug-tools-automation-release",
    "overclocking-tools-automation-pr",
    "overclocking-tools-automation-release",
    "selenium-automation-pr",
    "selenium-automation-release",
    "automation-architecture",
    "cloud-client-automation-pr",
    "cloud-client-automation-release",
    "google-meet-automation-pr",
    "google-meet-automation-release"
]
  for (item in items) {
    if (item.class.canonicalName == 'com.cloudbees.hudson.plugins.folder.Folder') {
        disableChildren(((com.cloudbees.hudson.plugins.folder.Folder) item).getItems())
    } else {
        if(pipelines.contains(item.name)){
          item.disabled=true
          item.save()
          print('\n')
          println(item.name)
         }
    }
  }
}