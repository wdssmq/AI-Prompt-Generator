#!/usr/bin/env python3
"""
AI 提示词生成器 - Python 版本
支持 YAML 配置文件，变量替换和随机选择功能
"""

import yaml
import re
import random
import argparse
import sys
from typing import Dict, List, Any


class PromptGenerator:
    def __init__(self, config_file: str):
        """初始化提示词生成器

        Args:
            config_file: YAML 配置文件路径
        """
        self.items = {}
        self.prompts = {}
        self.load_config(config_file)

    def load_config(self, config_file: str):
        """加载 YAML 配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)

            for section in config:
                if 'items' in section:
                    for item in section['items']:
                        self.items[item['name']] = item['content'].strip()

                if 'prompts' in section:
                    for prompt in section['prompts']:
                        self.prompts[prompt['name']] = prompt['content'].strip()

        except FileNotFoundError:
            print(f"错误：配置文件 '{config_file}' 不存在")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"错误：YAML 文件格式错误 - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误：加载配置文件失败 - {e}")
            sys.exit(1)

    def process_random_selection(self, text: str) -> str:
        """处理随机选择语法 {{rnd(选项1,选项2,选项3)}}"""
        rnd_pattern = r'\{\{rnd\(([^)]+)\)\}\}'

        def replace_rnd(match):
            options = [opt.strip() for opt in match.group(1).split(',')]
            return random.choice(options)

        return re.sub(rnd_pattern, replace_rnd, text)

    def process_if_conditions(self, text: str) -> str:
        """处理条件判断语法 {{if(变量):真值:假值}}"""
        if_pattern = r'\{\{if\(([^)]+)\):([^:]*):([^}]*)\}\}'

        def replace_if(match):
            var_name = match.group(1).strip()
            true_value = match.group(2).strip()
            false_value = match.group(3).strip()

            # 获取变量值
            if var_name in self.items:
                # 首先生成变量值并缓存
                var_value = self.generate_text(self.items[var_name]).strip()

                # 如果变量值为空或空白，返回假值
                if not var_value:
                    return false_value

                # 如果变量值不为空，处理真值
                # 在真值中替换同名变量为已生成的值
                result = true_value
                if '{{' + var_name + '}}' in result:
                    result = result.replace('{{' + var_name + '}}', var_value)

                # 处理其他变量
                if '{{' in result and '}}' in result:
                    result = self.generate_text(result)

                return result
            else:
                print(f"警告：条件判断中未找到变量 '{var_name}'")
                return false_value

        return re.sub(if_pattern, replace_if, text)

    def process_variables(self, text: str) -> str:
        """处理变量替换 {{variable_name}}"""
        var_pattern = r'\{\{([^}]+)\}\}'

        def replace_var(match):
            var_name = match.group(1).strip()
            if var_name in self.items:
                # 递归处理变量内容中的其他变量和随机选择
                return self.generate_text(self.items[var_name])
            else:
                print(f"警告：未找到变量 '{var_name}'")
                return match.group(0)  # 保持原样

        return re.sub(var_pattern, replace_var, text)

    def generate_text(self, template: str, max_depth: int = 10) -> str:
        """生成最终文本

        Args:
            template: 模板文本
            max_depth: 最大递归深度，防止循环引用

        Returns:
            处理后的文本
        """
        if max_depth <= 0:
            print("警告：达到最大递归深度，可能存在循环引用")
            return template

        # 先处理随机选择
        text = self.process_random_selection(template)

        # 处理条件判断
        text = self.process_if_conditions(text)

        # 检查是否还有变量需要替换
        if '{{' in text and '}}' in text:
            # 处理变量替换
            old_text = text
            text = self.process_variables(text)

            # 如果文本发生了变化，继续递归处理
            if text != old_text:
                text = self.generate_text(text, max_depth - 1)

        return text

    def generate_prompt(self, prompt_name: str) -> str:
        """生成指定名称的提示词

        Args:
            prompt_name: 提示词名称

        Returns:
            生成的提示词文本
        """
        if prompt_name not in self.prompts:
            raise ValueError(f"未找到提示词 '{prompt_name}'")

        return self.generate_text(self.prompts[prompt_name])

    def list_prompts(self) -> List[str]:
        """获取所有可用的提示词名称"""
        return list(self.prompts.keys())

    def list_items(self) -> List[str]:
        """获取所有可用的变量名称"""
        return list(self.items.keys())


def main():
    parser = argparse.ArgumentParser(description='AI 提示词生成器')
    parser.add_argument('config', help='YAML 配置文件路径')
    parser.add_argument('-p', '--prompt', help='指定要生成的提示词名称')
    parser.add_argument('-l', '--list', action='store_true', help='列出所有可用的提示词')
    parser.add_argument('-i', '--items', action='store_true', help='列出所有可用的变量')
    parser.add_argument('-n', '--number', type=int, default=1, help='生成次数（默认1次）')

    args = parser.parse_args()

    try:
        generator = PromptGenerator(args.config)

        if args.list:
            print("可用的提示词：")
            for prompt in generator.list_prompts():
                print(f"  - {prompt}")
            return

        if args.items:
            print("可用的变量：")
            for item in generator.list_items():
                print(f"  - {item}")
            return

        if args.prompt:
            print(f"生成提示词 '{args.prompt}'：")
            for i in range(args.number):
                if args.number > 1:
                    print(f"\n第 {i+1} 次生成：")
                result = generator.generate_prompt(args.prompt)
                print(result)
        else:
            # 交互模式
            print("AI 提示词生成器 - 交互模式")
            print("可用的提示词：", ', '.join(generator.list_prompts()))
            print("输入 'quit' 或 'exit' 退出\n")

            while True:
                try:
                    prompt_name = input("请输入提示词名称: ").strip()
                    if prompt_name.lower() in ['quit', 'exit']:
                        break

                    if not prompt_name:
                        continue

                    result = generator.generate_prompt(prompt_name)
                    print(f"\n生成的提示词：\n{result}\n")

                except KeyboardInterrupt:
                    print("\n再见！")
                    break
                except ValueError as e:
                    print(f"错误：{e}")
                except Exception as e:
                    print(f"发生错误：{e}")

    except Exception as e:
        print(f"程序执行失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
