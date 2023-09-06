import os
from moviepy.editor import AudioFileClip, CompositeAudioClip, afx


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

    def normalize_clip(clip):
        max_vol = clip.max_volume()
        return afx.volumex(clip, 1 / max_vol) if max_vol > 0 else clip

    voice_clips = [normalize_clip(AudioFileClip(file)) for file in voice_files]
    sfx_clips = [
        normalize_clip(AudioFileClip(file).fx(afx.volumex, 0.1)) if file else None
        for file in sfx_files
    ]

    return voice_clips, sfx_clips


def construct_paragraph(
    audio_clip, sound_effects, window_size=0.5, volume_threshold=0.005, top_k=2
):
    def split_audio():
        t = 0
        while t < duration:
            start_speaking = t
            while (
                t < duration
                and audio_clip.subclip(t, t + window_size).max_volume()
                >= volume_threshold
            ):
                t += window_size
            speaking_duration = max(0, t - start_speaking)

            start_silence = t
            while (
                t < duration
                and audio_clip.subclip(t, t + window_size).max_volume()
                < volume_threshold
            ):
                t += window_size
            silence_duration = max(0, t - start_silence)

            yield start_speaking, speaking_duration, start_silence, silence_duration

    duration = int(audio_clip.duration)
    speaking_clips = list(split_audio())
    speaking_clips.sort(key=lambda x: x[3], reverse=True)

    composite = []
    for i, (
        start_speaking,
        speaking_duration,
        start_silence,
        silence_duration,
    ) in enumerate(speaking_clips):
        if i < top_k:
            sfx = sound_effects[i]
            overlap_duration = min(sfx.duration, 2.0)
            sfx = sfx.fx(afx.audio_fadein, overlap_duration // 2).fx(
                afx.audio_fadeout, overlap_duration // 2
            )
            composite.extend(
                [
                    {"start": start_silence, "value": sfx, "is_sfx": True},
                    {
                        "start": start_speaking,
                        "value": audio_clip.subclip(
                            start_speaking, start_speaking + speaking_duration
                        ),
                        "is_sfx": False,
                    },
                ]
            )
        else:
            composite.append(
                {
                    "start": start_speaking,
                    "value": audio_clip.subclip(
                        start_speaking, start_silence + silence_duration
                    ),
                    "is_sfx": False,
                }
            )

    composite.sort(key=lambda x: x["start"])
    voice_offset = 0
    results = []
    for audio in composite:
        if not audio["is_sfx"]:
            results.append(audio["value"].set_start(voice_offset))
            voice_offset += audio["value"].duration
        else:
            results.append(audio["value"].set_start(voice_offset))

    return CompositeAudioClip(results).set_fps(44100)


def construct_audiobook(input_dir):
    voice_clips, sfx_clips = load_audio_files(input_dir)

    # BUGS: the voice audio doesn't finish the last words
    audiobook = CompositeAudioClip(
        [
            construct_paragraph(voice, sfx_clips, top_k=len(sfx_clips))
            for voice in voice_clips
        ]
    ).set_fps(44100)

    temp = os.path.join(input_dir, "final.mp3")
    audiobook.write_audiofile(temp, codec="mp3")

    with open(temp, "rb") as file:
        audio_bytes = file.read()

    return audio_bytes
