#!/usr/bin/env python3
"""
Interactive Portfolio Terminal - Flask Backend
A secure web terminal that executes both portfolio commands and system commands through a Flask API.
"""

import subprocess
import re
import psutil
import shlex
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'default-dev-key')

# Security: Restrict CORS to localhost only in development
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

# Portfolio data dictionary with personal information
portfolio_data = {
    "about":
    "I am a passionate Machine Learning Engineer and AI researcher with expertise in computer vision, NLP, and full-stack development. I have a proven track record of delivering innovative AI solutions in deepfake detection, document summarization, and secure payment systems with measurable impact. Currently pursuing B.Tech in Artificial Intelligence at SRM Institute of Science and Technology with a 9.3/10.0 CGPA.",
    "resume":
    "https://drive.google.com/file/d/1VX4AFT_gJGYr4WUpj6tzu7sa9qMnjOe3/view?usp=sharing",
    "skills":
    "Python (NumPy, Pandas, TensorFlow, PyTorch, Scikit-learn), SQL, Flask, OpenCV, YOLO, Vision Transformers, HuggingFace, Git, Figma",
    "projects":
    """🔥 My Top Projects:

1. Eco Route Optimizer- ML-powered eco-aware route optimization system using Google Cloud APIs
   🌐: https://github.com/shreeharini-261/Eco_Route_Optimizer

2. RAG Chatbot- Retrieval-Augmented Generation chatbot for document summarization and query answering
   🌐: https://github.com/shreeharini-261/RAG

3. Real-time OCR System- Handwritten text detection with bounding boxes and Excel export (88-92% accuracy)
   🌐: https://github.com/shreeharini-261/OCR_pytesseract""",
    "contact":
    """📧 Email: shreeharini261@gmail.com
📞 Phone: +91 9345599591
💼 LinkedIn: linkedin.com/in/shreeharini-s
🐙 GitHub: github.com/shreeharini-261
📍 Location: Chennai, India""",
    "education":
    """🎓 B.Tech in Artificial Intelligence
   SRM Institute of Science and Technology
   CGPA: 9.3/10.0
   
📜 Certifications:
   - NPTEL ELITE: Java, DBMS, Computer Architecture
   - Coursera: IBM Machine Learning & Deep Learning (90%)""",
    "experience":
    """💼 Professional Experience:

Caprae Capital - ML & Software Development Intern
- Built secure Stripe-based payment system (Flask, PostgreSQL) for SaaSquatch app
- Enabled subscription management and $1,000/month recurring revenue
- Implemented encryption for compliance and scalability

Hyperverge Nexus - Research Fellow  
- Developed deepfake detection model using EfficientNet-B7 + Vision Transformers
- Achieved 90% accuracy and reduced false positives by 25% vs baseline

NextGenAI - Technical Club Head
- Led ML/DL domain and mentored 40-member team
- Drove innovative AI projects and solutions""",
    "achievements":
    """🏆 **Key Achievements:**

🥇 NASA Impact Hackathon - 1st Prize
- Built time-series model for coral reef habitats using 5+ years of NASA geospatial data

🎤 AAIMB 2024 International Conference - Research Presenter
- Presented peer-reviewed research on RAG vs LLMs
- Demonstrated 22% metric improvement in document embedding tasks vs baselines"""
}

# Security: Allowlist of safe commands that can be executed
# This is much safer than a blacklist approach
SAFE_COMMANDS = {
    # File system operations (read-only)
    'ls': ['-l', '-a', '-la', '-h', '-R', '--color=auto'],
    'pwd': [],
    'whoami': [],
    'id': [],
    'cat': [],  # Will be validated for safe files only
    'head': ['-n'],
    'tail': ['-n'],
    'wc': ['-l', '-w', '-c'],
    'file': [],
    'stat': [],
    'find': ['-name', '-type', '-maxdepth'],  # Limited find operations

    # Process and system information
    'ps': ['aux', '-ef', '-u'],
    'top': ['-n'],
    'jobs': [],
    'uname': ['-a', '-r', '-s'],
    'uptime': [],
    'free': ['-h'],
    'df': ['-h'],
    'du': ['-h', '-s'],
    'lscpu': [],
    'lsblk': [],
    'mount': [],

    # Network information (read-only)
    'ping': ['-c'],  # Limited ping
    'host': [],
    'nslookup': [],
    'ifconfig': [],
    'ip': ['addr', 'route'],

    # Date and time
    'date': [],
    'cal': [],

    # Text processing
    'grep': ['-n', '-i', '-v', '-c'],
    'sort': [],
    'uniq': [],
    'cut': ['-d', '-f'],

    # Environment
    'env': [],
    'printenv': [],
    'which': [],
    'whereis': [],
    'type': [],

    # Safe utilities
    'echo': [],
    'printf': [],
    'basename': [],
    'dirname': [],
    'realpath': [],
    'readlink': []
}

# Files/paths that are safe to read
SAFE_READ_PATHS = [
    '/etc/os-release', '/etc/hostname', '/etc/timezone', '/proc/cpuinfo',
    '/proc/meminfo', '/proc/version', '/proc/uptime', '/proc/loadavg'
]


def is_command_safe(command):
    """
    Check if a command is safe to execute using an allowlist approach.
    Returns (is_safe: bool, safe_args: list) or (False, None) if unsafe.
    """
    try:
        # Parse command using shlex to handle quotes and escaping properly
        parts = shlex.split(command.strip())
        if not parts:
            return True, []

        base_command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        # Check if base command is in allowlist
        if base_command not in SAFE_COMMANDS:
            return False, None

        allowed_flags = SAFE_COMMANDS[base_command]

        # Validate arguments
        safe_args = [base_command]
        i = 0
        while i < len(args):
            arg = args[i]

            # Allow literal values (no dangerous characters)
            if not re.search(r'[;&|`$(){}\\]', arg):
                # For commands like cat, check if file path is safe
                if base_command == 'cat':
                    if arg.startswith('/') and arg not in SAFE_READ_PATHS:
                        return False, None
                    if '..' in arg or arg.startswith('~'):
                        return False, None

                # For flags, check if they're allowed
                if arg.startswith('-'):
                    if arg not in allowed_flags and not any(
                            arg.startswith(flag) for flag in allowed_flags):
                        # Allow some common safe flags not explicitly listed
                        if not re.match(r'^-[a-zA-Z0-9]+$', arg):
                            return False, None

                safe_args.append(arg)
                i += 1
            else:
                return False, None

        return True, safe_args

    except (ValueError, TypeError):
        # shlex.split failed - command has unsafe characters
        return False, None


def handle_portfolio_command(command):
    """
    Handle portfolio-specific commands.
    Returns (is_portfolio_cmd: bool, output: str) tuple.
    """
    command_lower = command.lower().strip()

    # Portfolio commands
    if command_lower == 'about':
        return True, portfolio_data['about']

    elif command_lower == 'resume':
        return True, f"📄 My Resume: {portfolio_data['resume']}"

    elif command_lower == 'skills':
        return True, f"💻 Technical Skills:\n{portfolio_data['skills']}"

    elif command_lower == 'projects':
        return True, portfolio_data['projects']

    elif command_lower == 'contact':
        return True, portfolio_data['contact']

    elif command_lower == 'education':
        return True, portfolio_data['education']

    elif command_lower == 'experience':
        return True, portfolio_data['experience']

    elif command_lower == 'achievements':
        return True, portfolio_data['achievements']

    elif command_lower == 'date':
        current_time = datetime.now()
        return True, current_time.strftime("📅 %A, %B %d, %Y\n🕒 %I:%M:%S %p")

    elif command_lower.startswith('echo '):
        echo_text = command[5:]  # Remove 'echo ' prefix
        return True, echo_text if echo_text.strip() else ""

    elif command_lower == 'echo':
        return True, ""  # Empty echo

    # Not a portfolio command
    return False, ""


def get_system_info():
    """
    Get system information using psutil.
    Returns formatted string with CPU, memory, and process information.
    """
    try:
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # Memory information
        memory = psutil.virtual_memory()
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        memory_percent = memory.percent

        # Disk information
        disk = psutil.disk_usage('/')
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        disk_percent = (disk.used / disk.total) * 100

        # Top 5 processes by CPU usage
        processes = []
        for proc in psutil.process_iter(
            ['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied,
                    psutil.ZombieProcess):
                pass

        # Sort by CPU usage and get top 5
        processes = sorted(processes,
                           key=lambda x: x['cpu_percent'] or 0,
                           reverse=True)[:5]

        # Format the output
        output = f"""
System Information:
==================

CPU Usage: {cpu_percent}% ({cpu_count} cores)
Memory Usage: {memory_used_gb:.1f}GB / {memory_total_gb:.1f}GB ({memory_percent}%)
Disk Usage: {disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB ({disk_percent:.1f}%)

Top Processes (by CPU):
----------------------
{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory%':<8}
{'-' * 50}"""

        for proc in processes:
            pid = proc['pid']
            name = proc['name'][:19] if proc['name'] else 'Unknown'
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            output += f"\n{pid:<8} {name:<20} {cpu:<8.1f} {mem:<8.1f}"

        return output

    except Exception as e:
        return f"Error retrieving system information: {str(e)}"


@app.route('/')
def index():
    """Serve the main terminal interface."""
    return render_template('index.html')


@app.route('/run_command', methods=['POST'])
def run_command():
    """
    Execute a system command and return the result.
    
    Expects JSON: {"command": "user_input"}
    Returns JSON: {"output": "combined_stdout_and_stderr", "status": return_code}
    """
    try:
        # Get command from JSON request
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({
                'output': 'Error: No command provided',
                'status': 1
            }), 400

        command = data['command'].strip()

        # Handle empty commands
        if not command:
            return jsonify({'output': '', 'status': 0})

        # First, check if it's a portfolio command
        is_portfolio_cmd, portfolio_output = handle_portfolio_command(command)
        if is_portfolio_cmd:
            return jsonify({'output': portfolio_output, 'status': 0})

        # Handle special sysinfo command
        if command.lower() == 'sysinfo':
            return jsonify({'output': get_system_info(), 'status': 0})

        # Security check using allowlist for system commands
        is_safe, safe_args = is_command_safe(command)
        if not is_safe or safe_args is None:
            return jsonify({
                'output':
                'Error: Command not allowed. Only safe read-only commands are permitted.',
                'status': 1
            }), 403

        # Execute the command using subprocess with shell=False for better security
        try:
            result = subprocess.run(
                safe_args,
                shell=False,  # Much safer than shell=True
                capture_output=True,
                text=True,
                timeout=15,  # Reduced timeout
                cwd=os.getcwd(),
                # Additional security: limit resources
                env=dict(os.environ, PATH='/usr/bin:/bin')  # Limit PATH
            )

            # Combine stdout and stderr
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += result.stderr

            return jsonify({'output': output, 'status': result.returncode})

        except subprocess.TimeoutExpired:
            return jsonify({
                'output': 'Error: Command timed out after 30 seconds',
                'status': 1
            }), 408

        except Exception as e:
            return jsonify({
                'output': f'Error executing command: {str(e)}',
                'status': 1
            }), 500

    except Exception as e:
        return jsonify({'output': f'Server error: {str(e)}', 'status': 1}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Run Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
