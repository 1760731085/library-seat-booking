from libs.info import infos
from libs.source import ZWYT
import time
import httpx


def process_reservation(yy, devName):
    """
    处理单个座位的预约逻辑
    """
    try:
        yy.reserve(devName)
        time.sleep(3)  # 增加5秒的延时，避免并发过多导致超时
    except httpx.TimeoutException:
        print(f"座位 {devName} 预约超时，不推送消息。")
    except Exception as e:
        print(e)
        if yy.pushplus_token:
            yy.pushplus(f"{yy.name} {devName} 预约失败", str(e))


def main(*args, **kwargs):
    # 遍历 info 信息，获取每个学生的昵称、预约座位号、用户名、密码、时间段、推送token（推送可以为空）
    for stu in infos:
        # 初始化预约对象
        yy = ZWYT(stu['name'], stu['sno'], stu['pwd'], stu['periods'], stu['pushplus'])

        # 遍历多个预约座位
        for devName in stu['devName']:
            process_reservation(yy, devName)  # 处理单个座位预约


if __name__ == '__main__':
    main()
