import os

infos = [
    {
        'sno': os.getenv('USER_SNO'),
        'pwd': os.getenv('USER_PWD'),
        'devName': ['103-90', '103-80', '103-70', '103-89', '103-79'],  # 多个预约位置
        'name': os.getenv('USER_NAME'),
        'periods': (
            ('9:30:00', '13:30:00'),
            ('14:30:00', '18:00:00'),
            ('18:30:00', '22:00:00')
        ),
        'pushplus': os.getenv('USER_PUSHPLUS')
    }
]
