# JLU-daily-attendance

__Hi！本项目是专门用于JLU每日健康打卡的自动脚本，适用于所有JLU postgraduate students__

[这个是隔壁大佬编写的for undergraduate students version](https://github.com/TechCiel/jlu-health-reporter)

### 使用注意事项
 1. 本脚本程序基于python3.7及以上环境使用，并没进行向后兼容的准备，但是欢迎各位提供issue,根据情况可能进行后续维护工作
 2. 本脚本实际操作是每20分钟进行一次打卡操作，若非部署在服务器上使用，请注意使用的时间，如果距离打卡结束不足20分钟，建议修改main.py装饰器里的minute参数，或者直接运行do_attendance.py
 3. 基于2条，可以自行修改打卡提交间隔时间，但建议不要小于2分钟，否则被封ip后果自负，此外注意当前脚本是在开始运行后x分钟才执行的打卡操作(这个可能以后会修改）
 
### 使用方式
 1. 下载脚本
 ```
 git clone https://github.com/genres17/JLU-daily-attendance.git
 cd daily attemdamce 
 ```
 2. 填写个人信息
 ```
 vim config.py
 ```
 然后按照里面注释填写即可，注意下面的校区等信息不要乱改，否则执行出错后果自负，除非你知道自己在做什么
 3. 执行程序
 ```
 python3 main.py 
 ```
 ### 免责声明
 本自动程序为个人使用开发，适用于吉林大学疫情期间研究生健康打卡的自动提交，未经充分测试，不保证正常工作，不建议没有调试能力的人使用。

__本程序以你所见到的样子呈现给你，不附带任何明示或暗示的担保，包括但不限于对功能合法性或对特定用途适用性的保证。在运行之前，你有责任理解其源代码的工作原理，并确认这是你想要执行的，本程序进行的操作都应被视为你本人进行、或由你授权代你进行的操作。在任何情况下，本程序作者与你决定运行本程序无关，不为你运行此程序所造成的任何损失、受到的处罚以及造成的法律后果等负任何责任。__

### 鸣谢
感谢以下两位大佬的帮助：

[@TechCiel](https://github.com/TechCiel)

[@DDavid](https://github.com/zjdavid)
