"""
预约
"""
from libs.info import infos
from libs.source import ZWYT
import time
import httpx  # 导入 httpx 模块


def main(*args, **kwargs):
    for stu in infos:
        for devName in stu['devName']:
            max_retries = 3  # 最大重试次数
            retry_count = 0

            while retry_count < max_retries:
                try:
                    yy = ZWYT(stu['name'], stu['sno'], stu['pwd'], stu['periods'], stu['pushplus'])
                    yy.reserve(devName)
                    time.sleep(2)
                    break  # 成功则退出重试循环

                except httpx.TimeoutException as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        print(f"座位 {devName} 预约超时，已重试{max_retries}次")
                    else:
                        print(f"座位 {devName} 预约超时，正在进行第{retry_count}次重试")
                    time.sleep(5)  # 重试前等待5秒
                    continue

                except Exception as e:
                    print(e)
                    if stu['pushplus']:
                        yy.pushplus(f"{stu['name']} {devName} 预约失败", e)
                    break  # 非超时异常直接退出重试


if __name__ == '__main__':
    main()
