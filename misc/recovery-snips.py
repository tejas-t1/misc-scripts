from recovery_lib.client.trigger import recovery_flow as recoveryApi
from rails.cases.test.RecoveryPolicy import RecoveryPolicy
from rails.cases.recovery.RecoveryTwoDotZero import RecoveryTwoDotZero

policy = RecoveryPolicy()
policy.Policy.NetworkReset = "Not Allowed"
policy.Policy.ResetButton = "Not Allowed"
d = policy.getDict()
RecoveryTwoDotZero.setToolcaseServiceAttribute("basrradlsi003.gar.corp.intel.com", "BASMECHBOX0254", "recovery", d)


recoveryArgs = {
    "controller": "basrradlsi003.gar.corp.intel.com",
    "sut": "PTL-QAC-PM",
    "system_ip": "10.223.215.6",
    "ttk_id": None,
    "ap_name": None,
    "ap_pwd": None,
    "tws_version": "4.x",
    "platform_config": None,
}
# Log.info(f"Recovery Args: {recoveryArgs}")
# with BackgroundVideoCapture() as videoCapture:
recoveryApi.callback(**recoveryArgs)