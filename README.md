# PKG-HELPER  
🚀 **MSYS2 + VSCode + Cpp Library + JSON 工具** 🚀

🌟 **专为 Windows 开发者设计的高效开发工具集，简化测试与开发流程！** 🌟  
基于 **MSYS2** 环境，结合 **VSCode 配置** 和 **JSON 管理**，让你在 Windows 上轻松搭建高效的开发、测试环境。

---

### 🛠️ **项目亮点**：

- **简化开发流程**：在 Windows 上快速搭建VSCode Cpp Library运行配置，`十分钟`解决你的烦恼。
- **高效开发体验**：完美集成 VSCode 配置，提高开发和调试效率。
- **C++ 强力支持**：优化 C++ 库和头文件管理，避免重复引用，让开发更顺畅。

---
### 📝 **使用说明**：

1. **下载并安装 PKG-HELPER**  
   前往 [GitHub Release 页面](https://github.com/LckOrLck/pkg-helper/releases)，下载最新版本的 `pkg-helper.exe` 文件，并将该文件所在的路径添加到系统的环境变量 **Path** 中，确保你能在终端中使用 `pkg-helper` 命令。

2. **安装 MSYS2**  
   如果你还没有安装 MSYS2，请前往 [MSYS2 官方网站](https://www.msys2.org/) 下载并安装。  
   安装时，请执行以下步骤：

   - 在 `MSYS2` 中安装开发工具链：  
     ```bash
     pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
     ```

   - 安装 `fmt` 库（用于格式化输出，推荐用于测试和日志记录）：  
     ```bash
     pacman -S mingw-w64-ucrt-x86_64-fmt
     # 需要安装其他库的话，可以参考 packages.msys2.org 进行第三方库的安装
     ```

   - 如需图形化界面支持，安装 QT6：  
     ```bash
     pacman -S mingw-w64-ucrt-x86_64-qt6
     ```

   - 将 `ucrt64/bin` 和 `ucrt64/lib` 文件夹添加到环境变量 **Path** 中，确保工具链命令可以在终端中执行。

3. **配置 VSCode**  
   确保你已安装 [VSCode](https://code.visualstudio.com/) 和 **C/C++ 插件**。

4. **使用 PKG-HELPER**  
   在 VSCode 内打开 **Terminal**，输入以下命令来生成所需的包和 JSON 配置文件：  
   ```bash
   pkg-helper package_name1 package_name2 ...
   ```
   生成的 JSON 配置文件将保存在项目的 `.vscode` 文件夹中。

5. **编译与运行**  
   默认情况下，生成的 JSON 配置文件支持单个 C/C++ 文件的编译与运行。  
   在 VSCode 中，点击 `Run/Debug C/C++ File` 按钮，开始构建与调试你的代码。

---

### 🚀 **立即体验，提升你的开发效率与测试体验！** 🌟
