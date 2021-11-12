简单的 RPS 模拟工作流程
===================

运行 [`./new.sh`](./new.sh) 就可以迅速交互式进行实验。

```bash
# NOTICE: Change to what you like!
EDITOR=vim
FILE_MANAGER=xdg-open
```

运行 `./new.sh` 将会在 `data` 目录下新建一个目录，并打开其中的 `config.json` 进行编辑。编辑完之后执行模拟和绘图的命令，执行完之后会自动打开目录用于预览。

-----

目录下文件的简要介绍：

```bash
.
├── data/       # 数据目录
├── template/   # 示例配置文件
├── plot/       # 绘图用脚本
├── manual_scripts/   # 手动运行的脚本
├── ... 
├── new.sh      # 入口脚本
├── main.py     # 计算脚本
├── plot.py     # 绘图脚本
├── ...
├── util.py     # 公用函数
└── README.md   # 本文件
```

