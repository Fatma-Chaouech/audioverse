import os
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

    # alternate between voice and sfx files
    sfx_adapted_files = []
    sfx_idx = 0
    for i in range(len(voice_files)):
        if sfx_idx >= len(sfx_files):
            sfx_adapted_files.extend([None] * (len(voice_files) - i))
            break

        voice = voice_files[i]
        sfx = sfx_files[sfx_idx]

        voice_indexes = os.path.basename(voice).split(".")[0][len("voice") :].split("_")
        sfx_filename = os.path.basename(sfx).split(".")[0][len("sfx") :].split("_")

        if voice_indexes == sfx_filename:
            sfx_adapted_files.append(sfx)
            sfx_idx += 1
        else:
            sfx_adapted_files.append(None)

    voice_files = [AudioFileClip(x).fx(audio_normalize) for x in voice_files]

    for i, x in enumerate(sfx_adapted_files):
        if x is not None:
            sfx_adapted_files[i] = (
                AudioFileClip(x).fx(audio_normalize).fx(afx.volumex, 0.1)
            )

    return voice_files, sfx_adapted_files


def apply_sfx_to_voice(voice_files, sfx_files):
    audiobook_clips = []
    voice_time = 0
    for i, voice_segment in enumerate(voice_files):
        voice_segment = voice_segment.set_start(voice_time)
        sound_effect = sfx_files[i]

        # if there is no sound effect, just add the voice segment
        if sound_effect is None:
            voice_time += voice_segment.duration
            audiobook_clips.append(voice_segment)
            continue

        overlap_duration = min(sound_effect.duration, 2.0)

        # make the sfx start at the end of the voice segment
        sound_effect = sound_effect.set_start(
            max(0, voice_segment.duration + voice_time - overlap_duration)
        )
        sound_effect = sound_effect.fx(afx.audio_fadein, overlap_duration // 2)
        sound_effect = sound_effect.fx(afx.audio_fadeout, overlap_duration // 2)
        audiobook_clips.extend([voice_segment, sound_effect])
        voice_time += voice_segment.duration
    clip = CompositeAudioClip(audiobook_clips).set_fps(44100)
    return clip


def contruct_audiobook(input_dir):
    voice_files, sfx_files = load_audio_files(input_dir)
    audiobook = apply_sfx_to_voice(voice_files, sfx_files)
    temp = os.path.join(input_dir, "final.mp3")
    audiobook.write_audiofile(temp, codec="mp3")
    with open(temp, "rb") as file:
        audio_bytes = file.read()
    return audio_bytes
