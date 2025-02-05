# Coze Bot AI 语音助手

这是一个基于 Coze 工作流的智能语音助手程序，实现了语音输入、AI 对话和语音输出的完整交互流程。支持实时语音录制和对话，并提供详细的处理进度和时间统计。

## 功能特点

1. **实时语音录制**
   - 按住按钮开始录音，松开结束录音
   - 实时显示录音时长
   - 自动保存为 WAV 格式
   - 16kHz 采样率，16位深度，单声道
   - 录音文件自动保存在 `input` 目录

2. **语音识别 (ASR)**
   - 使用 FunAudioLLM/SenseVoiceSmall 模型
   - 支持 WAV 格式音频输入
   - 自动识别中文语音内容
   - 实时显示识别进度

3. **AI 对话处理**
   - 基于 Coze 工作流
   - 智能对话响应
   - 支持上下文理解
   - 个性化回复风格
   - 显示处理进度

4. **语音合成 (TTS)**
   - 使用 FunAudioLLM/CosyVoice2-0.5B 模型
   - 支持自定义声音模型
   - 高质量语音输出
   - WAV 格式音频生成
   - 自动保存在 `output` 目录

5. **进度显示和时间统计**
   - 实时显示处理进度条
   - 显示当前处理阶段
   - 统计各阶段处理时间
   - 显示总体处理耗时
   - 清晰的状态提示

## 技术架构

- **音频录制**: PyAudio
- **语音识别**: SiliconFlow ASR API
- **对话处理**: Coze Workflow API
- **语音合成**: SiliconFlow TTS API
- **音频播放**: Pygame
- **图形界面**: PyQt5
- **多线程处理**: Python Threading

## 安装说明

1. **克隆项目**
   ```bash
   git clone git@github.com:wilsonwussd/Coze_Bot_AI_Example.git
   cd Coze_Bot_AI_Example
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   .\venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **安装系统依赖**
   
   在 Linux 上：
   ```bash
   sudo apt-get install python3-pyaudio portaudio19-dev
   ```
   
   在 macOS 上：
   ```bash
   brew install portaudio
   ```
   
   在 Windows 上：
   PyAudio 会通过 pip 自动安装

## 配置说明

在 `main.py` 中配置以下参数：

```python
# API 配置
ASR_API_TOKEN = "your_asr_token"
COZE_API_TOKEN = "your_coze_token"
WORKFLOW_ID = "your_workflow_id"
TTS_VOICE = "your_voice_model"

# 录音配置
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
```

## 使用方法

1. **运行程序**
   ```bash
   python main.py
   ```

2. **开始对话**
   - 按住"按住开始录音"按钮说话
   - 实时查看录音时长
   - 松开按钮结束录音
   - 观察处理进度和状态
   - 等待 AI 回复并播放语音

3. **查看处理进度**
   - 进度条显示整体进度
   - 状态标签显示当前动作
   - 时间统计显示各阶段耗时

4. **查看输出**
   - 语音识别结果实时显示
   - AI 回复显示在对话区域
   - 语音文件自动保存
   - 自动播放语音回复

## 项目结构

```
Coze_Bot_AI_Example/
├── main.py            # 主程序文件
├── requirements.txt   # 项目依赖
├── README.md         # 项目说明
├── input/            # 录音文件目录
└── output/           # 输出音频目录
```

## API 说明

### 1. ASR API
- 端点：`https://api.siliconflow.cn/v1/audio/transcriptions`
- 模型：`FunAudioLLM/SenseVoiceSmall`
- 支持格式：WAV

### 2. Coze Workflow API
- 使用 Coze Python SDK
- 支持自定义工作流配置
- 灵活的对话处理能力

### 3. TTS API
- 端点：`https://api.siliconflow.cn/v1/audio/speech`
- 模型：`FunAudioLLM/CosyVoice2-0.5B`
- 支持自定义声音模型

## 开发计划

- [x] 添加实时语音输入支持
- [x] 添加进度显示功能
- [x] 添加时间统计功能
- [x] 优化用户界面
- [ ] 添加对话历史保存功能
- [ ] 添加设置界面
- [ ] 支持更多音频格式
- [ ] 添加快捷键支持

## 注意事项

1. 确保有足够的磁盘空间存储音频文件
2. 需要稳定的网络连接
3. 确保麦克风权限已开启
4. API Token 请妥善保管
5. 录音时保持安静的环境

## 常见问题

1. **Q: 进度条卡在某个阶段怎么办？**
   A: 检查网络连接，确保 API 服务正常。如果问题持续，可以查看控制台输出的错误信息。

2. **Q: 录音质量不好怎么办？**
   A: 调整 `RATE` 和 `CHUNK` 参数，使用更好的麦克风，保持安静的录音环境。

3. **Q: 程序运行缓慢怎么办？**
   A: 检查网络连接，确保 API 服务正常，可以适当调整 `CHUNK` 大小。

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

- 项目维护者：Wilson Wu
- GitHub：[wilsonwussd](https://github.com/wilsonwussd)

## 致谢

- SiliconFlow 提供的 API 支持
- Coze 平台的工作流支持
- 开源社区的各种工具支持 