import openai
from moviepy.editor import AudioFileClip


def audio_to_text(file):
    # file.download("voice_message.ogg")
    audio_clip = AudioFileClip(file)
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    return transcript
