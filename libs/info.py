import os

infos = [
    {
        'sno': os.getenv('USER_SNO'),
        'pwd': os.getenv('USER_PWD'),
        'devName': ['103-090', '103-080', '103-089', '103-079'],  # 多个预约位置
        'name': os.getenv('USER_NAME'),
        'periods': (
            ('9:30:00', '13:30:00'),
            ('14:30:00', '18:00:00'),
            ('18:30:00', '22:00:00')
        ),
        'pushplus': os.getenv('USER_PUSHPLUS')
    }
]
