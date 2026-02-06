#!/usr/bin/env python3
"""
Manim Android Application
Runs Manim animations on Android devices using Kivy framework
"""

import os
import sys
from pathlib import Path

# Configure Kivy before importing
os.environ['KIVY_WINDOW'] = 'pygame'
os.environ['KIVY_HIDESHOW'] = '1'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window

import logging

# Configure window
Window.size = (1080, 1920)
Window.soft_input_mode = 'below_target'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try importing Manim components
try:
    from manim import *
    MANIM_AVAILABLE = True
    logger.info("✅ Manim imported successfully")
except ImportError as e:
    MANIM_AVAILABLE = False
    logger.warning(f"⚠️ Manim not available: {e}")

try:
    import numpy as np
    logger.info("✅ NumPy imported successfully")
except ImportError:
    logger.warning("⚠️ NumPy not available")

try:
    import matplotlib.pyplot as plt
    logger.info("✅ Matplotlib imported successfully")
except ImportError:
    logger.warning("⚠️ Matplotlib not available")


class ManimAndroidApp(App):
    """Main Manim Android Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Manim for Android'
        self.log_messages = []
        
    def build(self):
        """Build the application UI"""
        logger.info("Building application UI...")
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='🎬 Manim Animation Engine\nAndroid Version',
            size_hint_y=0.15,
            font_size='22sp'
        )
        main_layout.add_widget(header)
        
        # Status box
        status_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        
        manim_status = "✅ Available" if MANIM_AVAILABLE else "❌ Not Available"
        status_text = f"Manim: {manim_status}\nPython {sys.version.split()[0]}"
        
        status_label = Label(
            text=status_text,
            size_hint_y=0.5,
            font_size='14sp'
        )
        status_layout.add_widget(status_label)
        
        # Main status button
        status_button = Button(
            text='Check Dependencies',
            size_hint_y=0.5
        )
        status_button.bind(on_press=self.check_dependencies)
        status_layout.add_widget(status_button)
        
        main_layout.add_widget(status_layout)
        
        # Scrollable log area
        log_scroll = ScrollView(size_hint_y=0.4)
        self.log_label = Label(
            text='[System Logs]\n\n',
            size_hint_y=None,
            markup=True,
            font_size='12sp'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        log_scroll.add_widget(self.log_label)
        main_layout.add_widget(log_scroll)
        
        # Buttons layout
        buttons_layout = GridLayout(cols=2, size_hint_y=0.25, spacing=5)
        
        # Test render button
        test_button = Button(text='🎬 Test Render')
        test_button.bind(on_press=self.test_render)
        buttons_layout.add_widget(test_button)
        
        # Dependencies button
        deps_button = Button(text='📦 Dependencies')
        deps_button.bind(on_press=self.show_dependencies)
        buttons_layout.add_widget(deps_button)
        
        # Clear logs button
        clear_button = Button(text='🗑️ Clear Logs')
        clear_button.bind(on_press=self.clear_logs)
        buttons_layout.add_widget(clear_button)
        
        # Exit button
        exit_button = Button(text='❌ Exit')
        exit_button.bind(on_press=self.exit_app)
        buttons_layout.add_widget(exit_button)
        
        main_layout.add_widget(buttons_layout)
        
        self.add_log("Application started successfully")
        return main_layout
    
    def add_log(self, message):
        """Add message to log"""
        self.log_messages.append(message)
        # Keep only last 50 messages
        if len(self.log_messages) > 50:
            self.log_messages.pop(0)
        
        log_text = "[System Logs]\n\n" + "\n".join(self.log_messages)
        self.log_label.text = log_text
    
    def clear_logs(self, instance):
        """Clear log messages"""
        self.log_messages = []
        self.log_label.text = "[System Logs]\n\n"
        self.add_log("Logs cleared")
    
    def check_dependencies(self, instance):
        """Check and display dependency status"""
        logger.info("Checking dependencies...")
        self.add_log("🔍 Checking dependencies...")
        
        deps = {
            'Manim': MANIM_AVAILABLE,
            'NumPy': self.check_import('numpy'),
            'SciPy': self.check_import('scipy'),
            'Matplotlib': self.check_import('matplotlib'),
            'Pillow': self.check_import('PIL'),
            'SymPy': self.check_import('sympy'),
            'OpenCV': self.check_import('cv2'),
            'Kivy': self.check_import('kivy'),
        }
        
        for name, available in deps.items():
            status = "✅" if available else "❌"
            self.add_log(f"{status} {name}")
            logger.info(f"{name}: {'Available' if available else 'Not available'}")
    
    def show_dependencies(self, instance):
        """Show detailed dependencies"""
        logger.info("Showing detailed dependencies...")
        self.check_dependencies(instance)
        self.add_log("")
        self.add_log("📋 Python Packages:")
        
        try:
            import numpy
            self.add_log(f"  NumPy: {numpy.__version__}")
        except ImportError:
            pass
        
        try:
            import scipy
            self.add_log(f"  SciPy: {scipy.__version__}")
        except ImportError:
            pass
        
        try:
            import matplotlib
            self.add_log(f"  Matplotlib: {matplotlib.__version__}")
        except ImportError:
            pass
    
    @staticmethod
    def check_import(module_name):
        """Check if module can be imported"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    def test_render(self, instance):
        """Test rendering with Manim"""
        logger.info("Starting test render...")
        self.add_log("")
        self.add_log("🎬 Starting test render...")
        
        if not MANIM_AVAILABLE:
            self.add_log("❌ Manim not available - cannot render")
            logger.error("Manim not available")
            return
        
        try:
            self.add_log("⏳ Rendering circle animation...")
            logger.info("Rendering simple circle animation")
            
            # Simple test: create a basic animation
            # This would normally render to a video file
            self.add_log("✅ Test render would complete here")
            self.add_log("📌 Full animations require more setup")
            
            logger.info("Test render simulation completed")
        except Exception as e:
            error_msg = f"❌ Render failed: {str(e)}"
            self.add_log(error_msg)
            logger.error(f"Render failed: {e}", exc_info=True)
    
    def exit_app(self, instance):
        """Exit application"""
        logger.info("Exiting application...")
        self.add_log("👋 Exiting application...")
        self.stop()


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Manim Android Application Starting")
    logger.info("=" * 60)
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    
    app = ManimAndroidApp()
    app.run()
    