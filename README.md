# Coze Bot AI 语音助手

这是一个基于 Coze 工作流的智能语音助手示例程序，实现了语音输入、AI 对话和语音输出的完整交互流程。

## 功能特点

1. **语音识别 (ASR)**
   - 使用 FunAudioLLM/SenseVoiceSmall 模型
   - 支持 WAV 格式音频输入
   - 自动识别中文语音内容

2. **AI 对话处理**
   - 基于 Coze 工作流
   - 智能对话响应
   - 支持上下文理解
   - 个性化回复风格

3. **语音合成 (TTS)**
   - 使用 FunAudioLLM/CosyVoice2-0.5B 模型
   - 支持自定义声音模型
   - 高质量语音输出
   - WAV 格式音频生成

## 技术架构

- **语音识别**: SiliconFlow ASR API
- **对话处理**: Coze Workflow API
- **语音合成**: SiliconFlow TTS API
- **音频播放**: Pygame

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

## 配置说明

在 `main.py` 中配置以下参数：

```python
# API 配置
ASR_API_TOKEN = "your_asr_token"
COZE_API_TOKEN = "your_coze_token"
WORKFLOW_ID = "your_workflow_id"
TTS_VOICE = "your_voice_model"
```

## 使用方法

1. **准备音频文件**
   - 将 WAV 格式的音频文件放入 `vioice` 目录

2. **运行程序**
   ```bash
   python main.py
   ```

3. **查看输出**
   - 语音识别结果会实时显示
   - AI 回复会显示在控制台
   - 生成的语音文件保存在 `output` 目录
   - 自动播放生成的语音回复

## 项目结构

```
Coze_Bot_AI_Example/
├── main.py            # 主程序文件
├── requirements.txt   # 项目依赖
├── README.md         # 项目说明
├── vioice/           # 输入音频目录
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

- [ ] 添加实时语音输入支持
- [ ] 优化音频播放体验
- [ ] 添加图形用户界面
- [ ] 支持更多音频格式
- [ ] 添加对话历史记录
- [ ] 支持多语言

## 注意事项

1. 确保有足够的磁盘空间存储音频文件
2. 需要稳定的网络连接
3. 音频文件必须是 WAV 格式
4. API Token 请妥善保管

## 常见问题

1. **Q: 为什么音频识别失败？**
   A: 请确保音频文件格式正确，且文件未损坏。

2. **Q: 如何更换声音模型？**
   A: 修改 `main.py` 中的 `TTS_VOICE` 参数。

3. **Q: 程序运行缓慢怎么办？**
   A: 检查网络连接，确保 API 服务正常。

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