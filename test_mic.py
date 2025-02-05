import sys
import pyaudio
import wave
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from threading import Thread

class AudioRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # 音频参数设置
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.recording = False
        self.frames = []
        self.p = None
        self.stream = None
        self.recording_time = 0
        
        # 创建定时器用于更新录音时长显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.setInterval(100)  # 每100ms更新一次
        
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('录音程序')
        self.setGeometry(300, 300, 300, 200)
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建录音按钮
        self.record_button = QPushButton('按住开始录音', self)
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_recording)
        
        # 创建时间显示标签
        self.time_label = QLabel('0.0 秒', self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建状态显示标签
        self.status_label = QLabel('等待录音...', self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加部件到布局
        layout.addWidget(self.record_button)
        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        
    def update_time(self):
        """更新录音时长显示"""
        self.recording_time += 0.1
        self.time_label.setText(f'{self.recording_time:.1f} 秒')
        
    def record_thread(self):
        """录音线程"""
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        
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
        
        # 启动录音线程
        self.record_thread = Thread(target=self.record_thread)
        self.record_thread.start()
        
        # 启动定时器
        self.timer.start()
        
    def stop_recording(self):
        """停止录音"""
        if not self.recording:
            return
            
        self.recording = False
        self.timer.stop()
        
        # 等待录音线程结束
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
        
        # 停止并关闭音频流
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.p:
            self.p.terminate()
        
        # 更新界面状态
        self.status_label.setText('录音结束')
        self.record_button.setText('按住开始录音')
        
        # 保存录音
        if len(self.frames) > 0:
            self.save_recording()
        else:
            self.status_label.setText('未检测到有效录音')
            
    def save_recording(self):
        """保存录音文件"""
        # 确保input目录存在
        if not os.path.exists('input'):
            os.makedirs('input')
            
        # 保存录音文件
        output_file = "input/recording.wav"
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        self.status_label.setText(f'录音已保存到: {output_file}')

def main():
    app = QApplication(sys.argv)
    recorder = AudioRecorder()
    recorder.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 