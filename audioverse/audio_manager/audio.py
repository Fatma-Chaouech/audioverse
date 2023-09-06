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
    voice_files = [AudioFileClip(x).fx(audio_normalize) for x in voice_files]
    for i, x in enumerate(sfx_files):
        if x is not None:
            sfx_files[i] = AudioFileClip(x).fx(audio_normalize).fx(afx.volumex, 0.1)

    return voice_files, sfx_files


def construct_paragraph(
    audio_clip,
    sound_effects,
    window_size=0.5,
    volume_threshold=0.005,
    top_k=2,
):
    speaking_clips = []
    duration = int(audio_clip.duration)
    t = 0

    while t < duration:
        # find the speaking clip
        start_speaking = t
        while (
            t < duration
            and audio_clip.subclip(t, min(duration, t + window_size)).max_volume()
            >= volume_threshold
        ):
            t += window_size

        speaking_duration = max(0, t - start_speaking)

        # find the silence clip
        start_silence = min(duration, t)
        while (
            t < duration
            and audio_clip.subclip(t, min(duration, t + window_size)).max_volume()
            < volume_threshold
        ):
            t += window_size

        silence_duration = max(0, t - start_silence)

        speaking_clips.append(
            {
                "silence_duration": silence_duration,
                "speaking_duration": speaking_duration,
                "start_silence": start_silence,
                "start_speaking": start_speaking,
            }
        )
    speaking_clips.sort(key=lambda x: x["silence_duration"], reverse=True)

    composite = []
    for i in range(len(speaking_clips)):
        silence_duration, speaking_duration, start_silence, start_speaking = list(
            speaking_clips[i].values()
        )

        if i < top_k:
            # insert sound effect at the start of speaking
            sfx = sound_effects[i]
            overlap_duration = min(sfx.duration, 2.0)
            sfx = sfx.fx(afx.audio_fadein, overlap_duration // 2)
            sfx = sfx.fx(afx.audio_fadeout, overlap_duration // 2)

            composite.append({"start": start_silence, "value": sfx, "is_sfx": True})

            # append the speaking part to the composite
            composite.append(
                {
                    "start": start_speaking,
                    "value": audio_clip.subclip(
                        start_speaking, start_speaking + speaking_duration
                    ),
                    "is_sfx": False,
                }
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
        # "start" of sfx is -1, so don't consider all of the sfx
        if not audio["is_sfx"]:
            results.append(audio["value"].set_start(voice_offset))
            # print('Voice offset', voice_offset)
            voice_offset += audio["value"].duration
        else:
            results.append(
                audio["value"].set_start(voice_offset)
            )

    return CompositeAudioClip(results).set_fps(44100)


def construct_audiobook(input_dir):
    voice_files, sfx_files = load_audio_files(input_dir)
    # sfx aren't in place, the audio isn't complete (at the end) **see36**
    audiobook = CompositeAudioClip(
        [
            construct_paragraph(voice_file, sfx_files, top_k=len(sfx_files))
            for voice_file in voice_files
        ]
    ).set_fps(44100)
    temp = os.path.join(input_dir, "final.mp3")
    audiobook.write_audiofile(temp, codec="mp3")
    with open(temp, "rb") as file:
        audio_bytes = file.read()
    return audio_bytes
