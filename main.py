import functools
import os, re, shutil

dirPath = "E:\CherryGS\TemplateCreater\ACM Template" # 放置 main.tex 的主文件夹
resPath = os.path.join(dirPath, "resource") # 放置 markdown 格式模板文件，尽量不要使用标题
tempPath =  "E:\CherryGS\TemplateCreater\Test" # 生成临时文件夹
outPath = "E:\CherryGS\TemplateCreater\ACM Template" # pdf 生成文件夹
orderPattern = "^[0-9]\d*#" # 正则，删除用来排序的部分文件名
numPattern = "^[0-9]\d*" # 正则，找开头的数字，其中，数字0代表该文件夹的前言
keyStr = "%--key--" # 在此之后开始插入内容
pandocCMD = "pandoc \"{}\" --listings -o \"{}\"" # md 转换 latex
compileCMD = "xelatex main.tex" # 编译 tex 的指令

content = [
    "\chapter{{{}}}", "\section{{{}}}", "\subsection{{{}}}", "\subsubsection{{{}}}", "\paragraph{{{}}}"
]
# latex 目录结构，目前最多支持5层

def check_and_create(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return 1
    return 0

check_and_create(dirPath)
check_and_create(resPath)
check_and_create(tempPath)
check_and_create(outPath)

out_pointer = open(os.path.join(tempPath, "main.tex"), "w", encoding="UTF8")
in_pointer = open(os.path.join(dirPath, "main.tex"), "r", encoding="UTF8")
line = in_pointer.readline()

cnt = 0 # 防止重复

def cv(txt :str):
    txt = txt.replace("_", "\_")
    return txt

def cmp(a, b):
    r1 = re.search(numPattern, a).group()
    r2 = re.search(numPattern, b).group()
    return int(r1) - int(r2)

def sol(dep, path):
    global cnt
    if dep > 4:
        raise ValueError("目录结构大于5层，暂不支持")
    lis = os.listdir(path)
    lis.sort(key=functools.cmp_to_key(cmp))
    for pth in lis:
        pth = os.path.join(path, pth)
        print(pth)
        name = os.path.split(pth)[1]
        patt = re.search(orderPattern, name).group()
        name = name.replace(patt, '')
        Rname = os.path.splitext(name)[0]
        
        # 特殊标志，代表该文件为文件夹的前言
        if patt != '0#': 
            out_pointer.write(cv(content[dep].format(Rname) + '\n'))
        if os.path.isdir(pth):
            sol(dep+1, pth)
        else:
            cnt += 1
            fPath = os.path.join(tempPath, str(cnt) + Rname + '.tex') # 通过 cnt 防止重复
            os.system(pandocCMD.format(pth, fPath)) # 转换 markdown 为 latex
            out_pointer.write(cv("\input{{{}}} \n ".format(str(cnt) + Rname + '.tex')))

def del_others(path):
    files = os.listdir(path)
    del_suffix = ['toc', 'vrb', 'aux', 'log', 'nav', 'out', 'snm', 'synctex.gz']
    for file in files:
        for suffix in del_suffix:
            if file.endswith(suffix):
                os.remove(file)

def compile(path, num, cl):
    os.chdir(tempPath)
    while num:
        os.system(compileCMD)
        num -= 1
    pdf = os.path.join(path, "main.pdf")
    if os.path.isfile(pdf):
        os.remove(pdf)
    shutil.move("main.pdf", path)
    if cl:
        del_others(tempPath)


if __name__ == "__main__" :
    while line:
        if line.strip() == keyStr:
            sol(0, resPath)
        else:
            out_pointer.write(line)
        line = in_pointer.readline()
    in_pointer.close()
    out_pointer.close()
    compile(outPath, 2, 1)
    os.chdir(resPath)
    shutil.rmtree(tempPath)
