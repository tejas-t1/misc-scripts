missing = ['usbdll@1.1', 'windowsdevicesensors@1.0.0.17', 'sensorinfo@2.0.0.0', 'autohotkey@1.1.26.01', 'usbtreeviewer@3.3.7', 'subinacl@5.2.3790.1180', 'dpcdtool@1.0', 'FTDIWrapper@1.0', 'mdavt@2022.04.01.0', 'chromeinstaller@84.0.4147.135', 'waksource_prod@1888.0', 'sensorviewer@2.93.0.0', 'WoVApp@3.1.0.11', 'exiftool@12.12', 'curl@7.28.1', 'pnrtool@2.69.0.0', 'gpiotsttool@2.0.0', 'cvfLoader@1.0.0', 'UnitTestIVSC@1.0.0.12', 'iasl@1.0.0.13', 'cnviwol@1.1', 'IVSC_malformed_files@1.1.0.11', 'pythonEFIRemote@3.3', 'querypresence@1.0.0.3', 'cmake@3.21.2-patch1', 'cstsampleapp@1.1.6000.10', 'onebox-software@3.0.0', 'teraterm@4.106', 'spiflashdnx@1.0', 'IVSCTest@1.0.0.0', 'tcm_tqc@23.2', 'python3@3.7.4', 'DriverLogCapture@1.0.0.5', 'hclient@1.0', 'multitouch@1.0.1', 'windows-10-hyper-v@1.0.0.0', 'bdcamsetup@6.0.4', 'presentmon@1.1', 'steamcmd@1.2', 'DevIntf@0.02', 'winobj@3.10.0.1', 'asl@0.01', 'ecSimulator@1.7.2', 'digiinfo@1.0', 'setacl@3.1.2.86', 'hidwovledetw@1.0', 'hidvalidator@1.0', 'mvahelper@1.0.55.0', 'strings@2.53', 'pgtool@2.0.0.7', 'RailsRecoverSutWifi@1.0.0', 'burninnew@10.2.1001.20220828', 'pmemUtil@0.1', 'sealtest@1.0', 'tracedecoder@1.0', 'autologger@1.0', 'GNA_Activity_Monitor_Tool@1.0', 'rh_rt_demo_app@1.0.0.749', 'tuningwizardclientfiles@1.0', 'dttpageinfo@1.0', 'putty.install@0.77', 'couchDB@3.1.1.1', 'wovledApplication@1.0.2', 'EnableDisableCETForAllApps@1.0.1', 'tdt-eng@6.12.0.0-pop-up-fix', 'firmwarewacom@1.0.1', 'coreinfo@3.52', 'windows11-level2-vm@1.0.0.7', 'pycst-backend@1.0.3', 'cetperf@1.0.1', 'hgsplusworkload@1.9', 'linpacktestwindows@1.1', 'emulatorvalidationtools@1.0.2', 'woshwctrsinstall1@2.0.1', 'onnx@1.0.2', 'classxapps@1.0.6', 'threadpriority@1.1.0', 'meshcmd@0.9.5.2', 'pauseapplicationwindows@1.0.3', 'telephonytool@1.0.0', 'battlenetlauncher@1.0.1', 'mbnsms@1.0.1', 'icbuild@0.1.0.257', 'ds_expanse@1.2', 'crystaldiskinfo@8.17.4', 'opencv@4.6.0-patch3', 'vpuSampleImages@1.1', 'visual2019StudioCommunity@16.11.19.0', 'dttcVsctData@1.0', 'ddt@9.0.10702.25133', 'ddtui@9.0.10702.25133', 'ipfui@1.0.10702.25133', 'ipf@1.0.10702.25133', 'endurancegaming@0.9.15.0', 'backgroundimagesample@1.0.0', 'CnviModemTool@1.0', 'nodejsfilesforamteventfilter@1.0.0', 'nodejs@18.12.1', 'solar3@3.22.440.0', 'threeDMark@1.0.7', 'crystaldiskspd@8.0.4', 'CnviAirplaneRfTool@1.0', 'CnviLocApp@2.0', 'emaserver@1.12.2', 'rmcpping@1.0.0', 'winthrax@3.4.5.0', 'isd@2238.0.0', 'steam-offline@1.0', 'geforce-game-ready-driver-win10@531.41', 'sigcheck@2.90', 'video_samples@1.0.1', 'Alexa@1.0.0.0-patch', 'cnviWakeServer@1.0', 'WakeOnPatternClient@2.1.0.1', 'ThreadSpawning@1.0.1-patch', 'poolmon@10.0.22621.1', 'wallpapers@1.0.0', 'pingtesttool@1.1.0.0', 'Tesseract-OCR@5.3.3', 'CnviAutomation@3.2', 'RWLicense@1.0', 'DisplayInfo@1.0', 'DGReadinessTool@3.6', 'powermeter@1.0.0005.902', 'zoom@6.16.11.43767', 'yamnic@1.0', 'notmyfault@4.20', 'googlechromedev@120.0.6062.2', 'Googlechromeonline@119.0.6045.106', 'DisplayMultiMonitorTool@120.0.6062.2', 'obs-studio@29.1.3', 'RealtekCardReaderDriver@1.0.0', 'Movies-And-Tv@22091.10061.0', 'openvino-test@2.0', 'iometerx@1.1.1', 'RTSS@7.3.5.0', 'visionTest@3.2.6.705', 'WIMAGER@6.7.2.0']
# print(len(missing))

# exit()
import requests

source_artifactory_url = "https://ubit-artifactory-ba.intel.com/artifactory"
destination_artifactory_url = "https://ubit-artifactory-or.intel.com/artifactory"
source_artifactory_repo = destination_artifactory_repo = 'occ-nuget-local'

for i in missing:
    source_package_name, source_package_version= i.split('@')
    response = requests.post(
            "https://cje-fm-owrp-prod02.devtools.intel.com/ccg-cpe-cicd/job/sync-artifacts-between-ba-and-or/buildWithParameters",
            data={
                "source_artifactory": source_artifactory_url,
                "destination_artifactory": destination_artifactory_url,
                "source_artifactory_repo": source_artifactory_repo,
                "destination_artifactory_repo": destination_artifactory_repo,
                "source_package_name": source_package_name,
                "source_package_version": source_package_version,
            },
            auth=('sys_adoadd', "<TOKEN"),
        )
    response.raise_for_status()