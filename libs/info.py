import os

infos = [
    {
        'sno': os.getenv('USER_SNO'),         # 从环境变量获取学号
        'pwd': os.getenv('USER_PWD'),         # 从环境变量获取密码
        'devName': os.getenv('USER_DEVNAME'), # 从环境变量获取预约的座位号
        'name': os.getenv('USER_NAME'),       # 从环境变量获取用户名
        'periods': (
            ('9:30:00', '13:30:00'),
            ('14:30:00', '18:00:00'),
            ('18:30:00', '22:00:00')
        ),
        'pushplus': os.getenv('USER_PUSHPLUS')  # 从环境变量获取 pushplus 的 token（用于推送消息到微信，可为空）
    }
]