import os
import time
import json
import wave
import pyaudio
import requests
from pathlib import Path
from openai import OpenAI
import pygame
from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                           QWidget, QLabel, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from threading import Thread
import sys
from datetime import datetime

# API 配置
ASR_API_TOKEN = "sk-ijrbblmmorcoszexftooqredccpznqswtrwsivnbusucfrpv"
COZE_API_TOKEN = "pat_vsRmtmgItCScWkeUQeFA2rTxIzOzqmfLDC0pHya1u9H37aiCsxDUuHDOmuJdtZJr"
WORKFLOW_ID = "7466919232299941923"
TTS_VOICE = "speech:dengziqi:1u9ttv0p3u:dkwsggzvihmgjekvpvdr"

class RecordingThread(Thread):
    def __init__(self, stream, chunk):
        super().__init__()
        self.stream = stream
        self.chunk = chunk
        self.frames = []
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            except Exception as e:
                print(f"录音错误: {str(e)}")
                break

    def stop(self):
        self.running = False

    def get_frames(self):
        return self.frames

class VoiceAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_audio()
        pygame.mixer.init()
        
    def init_audio(self):
        """初始化音频参数"""
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.recording = False
        self.frames = []
        self.p = None
        self.stream = None
        self.recording_time = 0
        self.record_thread = None
        
        # 创建定时器用于更新录音时长显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.setInterval(100)
        
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('Coze Bot AI 语音助手')
        self.setGeometry(300, 300, 500, 500)  # 增加窗口高度
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建录音按钮
        self.record_button = QPushButton('按住开始录音', self)
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_and_process)
        
        # 创建时间显示标签
        self.time_label = QLabel('0.0 秒', self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建状态显示标签
        self.status_label = QLabel('等待录音...', self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        
        # 创建处理时间显示标签
        self.process_time_label = QLabel('处理时间: ', self)
        self.process_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建对话显示区域
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        
        # 添加部件到布局
        layout.addWidget(self.record_button)
        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.process_time_label)
        layout.addWidget(self.chat_display)
        
    def update_time(self):
        """更新录音时长显示"""
        self.recording_time += 0.1
        self.time_label.setText(f'{self.recording_time:.1f} 秒')
            
    def start_recording(self):
        """开始录音"""
        self.recording = True
        self.frames = []
        self.recording_time = 0
        
        # 创建PyAudio对象
        self.p = pyaudio.PyAudio()
        
        # 打开音频流
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        # 更新界面状态
        self.status_label.setText('正在录音...')
        self.record_button.setText('松开结束录音')
        
        # 创建并启动录音线程
        self.record_thread = RecordingThread(self.stream, self.CHUNK)
        self.record_thread.start()
        
        # 启动定时器
        self.timer.start()
        
    def stop_recording(self):
        """停止录音"""
        if not self.recording:
            return
            
        self.recording = False
        self.timer.stop()
        
        # 停止录音线程
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.stop()
            self.record_thread.join()
            self.frames = self.record_thread.get_frames()
        
        # 停止并关闭音频流
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.p:
            self.p.terminate()
        
        # 更新界面状态
        self.status_label.setText('录音结束')
        self.record_button.setText('按住开始录音')
        
    def save_recording(self):
        """保存录音文件"""
        if not os.path.exists('input'):
            os.makedirs('input')
            
        output_file = "input/recording.wav"
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        return output_file
        
    def update_progress(self, value, status):
        """更新进度条和状态"""
        self.progress_bar.setValue(value)
        self.status_label.setText(status)
        QApplication.processEvents()  # 确保UI更新
        
    def format_time(self, seconds):
        """格式化时间显示"""
        return f"{seconds:.2f}秒"
        
    def stop_and_process(self):
        """停止录音并处理音频"""
        self.stop_recording()
        
        if len(self.frames) > 0:
            start_time = time.time()
            process_times = {}
            
            # 保存录音 (5%)
            self.update_progress(5, '正在保存录音...')
            audio_file = self.save_recording()
            process_times['保存录音'] = time.time() - start_time
            
            # 语音识别 (30%)
            self.update_progress(30, '正在进行语音识别...')
            asr_start = time.time()
            text = self.convert_audio_to_text(audio_file)
            process_times['语音识别'] = time.time() - asr_start
            
            if text:
                self.chat_display.append(f"你说: {text}")
                
                # 调用 Coze 工作流 (60%)
                self.update_progress(60, '正在生成AI回复...')
                coze_start = time.time()
                response_text = self.call_coze_workflow(text)
                process_times['AI回复'] = time.time() - coze_start
                
                if response_text:
                    self.chat_display.append(f"AI: {response_text}")
                    
                    # 生成语音回复 (90%)
                    self.update_progress(90, '正在生成语音...')
                    tts_start = time.time()
                    speech_file = self.text_to_speech(response_text)
                    process_times['语音合成'] = time.time() - tts_start
                    
                    if speech_file:
                        # 播放语音 (100%)
                        self.update_progress(100, '正在播放回复...')
                        play_start = time.time()
                        self.play_audio(speech_file)
                        process_times['语音播放'] = time.time() - play_start
                        
                        # 显示各阶段处理时间
                        time_info = "处理时间统计:\n"
                        for stage, t in process_times.items():
                            time_info += f"{stage}: {self.format_time(t)}\n"
                        time_info += f"总耗时: {self.format_time(time.time() - start_time)}"
                        self.process_time_label.setText(time_info)
                        
                        self.update_progress(0, '等待录音...')
                    else:
                        self.update_progress(0, '语音生成失败')
                else:
                    self.update_progress(0, '获取回复失败')
            else:
                self.update_progress(0, '语音识别失败')
        else:
            self.update_progress(0, '未检测到有效录音')
            
    def convert_audio_to_text(self, audio_file_path):
        """使用 ASR API 将音频文件转换为文字"""
        url = "https://api.siliconflow.cn/v1/audio/transcriptions"
        
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
            
    def call_coze_workflow(self, text):
        """调用 Coze 工作流处理文本"""
        try:
            coze = Coze(
                auth=TokenAuth(token=COZE_API_TOKEN),
                base_url=COZE_CN_BASE_URL
            )
            
            response = coze.workflows.runs.create(
                workflow_id=WORKFLOW_ID,
                parameters={"text": text}
            )
            
            if response and response.data:
                if isinstance(response.data, str):
                    try:
                        data = json.loads(response.data)
                        return data.get('data', '')
                    except json.JSONDecodeError:
                        return response.data
                elif isinstance(response.data, dict):
                    return response.data.get('data', '')
            return None
        except Exception as e:
            print(f"Coze 工作流调用失败: {str(e)}")
            return None
            
    def text_to_speech(self, text):
        """使用 TTS API 将文本转换为语音"""
        try:
            if not os.path.exists('output'):
                os.makedirs('output')
                
            speech_file_path = Path("output") / "response.wav"
            
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
            
            response = requests.post(url, headers=headers, json=data, stream=True)
            response.raise_for_status()
            
            with open(speech_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return str(speech_file_path)
        except Exception as e:
            print(f"TTS API 调用失败: {str(e)}")
            return None
            
    def play_audio(self, audio_file_path):
        """使用 pygame 播放音频文件"""
        try:
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"音频播放失败: {str(e)}")

def main():
    app = QApplication(sys.argv)
    assistant = VoiceAssistant()
    assistant.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 