# Wisper_HUA1

音频用 w(h)isper 转成文字。

## 批量把俄语 MP4 转成 TXT

已提供脚本：`transcribe_mp4_folder.py`

输出格式（每行）：

`开始时间戳 结束时间戳 0 这句话`

例如：

`1.120 3.560 0 Привет мир`

### 使用方法

1. 安装依赖：

```bash
pip install -U openai-whisper
```

2. 执行脚本（默认俄语 `ru`）：

```bash
python transcribe_mp4_folder.py /path/to/mp4_folder
```

可选参数：

- `--output-dir /path/to/output_folder`：指定 txt 输出目录（默认与输入目录相同）
- `--model base`：指定 whisper 模型（tiny/base/small/medium/large）
- `--language ru`：指定语言代码
