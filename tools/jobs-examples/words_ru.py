import json, sys
src = sys.argv[1]; out = src[:-4] + "_words.json"
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = m.transcribe(src, word_timestamps=True, language="ru", vad_filter=False)
words = [dict(w=x.word, s=round(x.start, 3), e=round(x.end, 3)) for s in segs for x in s.words]
json.dump(words, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("words", len(words))
