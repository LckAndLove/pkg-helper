import subprocess
import json
import sys
import os
import argparse

def get_pkg_config_info(packages):
    """获取 pkg-config 对应包的 cflags 和 libs"""
    pkg_info = {}
    
    try:
        # 获取所有包的 cflags 和 libs
        cflags = subprocess.check_output(['pkg-config', '--cflags'] + packages, universal_newlines=True).strip()
        libs = subprocess.check_output(['pkg-config', '--libs'] + packages, universal_newlines=True).strip()

        # 将 cflags 和 libs 加入到字典中
        pkg_info["cflags"] = cflags
        pkg_info["libs"] = libs

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing pkg-config for {packages}: {e}")
    
    return pkg_info

def convert_to_windows_path(path):
    """将 Linux 风格路径转换为 Windows 风格路径，并简化路径"""
    path = path.replace('/', '\\')  # 转换为 Windows 风格路径
    return os.path.normpath(path)  # 使用 normpath 来简化路径

def create_task_json(gcc_path, packages):
    """动态创建 JSON 任务"""
    # 获取 pkg-config 对应包的 cflags 和 libs
    pkg_info = get_pkg_config_info(packages)
    
    # 固定的 args 参数
    args = [
        "-fdiagnostics-color=always",
        "-g",
        "${file}",
        "-o",
        "${fileDirname}\\${fileBasenameNoExtension}.exe"
    ]
    
    # 用来存储已添加的库，避免重复添加
    added_libs = set()

    # 获取 cflags 和 libs
    cflags = pkg_info.get("cflags", "")
    libs = pkg_info.get("libs", "")
    
    # 将 cflags 处理并添加到 args
    if cflags:
        cflags_list = cflags.split()  # 拆分参数
        for flag in cflags_list:
            args.append(f"{convert_to_windows_path(flag)}")  # 路径加上引号

    # 将 libs 处理并添加到 args
    if libs:
        libs_list = libs.split()  # 拆分参数
        for flag in libs_list:
            if flag.startswith("-l") and flag not in added_libs:
                args.append(flag)  # 库参数不需要再加双引号
                added_libs.add(flag)
            else:
                args.append(f"{convert_to_windows_path(flag)}")  # 其他库路径加引号
    
    # 创建任务 JSON 配置
    task = {
        "tasks": [
            {
                "type": "cppbuild",
                "label": "C/C++: g++.exe 生成活动文件",
                "command": gcc_path,
                "args": args,
                "options": {
                    "cwd": "${fileDirname}"
                },
                "problemMatcher": [
                    "$gcc"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "detail": "调试器生成的任务。"
            }
        ],
        "version": "2.0.0"
    }
    
    return json.dumps(task, indent=4)

def get_gcc_path(libs):
    """通过 libs 路径推断 g++ 的路径"""
    print(f"推断 g++ 路径...")

    # 查找 -L 后面跟的路径
    lib_path = None
    for flag in libs.split():
        if flag.startswith("-L"):
            lib_path = flag[2:]  # 去掉 -L 前缀
            break
    
    if not lib_path:
        print("Error: 未找到 -L 参数中的库路径.")
        sys.exit(1)

    # 假设 g++ 在 lib 所在的目录上级的 bin 目录下
    bin_dir = os.path.join(lib_path, '..', 'bin')
    
    # 使用 os.path.normpath 来简化路径
    gcc_path = os.path.normpath(os.path.join(bin_dir, 'g++.exe'))
    
    # 检查推断出来的路径是否存在
    if os.path.exists(gcc_path):
        return gcc_path
    else:
        print(f"Error: g++ not found in {bin_dir}. Please manually specify the g++ path.")
        sys.exit(1)

def save_to_tasks_json(task_json):
    """将生成的 JSON 配置保存到 .vscode/tasks.json"""
    task_file = os.path.join(".vscode", "tasks.json")
    try:
        os.makedirs(".vscode", exist_ok=True)
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(json.loads(task_json), f, ensure_ascii=False, indent=4)
        print(f"任务配置已保存到 {task_file}")
    except Exception as e:
        print(f"保存 tasks.json 时发生错误: {e}")

def save_to_c_cpp_properties_json(cpp_properties_json):
    """将生成的 c_cpp_properties.json 配置保存到 .vscode/c_cpp_properties.json"""
    cpp_properties_file = os.path.join(".vscode", "c_cpp_properties.json")
    try:
        os.makedirs(".vscode", exist_ok=True)
        with open(cpp_properties_file, 'w', encoding='utf-8') as f:
            json.dump(json.loads(cpp_properties_json), f, ensure_ascii=False, indent=4)
        print(f"c_cpp_properties.json 配置已保存到 {cpp_properties_file}")
    except Exception as e:
        print(f"保存 c_cpp_properties.json 时发生错误: {e}")

def create_c_cpp_properties_json(cflags, gcc_path):
    """生成 c_cpp_properties.json 配置"""
    include_path = None
    if cflags:
        cflags_list = cflags.split()
        for flag in cflags_list:
            if flag.startswith("-I"):
                include_path = convert_to_windows_path(flag[2:])
                break  # 只取第一个路径

    cpp_properties = {
        "configurations": [
            {
                "name": "Win32",
                "includePath": ["${workspaceFolder}/**", f"{include_path}\\**"],
                "defines": [
                    "_DEBUG",
                    "UNICODE",
                    "_UNICODE"
                ],
                "compilerPath": gcc_path,
                "cStandard": "c17",
                "cppStandard": "gnu++17",
                "intelliSenseMode": "windows-gcc-x64"
            }
        ],
        "version": 4
    }

    return json.dumps(cpp_properties, indent=4)

def main():
    """主函数，用于解析命令行参数并执行相关操作"""
    parser = argparse.ArgumentParser(description="根据 pkg-config 获取 C/C++ 包的编译信息，并生成 VSCode 配置文件")
    
    parser.add_argument('packages', metavar='PACKAGE', type=str, nargs='+', 
                        help='提供需要处理的包名，可以是任意有效的包')

    args = parser.parse_args()

    if not args.packages:
        print("错误: 请提供至少一个包名，格式：python script.py <package1> <package2> ...")
        sys.exit(1)
    
    # 获取 pkg-config 的 libs 信息
    pkg_info = get_pkg_config_info(args.packages)

    # 通过 libs 路径推断 gcc 路径
    libs = pkg_info.get("libs", "")
    gcc_path = get_gcc_path(libs)

    # 生成任务 JSON
    task_json = create_task_json(gcc_path, args.packages)

    # 保存到 .vscode/tasks.json
    save_to_tasks_json(task_json)

    # 获取 cflags 并生成 c_cpp_properties.json
    cflags = pkg_info.get("cflags", "")
    cpp_properties_json = create_c_cpp_properties_json(cflags, gcc_path)

    # 保存到 .vscode/c_cpp_properties.json
    save_to_c_cpp_properties_json(cpp_properties_json)

if __name__ == "__main__":
    main()
