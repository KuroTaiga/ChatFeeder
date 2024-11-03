import tkinter as tk
from tkinter import ttk
import cv2
import os
import mediapipe as mp
import numpy as np
from typing import Set, Dict, List, Tuple
from PIL import Image, ImageTk

class EnhancedPoseDebugTool:
    def __init__(self, video_folder: str, blender_folder: str, custom_folder: str  = "../custom_video",custom_model: str = "../custom_model"):
        """
        Initialize the enhanced debug tool with GUI controls
        
        Args:
            video_folder (str): Path to folder containing video files
        """
        self.video_folder = video_folder
        self.blender_folder = blender_folder

        self.custom_video_folder = custom_folder
        os.makedirs(custom_folder, exist_ok=True)

        self.custom_model_dir = custom_model
        os.makedirs(custom_model,exist_ok=True)

        self.selected_landmarks: Set[int] = set()
        self.is_paused = False
        self.current_speed = 1.0
        self.frame_size = (640, 480)  # Default size, will be updated
        # mediapipe lanmarks
        self.landmark_names = {
            0: "nose",
            1: "left eye (inner)",
            2: "left eye",
            3: "left eye (outer)",
            4: "right eye (inner)",
            5: "right eye",
            6: "right eye (outer)",
            7: "left ear",
            8: "right ear",
            9: "mouth (left)",
            10: "mouth (right)",
            11: "left shoulder",
            12: "right shoulder",
            13: "left elbow",
            14: "right elbow",
            15: "left wrist",
            16: "right wrist",
            17: "left pinky",
            18: "right pinky",
            19: "left index",
            20: "right index",
            21: "left thumb",
            22: "right thumb",
            23: "left hip",
            24: "right hip",
            25: "left knee",
            26: "right knee",
            27: "left ankle",
            28: "right ankle",
            29: "left heel",
            30: "right heel",
            31: "left foot index",
            32: "right foot index"
        }
        
        # MediaPipe initialization
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose_models = {
            "MediaPipe Pose": self.mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            ),
            "MediaPipe Pose (Performance)": self.mp_pose.Pose(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            ),
            "MediaPipe Pose (Accuracy)": self.mp_pose.Pose(
                model_complexity=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        }
        self.current_pose_model = "MediaPipe Pose"
        
        # Initialize GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI window and controls"""
        self.root = tk.Tk()
        self.root.title("Pose Estimation Debug Tool")
        
        # Configure grid weight
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)  # Landmark panel doesn't resize
        
        # Create main frames
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.video_container = ttk.Frame(self.root)
        self.video_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.video_container.grid_rowconfigure(0, weight=1)
        self.video_container.grid_rowconfigure(1, weight=1)
        self.video_container.grid_columnconfigure(0, weight=1)
        
        self.landmark_frame = ttk.Frame(self.root)
        self.landmark_frame.grid(row=1, column=1, sticky="ns", padx=5, pady=5)
        
        # Setup controls
        self.setup_control_panel()
        
        # Setup video display
        self.video_canvas = tk.Canvas(self.video_container, bg='black')
        self.video_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.landmark_canvas = tk.Canvas(self.video_container, bg='white')
        self.landmark_canvas.grid(row=1, column=0, sticky="nsew")
        
        # Setup landmark selection panel
        self.setup_landmark_panel()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)
        
    def setup_control_panel(self):
        """Setup the control panel with dropdowns and buttons"""
        # Model selection
        ttk.Label(self.control_frame, text="Model:").pack(side=tk.LEFT, padx=5)
        self.model_var = tk.StringVar(value="MediaPipe Pose")
        model_dropdown = ttk.Combobox(self.control_frame, 
                                    textvariable=self.model_var,
                                    values=list(self.pose_models.keys()),
                                    state="readonly")
        model_dropdown.pack(side=tk.LEFT, padx=5)
        model_dropdown.bind('<<ComboboxSelected>>', self.on_model_change)
        
        # Video selection
        ttk.Label(self.control_frame, text="Video:").pack(side=tk.LEFT, padx=5)
        self.video_var = tk.StringVar()
        video_list = [f for f in os.listdir(self.video_folder) if f.endswith('.mp4')]
        video_dropdown = ttk.Combobox(self.control_frame, 
                                    textvariable=self.video_var,
                                    values=video_list,
                                    state="readonly")
        video_dropdown.pack(side=tk.LEFT, padx=5)
        video_dropdown.bind('<<ComboboxSelected>>', self.on_video_change)
        
        # Playback speed
        ttk.Label(self.control_frame, text="Speed:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(value="1.0x")
        speed_dropdown = ttk.Combobox(self.control_frame,
                                    textvariable=self.speed_var,
                                    values=[0.25, 0.5, 1, 1.5, 2.0],
                                    state="readonly")
        speed_dropdown.pack(side=tk.LEFT, padx=5)
        speed_dropdown.bind('<<ComboboxSelected>>', self.on_speed_change)
        
        # Control buttons
        self.play_button = ttk.Button(self.control_frame, text="Play", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        
    def setup_landmark_panel(self):

        """Setup the panel for landmark selection with descriptive names"""
        # Create frame for landmark selection
        selection_frame = ttk.Frame(self.landmark_frame)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add title
        ttk.Label(selection_frame, text="Select Landmarks to Track:").pack()
        
        # Create listbox with scrollbar
        list_frame = ttk.Frame(selection_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.landmark_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            height=20,
            width=25
        )
        self.landmark_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.landmark_listbox.yview)
        
        # Add landmarks with descriptive names
        for idx in range(33):
            self.landmark_listbox.insert(
                tk.END, 
                f"{idx} - {self.landmark_names[idx]}"
            )
            
        self.landmark_listbox.bind('<<ListboxSelect>>', self.on_landmark_select)
        
        # Add "Select All" and "Clear All" buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Select All", 
            command=self.select_all_landmarks
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all_landmarks
        ).pack(side=tk.LEFT, padx=2)
    
    def select_all_landmarks(self):
        """Select all landmarks in the listbox"""
        self.landmark_listbox.selection_set(0, tk.END)
        self.selected_landmarks = set(range(33))

    def clear_all_landmarks(self):
        """Clear all landmark selections"""
        self.landmark_listbox.selection_clear(0, tk.END)
        self.selected_landmarks.clear()

    def create_landmark_video(self, frame: np.ndarray, results) -> np.ndarray:
        """Create a frame with pose landmarks, highlighting selected landmarks"""
        h, w = frame.shape[:2]
        landmark_frame = np.ones((h, w, 3), dtype=np.uint8) * 255
        
        if results.pose_landmarks:
            # Draw all landmarks and connections in gray
            self.mp_drawing.draw_landmarks(
                landmark_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(128, 128, 128), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(128, 128, 128), thickness=2)
            )
            
            # Highlight selected landmarks in red and add labels
            for idx in self.selected_landmarks:
                landmark = results.pose_landmarks.landmark[idx]
                pos = (int(landmark.x * w), int(landmark.y * h))
                
                # Draw larger red circle for selected landmark
                cv2.circle(landmark_frame, pos, 5, (0, 0, 255), -1)
                
                # Add landmark name as label
                label = self.landmark_names[idx]
                cv2.putText(
                    landmark_frame,
                    label,
                    (pos[0] + 10, pos[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1
                )
                
        return landmark_frame
        
    def on_window_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.root:
            # Update frame size
            canvas_width = self.video_canvas.winfo_width()
            canvas_height = self.video_canvas.winfo_height()
            if canvas_width > 1 and canvas_height > 1:  # Avoid invalid sizes
                self.frame_size = (canvas_width, canvas_height)
    
    def resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame to fit current window size while maintaining aspect ratio"""
        target_width, target_height = self.frame_size
        h, w = frame.shape[:2]
        
        # Calculate scaling factor to maintain aspect ratio
        scale = min(target_width/w, target_height/h)
        new_width = int(w * scale)
        new_height = int(h * scale)
        
        return cv2.resize(frame, (new_width, new_height))
    
    def on_model_change(self, event):
        """Handle model selection change"""
        self.current_pose_model = self.model_var.get()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.restart_video()
            
    def on_video_change(self, event):
        """Handle video selection change"""
        self.restart_video()
        
    def on_speed_change(self, event):
        """Handle playback speed change"""
        self.current_speed = float(self.speed_var.get().replace('x', ''))
        
    def on_landmark_select(self, event):
        """Handle landmark selection"""
        selection = self.landmark_listbox.curselection()
        self.selected_landmarks = set(selection)
        
    def toggle_play(self):
        """Toggle video playback"""
        self.is_paused = not self.is_paused
        self.play_button.config(text="Pause" if not self.is_paused else "Play")
        
    def reset(self):
        """Reset all selections and video"""
        self.landmark_listbox.selection_clear(0, tk.END)
        self.selected_landmarks.clear()
        self.restart_video()
        
    def restart_video(self):
        """Restart video playback"""
        if hasattr(self, 'cap'):
            self.cap.release()
        
        video_path = os.path.join(self.video_folder, self.video_var.get())
        self.cap = cv2.VideoCapture(video_path)
        
    def create_landmark_video(self, frame: np.ndarray, results) -> np.ndarray:
        """Create a frame with pose landmarks, highlighting selected landmarks"""
        h, w = frame.shape[:2]
        landmark_frame = np.ones((h, w, 3), dtype=np.uint8) * 255
        
        if results.pose_landmarks:
            # Draw all landmarks and connections
            self.mp_drawing.draw_landmarks(
                landmark_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(128, 128, 128), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(128, 128, 128), thickness=2)
            )
            
            # Highlight selected landmarks
            for idx in self.selected_landmarks:
                landmark = results.pose_landmarks.landmark[idx]
                pos = (int(landmark.x * w), int(landmark.y * h))
                cv2.circle(landmark_frame, pos, 5, (0, 0, 255), -1)
                
        return landmark_frame
    
    def update_canvas_image(self, canvas, image):
        """Update canvas with resized image"""
        # Convert CV2 frame to PhotoImage
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = self.resize_frame(image)
        photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        
        # Update canvas
        canvas.delete("all")
        canvas.create_image(
            self.frame_size[0]//2,
            self.frame_size[1]//2,
            image=photo,
            anchor="center"
        )
        canvas.image = photo  # Keep reference
        
    def update(self):
        """Update video frames and process pose estimation"""
        if hasattr(self, 'cap') and self.cap.isOpened() and not self.is_paused:
            ret, frame = self.cap.read()
            
            if ret:
                # Process frame with MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose_models[self.current_pose_model].process(frame_rgb)
                
                # Create landmark visualization
                landmark_frame = self.create_landmark_video(frame, results)
                
                # Update canvases
                self.update_canvas_image(self.video_canvas, frame)
                self.update_canvas_image(self.landmark_canvas, landmark_frame)
            else:
                # Restart video when it ends
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Schedule next update
        self.root.after(int(1000/30/self.current_speed), self.update)
        
    def run(self):
        """Start the application"""
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Start update loop
        self.update()
        self.root.mainloop()
        
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'cap'):
            self.cap.release()
        for model in self.pose_models.values():
            model.close()

if __name__ == "__main__":
    video_folder = "../real_video"  # Update this path as needed
    blender_folder= "../blender_video"
    app = EnhancedPoseDebugTool(video_folder,blender_folder)
    app.run()