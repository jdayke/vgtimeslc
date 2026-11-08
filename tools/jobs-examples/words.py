import json, sys
src = r"J:\Claude\VGTimes and LibertyCity\Work\2026 11 06 Lucia\voices\EN_Ava_lucia.mp3"
out = r"J:\Claude\VGTimes and LibertyCity\Work\2026 11 06 Lucia\voices\EN_Ava_lucia_words.json"
try:
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cuda", compute_type="float16")
    segs, _ = m.transcribe(src, word_timestamps=True, language="en")
    words = [dict(w=x.word, s=round(x.start, 3), e=round(x.end, 3)) for s in segs for x in s.words]
except ImportError:
    import whisper
    m = whisper.load_model("small.en")
    r = m.transcribe(src, word_timestamps=True, language="en")
    words = [dict(w=x["word"], s=round(x["start"], 3), e=round(x["end"], 3)) for s in r["segments"] for x in s["words"]]
json.dump(words, open(out, "w"), indent=0)
for w in words: print(w)
