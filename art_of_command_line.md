## 基础
+ 学习bash基础，man bash至少全文浏览一遍。其他的shell可能也很好用，但是Bash功能足够强大并且几乎总是可用的。像zsh、fish等其他shell可以在自己设备上玩玩不要过度依赖。
+ 熟悉至少一个基于文本的编辑器。vim（vi）是一个很好的选择。大部分情况下vim比emacs，大型IDE更好用。
+ 使用 man命令阅读文档，学会使用 apropos查找文档。有些命令并没有对应的可执行文件，而是在bash内置好的，可以使用 help 和 hell -d 命令获取帮助信息。 用 type命令 来判断这个命令到底是可执行文件、shell内置命令还是别名。
+ 学会使用 > 和 < 重定向输出和输入，使用 | 重定向管道。明白 > 会覆盖输出文件，>>是在文件末尾追加。了解标准输出 stdout和标准错误 stderr。
+ 学会使用 Bash中的任务管理工具：&，ctrl-z，ctrl-c，jobs，fg，bg，kill等。
+ 学会使用 ssh 进行远程命令行登录，最好知道如何使用 ssh-agent，ssh-add 等命令来实现基础的无密码认证登录。
+ 学会基本的文件管理工具：ls 和 ls -l （了解 ls -l 中每一列代表的意义），less，head，tail 和 tail -f （甚至 less +F），ln 和 ln -s （了解硬链接与软链接的区别），chown，chmod，du （硬盘使用情况概述：du -hs *）。 关于文件系统的管理，学习 df，mount，fdisk，mkfs，lsblk。知道 inode 是什么（与 ls -i 和 df -i 等命令相关）。
+ 学习基本的网络管理工具：ip 或 ipconfig，dig。
+ 学习并使用一种版本控制管理系统，如 git。
+ 熟悉正则表达式，学会使用 grep／egrep，它们的参数中 -i，-o，-v，-A，-B 和 -C 这些是很常用并值得认真学习的。
+ 学会使用 apt-get，yum，dnf 或 pacman （具体使用哪个取决于你使用的 Linux 发行版）来查找和安装软件包。并确保你的环境中有 pip 来安装基于 Python 的命令行工具 （接下来提到的部分程序使用 pip 来安装会很方便）。

## 日常使用
+ 在 Bash 中，可以通过按 Tab 键实现自动补全参数，使用 ctrl-r 搜索命令行历史记录（按下按键之后，输入关键字便可以搜索，重复按下 ctrl-r 会向后查找匹配项，按下 Enter 键会执行当前匹配的命令，而按下右方向键会将匹配项放入当前行中，不会直接执行，以便做出修改）。
+ 在 Bash 中，可以按下 ctrl-w 删除你键入的最后一个单词，ctrl-u 可以删除行内光标所在位置之前的内容，alt-b 和 alt-f 可以以单词为单位移动光标，ctrl-a 可以将光标移至行首，ctrl-e 可以将光标移至行尾，ctrl-k 可以删除光标至行尾的所有内容，ctrl-l 可以清屏。键入 man readline 可以查看 Bash 中的默认快捷键。内容有很多，例如 alt-. 循环地移向前一个参数，而 alt-* 可以展开通配符。
+ 执行 set -o vi 来使用 vi 风格的快捷键，而执行 set -o emacs 可以把它改回来。
+ 为了便于编辑长命令，在设置你的默认编辑器后（例如 export EDITOR=vim），ctrl-x ctrl-e 会打开一个编辑器来编辑当前输入的命令。在 vi 风格下快捷键则是 escape-v。
+ 键入 history 查看命令行历史记录，再用 !n（n 是命令编号）就可以再次执行。其中有许多缩写，最有用的大概就是 !$， 它用于指代上次键入的参数，而 !! 可以指代上次键入的命令了（参考 man 页面中的“HISTORY EXPANSION”）。不过这些功能，你也可以通过快捷键 ctrl-r 和 alt-. 来实现。
+ 如果输入命令的时候中途改了主意，按下 alt-# 在行首添加 # 把它当做注释再按下回车执行（或者依次按下 ctrl-a， #， enter）。这样做的话，之后借助命令行历史记录，你可以很方便恢复你刚才输入到一半的命令。
+ 使用 xargs （ 或 parallel）。他们非常给力。注意到你可以控制每行参数个数（-L）和最大并行数（-P）。如果不确定它们是否会按你想的那样工作，先使用 xargs echo 查看一下。此外，使用 -I{} 会很方便。
+ pstree -p 以一种优雅的方式展示进程树
+ 使用 pgrep 和 pkill 根据名字查找进程或发送信号（-f 参数通常有用）。
+ 了解你可以发往进程的信号的种类。比如，使用 kill -STOP [pid] 停止一个进程。使用 man 7 signal 查看详细列表。
+ 使用 nohup 或 disown 使一个后台进程持续运行。
+ 使用 netstat -lntp 或 ss -plat 检查哪些进程在监听端口（默认是检查 TCP 端口; 添加参数 -u 则检查 UDP 端口）或者 lsof -iTCP -sTCP:LISTEN -P -n (这也可以在 OS X 上运行)。
+ lsof 来查看开启的套接字和文件。
+ 使用 uptime 或 w 来查看系统已经运行多长时间。
+ 可以把别名、shell 选项和常用函数保存在 ~/.bashrc，这样做的话你就可以在所有 shell 会话中使用你的设定。
+ 把环境变量的设定以及登陆时要执行的命令保存在 ~/.bash_profile。而对于从图形界面启动的 shell 和 cron 启动的 shell，则需要单独配置文件。
+ 要想在几台电脑中同步你的配置文件（例如 .bashrc 和 .bash_profile），可以借助 Git。
+ 通过使用 <(some command) 可以将输出视为文件。例如，对比本地文件 /etc/hosts 和一个远程文件：
+ 
  
