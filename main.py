"""
Manim Android Application
Renders Manim scenes on Android devices with Kivy UI
"""

import os
import sys
import threading
import subprocess
import json
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Set window size for better UI
Window.size = (540, 960)

# Default Manim scene for demonstration
DEFAULT_CODE = """
from manim import *

class AndroidDemo(Scene):
    def construct(self):
        # Create shapes
        circle = Circle(color=BLUE, radius=1)
        square = Square(color=RED, side_length=2)
        text = Text("Manim on Android!", font_size=40, color=WHITE)
        
        # Add background
        background = Rectangle(width=14, height=8, color=BLACK, fill_opacity=0.8)
        self.add(background)
        
        # Animations
        self.play(Create(circle), run_time=1)
        self.wait(0.5)
        self.play(Transform(circle, square), run_time=1.5)
        self.wait(0.5)
        self.play(Write(text), run_time=2)
        self.wait(2)
"""


class ManimAndroidApp(App):
    """
    Main Manim Android Application
    
    Features:
    - Code editor for writing Manim scenes
    - Real-time rendering with status updates
    - Video playback of rendered animations
    - Error reporting with detailed logs
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Manim Android"
        self.rendering = False
        self.last_video_path = None
        
    def build(self):
        """Build the Kivy UI"""
        # Main container
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ========== TITLE ==========
        title = Label(
            text='[b]Manim Animation Studio[/b]',
            markup=True,
            size_hint_y=0.05,
            font_size='18sp'
        )
        main_layout.add_widget(title)
        
        # ========== CODE EDITOR ==========
        code_label = Label(text='Code Editor:', size_hint_y=0.02, font_size='12sp')
        main_layout.add_widget(code_label)
        
        self.code_input = TextInput(
            text=DEFAULT_CODE,
            size_hint_y=0.35,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0.9, 0.9, 0.9, 1),
            font_size='10sp'
        )
        main_layout.add_widget(self.code_input)
        
        # ========== CONTROL BUTTONS ==========
        button_layout = GridLayout(cols=3, size_hint_y=0.08, spacing=10)
        
        render_btn = Button(text='[b]RENDER[/b]', markup=True, background_color=(0.2, 0.6, 0.2, 1))
        render_btn.bind(on_press=self.on_render_pressed)
        button_layout.add_widget(render_btn)
        
        clear_btn = Button(text='Clear', background_color=(0.6, 0.2, 0.2, 1))
        clear_btn.bind(on_press=self.on_clear_pressed)
        button_layout.add_widget(clear_btn)
        
        reset_btn = Button(text='Reset Demo', background_color=(0.2, 0.2, 0.6, 1))
        reset_btn.bind(on_press=self.on_reset_pressed)
        button_layout.add_widget(reset_btn)
        
        self.render_btn = render_btn  # Store reference to disable during rendering
        main_layout.add_widget(button_layout)
        
        # ========== STATUS DISPLAY ==========
        status_label = Label(text='Status: Ready', size_hint_y=0.02, font_size='11sp')
        self.status_label = status_label
        main_layout.add_widget(status_label)
        
        # ========== VIDEO PLAYER ==========
        video_label = Label(text='Preview:', size_hint_y=0.02, font_size='12sp')
        main_layout.add_widget(video_label)
        
        self.video_player = Video(
            size_hint_y=0.4,
            options={'eos': 'loop'},
            state='pause'
        )
        main_layout.add_widget(self.video_player)
        
        # ========== INFO FOOTER ==========
        info_layout = BoxLayout(size_hint_y=0.08, orientation='vertical')
        
        info_text = Label(
            text='💡 Tip: Use low quality (-ql) and fewer frames for fast rendering',
            size_hint_y=0.5,
            font_size='10sp'
        )
        info_layout.add_widget(info_text)
        
        file_info = Label(text='Files saved to: {}/media'.format(self.user_data_dir), size_hint_y=0.5, font_size='9sp')
        self.file_info_label = file_info
        info_layout.add_widget(file_info)
        
        main_layout.add_widget(info_layout)
        
        return main_layout

    def on_render_pressed(self, instance):
        """Handle render button press"""
        if self.rendering:
            self.show_error("Already rendering! Please wait...")
            return
        
        code = self.code_input.text.strip()
        if not code:
            self.show_error("Code editor is empty!")
            return
        
        self.status_label.text = "Status: Rendering (this may take time)..."
        self.render_btn.disabled = True
        
        # Run rendering in background thread
        thread = threading.Thread(target=self.render_animation, args=(code,))
        thread.daemon = True
        thread.start()

    def on_clear_pressed(self, instance):
        """Clear code editor"""
        self.code_input.text = ""
        self.status_label.text = "Status: Code cleared"

    def on_reset_pressed(self, instance):
        """Reset to demo code"""
        self.code_input.text = DEFAULT_CODE
        self.status_label.text = "Status: Demo code loaded"

    def render_animation(self, code):
        """
        Render Manim animation in background thread
        
        Args:
            code (str): Python code containing Manim scene
        """
        self.rendering = True
        
        try:
            # Create working directory
            work_dir = os.path.join(self.user_data_dir, 'render_session')
            os.makedirs(work_dir, exist_ok=True)
            
            # Save code to temporary script
            script_path = os.path.join(work_dir, 'scene.py')
            with open(script_path, 'w') as f:
                # Add necessary imports if not present
                if 'from manim import' not in code:
                    f.write('from manim import *\n\n')
                f.write(code)
            
            # Log the script for debugging
            self.log_message(f"Script saved to: {script_path}")
            
            # Extract scene class name from code
            scene_name = self.extract_scene_name(code)
            if not scene_name:
                raise ValueError("Could not find a Scene class in the code!")
            
            self.log_message(f"Rendering scene: {scene_name}")
            
            # Manim command with conservative settings for Android
            # -ql = low quality (480p, 15fps)
            # -p = open in player after rendering
            # --disable_caching = avoid disk cache issues on mobile
            cmd = [
                sys.executable, '-m', 'manim',
                '-ql',  # Low quality for faster rendering
                '--disable_caching',
                '-o', 'output',
                script_path,
                scene_name
            ]
            
            self.log_message(f"Running command: {' '.join(cmd)}")
            
            # Execute manim
            process = subprocess.Popen(
                cmd,
                cwd=work_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Capture output
            stdout, stderr = process.communicate()
            
            self.log_message("=== MANIM OUTPUT ===")
            if stdout:
                self.log_message(stdout)
            if stderr:
                self.log_message(f"STDERR: {stderr}")
            
            if process.returncode != 0:
                raise RuntimeError(f"Manim failed with return code {process.returncode}\n{stderr}")
            
            # Find rendered video
            video_path = self.find_video_file(work_dir)
            if not video_path:
                raise FileNotFoundError("No video file found after rendering!")
            
            self.log_message(f"Video found: {video_path}")
            self.last_video_path = video_path
            
            # Update UI in main thread
            Clock.schedule_once(lambda dt: self.on_render_success(video_path), 0)
            
        except Exception as e:
            error_msg = f"Render Error: {str(e)}"
            self.log_message(f"ERROR: {error_msg}")
            Clock.schedule_once(lambda dt: self.show_error(error_msg), 0)
            
        finally:
            self.rendering = False
            Clock.schedule_once(lambda dt: self._enable_render_button(), 0)

    def on_render_success(self, video_path):
        """Handle successful render"""
        if os.path.exists(video_path):
            self.video_player.source = video_path
            self.video_player.state = 'play'
            self.status_label.text = f"✓ Render successful! ({os.path.getsize(video_path) / 1024:.1f} KB)"
        else:
            self.show_error("Video file not found at specified path!")

    def _enable_render_button(self):
        """Re-enable render button"""
        self.render_btn.disabled = False

    @staticmethod
    def extract_scene_name(code):
        """
        Extract first Scene class name from code
        
        Args:
            code (str): Python code
            
        Returns:
            str: Scene class name or None
        """
        import re
        # Match: class SomeName(Scene):
        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
        return match.group(1) if match else None

    @staticmethod
    def find_video_file(root_dir):
        """
        Recursively find video file in directory tree
        Manim creates: media/videos/scene_name/480p15/output.mp4
        
        Args:
            root_dir (str): Root directory to search
            
        Returns:
            str: Path to video file or None
        """
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(('.mp4', '.webm', '.mov')):
                    return os.path.join(root, file)
        return None

    def show_error(self, message):
        """Display error message in status label"""
        self.status_label.text = f"✗ {message}"

    def log_message(self, message):
        """Log message to file for debugging"""
        log_dir = os.path.join(self.user_data_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'manim.log')
        try:
            with open(log_file, 'a') as f:
                f.write(message + '\n')
        except Exception:
            pass  # Silent fail for logging


if __name__ == '__main__':
    app = ManimAndroidApp()
    app.run()
    