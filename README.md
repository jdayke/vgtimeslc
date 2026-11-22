# VGTimes & LibertyCity — шортсы с Claude

Всё, что нужно, чтобы делать вертикальные ролики для VGTimes и LibertyCity так же, как мы: правила монтажа, промпты для подбора тем и SEO, логотипы, скрипты для ПК и шаблон проекта CapCut.

Обновлено 22.11.2026. [Ноябрьские правила, репосты и UGC](knowledge/05-november-updates.md).

## Что где лежит

| Папка | Что внутри |
|---|---|
| `knowledge/` | Знания для Claude: `01` монтаж и шаблон, `02` подборка тем, `03` SEO-пакет, `04` текст для поля Instructions проекта |
| `graphics/logos/` | Логотипы-оверлеи VG001–VG003 и LC 001–LC 003 (обычные и `RIGHT`). Сейчас используются **VG003** и **LC 002** |
| `tools/` | `runner.cmd`/`runner.ps1` — раннер заданий, через который Claude запускает ffmpeg и Python на ПК; `download.cmd`/`download.ps1` — скачивание по ссылкам из `links.txt` (yt-dlp) |
| `tools/jobs-examples/` | Реальные задания прошлых роликов: рендер Paris и Jason (ffmpeg + NVENC), озвучка edge-tts с повторами, тайминги слов whisper, клонирование проекта CapCut, загрузка пресс-кита Rockstar и музыки |
| `capcut-template/VGT & LC/` | Эталонный проект CapCut 9.7 (только JSON, без видео) — из него клонируется структура новых проектов |
| `examples/` | Готовые SEO-пакеты (Paris, Jason), тексты озвучки, ffmpeg filter_complex для сборки, пример таймингов слов |
| `ideas/` | Пример подборки тем и журнал `_log.md` |
| `music/` | Ссылки на треки Kevin MacLeod (CC BY 4.0). Сами WAV не храним — скачать по ссылке |

## Как установить

1. **Проект в claude.ai.** Создать Project, в Instructions вставить `knowledge/04 Инструкции проекта.txt`, в Project knowledge загрузить `knowledge/01`, `02`, `03`.
2. **Папка на ПК.** Склонировать репозиторий, создать рядом рабочую папку со структурой `Footage\`, `Graphics\`, `Work\`, `Renders\`, `Tools\`, `Ideas\`. Положить логотипы из `graphics/logos` в `Graphics\`, содержимое `tools/` — в `Tools\`.
3. **Пути.** В `knowledge/01` заполнить раздел «Настрой под себя» (рабочая папка, CapCut Drafts, ffmpeg, шрифт). Проще всего попросить Claude в чате проекта: «вот мои пути, обнови файл 01».
4. **Приложение Claude для ПК.** Подключить рабочую папку и папку `CapCut Drafts` («+» → Add folder).
5. **Раннер.** Запустить `Tools\runner.cmd` двойным кликом. После перезагрузки ПК — снова.
6. **Поиск тем.** Поставить расширение Claude in Chrome и войти в этом Chrome в Reddit, X и TikTok: из облака Claude эти сайты почти не видит.

## Что нужно поставить на ПК

- ffmpeg (в `runner.ps1` путь `C:\ffmpeg\bin` — поправить под себя). Для NVENC нужна видеокарта NVIDIA, иначе заменить `h264_nvenc` на `libx264`.
- Python 3 + `edge-tts`, `faster-whisper`, `Pillow`; `yt-dlp` для `download.ps1`.
- CapCut для ПК (проверено на 9.7).
- Шрифты (в репозиторий не кладём из-за лицензий): **Montserrat Black** (бесплатный, Google Fonts), **TT Commons Pro Condensed ExtraBlack** (платный, TypeType), **Rhythmic** (рукописный).

## Про шаблон CapCut

Это рабочий проект, а не пустой шаблон: в нём ссылки на видео и музыку с ПК автора, поэтому в CapCut у друга клипы будут «офлайн». Он нужен как образец структуры: Claude копирует из него устройство дорожек, Blur-фон, текст с фоном, логотип с Fade In и эффекты, а медиа подставляет свои. Важно: `id` в `draft_content.json` должен совпадать с `main_timeline_id` в `Timelines/project.json` и с именем папки в `Timelines/`.

## Правила, которые важно не потерять

- Темы про GTA и Rockstar делаем в трёх версиях: VGTimes, LibertyCity, LibertyCity RU. Все остальные игры идут только на VGTimes.
- К каждому готовому ролику нужен SEO-пакет (`knowledge/03`).
- Факты и даты перепроверяем поиском, в том числе релиз GTA 6. Мод, слух или AI-ролик не выдаём за официальное.
- Новые решения по стилю записываем в `knowledge/` и коммитим, чтобы они не терялись между чатами.

[Комплект для коллег в ChatGPT](chatgpt/README.md)
