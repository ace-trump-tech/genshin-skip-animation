# 原神动画跳过工具 / Genshin Impact Auto-Skip Animation

> **免责声明 / Disclaimer**  
> 本工具由”源批之星“鲁健友情贡献，仅用于**教育目的**，不修改游戏内存或网络数据包。但任何第三方自动化工具都可能违反游戏服务条款，导致账号被封禁。**请务必在废弃的小号上测试，主号使用风险自负。**  
> *This tool is for **educational purposes only**. It does not modify game memory or network packets. However, any third‑party automation may violate the game's Terms of Service and could lead to account suspension. **Always test on a disposable alt account. Use on your main account at your own risk.***

---

## 简介 / Introduction

一个基于 **计算机视觉 + 模拟输入** 的自动化工具，用于自动跳过《原神》中的过场动画、对话选项和加载界面。  
*A computer vision + input simulation tool that automatically skips cutscenes, dialog options, and loading screens in Genshin Impact.*

---

## 功能 / Features

- 检测“跳过”按钮并自动点击  
- 检测对话选项并自动按 `F` 键继续  
- 检测加载完成画面并点击屏幕中央  
- 全局热键控制启动/停止  
- 可配置的识别阈值和延迟参数  

- Detect the "Skip" button and click it automatically  
- Detect dialog options and press `F` to continue  
- Detect loading completion and click the screen center  
- Global hotkeys to start/stop the automation  
- Configurable confidence thresholds and delays

---

## 系统要求 / Requirements

- Python 3.8+
- Windows / macOS / Linux (with X11)
- 《原神》以**窗口模式**运行（推荐，保证截图稳定）  
- Genshin Impact running in **windowed mode** (recommended for stable screen capture)

---

## 安装 / Installation

### 1. 克隆仓库 / Clone the repository
```bash
git clone https://github.com/yourusername/genshin-skip-animation.git
cd genshin-skip-animation
```

### 2. 创建虚拟环境（可选）/ Create a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. 安装依赖 / Install dependencies
```bash
pip install -r requirements.txt
```

### 4. 截取 UI 模板 / Capture UI templates
启动游戏，找到有“跳过”按钮或对话选项的场景，用截图工具截取**小且特征明显**的图片，保存到 `assets/templates/` 目录下：
- `skip_button.png` – 蓝色“跳过”按钮  
- `dialog_option.png` – 对话选项框（或任何独特部分）  
- `loading_finish.png` – “点击继续”文字或区域  

> **提示**：模板越小越好（约 50×50 像素），使用 `.png` 格式，可保留透明背景。  
> *Tip: Keep templates small (~50x50 pixels) and use `.png` format with transparency if possible.*

### 5. 调整配置（可选）/ Adjust configuration (optional)
编辑 `config.yaml` 修改热键、置信度、延迟等。  
*Edit `config.yaml` to change hotkeys, confidence threshold, delays, etc.*

---

## 使用方法 / Usage

1. **运行脚本 / Run the script**
   ```bash
   python main.py
   ```

2. **在游戏中 / In Genshin Impact** (游戏窗口必须可见，不能最小化)  
   - 按下 `Ctrl+Shift+S`（默认）启动自动跳过  
   - 按下 `Ctrl+Shift+X`（默认）停止  
   - 脚本会将操作记录到控制台和 `assets/logs/run.log` 中  

   *Press `Ctrl+Shift+S` (default) to start auto‑skip. Press `Ctrl+Shift+X` (default) to stop. The script logs actions to the console and `assets/logs/run.log`.*

3. **停止脚本 / Stop the script** – 在终端按 `Ctrl+C`。

---

## 工作原理 / How It Works

- 持续捕获屏幕指定区域（或全屏）  
- 使用 OpenCV 模板匹配定位预设的 UI 元素  
- 找到匹配后，通过 `pyautogui` 模拟鼠标点击或按键  
- 状态机按优先级处理：跳过按钮 > 对话选项 > 加载完成  
- 全局热键通过 `pynput` 实现  

*The program continuously captures a region of the screen (or full screen). It uses OpenCV template matching to locate predefined UI elements. When a match is found, it triggers a simulated mouse click or key press via `pyautogui`. A state machine prioritizes actions: skip button > dialog > loading screen. Global hotkeys are implemented using `pynput`.*

---

## 项目结构 / Project Structure

```
genshin-skip-animation/
├── .gitignore
├── README.md
├── requirements.txt
├── config.yaml
├── main.py
├── core/
│   ├── __init__.py
│   ├── screen_capture.py
│   ├── image_recognition.py
│   ├── input_simulator.py
│   └── state_machine.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── hotkey_listener.py
├── assets/
│   ├── templates/
│   │   ├── skip_button.png
│   │   ├── dialog_option.png
│   │   └── loading_finish.png
│   └── logs/
└── tests/
    ├── test_capture.py
    ├── test_recognition.py
    └── test_simulator.py
```

---

## 常见问题 / Troubleshooting

| 问题 / Issue | 可能解决方案 / Possible Solution |
|--------------|----------------------------------|
| 无法检测到元素 / No detection | 降低 `config.yaml` 中的 `confidence` 值，或重新截取更独特的模板。 <br> *Decrease `confidence` in config, or recapture templates with better distinctness.* |
| 游戏没有反应 / Game not responding | 将原神设置为**窗口模式**（非独占全屏）。<br>*Run Genshin in **windowed mode** (not fullscreen exclusive).* |
| 热键无效 / Hotkeys not working | Windows 以管理员身份运行脚本；macOS 给予辅助功能权限。<br>*Run script as administrator on Windows, or give accessibility permissions on macOS.* |
| PyAutoGUI 无法控制鼠标 | 关闭鼠标加速或安全软件，测试 `pyautogui.moveTo(100,100)` 是否正常工作。<br>*Disable mouse acceleration / security software and test if `pyautogui.moveTo(100,100)` works.* |

---

## 贡献 / Contributing

欢迎提交 Issue 或 Pull Request。本项目旨在学习计算机视觉与自动化技术。  
*Feel free to open issues or pull requests. This project is meant for learning computer vision and automation techniques.*

---

## 许可证 / License

MIT 许可证。仅供非商业、教育用途。  
*MIT License – for non‑commercial, educational purposes only.*

---

## 致谢 / Acknowledgements
- 源批之星鲁健的所有代码创作
- OpenCV, PyAutoGUI, MSS, pynput – 优秀的开源库  
- 《原神》社区提供的灵感  

*OpenCV, PyAutoGUI, MSS, pynput – great open‑source libraries.  
The Genshin Impact community for inspiration.*
