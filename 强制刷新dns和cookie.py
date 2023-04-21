import subprocess
from getpass import getpass

# 清除 Chrome 缓存
subprocess.call(['defaults', 'write', 'com.google.Chrome', 'DisableCaches', '-bool', 'true'])

# 刷新 DNS（需要管理员密码）
mac_version = subprocess.check_output(["sw_vers", "-productVersion"]).decode("utf-8")
if mac_version.startswith('10.14'):
    # macOS Mojave 或更早版本的方法：
    sudo_password = getpass("请输入管理员密码：")
    subprocess.call('echo %s | sudo -S dscacheutil -flushcache' % sudo_password, shell=True)
else:
    # macOS Catalina 以及之后版本的方法：
    sudo_password = getpass("请输入管理员密码：")
    subprocess.call('echo %s | sudo -S killall -HUP mDNSResponder' % sudo_password, shell=True)
