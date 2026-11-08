import json, sys
src = sys.argv[1]; out = src[:-4] + "_words.json"
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(src, word_timestamps=True, language="en")
words = [dict(w=x.word, s=round(x.start, 3), e=round(x.end, 3)) for s in segs for x in s.words]
json.dump(words, open(out, "w"), indent=0)
print(" ".join("%s[%.2f-%.2f]" % (w["w"].strip(), w["s"], w["e"]) for w in words))
