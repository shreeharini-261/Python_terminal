# 🚀 Interactive Portfolio Terminal

> A unique web-based terminal application that combines personal portfolio presentation with system command execution capabilities.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)


## 📋 Overview

**Interactive Portfolio Terminal** is a creative and technical showcase that presents my professional portfolio through an authentic terminal interface. This innovative application merges personal branding with technical functionality, offering visitors an engaging way to explore professional background, skills, and projects while maintaining the familiar feel of a command-line environment.

### ✨ Why a Terminal Portfolio?

- **Unique Experience**: Stand out with an interactive, developer-focused presentation
- **Technical Showcase**: Demonstrates full-stack development skills and creativity
- **Authentic Feel**: Real terminal functionality with portfolio integration
- **Professional Impact**: Memorable way to present technical expertise

## 🌟 Features

### 📋 Portfolio Commands
- **`about`** - Learn about background and expertise in AI/ML
- **`resume`** - Direct link to downloadable resume
- **`skills`** - Technical skills including Python, TensorFlow, AWS, and more
- **`projects`** - Showcase of top projects with GitHub links
- **`contact`** - Professional contact information and social links
- **`education`** - Academic background and certifications
- **`experience`** - Professional work experience and internships
- **`achievements`** - Awards, hackathon wins, and recognitions
- **`date`** - Current date and time
- **`echo [text]`** - Echo functionality with custom messages

### 💻 System Commands
- **File Operations**: `ls`, `pwd`, `cat`, `head`, `tail`
- **Process Info**: `ps`, `top`, `jobs`
- **System Stats**: `df`, `du`, `free`, `uptime`, `uname`
- **Network Utils**: `ping`, `host`, `nslookup` (limited)
- **Monitoring**: `sysinfo` - Detailed system information with psutil

### 🔒 Security Features
- **Command Allowlist**: Only safe, read-only commands permitted
- **Input Sanitization**: Protection against command injection
- **CORS Protection**: Restricted to localhost origins
- **Timeout Controls**: 15-second timeout for system commands
- **Path Restrictions**: Limited file access for security

### 🎨 User Experience
- **Authentic Terminal**: Black background with green monospace text
- **Command History**: Navigate with ↑/↓ arrow keys
- **Auto-complete**: Tab completion for commands
- **Responsive Design**: Works on desktop and mobile
- **Real-time Execution**: Instant command processing

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd interactive-portfolio-terminal
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-cors psutil
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the terminal**
   Open your browser and navigate to `http://localhost:5000`


## 📖 Usage Guide

### Getting Started
1. **Welcome Screen**: You'll see a welcome message with available commands
2. **Help Command**: Type `help` for a comprehensive command list
3. **Portfolio Exploration**: Start with `about` to learn about Shreeharini
4. **Project Showcase**: Use `projects` to see top development work
5. **Contact Info**: Type `contact` for professional contact details

### Example Session
```bash
visitor@portfolio:~$ about
I am a passionate Machine Learning Engineer and AI researcher with expertise in computer vision, NLP, and full-stack development...

visitor@portfolio:~$ skills
💻 Technical Skills:
Python (NumPy, Pandas, TensorFlow, PyTorch, Scikit-learn), SQL, Java, Flask, FastAPI, OpenCV, YOLO, Vision Transformers...

visitor@portfolio:~$ projects
🔥 **My Top Projects:**

1. **Eco Route Optimizer** - ML-powered eco-aware route optimization system using Google Cloud APIs
   🌐: https://github.com/shreeharini-261/Eco_Route_Optimizer

visitor@portfolio:~$ ls -la
total 56
drwxr-xr-x 1 runner runner   210 Sep 21 04:29 .
drwxrwxrwx 1 runner runner    46 Sep 21 03:56 ..
-rw-r--r-- 1 runner runner 14379 Sep 21 04:29 main.py
...

visitor@portfolio:~$ echo "Impressive portfolio!"
Impressive portfolio!
```

## 🛠️ Technical Architecture

### Backend (Flask)
- **Framework**: Flask 3.1.2 with CORS support
- **Security**: Command allowlist with input sanitization
- **Process Management**: Subprocess execution with timeout controls
- **System Monitoring**: psutil integration for system stats
- **Portfolio Data**: Structured dictionary with personal information

### Frontend (Vanilla JavaScript)
- **Terminal Emulation**: CSS Grid layout with monospace fonts
- **Command Processing**: Fetch API for backend communication
- **History Management**: Local storage for command history
- **UI/UX**: Responsive design with terminal aesthetics
- **Error Handling**: Graceful error display and status codes

### File Structure
```
interactive-portfolio-terminal/
├── main.py                 # Flask application and portfolio logic
├── templates/
│   └── index.html         # Terminal interface template
├── static/
│   └── style.css          # Terminal styling and responsive design
├── README.md              # Project documentation
└── replit.md              # Replit-specific configuration
```

## 🎯 Portfolio Highlights

### Professional Background
- **Current**: B.Tech in Artificial Intelligence (CGPA: 9.3/10.0)
- **Experience**: ML Engineer internships at Caprae Capital and Hyperverge Nexus
- **Leadership**: Technical Club Head at NextGenAI

### Key Achievements
- 🥇 **NASA Impact Hackathon Winner** - Coral reef habitat modeling
- 🎤 **AAIMB 2024 Conference Presenter** - RAG vs LLMs research
- 💻 **90% Accuracy** - Deepfake detection model development

### Technical Expertise
- **AI/ML**: TensorFlow, PyTorch, Computer Vision, NLP
- **Cloud Platforms**: AWS, Google Cloud Platform
- **Development**: Python, Flask, FastAPI, PostgreSQL
- **Specialized**: YOLO, Vision Transformers, HuggingFace

## 🔗 Links and Contact

- **Portfolio Terminal**: [Live Demo](your-replit-url)
- **GitHub**: [github.com/shreeharini-261](https://github.com/shreeharini-261)
- **LinkedIn**: [linkedin.com/in/shreeharini-s](https://linkedin.com/in/shreeharini-s)
- **Email**: shreeharini261@gmail.com
- **Resume**: [Download PDF](https://drive.google.com/file/d/1VX4AFT_gJGYr4WUpj6tzu7sa9qMnjOe3/view?usp=sharing)

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are welcome! If you'd like to create your own portfolio terminal:

1. Fork this repository
2. Update the `portfolio_data` dictionary in `main.py` with your information
3. Customize the styling in `static/style.css`
4. Deploy on your preferred platform

## 🙏 Acknowledgments

- **Inspiration**: Classic Unix terminals and developer culture
- **Design**: Modern terminal emulators and developer tools
- **Technical Stack**: Flask community and Python ecosystem
