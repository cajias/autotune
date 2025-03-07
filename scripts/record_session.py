#!/usr/bin/env python
"""
Interactive recording session with teleprompter-like interface
"""
import os
import sys
import time
import json
import curses
import argparse
import threading
from pathlib import Path
from datetime import datetime

import sounddevice as sd
import soundfile as sf
import numpy as np

# Configuration
SAMPLE_RATE = 44100
CHANNELS = 1
SCROLL_DELAY = 0.05  # Adjust scroll speed
RECORDING_LENGTH = 60  # 1 minute recordings
SESSIONS_PER_USER = 10

# Text samples for recording - each should take about 1 minute to read naturally
TEXT_SAMPLES = [
    # Sample 1 - General introduction
    """Hello! I'm recording this sample to create a digital version of my voice. 
    This is a natural way of speaking, using different intonations and expressions. 
    Voice synthesis technology has come a long way, and it's fascinating how we can 
    now create such realistic digital voices. I'm making sure to speak clearly and 
    at a consistent pace, which helps create better quality results. It's important 
    to maintain a steady rhythm while speaking, but also to sound natural and not robotic.""",

    # Sample 2 - Technical description
    """Let me explain how neural networks process information. The system consists of 
    interconnected nodes, similar to neurons in a human brain. Each connection has 
    a weight that determines its importance. When data flows through the network, 
    these weights are adjusted through a process called training. This allows the 
    network to recognize patterns and make predictions based on input data. The more 
    data we provide, the better the network becomes at its assigned task.""",

    # Sample 3 - Story narration
    """The morning sun cast long shadows across the quiet valley. Birds were beginning 
    their daily chorus, filling the air with melodic songs. A gentle breeze rustled 
    through the leaves, creating a peaceful atmosphere. In the distance, mountains 
    stood majestically against the clear blue sky. This was the perfect moment to 
    pause and appreciate nature's beauty. The world seemed to slow down, if only 
    for a brief moment.""",

    # Sample 4 - Professional presentation
    """Today, I'd like to present our quarterly results. Our team has achieved 
    significant progress in all key metrics. Customer satisfaction has increased 
    by fifteen percent, while operational costs have decreased. We've implemented 
    new systems that streamline our workflow and improve efficiency. Looking ahead, 
    we're optimistic about our growth prospects and market position. These results 
    reflect the dedication of our entire team.""",

    # Sample 5 - Scientific explanation
    """The water cycle is a continuous process on Earth. Water evaporates from 
    oceans, lakes, and rivers due to solar heating. This vapor rises into the 
    atmosphere, where it cools and condenses into clouds. When conditions are right, 
    precipitation occurs in the form of rain or snow. This water then returns to 
    the Earth's surface, completing the cycle. Understanding this process is crucial 
    for climate science.""",

    # Sample 6 - Creative description
    """Imagine walking through an ancient forest. Towering trees stretch endlessly 
    upward, their branches creating intricate patterns against the sky. Sunlight 
    filters through the canopy, casting dappled shadows on the forest floor. The 
    air is rich with the scent of pine and earth. Each step reveals new details: 
    delicate ferns, colorful mushrooms, and the occasional glimpse of wildlife 
    moving quietly through the undergrowth.""",

    # Sample 7 - Historical narrative
    """The Industrial Revolution transformed society in profound ways. Steam power 
    and mechanical innovation revolutionized manufacturing processes. Cities grew 
    rapidly as people moved from rural areas to find work in factories. New 
    transportation systems, like railways, connected distant regions. This period 
    of change laid the foundation for our modern world, though it also brought 
    significant social and environmental challenges.""",

    # Sample 8 - Educational content
    """Let's explore how sound waves work. Sound is a form of energy that travels 
    through matter as a wave. When you speak, your vocal cords vibrate, creating 
    these waves in the air. The waves have properties like frequency, which determines 
    pitch, and amplitude, which affects volume. Your ear captures these waves and 
    converts them into signals your brain can interpret as sound.""",

    # Sample 9 - Personal reflection
    """Looking back on the past year, I've learned many valuable lessons about 
    adaptation and resilience. Change is constant, and our ability to adjust and 
    grow determines our success. I've found that maintaining a positive attitude 
    while facing challenges leads to better outcomes. It's important to celebrate 
    small victories and learn from setbacks. Every experience contributes to our 
    personal growth.""",

    # Sample 10 - Future vision
    """As we look toward the future of technology, we see incredible possibilities. 
    Artificial intelligence will continue to evolve and integrate into daily life. 
    Renewable energy systems will become more efficient and widespread. Transportation 
    will be transformed by autonomous vehicles. Medical breakthroughs will extend 
    and improve human life. The key is to guide these advances responsibly and 
    ethically."""
]

class Teleprompter:
    def __init__(self, text, window):
        self.text = text
        self.window = window
        self.current_line = 0
        self.lines = text.split('\n')
        self.max_lines = curses.LINES - 2
        self.running = True
        
    def display(self):
        while self.running and self.current_line < len(self.lines):
            self.window.clear()
            
            # Display current visible lines
            for i in range(self.max_lines):
                line_idx = self.current_line + i
                if line_idx < len(self.lines):
                    try:
                        # Ensure line fits within window width
                        line = self.lines[line_idx][:curses.COLS-1]
                        self.window.addstr(i, 0, line)
                    except curses.error:
                        pass
            
            self.window.refresh()
            time.sleep(SCROLL_DELAY)
            self.current_line += 1
        
        # Wait at the end to ensure all text is read
        if self.running:
            time.sleep(2)

def record_audio(filename, duration):
    """Record audio for the specified duration"""
    # Record with a bit of padding
    samples = int((duration + 0.5) * SAMPLE_RATE)
    
    recording = sd.rec(samples, samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    
    # Trim any silence at the beginning and end
    recording = recording.reshape(-1)
    
    # Save the recording
    sf.write(filename, recording, SAMPLE_RATE)

def get_session_info(user_id):
    """Get information about the user's recording sessions"""
    sessions_dir = Path("recordings") / user_id
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    # Load or create session info
    info_file = sessions_dir / "session_info.json"
    if info_file.exists():
        with open(info_file, 'r') as f:
            info = json.load(f)
    else:
        info = {
            "user_id": user_id,
            "completed_sessions": [],
            "last_session": None
        }
    
    return info, sessions_dir

def save_session_info(sessions_dir, info):
    """Save session information"""
    info_file = sessions_dir / "session_info.json"
    with open(info_file, 'w') as f:
        json.dump(info, f, indent=2)

def run_session(stdscr, user_id, session_num):
    """Run a recording session"""
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Set up the window
    stdscr.clear()
    stdscr.refresh()
    
    # Create recording directory
    sessions_dir = Path("recordings") / user_id
    session_dir = sessions_dir / f"session_{session_num}"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Record the sample
    text = TEXT_SAMPLES[session_num - 1]
    output_file = session_dir / f"recording_{session_num}.wav"
    
    # Show instructions
    stdscr.addstr(0, 0, f"Session {session_num} of {SESSIONS_PER_USER}")
    stdscr.addstr(1, 0, "Press SPACE to start recording (will record for 1 minute)")
    stdscr.addstr(2, 0, "Press 'q' to quit")
    stdscr.refresh()
    
    while True:
        c = stdscr.getch()
        if c == ord(' '):
            break
        elif c == ord('q'):
            return False
    
    # Start recording in a separate thread
    recording_thread = threading.Thread(
        target=record_audio, 
        args=(output_file, RECORDING_LENGTH)
    )
    recording_thread.start()
    
    # Show recording status
    stdscr.clear()
    stdscr.addstr(0, 0, "Recording... ", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr("Follow the text below:")
    stdscr.refresh()
    
    # Run teleprompter
    prompter = Teleprompter(text, stdscr)
    prompter_thread = threading.Thread(target=prompter.display)
    prompter_thread.start()
    
    # Wait for recording to complete
    recording_thread.join()
    prompter.running = False
    prompter_thread.join()
    
    # Show completion message
    stdscr.clear()
    stdscr.addstr(0, 0, "Recording complete!", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(1, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Record voice samples with a teleprompter interface")
    parser.add_argument("user_id", help="Unique identifier for the user")
    parser.add_argument("--simple", action="store_true", help="Use simple mode without curses interface")
    args = parser.parse_args()
    
    # Get session information
    info, sessions_dir = get_session_info(args.user_id)
    completed = set(info["completed_sessions"])
    
    # Check if all sessions are completed
    if len(completed) >= SESSIONS_PER_USER:
        print(f"All {SESSIONS_PER_USER} sessions completed for user {args.user_id}!")
        print("You can now train your voice model.")
        return
    
    # Find the next session to record
    next_session = 1
    while next_session in completed and next_session <= SESSIONS_PER_USER:
        next_session += 1
    
    print(f"Starting session {next_session} of {SESSIONS_PER_USER}")
    print(f"Completed sessions: {len(completed)}")
    
    try:
        if args.simple:
            # Simple mode without curses
            print("\nSimple mode: Recording without teleprompter interface")
            
            # Create recording directory
            session_dir = sessions_dir / f"session_{next_session}"
            session_dir.mkdir(parents=True, exist_ok=True)
            output_file = session_dir / f"recording_{next_session}.wav"
            
            # Show the text to read
            text = TEXT_SAMPLES[next_session - 1]
            print("\nPlease read the following text:")
            print("=" * 80)
            print(text)
            print("=" * 80)
            
            input("\nPress Enter to start recording (will record for 1 minute)...")
            
            print("Recording... Please read the text above.")
            record_audio(output_file, RECORDING_LENGTH)
            print("Recording complete!")
            
            success = True
        else:
            # Run the recording session with curses interface
            success = curses.wrapper(run_session, args.user_id, next_session)
        
        if success:
            # Update session information
            completed.add(next_session)
            info["completed_sessions"] = sorted(list(completed))
            info["last_session"] = datetime.now().isoformat()
            save_session_info(sessions_dir, info)
            
            remaining = SESSIONS_PER_USER - len(completed)
            print(f"\nSession {next_session} completed successfully!")
            print(f"Remaining sessions: {remaining}")
        
    except KeyboardInterrupt:
        print("\nRecording session interrupted.")
    except Exception as e:
        print(f"\nError during recording: {e}")
        print("Try using --simple mode if you're having issues with the interface.")
    
    if len(completed) >= SESSIONS_PER_USER:
        print("\nAll recording sessions completed!")
        print("You can now train your voice model.")

if __name__ == "__main__":
    main()