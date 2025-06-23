#!/usr/bin/env python3

import sys
import json
import os
from pathlib import Path
from PyQt5 import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QGridLayout, 
                           QScrollArea, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt as QtCore
from PyQt5.QtGui import QPixmap

# Set Qt platform plugin path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(Qt.__file__), "Qt", "plugins")


class LLMResultViewer(QMainWindow):
    def __init__(self, results_file):
        super().__init__()
        self.setWindowTitle("RoboSense LLM Results Viewer")
        self.setGeometry(100, 100, 1600, 900)
        
        # Load results data
        with open(results_file, 'r') as f:
            self.results = json.load(f)
        self.current_index = 0
        self.total_results = len(self.results)
        
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Navigation panel
        nav_panel = QWidget()
        nav_layout = QHBoxLayout(nav_panel)
        
        # Previous button
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.show_previous)
        nav_layout.addWidget(self.prev_btn)
        
        # Index display and input
        index_widget = QWidget()
        index_layout = QHBoxLayout(index_widget)
        
        # Current index spinbox
        self.index_spinbox = QSpinBox()
        self.index_spinbox.setRange(0, self.total_results - 1)
        self.index_spinbox.setValue(0)
        self.index_spinbox.valueChanged.connect(self.on_index_changed)
        index_layout.addWidget(self.index_spinbox)
        
        # Total count label
        total_label = QLabel(f"/ {self.total_results - 1}")
        index_layout.addWidget(total_label)
        
        nav_layout.addWidget(index_widget)
        
        # Next button
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.show_next)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addWidget(nav_panel)
        
        # Image display area
        image_widget = QWidget()
        self.image_layout = QGridLayout(image_widget)
        
        # Create image labels for 6 views
        self.image_labels = {}
        camera_names = ['CAM_FRONT', 'CAM_FRONT_RIGHT', 'CAM_FRONT_LEFT',
                       'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_BACK_LEFT']
        positions = [(0,1), (0,2), (0,0), (1,1), (1,2), (1,0)]
        
        for cam, pos in zip(camera_names, positions):
            label = QLabel()
            label.setFixedSize(400, 225)  # 16:9 aspect ratio
            label.setAlignment(QtCore.AlignCenter)
            self.image_labels[cam] = label
            self.image_layout.addWidget(label, *pos)
            
        main_layout.addWidget(image_widget)
        
        # QA display
        qa_widget = QWidget()
        qa_layout = QVBoxLayout(qa_widget)
        
        # Category label
        self.category_label = QLabel()
        self.category_label.setStyleSheet("QLabel { font-weight: bold; font-size: 14px; }")
        qa_layout.addWidget(self.category_label)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; }")
        qa_layout.addWidget(self.question_label)
        
        # Answer label
        self.answer_label = QLabel()
        self.answer_label.setWordWrap(True)
        self.answer_label.setStyleSheet("QLabel { background-color: #e0e0e0; padding: 10px; }")
        qa_layout.addWidget(self.answer_label)
        
        scroll = QScrollArea()
        scroll.setWidget(qa_widget)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        # Initialize the first result
        self.update_display()
        
    def update_display(self):
        result = self.results[self.current_index]
        
        # Update images
        for cam_name, label in self.image_labels.items():
            img_path = result['img_paths'][cam_name]
            # Make path absolute if relative
            if not os.path.isabs(img_path):
                img_path = os.path.join(os.getcwd(), img_path)
            
            pixmap = QPixmap(img_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(label.size(), QtCore.KeepAspectRatio, QtCore.SmoothTransformation)
                label.setPixmap(scaled_pixmap)
            else:
                label.setText(f"Failed to load\n{img_path}")
        
        # Update QA display
        self.category_label.setText(f"Category: {result['category'].upper()}")
        self.question_label.setText(f"Q: {result['question']}")
        self.answer_label.setText(f"A: {result['answer']}")
        
        # Update index display
        self.index_spinbox.setValue(self.current_index)
        
        # Update button states
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < self.total_results - 1)
        
    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()
            
    def show_next(self):
        if self.current_index < self.total_results - 1:
            self.current_index += 1
            self.update_display()
            
    def on_index_changed(self, new_index):
        if 0 <= new_index < self.total_results and new_index != self.current_index:
            self.current_index = new_index
            self.update_display()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python visual.py <results_json_file>")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    window = LLMResultViewer(sys.argv[1])
    window.show()
    sys.exit(app.exec_())
