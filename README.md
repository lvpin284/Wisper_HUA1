# Wisper_HUA1

音频用 [OpenAI Whisper](https://github.com/openai/whisper) 转成文字。

本仓库已将 openai/whisper 源码直接内嵌（`whisper/` 目录），无需另行 `pip install openai-whisper`。

## 快速上手（五步走）

1. **克隆仓库**
2. **安装依赖**（见下方"安装依赖"节）
3. **准备模型权重文件**（见下方"模型权重"节，**离线环境必读**）
4. **把 MP4 文件放到一个目录里**
5. **运行脚本**（见下方"使用方法"节）

---

## 目录结构

```
Wisper_HUA1/
├── whisper/                  # openai/whisper 源码（内嵌）
├── transcribe_mp4_folder.py  # 批量转写脚本
├── requirements.txt          # Python 依赖
└── README.md
```

---

## 安装依赖

克隆本仓库后，只需安装运行依赖（torch、numpy 等），**无需** 单独安装 openai-whisper：

```bash
pip install -r requirements.txt
```

> **注意**：还需要安装 [ffmpeg](https://ffmpeg.org/)，用于音频解码：
> - macOS：`brew install ffmpeg`
> - Ubuntu/Debian：`sudo apt install ffmpeg`
> - Windows：从 https://ffmpeg.org/download.html 下载并加入 PATH

---

## 模型权重

### 方式一：有网络时自动下载（默认）

首次运行脚本时，程序会自动从 OpenAI 服务器下载模型权重并缓存到 `~/.cache/whisper/`，之后无需重复下载。

### 方式二：离线 / 无法联网时手动下载（重要）

如果运行时看到以下报错：

```
OSError: [Errno 99] Cannot assign requested address
urllib.error.URLError: <urlopen error [Errno 99] Cannot assign requested address>
```

说明当前机器**无法访问外网**，需要在另一台有网的机器上手动下载模型文件，再拷贝过来。

**步骤：**

1. 在能联网的机器（或通过代理）下载对应模型文件：

   | 模型名 | 文件名 | 大小 | 下载链接 |
   |--------|--------|------|----------|
   | `tiny` | `tiny.pt` | ~75 MB | https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt |
   | `base` | `base.pt` | ~145 MB | https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt |
   | `small` | `small.pt` | ~484 MB | https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt |
   | `medium` | `medium.pt` | ~1.5 GB | https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt |
   | `large-v3` | `large-v3.pt` | ~3.1 GB | https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt |

   例如，下载 `base` 模型（推荐先从此开始）：
   ```bash
   wget -O base.pt "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt"
   ```

2. 将下载好的 `.pt` 文件**拷贝到目标机器**，放到以下路径之一：

   - **方法 A（推荐）**：放入 `~/.cache/whisper/` 目录，文件名保持原样（如 `base.pt`）：
     ```bash
     mkdir -p ~/.cache/whisper
     cp base.pt ~/.cache/whisper/base.pt
     ```
     之后正常运行脚本即可，程序会自动找到缓存文件：
     ```bash
     python transcribe_mp4_folder.py /path/to/mp4_folder --model base
     ```

   - **方法 B**：将文件放到任意路径，然后用 `--model` 直接指定文件的完整路径：
     ```bash
     python transcribe_mp4_folder.py /path/to/mp4_folder --model /data/models/base.pt
     ```

---

## 使用方法

执行脚本（默认俄语 `ru`）：

```bash
python transcribe_mp4_folder.py /path/to/mp4_folder
```

可选参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-dir DIR` | 与输入目录相同 | 指定 txt 输出目录 |
| `--model MODEL` | `base` | whisper 模型名（`tiny`/`base`/`small`/`medium`/`large`）或本地 `.pt` 文件路径 |
| `--language LANG` | `ru` | 语言代码（如 `zh`、`en`、`ru`） |

输出格式（每行）：

```
开始时间戳 结束时间戳 0 这句话
```

例如：

```
1.120 3.560 0 Привет мир
```

---

## Whisper 模型对比

| 模型 | 参数量 | 速度 | 精度 | 推荐场景 |
|------|--------|------|------|----------|
| tiny | 39 M | 最快 | 较低 | 快速测试 |
| base | 74 M | 快 | 一般 | 日常使用（默认） |
| small | 244 M | 中等 | 较好 | 精度要求较高 |
| medium | 769 M | 慢 | 好 | 生产环境 |
| large-v3 | 1550 M | 最慢 | 最高 | 最高精度 |

> **建议**：俄语转写推荐使用 `small` 或 `medium` 模型以获得更好的识别效果。

---

## 常见问题

### Q：运行报错 `Cannot assign requested address` 或 `URLError`

**原因**：当前机器无法访问外网，无法自动下载模型权重。

**解决**：按照上方"方式二：离线/无法联网时手动下载"的步骤，手动下载模型文件并放到 `~/.cache/whisper/` 目录。

---

### Q：如何确认模型文件已经放好？

```bash
ls ~/.cache/whisper/
# 应该看到类似：base.pt
```

---

### Q：用 GPU 还是 CPU？

程序会自动检测。有 NVIDIA GPU 且安装了 CUDA 版 torch 时使用 GPU，否则用 CPU（速度较慢）。

检查当前是否使用 GPU：
```python
import torch
print(torch.cuda.is_available())
```
