---
name: repost
description: Render finished English-language vertical VGTimes or LibertyCity gaming repost Shorts from supplied social-media links or media and a short hook. Use when the user invokes $repost, asks for a repost-style Short, supplies an X/Twitter post for repackaging, or wants the approved light social-card layout with preserved source audio.
---

# Repost

Produce the finished repost by default. Keep the workflow conservative, reuse approved assets, and avoid unnecessary browsing or long source review.

## Load the rules

Read [references/brand-rules.md](references/brand-rules.md) before choosing the outlet, layout, crop, or copy treatment.

## Respect task state

- If the user says `ничего не делай`, `только изучи`, or `только анализ`, inspect read-only and create nothing.
- If the user asks only for a diagnosis or opinion, do not implement changes.
- If the user explicitly requests a preview, render only one still or the first 3 seconds and stop.
- Otherwise, when the source and hook are supplied, render the complete repost immediately. Do not stop at a preview.
- Do not use Premiere or GUI automation unless the user explicitly requests an editable Premiere project.

## Build the repost

1. Download the supplied source only when it is not already local.
2. Probe it once with `ffprobe` and keep the original audio.
3. Route general gaming topics to VGTimes and Rockstar topics to LibertyCity.
4. Use the approved 1080x1920 light repost card and current approved outlet assets.
5. Write every hook and all added on-screen copy in natural English, even when the user's instruction is in another language. Translate the supplied idea rather than displaying non-English text. Correct obvious typos without changing the meaning. Use ALL CAPS and no final period; preserve a question or exclamation mark.
6. Place the wide source below the card and enlarge its fit-to-width size to 125%, centered horizontally. This is the default crop.
7. Inspect at least six representative source frames before the full render. If the 125% crop substantially cuts a face, main action, essential HUD, captions, or another important subject, use the original 100% fit-to-width size instead. Do not choose an intermediate zoom unless the user requests it.
8. Fill the unused lower canvas with the same light background as the card. Never stretch the source or crop it to fill the whole vertical canvas.
9. Render the complete source up to 59 seconds unless the user requests a different edit.

## Rendering

- Prefer FFmpeg for static layouts and simple overlays; use an existing approved Remotion repost template when available.
- Reuse assets by direct reference or hardlink instead of copying large media.
- Export 1080x1920, square pixels, H.264 High, AAC stereo 48 kHz, and `faststart`.
- Use RTX 4090/NVENC for the final encode when available.
- Preserve source attribution and accurately label fan-made, modded, unused, or archival material when required.
- Use clear versioned filenames and never overwrite a previously approved export.

## Compact QA

Run only:

1. `ffprobe` for duration, dimensions, frame rate, codecs, and audio.
2. `blackdetect` for technical black frames.
3. Start, middle, and end frame extraction to confirm layout and continuity.

Return the finished file first, followed by a short specification summary. Do not provide an SEO package unless requested.

## SEO package

When the user requests an SEO package:

- Write every platform's copy in English and return four separate sections in this order: YouTube, X, Instagram, TikTok. Never reuse one unchanged caption across all platforms.
- For YouTube, provide an SEO title, a searchable description with source credit, 3 relevant hashtags, and a comma-and-space-separated tags line of exactly 500 characters. Count every letter, comma, and space programmatically; never return 499 or 501 characters. Do not put `#` hashtags in the tags field.
- For X, provide one self-contained post no longer than 280 characters including credit and 1–3 hashtags. Lead with the strongest fact or reaction and avoid an Instagram-style block of hashtags.
- For Instagram, provide a readable caption with a hook, short context, a natural engagement question, source credit, and 5–8 targeted hashtags. Use paragraph breaks.
- For TikTok, provide a compact discovery-focused caption with the game/topic keyword in the first sentence, source credit when space permits, and 3–5 targeted hashtags. Keep it shorter and more immediate than Instagram.
- Use only relevant search phrases and avoid duplicate or generic filler tags.

## Failure handling

- Stop after one repeated failure and diagnose the cause before changing methods.
- Do not invent unsupported GUI workarounds or claim success before verifying the exported container.
