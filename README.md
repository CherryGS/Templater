# Templater

通过文件夹与markdown形成的文档树创建pdf

正常的文件名前加入 "数字#" 来代表该文件在此文件夹中的顺序

其中，"0#" 代表此文件是该文件夹的引言，不作为目录的一部分

使用 pandoc 将 md 转换为 latex

使用 xelatex 将 latex 渲染为 pdf

如果文件名中含有保留词，请在 main.py 中的 rpDic 字典中添加

本机使用软件版本见 version.txt