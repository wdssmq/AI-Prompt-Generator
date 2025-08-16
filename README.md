# AI 提示词生成器

一个基于 YAML 配置的 AI 提示词生成工具，支持变量替换和随机选择功能。

## 功能特性

- 📝 YAML 配置文件定义提示词模板
- 🔄 变量替换功能 `{{variable}}`
- 💾 缓存变量功能 `{{$variable}}`
- 🎲 随机选择功能 `{{rnd(选项1,选项2,)}}`
- 🔀 条件判断功能 `{{if(条件):内容:}}`
- 🐍 Python 版本
- 🌐 JavaScript 版本（预定）

## YAML 配置格式

```yaml
- items:
  - name: base
    content: |
      女性，二次元少女

  - name: 动物类型
    content: |
      {{rnd(猫,兔子,)}}

  - name: 动物
    content: |
      {{if($动物类型):桌子上有{{$动物类型}}:}}

  - name: 头发
    content: |
      {{rnd(黑,白,红,蓝)}}色头发

- prompts:
  - name: demo
    content: |
      {{base}}，坐在椅子上，{{头发}}，{{动物}}

  - name: demo_cache
    content: |
      {{base}}，坐在椅子上，{{$头发}}，{{动物}}
      再次提到：{{$动物类型}}和{{$头发}}

  - name: demo_mixed
    content: |
      初始：{{$动物类型}}，{{$头发}}
      重新随机：{{动物类型}}，{{头发}}
      保持缓存：{{$动物类型}}，{{$头发}}

```

### 语法说明

- **`{{variable}}`** - 普通变量引用，每次都重新生成随机值
- **`{{$variable}}`** - 缓存变量引用，同一次生成中保持一致的值
- **`{{rnd(选项1,选项2,选项3)}}`** - 随机选择一个选项
- **`{{if(变量):真值:假值}}`** - 条件判断，变量有值时显示真值，否则显示假值

## 使用方法

### Python 版本

#### 基本用法

```bash
# 进入 python 目录
cd python

# 安装依赖
pip install -r requirements.txt

# 执行（默认为交互模式）
python prompt_generator.py ../examples/config.yaml

# 生成指定提示词
python prompt_generator.py ../examples/config.yaml -p demo

# 使用自行定义的配置文件，放在根目录下可以被 git 忽略（推荐）
python prompt_generator.py ../config.yaml [选项]

```

> **注意：** 用户的实际配置文件通常放在项目根目录下（如 `config.yaml`），这些文件会被 git 忽略，不会被提交到版本库中。`examples/` 目录下的配置文件仅作为参考示例。

#### 命令参数

```bash
# 基本语法
python prompt_generator.py <配置文件> [选项]

# 参数说明：
#   配置文件                 YAML 配置文件路径
#   -p, --prompt PROMPT     指定要生成的提示词名称
#   -l, --list              列出所有可用的提示词
#   -i, --items             列出所有可用的变量
#   -n, --number NUMBER     生成次数（默认1次），为 -p 的附加选项
#   -r, --rnd               对列表随机排序输出，为 -l 的附加选项
#   -h, --help              显示帮助信息

```

#### 使用示例

```bash
# 列出配置文件中所有可用的提示词
python prompt_generator.py ../config.yaml -l

# 列出配置文件中所有可用的变量
python prompt_generator.py ../config.yaml -i

# 生成指定名称的提示词
python prompt_generator.py ../config.yaml -p demo

# 生成指定提示词多次
python prompt_generator.py ../config.yaml -p demo -n 5

# 交互模式（默认）
python prompt_generator.py ../config.yaml

# 使用示例配置文件
python prompt_generator.py ../examples/config.yaml -p demo

```

## 目录结构

```plaintext
├── README.md
├── .editorconfig
├── python/
│   ├── prompt_generator.py
│   └── requirements.txt
└── examples/
    └── config.yaml

```
