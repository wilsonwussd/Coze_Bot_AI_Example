import os
import time
import json
import requests
from pathlib import Path
from openai import OpenAI
import pygame
from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth

# API 配置
ASR_API_TOKEN = "sk-ijrbblmmorcoszexftooqredccpznqswtrwsivnbusucfrpv"
COZE_API_TOKEN = "pat_vsRmtmgItCScWkeUQeFA2rTxIzOzqmfLDC0pHya1u9H37aiCsxDUuHDOmuJdtZJr"
WORKFLOW_ID = "7466919232299941923"
TTS_VOICE = "speech:dengziqi:1u9ttv0p3u:dkwsggzvihmgjekvpvdr"

# 初始化 pygame 音频
pygame.mixer.init()

def convert_audio_to_text(audio_file_path):
    """
    使用 ASR API 将音频文件转换为文字
    """
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"
    
    # 准备文件数据
    files = {
        'file': ('audio.wav', open(audio_file_path, 'rb'), 'audio/wav'),
        'model': (None, 'FunAudioLLM/SenseVoiceSmall')
    }
    
    headers = {
        "Authorization": f"Bearer {ASR_API_TOKEN}"
    }
    
    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json().get('text', '')
    except Exception as e:
        print(f"ASR API 调用失败: {str(e)}")
        return None
    finally:
        files['file'][1].close()

def call_coze_workflow(text):
    """
    调用 Coze 工作流处理文本
    """
    try:
        coze = Coze(
            auth=TokenAuth(token=COZE_API_TOKEN),
            base_url=COZE_CN_BASE_URL
        )
        
        # 创建工作流实例
        response = coze.workflows.runs.create(
            workflow_id=WORKFLOW_ID,
            parameters={"text": text}
        )
        
        # 解析响应数据
        if response and response.data:
            # 如果响应数据是字符串，尝试解析 JSON
            if isinstance(response.data, str):
                try:
                    data = json.loads(response.data)
                    return data.get('data', '')
                except json.JSONDecodeError:
                    return response.data
            # 如果响应数据是字典
            elif isinstance(response.data, dict):
                return response.data.get('data', '')
        return None
    except Exception as e:
        print(f"Coze 工作流调用失败: {str(e)}")
        return None

def text_to_speech(text):
    """
    使用 TTS API 将文本转换为语音
    """
    try:
        # 创建输出目录
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # 设置输出文件路径
        speech_file_path = output_dir / "response.wav"
        
        # 准备请求数据
        url = "https://api.siliconflow.cn/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {ASR_API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            "voice": TTS_VOICE,
            "input": text,
            "response_format": "wav",
            "stream": False
        }
        
        # 发送请求
        print("DEBUG - TTS 请求数据:", json.dumps(data, ensure_ascii=False))
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        # 保存音频文件
        with open(speech_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return str(speech_file_path)
    except Exception as e:
        print(f"TTS API 调用失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"响应内容: {e.response.text}")
        return None

def play_audio(audio_file_path):
    """
    使用 pygame 播放音频文件
    """
    try:
        # 加载音频文件
        pygame.mixer.music.load(audio_file_path)
        # 播放音频
        pygame.mixer.music.play()
        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"音频播放失败: {str(e)}")

def process_audio_files():
    """
    处理 voice 文件夹中的所有音频文件
    """
    voice_dir = "vioice"  # 注意：文件夹名称是 "vioice"
    
    if not os.path.exists(voice_dir):
        print(f"错误: {voice_dir} 文件夹不存在")
        return
    
    # 遍历 voice 文件夹中的所有 wav 文件
    for filename in os.listdir(voice_dir):
        if filename.lower().endswith('.wav'):
            audio_path = os.path.join(voice_dir, filename)
            print(f"\n处理音频文件: {filename}")
            
            # 1. 将音频转换为文字
            text = convert_audio_to_text(audio_path)
            if text:
                print(f"语音识别结果: {text}")
                
                # 2. 调用 Coze 工作流
                response_text = call_coze_workflow(text)
                if response_text:
                    print(f"Coze 工作流回复: {response_text}")
                    
                    # 3. 将回复转换为语音
                    print("正在生成语音回复...")
                    speech_file = text_to_speech(response_text)
                    if speech_file:
                        print(f"语音生成成功: {speech_file}")
                        
                        # 4. 播放语音回复
                        print("正在播放语音回复...")
                        play_audio(speech_file)
                    else:
                        print("语音生成失败")
                else:
                    print("获取 Coze 回复失败")
            else:
                print("语音识别失败，跳过该文件")

if __name__ == "__main__":
    print("开始处理音频文件...")
    process_audio_files()
    print("\n处理完成!")
    # 退出 pygame
    pygame.mixer.quit() 