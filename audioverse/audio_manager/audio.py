import os
import numpy as np
from moviepy.editor import AudioFileClip, CompositeAudioClip, afx


def audio_normalize(clip):
    mv = clip.max_volume()
    if mv > 0:
        return afx.volumex(clip, 1 / mv)
    return clip


def load_audio_files(input_dir):
    voice_files = sorted(
        [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.startswith("voice")
        ]
    )
    sfx_files = sorted(
        [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.startswith("sfx")
        ]
    )

    # # alternate between voice and sfx files
    # sfx_adapted_files = []
    # sfx_idx = 0
    # for i in range(len(voice_files)):
    #     if sfx_idx >= len(sfx_files):
    #         sfx_adapted_files.extend([None] * (len(voice_files) - i))
    #         break

    #     voice = voice_files[i]
    #     sfx = sfx_files[sfx_idx]

    #     voice_indexes = os.path.basename(voice).split(".")[0][len("voice") :].split("_")
    #     sfx_filename = os.path.basename(sfx).split(".")[0][len("sfx") :].split("_")

    #     if voice_indexes == sfx_filename:
    #         sfx_adapted_files.append(sfx)
    #         sfx_idx += 1
    #     else:
    #         sfx_adapted_files.append(None)

    voice_files = [AudioFileClip(x).fx(audio_normalize) for x in voice_files]
    for i, x in enumerate(sfx_files):
        if x is not None:
            sfx_files[i] = (
                AudioFileClip(x).fx(audio_normalize).fx(afx.volumex, 0.1)
            )

    return voice_files, sfx_files


def get_speaking(audio_clip, window_size=0.5, volume_threshold=0.001, ease_in=0.25, min_consecutive_windows=5):
    speaking_clips = []
    t = 0
    while t < audio_clip.duration:
        consecutive_silence, start_silence = 0, t
        while t < audio_clip.duration and audio_clip.subclip(t, t + window_size).max_volume() < volume_threshold:
            t += window_size
            consecutive_silence += 1
        
        while t < audio_clip.duration and audio_clip.subclip(t, t + window_size).max_volume() >= volume_threshold:
            t += window_size
        
        if consecutive_silence >= min_consecutive_windows:
            print('Found speaking interval', start_silence, t)
            speaking_clips.append(audio_clip.subclip(start_silence - ease_in, t + ease_in))

    # Ensure that there's at least one speaking interval
    if not speaking_clips:
        speaking_clips.append(audio_clip.subclip(0, t))

    return speaking_clips
       

def apply_sfx_to_voice(voice_files, sfx_files):
    audiobook_clips = []
    voice_time = 0
    sfx_id = 0

    for paragraph_voice in voice_files:
        assert len(paragraph_voice) == len(sfx_files) + 1
        paragraph_sfx = (
            sfx_files[sfx_id : sfx_id + len(paragraph_voice)]
            if len(paragraph_voice) > 1
            else None
        )
        if len(paragraph_voice) > 1:
            sfx_id += len(paragraph_voice) - 1

        for i, voice_segment in enumerate(paragraph_voice):
            print("len of paragraph_voice", len(paragraph_voice))
            print("len of paragraph_sfx", len(paragraph_sfx))
            voice_segment = voice_segment.set_start(voice_time)

            if (
                paragraph_sfx is None
                or i >= len(paragraph_voice) - 1
                or (i <= len(paragraph_sfx) - 1 and paragraph_sfx[i] is None)
            ):
                print('Appeneding voice segment')
                voice_time += voice_segment.duration
                audiobook_clips.append(voice_segment)
            else:
                sound_effect = paragraph_sfx[i]
                overlap_duration = min(sound_effect.duration, 2.0)
                sound_effect = sound_effect.set_start(
                    max(0, voice_segment.duration + voice_time - overlap_duration)
                )
                sound_effect = sound_effect.fx(afx.audio_fadein, overlap_duration // 2)
                sound_effect = sound_effect.fx(afx.audio_fadeout, overlap_duration // 2)
                audiobook_clips.extend([voice_segment, sound_effect])
                voice_time += voice_segment.duration

            # paragraph_duration += voice_segment.duration

        # # Add a 2-second pause between paragraphs
        # if paragraph_duration > 0:
        #     pause = afx.silence(2.0)
        #     paragraph_clip.append(pause)
        #     voice_time += pause.duration

    clip = CompositeAudioClip(audiobook_clips).set_fps(44100)
    return clip


def construct_audiobook(input_dir):
    voice_files, sfx_files = load_audio_files(input_dir)
    ###########################
    # change the seconds of wait in get_speaking
    ##########################
    voice_files = [get_speaking(voice_file) for voice_file in voice_files]
    audiobook = apply_sfx_to_voice(voice_files, sfx_files)
    temp = os.path.join(input_dir, "final.mp3")
    audiobook.write_audiofile(temp, codec="mp3")
    with open(temp, "rb") as file:
        audio_bytes = file.read()
    return audio_bytes
