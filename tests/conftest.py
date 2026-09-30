import platform

def mock_uname():
    return platform.uname_result('Windows', 'localhost', '10', '10.0.19041', 'AMD64', 'AMD64')

platform.uname = mock_uname
platform.machine = lambda: 'AMD64'
platform._get_machine_win32 = lambda: 'AMD64'
platform._wmi_query = lambda query: []