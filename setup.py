from setuptools import setup, find_packages

setup(
    name="autotune",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch",
        "librosa",
        "soundfile",
        "matplotlib",
        "tqdm",
    ],
    extras_require={
        'tts': ['TTS'],  # Optional TTS dependency
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A voice cloning and text-to-speech tool using Coqui TTS",
    keywords="tts, voice-cloning, speech-synthesis",
    python_requires=">=3.7",  # Base requirement without TTS
)