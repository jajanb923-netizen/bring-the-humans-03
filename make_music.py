#!/usr/bin/env python3
"""Synthesize a short upbeat music bed for the TikTok ad (24 s, 120 BPM).

All synthesis, no samples: a four-on-the-floor kick, offbeat hats, a
punchy A-minor bassline and a quiet bright arp. Mixed low so the
voiceover stays on top; fades in and out at the ends.
"""
import numpy as np
from scipy.io import wavfile

SR = 48000
DUR = 24.0
BPM = 120
BEAT = 60.0 / BPM  # 0.5 s

N = int(SR * DUR)
t = np.arange(N) / SR
mix = np.zeros(N)


def add(sig, start, gain=1.0):
    s = int(start * SR)
    e = min(N, s + len(sig))
    mix[s:e] += gain * sig[: e - s]


def kick(dur=0.22):
    n = int(SR * dur)
    tt = np.arange(n) / SR
    freq = 150 * np.exp(-tt * 22) + 45
    phase = np.cumsum(freq) / SR * 2 * np.pi
    env = np.exp(-tt * 28)
    return np.sin(phase) * env


def hat(dur=0.05):
    n = int(SR * dur)
    noise = np.random.default_rng(7).standard_normal(n)
    # crude highpass: diff
    hp = np.diff(noise, prepend=0)
    env = np.exp(-np.arange(n) / SR * 220)
    return hp * env * 0.6


def bass_note(freq, dur):
    n = int(SR * dur)
    tt = np.arange(n) / SR
    env = np.exp(-tt * 9)
    return (np.sin(2 * np.pi * freq * tt)
            + 0.4 * np.sin(2 * np.pi * freq * 2 * tt)) * env


def pluck(freq, dur=0.22):
    n = int(SR * dur)
    tt = np.arange(n) / SR
    env = np.exp(-tt * 16)
    return (np.sin(2 * np.pi * freq * tt)
            + 0.5 * np.sin(2 * np.pi * freq * 2 * tt)
            + 0.2 * np.sin(2 * np.pi * freq * 3 * tt)) * env


# Kick on every beat, hats on offbeat 8ths
for b in range(int(DUR / BEAT)):
    add(kick(), b * BEAT, 0.9)
    add(hat(), b * BEAT + BEAT / 2, 0.35)
    add(hat(), b * BEAT + BEAT * 0.25, 0.18)
    add(hat(), b * BEAT + BEAT * 0.75, 0.18)

# Bassline: Am - F - C - G, one bar each (4 beats per bar)
roots = [55.0, 43.65, 65.41, 49.0]  # A1 F1 C2 G1
for bar, root in enumerate(roots * 3):  # 12 bars = 24 s
    start = bar * 4 * BEAT
    for beat in range(4):
        add(bass_note(root, BEAT * 0.9), start + beat * BEAT, 0.55)
        if beat == 3:
            add(bass_note(root * 1.5, BEAT * 0.45),
                start + beat * BEAT + BEAT / 2, 0.4)

# Bright arp on 16ths, A minor pentatonic, quiet
arp = [220.0, 261.63, 329.63, 440.0, 523.25, 440.0, 329.63, 261.63]
sixteenth = BEAT / 4
for i in range(int(DUR / sixteenth)):
    if i % 2 == 0:  # 8ths only, keep it airy
        add(pluck(arp[(i // 2) % len(arp)]), i * sixteenth, 0.16)

# Fades: 0.4 s in, 1.2 s out
fade_in = np.minimum(1.0, t / 0.4)
fade_out = np.minimum(1.0, (DUR - t) / 1.2)
mix *= fade_in * fade_out

# Normalize to -14 dBFS peak, stereo
peak = np.abs(mix).max()
mix = mix / peak * 10 ** (-14 / 20)
stereo = np.stack([mix, mix], axis=1)
wavfile.write("assets/audio/music.wav", SR, (stereo * 32767).astype(np.int16))
print("wrote assets/audio/music.wav", DUR, "s, peak", round(float(peak), 3))
