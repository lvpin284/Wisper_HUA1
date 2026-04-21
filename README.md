# Wisper_HUA1

音频用 [OpenAI Whisper](https://github.com/openai/whisper) 转成文字。

本仓库已将 openai/whisper 源码直接内嵌（`whisper/` 目录），无需另行 `pip install openai-whisper`。

## 批量把俄语 MP4 转成 TXT

已提供脚本：`transcribe_mp4_folder.py`

输出格式（每行）：

`开始时间戳 结束时间戳 0 这句话`

例如：

`1.120 3.560 0 Привет мир`

## 目录结构

```
Wisper_HUA1/
├── whisper/                  # openai/whisper 源码（内嵌）
├── transcribe_mp4_folder.py  # 批量转写脚本
├── requirements.txt          # Python 依赖
└── README.md
```

## 安装依赖

克隆本仓库后，只需安装运行依赖（torch、numpy 等），**无需** 单独安装 openai-whisper：

```bash
pip install -r requirements.txt
```

> **注意**：还需要安装 [ffmpeg](https://ffmpeg.org/)，用于音频解码：
> - macOS：`brew install ffmpeg`
> - Ubuntu/Debian：`sudo apt install ffmpeg`
> - Windows：从 https://ffmpeg.org/download.html 下载并加入 PATH

## 使用方法

执行脚本（默认俄语 `ru`）：

```bash
python transcribe_mp4_folder.py /path/to/mp4_folder
```

可选参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-dir DIR` | 与输入目录相同 | 指定 txt 输出目录 |
| `--model MODEL` | `base` | whisper 模型：`tiny` / `base` / `small` / `medium` / `large` |
| `--language LANG` | `ru` | 语言代码（如 `zh`、`en`、`ru`） |

## Whisper 模型对比

| 模型 | 参数量 | 速度 | 精度 |
|------|--------|------|------|
| tiny | 39 M | 最快 | 较低 |
| base | 74 M | 快 | 一般 |
| small | 244 M | 中等 | 较好 |
| medium | 769 M | 慢 | 好 |
| large | 1550 M | 最慢 | 最高 |

首次运行时模型权重会自动从 OpenAI 服务器下载并缓存到 `~/.cache/whisper/`。
