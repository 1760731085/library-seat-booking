# 简介

实现广州大学图书馆的座位自动预约、自动签到, 让你不再烦恼总是挑不到座位或者忘记签到。该项目可实现**多个用户**同时预约、签到，只需要在 `info.py` 填上多个用户信息即可。

<br/>

# 项目结构

~~~shell
├── README.md
├── json             # 保存每个房间和座位的信息
│   ├── 101.json
│   ├── 202.json
│   ├── 203.json
│   ├── 204.json
│   ├── 205.json
│   ├── ........
├── libs
│   ├── __init__.py
│   ├── info.py      # 保存个人信息
│   ├── rsa.py       # RSA 加密算法的实现
│   └── source.py    # 核心代码
├── requirements.txt # 依赖项
├── reserve.py       # 预约
└── sign.py          # 签到
~~~

<br/>

# 运行

下面的教程部署在服务器或云函数, 如需用 Github Action 部署, 请查看

1. 克隆或者下载代码

2. 安装依赖

   ~~~shell
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ~~~

3. 修改 `libs\info.py`文件，填上自己的学号、密码以及要预约的座位号

4. 运行 `reserve.py`即可预约，运行 `sign.py`可签到

   ~~~shell
   python reserve.py
   ~~~

   ~~~shell
   python sign.py
   ~~~

<br/>

# 待实现

- [ ] 一楼研讨间的预约和签到
- [ ] 五楼研讨间的预约和签到
- [x] 能自动签到对应预约的座位
- [ ] 摈弃 json 文件, 座位 ID 根据请求查询
- [x] 用户可自定义预约时间
- [ ] 处理教务系统要求改密码问题

<br/>

# 部署

> 为了实现自动预约 + 自动签到, 需要每天定时执行预约和签到脚本。可以部署到**自己的电脑**、**服务器**、**云函数**、**GitHub Actions**。(若要部署到自己的电脑, 则需要一直开机)

* `reserve.py`预约脚本可于每天早上 6:15:40 执行, 因为系统每天 6:15 开放预约
* `sign.py`签到脚本可于预约时间的1分钟后执行, 比如预约 8:30~12:30, 可 8:31 执行签到

<br/>

1. 部署到 Windows 的可以使用计划任务定时执行脚本 (自行百度)

2. 部署到 Ubuntu/CentOS 服务器的可以使用 `crontab` 定时执行脚本 (自行百度)

3. **推荐部署到云函数(腾讯云函数、阿里云函数都行), 因为它们有免费额度, 相当于白嫖**
   这里以阿里云函数为例

   1. 打开[阿里云官网](https://www.aliyun.com/), 注册阿里云账号

   2. 打开[函数计算页面](https://www.aliyun.com/product/fc)

      ![image-20230514115141532](https://img-blog.csdnimg.cn/0e99a68cb9294e0c9185887bb7e8839b.png)

   3. 点管理控制台

   4. 选择服务及函数，再点击创建服务，随便给个名字，例如我取名叫 `Library`
      ![image](https://github.com/ChaXxl/GZHU_LibraryAutoReserve_sign/assets/40326898/31bc937b-8f67-4579-b6ae-bb280fb77f1b)

   5. 创建`两个函数`，分别用于预约和签到。

      * 创建函数的方式：使用内置运行时创建
      * 函数名称：可以叫做 `Reserve` 和 `Sign`，随意
      * 请求处理程序类型：处理 HTTP 请求
      * 运行环境：Python 3.8 以上就行
      * 代码上传方式：可以选择通过文件夹 或 zip 包上传代码，反正上传代码就行
      * 执行超时时间：160 以上
      * 请求处理程序： 分别是`reserve.main`、`sign.main`(即执行 rserve.py 里的 main 函数和 sign.py 里的 main 函数)
      * 其余参数默认即可

      ![image-20231105092652349](https://img-blog.csdnimg.cn/36185a99601a47da818013f2b442aa53.png)

      

      ![image-20231105094104565](https://img-blog.csdnimg.cn/862e394da20b498fa9c023ba0ec917d3.png)

      <br/>

      两个函数示例：
      ![image](https://github.com/ChaXxl/GZHU_LibraryAutoReserve_sign/assets/40326898/59721804-99dc-4631-997b-f5b72457cfb4)

   6. 点击打开终端，输入以下命令安装依赖项

      * `-t .`: 表示将依赖安装置该目录下
      * `-r `: 指定对应的 requirements.txt 文件, 去安装这个文件里面的包     

      ~~~shell
      pip install -t . -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
      ~~~

      ![image](https://github.com/ChaXxl/GZHU_LibraryAutoReserve_sign/assets/40326898/dba1416d-9504-44ad-8b87-96b457b27e3f)

   7. 配置触发器

      * 触发器类型：选择异步调用

      * 触发器名称：随便起个

      * 预约函数的触发方式可以选我这个，我这个是每天 6:15:20 触发的意思

        ~~~shell
        CRON_TZ=Asia/Shanghai 20 15 6 * * *
        ~~~

        ![image](https://github.com/ChaXxl/GZHU_LibraryAutoReserve_sign/assets/40326898/7894b695-0eb0-4f90-8400-0cbed5ff23dd)

      * 签到函数的触发方式，我这个是每天的 8:21、8:31、8:35、8:55、12:31、13:55、16:31、20:31... 触发，弄这么多个触发点是为了以防万一签到失败，多来几次

        ~~~shell
        CRON_TZ=Asia/Shanghai 0 21,30,35,55 8,12,13,16,20 * * *
        ~~~

   8. 代码上传后记得点击部署，也可以点一下测试函数看看能不能正常运行，只要有输出就说明正常，`不用管它的报错`

      ![image](https://github.com/ChaXxl/GZHU_LibraryAutoReserve_sign/assets/40326898/1ffc4d34-9691-4291-bc6d-e813bcdb1581)


​      
​      
​      




​      

<br/>

<br/>

# 运行示例

* 预约成功示例

  <img src="https://img-blog.csdnimg.cn/00cf03bd51f1410eaeca5022f315f598.png" alt="image-20230514112415314" style="zoom:67%;" />



* 签到成功示例

  <img src="https://img-blog.csdnimg.cn/6ee31a0dd74941eeaa197474df1aee73.png" alt="image-20230514113116310" style="zoom:67%;" />



# 部署到github action

### 1. 项目结构准备

首先，确保你的项目结构清晰，包含所有必须的文件，例如：

```
.
├── .github
│   └── workflows
│       └── book_seat.yml  # GitHub Actions 的工作流文件
├── libs
│   ├── info.py  # 用户信息
│   └── source.py  # 业务逻辑
├── reserve.py  # 预约脚本
├── sign.py  # 签到脚本
└── requirements.txt  # Python 依赖
```

### 2. 创建 GitHub Actions 工作流文件

在 `.github/workflows/` 目录下创建一个名为 `book_seat.yml` 的文件，定义 GitHub Actions 工作流，通过 `env` 关键字设置环境变量，将 GitHub Secrets 的值传递给你的脚本。

#### 示例 `book_seat.yml`：

```yaml
name: Book and Sign Seats

on:
  # 可自定义，运行签到脚本的时间要与info.py中的内容匹配
  schedule:
    # 每天的 6:15 运行预约脚本
    - cron: '15 6 * * *'
    # 每天的 8:21、8:31、8:35、8:55、12:31、13:55、16:31、20:31运行签到脚本
    - cron: '21,31,35,55 8,12,13,16,20 * * *'
  workflow_dispatch:

jobs:
  reserve:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python 3.8
        uses: actions/setup-python@v4
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Reserve Script
        env:
          USER_NAME: ${{ secrets.USER_NAME }}
          USER_SNO: ${{ secrets.USER_SNO }}
          USER_PWD: ${{ secrets.USER_PWD }}
          USER_DEVNAME: ${{ secrets.USER_DEVNAME }}
          USER_PUSHPLUS: ${{ secrets.USER_PUSHPLUS }}
        run: |
          python reserve.py

  sign:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python 3.8
        uses: actions/setup-python@v4
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Sign Script
        env:
          USER_NAME: ${{ secrets.USER_NAME }}
          USER_SNO: ${{ secrets.USER_SNO }}
          USER_PWD: ${{ secrets.USER_PWD }}
          USER_DEVNAME: ${{ secrets.USER_DEVNAME }}
          USER_PUSHPLUS: ${{ secrets.USER_PUSHPLUS }}
        run: |
          python sign.py
```

#### 解释：

- ```
  on.schedule.cron
  ```

  ：定义了定时触发规则，使用 Cron 表达式。比如：

  - `15 6 * * *` 表示每天 6:15 触发一次预约任务。
  - `21,31,35,55 8,12,13,16,20 * * *` 表示每天在指定的时间点多次触发签到任务。

- `workflow_dispatch`：允许你手动触发工作流（比如调试时可以通过 GitHub 前端手动执行）。

- 两个 Job

  ：我们定义了两个独立的 Job，分别用于运行预约（

  ```
  reserve.py
  ```

  ）和签到（

  ```
  sign.py
  ```

  ）脚本。

  - **Job 1 - `reserve`**：通过定时触发预约脚本 `reserve.py`。
  - **Job 2 - `sign`**：通过定时触发签到脚本 `sign.py`。

- 每个 Job 都包括以下步骤：

  1. **Checkout 代码**：使用 `actions/checkout@v3` 拉取你的 GitHub 仓库代码。
  2. **设置 Python 环境**：使用 `actions/setup-python@v4` 设置 Python 3.8 环境。
  3. **安装依赖**：通过 `pip install -r requirements.txt` 安装 Python 项目的依赖。
  4. **运行脚本**：执行 `python reserve.py` 或 `python sign.py` 来运行预约或签到脚本。

### 3. 配置用户信息

为了将敏感信息（如学号、密码等）从代码中移除，并且在 GitHub Actions 中使用 **GitHub Secrets** 来存储这些敏感数据，建议修改 `libs/info.py` 文件，使用环境变量（`os.getenv()`）来动态获取这些信息。这种做法可以保护你的隐私，并且在不同的环境中灵活配置数据。

#### 示例 `info.py`：

可以通过 `os.getenv()` 从环境变量中获取学号、密码、座位号等信息，而不需要将这些信息直接写入代码中。

```python
import os

infos = [
    {
        'sno': os.getenv('USER_SNO'),         # 从环境变量获取学号
        'pwd': os.getenv('USER_PWD'),         # 从环境变量获取密码
        'devName': os.getenv('USER_DEVNAME'), # 从环境变量获取预约的座位号
        'name': os.getenv('USER_NAME'),       # 从环境变量获取用户名
        'periods': (
            # 自己修改成自己想要的时段
            ('9:30:00', '13:30:00'),
            ('14:30:00', '18:00:00'),
            ('18:30:00', '22:00:00')
        ),
        'pushplus': os.getenv('USER_PUSHPLUS')  # 从环境变量获取 pushplus 的 token（用于推送消息到微信，可为空）
    }
]
```



### 4. **推送代码到 GitHub**

现在，你可以将项目推送到 GitHub 仓库。

```bash
# 进入你的项目目录
cd path/to/your/project  
# 初始化本地 Git 仓库：
git init
# 添加所有项目文件到 Git 仓库：
git add .
# 提交这些文件：
git commit -m "Initial commit"
# 在终端中，将本地仓库与 GitHub 仓库关联：
git remote add origin https://github.com/your-username/library-seat-booking.git
# 推送本地代码到 GitHub 仓库：
git push -u origin master
```

### 5. 在 GitHub 中配置 Secrets（环境变量

为了让 GitHub Actions 获取这些敏感信息，你需要将这些信息存储在 GitHub 仓库的 **Secrets** 中：

1. 打开你的 GitHub 仓库，进入对应的项目页面。
2. 依次点击 **Settings** → **Secrets and variables** → **Actions** → **New repository secret**。
3. 你需要为每个用户的信息创建相应的 Secrets。例如：
   - `USER_NAME`: 你的名字。
   - `USER_SNO`: 你的学号。
   - `USER_PWD`: 你的密码。
   - `USER_DEVNAME`: 预约的座位号。
   - `USER_PUSHPLUS`: PushPlus 的 Token，如果不需要推送功能可以留空。



### 6. **查看 GitHub Actions 执行结果**

推送代码后，GitHub Actions 会根据你设置的定时任务自动触发工作流。你可以通过以下步骤查看执行情况：

1. 打开你的 GitHub 仓库。
2. 点击 **Actions** 标签页。
3. 你会看到已执行的工作流，点击任意一个工作流可以查看详细的日志输出和执行结果。

### 7. **手动触发工作流**

如果你想手动触发工作流进行调试，执行以下步骤：

1. 打开你的 GitHub 仓库。
2. 点击 **Actions** 标签页。
3. 找到你定义的工作流（例如 `Book and Sign Seats`），并点击它。
4. 点击右上角的 **Run workflow** 按钮，选择手动运行工作流。

### 总结

通过 GitHub Actions 的定时触发功能，你可以轻松实现自动化的预约和签到任务，类似于阿里云函数的定时触发器。GitHub Actions 的优势在于它与代码库紧密集成，易于调试和维护，无需额外的服务器或云服务配置。

希望这个方案能够帮助你实现图书馆座位的自动预约和签到任务！
