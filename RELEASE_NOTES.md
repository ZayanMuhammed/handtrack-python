# 📝 Release Notes

All notable changes to the HandTrack Python project will be documented in this file.

---

## [1.0.0] - 2026-02-01

### ✨ Features
- **Hand Gesture Recognition** - Real-time detection of hand landmarks using MediaPipe AI
- **Cursor Control** - Index finger position controls mouse pointer with smoothing
- **Click & Drag** - Pinch gesture (index + thumb) for left-click and drag operations
- **Double Click** - Rapid successive pinches trigger double-click events
- **Scroll Control** - Fist gesture with vertical movement for smooth scrolling
- **Hotkey Support** - Middle finger down triggers Windows Hide (Win+H) command
- **Performance Optimization** - Intelligent cursor smoothing with configurable acceleration
- **Visual Feedback** - Hand skeleton overlay on video feed for real-time guidance

### 🛠️ Technical Details
- Built with Python 3.9+
- Powered by OpenCV for video processing
- MediaPipe Hands for AI-driven landmark detection
- PyAutoGUI for cross-platform cursor/keyboard control
- Windows API integration for native screen metrics

### 📋 Configuration Options
- Adjustable detection confidence thresholds
- Customizable cursor smoothing factor
- Tunable gesture detection distances
- Configurable scroll cooldown timers

### 🎮 Gesture Table
| Gesture | Action | Sensitivity |
|---------|--------|-------------|
| Index Finger | Cursor Position | Real-time |
| Pinch (Index+Thumb) | Click/Drag | 40px distance |
| Double Pinch | Double Click | 0.5s window |
| Fist + Move | Scroll | 0.15s cooldown |
| Middle Finger Down | Win+H Hotkey | 1s cooldown |

### 🐛 Known Issues
- Performance depends on webcam quality and lighting conditions
- Single hand tracking mode (multi-hand support coming soon)
- Windows-only for hotkey functionality
- May require calibration for different hand sizes

### 📦 Dependencies
- `opencv-python` (cv2)
- `mediapipe=0.10.9`
- `pyautogui`
- `protobuf=3.20.3`

### 🚀 Performance Notes
- Average detection latency: 16-33ms (30-60 FPS)
- CPU usage: 15-25% on modern processors
- GPU acceleration supported with CUDA-enabled OpenCV

---

## [0.9.0] - 2026-01-20

### 🎯 Initial Release Candidate
- Core hand tracking functionality
- Basic gesture recognition
- Cursor movement and clicking
- Early testing phase

### ⚠️ Limitations
- Limited gesture vocabulary
- No multi-hand support
- Gesture recognition needs refinement

---

## 🗺️ Roadmap

### Planned for v1.1.0
- [ ] Multi-hand gesture support
- [ ] Gesture customization UI
- [ ] Hand pose classification (open/closed/peace)
- [ ] Gesture recording and playback
- [ ] Performance metrics dashboard

### Planned for v1.2.0
- [ ] Cross-platform support (macOS, Linux)
- [ ] Virtual keyboard overlay
- [ ] Advanced hand pose recognition
- [ ] Machine learning gesture training
- [ ] Plugin system for custom gestures

### Planned for v2.0.0
- [ ] Mobile app support
- [ ] Cloud-based gesture library
- [ ] Real-time collaboration
- [ ] Advanced AI pose estimation
- [ ] Full accessibility suite

---

## 📞 Support

For issues, bug reports, or feature requests, please open an issue on the project repository.

---

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated:** February 1, 2026
