"""
预约
"""
from libs.info import infos
from libs.source import ZWYT
import time
import httpx  # 导入 httpx 模块


def main(*args, **kwargs):
    # 遍历 info 信息，获取每个用户的昵称、预约座位号、用户名、密码、时间段、推送token（推送可以为空）
    for stu in infos:
        for devName in stu['devName']:  # 遍历多个预约位置
            try:
                # 初始化类示例，传入昵称、用户名、密码、时间段、推送token（推送可以为空）
                yy = ZWYT(stu['name'], stu['sno'], stu['pwd'], stu['periods'], stu['pushplus'])

                # 调用预约函数预约，传入预约座位号
                yy.reserve(devName)

                time.sleep(2)  # 增加2秒的延时，避免并发过多导致超时
            except httpx.TimeoutException as e:
                print(f"座位 {devName} 预约超时，不推送消息。")
                continue

            except Exception as e:
                print(e)
                if stu['pushplus']:
                    yy.pushplus(f"{stu['name']} {devName} 预约失败", e)  # 只有非超时异常才推送
                continue


if __name__ == '__main__':
    main()
