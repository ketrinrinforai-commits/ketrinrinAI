from pathlib import Path
import textwrap
from urllib.parse import quote

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ketrinrin-ai-portfolio.pdf"
BUILD = ROOT / ".pdf-build"
BUILD.mkdir(exist_ok=True)
PUBLIC_FOLDER_URL = "https://disk.yandex.ru/d/xoXUtzBqId7gAg"
PORTRAIT = Path("/Users/rabota/Documents/Снимок экрана 2026-06-24 в 17.48.12.png")

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
pdfmetrics.registerFont(TTFont("Portfolio", FONT))
pdfmetrics.registerFont(TTFont("Portfolio-Bold", FONT_BOLD))

PAGE_W, PAGE_H = landscape(A4)

PAPER = colors.HexColor("#f7f3ea")
PAPER_STRONG = colors.HexColor("#efe7d8")
INK = colors.HexColor("#171513")
MUTED = colors.HexColor("#6d675e")
CORAL = colors.HexColor("#e85936")
TEAL = colors.HexColor("#14796f")
GOLD = colors.HexColor("#efbf3b")
WHITE = colors.HexColor("#fffdfa")
LINE = colors.HexColor("#d8cebe")
DARK = colors.HexColor("#161513")


def image_path(name):
    return ROOT / "assets" / "thumbnails" / name


def work_url(path):
    return f"{PUBLIC_FOLDER_URL}?path={quote(path)}"


def crop_image(src, w, h, name):
    img = Image.open(src).convert("RGB")
    target_ratio = w / h
    ratio = img.width / img.height
    if ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        box = (left, 0, left + new_w, img.height)
    else:
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        box = (0, top, img.width, top + new_h)
    out = BUILD / name
    img.crop(box).resize((int(w * 2), int(h * 2))).save(out, quality=92)
    return out


def draw_text(c, text, x, y, size=12, font="Portfolio", color=INK, leading=None, max_width=None, max_lines=None):
    c.setFillColor(color)
    c.setFont(font, size)
    if max_width is None:
        c.drawString(x, y, text)
        return y - (leading or size * 1.25)
    avg = size * 0.48
    width_chars = max(12, int(max_width / avg))
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width_chars) or [""])
    if max_lines is not None:
        lines = lines[:max_lines]
    line_h = leading or size * 1.25
    for line in lines:
        c.drawString(x, y, line)
        y -= line_h
    return y


def draw_label(c, text, x, y, color=TEAL):
    c.setStrokeColor(color)
    c.setLineWidth(1.4)
    c.line(x, y + 4, x + 30, y + 4)
    draw_text(c, text.upper(), x + 40, y, 8.5, "Portfolio-Bold", color)


def draw_page_num(c, n):
    draw_text(c, f"ketrinrin AI portfolio / {n:02d}", 42, 22, 8.5, "Portfolio-Bold", MUTED)


def draw_title(c, title, subtitle=None, page_num=None, dark=False):
    bg = DARK if dark else PAPER
    fg = WHITE if dark else INK
    muted = colors.HexColor("#c8bfb2") if dark else MUTED
    c.setFillColor(bg)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_label(c, "AI video creator / motion storytelling", 42, PAGE_H - 56, GOLD if dark else TEAL)
    draw_text(c, title, 42, PAGE_H - 112, 38, "Portfolio-Bold", fg, 41, 560)
    if subtitle:
        draw_text(c, subtitle, 44, PAGE_H - 232, 14, "Portfolio", muted, 19, 500)
    if page_num:
        draw_page_num(c, page_num)


def rounded_rect(c, x, y, w, h, fill, stroke=None):
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1 if stroke else 0)


def cover(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    hero = crop_image(image_path("project-6.jpg"), PAGE_W, PAGE_H, "cover.jpg")
    c.drawImage(ImageReader(hero), 0, 0, PAGE_W, PAGE_H, mask=None)
    c.setFillColor(colors.Color(0.97, 0.94, 0.88, alpha=0.86))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_label(c, "AI video creator / motion storytelling", 48, PAGE_H - 78, TEAL)
    draw_text(c, "ketrinrin AI", 48, PAGE_H - 138, 22, "Portfolio-Bold", INK)
    draw_text(c, "Видео, промо и\nвизуальные миры\nс помощью ИИ", 46, PAGE_H - 205, 50, "Portfolio-Bold", INK, 55, 520)
    draw_text(
        c,
        "AI-видео для брендов, событий и личных проектов: reels, промо, видеоафиши, AI-сериалы, поздравления и памятные ролики.",
        50,
        95,
        15,
        "Portfolio",
        colors.HexColor("#3e3933"),
        21,
        520,
    )
    c.setFillColor(INK)
    c.circle(48, 46, 7, fill=1, stroke=0)
    draw_text(c, "e.s.a.22@yandex.ru   /   Telegram @ketrinrin   /   Instagram @ketrin__rin", 66, 41, 10, "Portfolio-Bold", INK)
    c.showPage()


def about(c):
    draw_title(c, "Обо мне", None, 2)
    portrait = crop_image(PORTRAIT, 245, 330, "portrait.jpg")
    c.drawImage(ImageReader(portrait), 48, 86, 245, 330)
    c.setStrokeColor(LINE)
    c.setLineWidth(1.4)
    c.roundRect(48, 86, 245, 330, 8, fill=0, stroke=1)
    draw_text(c, "Сапрыкина Екатерина", 335, PAGE_H - 154, 28, "Portfolio-Bold", INK, 32, 420)
    draw_text(c, "AI-креатор / AI-режиссер", 337, PAGE_H - 198, 17, "Portfolio-Bold", TEAL, 20, 420)
    draw_text(
        c,
        "Создаю AI-контент для брендов, событий и личных проектов: от промо-роликов, reels и видеоафиш до AI-сериалов, поздравлений и памятных видео.",
        337,
        PAGE_H - 246,
        13.5,
        "Portfolio",
        colors.HexColor("#3e3933"),
        18,
        415,
    )
    draw_text(
        c,
        "Работала с брендами Karnity и Aurumix, фестивалем Летник, чемпионатами Стрелка и Cever Dance Forever, а также с event- и личными проектами.",
        337,
        PAGE_H - 322,
        13.5,
        "Portfolio",
        colors.HexColor("#3e3933"),
        18,
        415,
    )
    rounded_rect(c, 337, 118, 368, 72, WHITE, LINE)
    draw_text(c, "Портфолио и все работы", 357, 160, 10, "Portfolio-Bold", TEAL)
    draw_text(c, "disk.yandex.ru/d/xoXUtzBqId7gAg", 357, 136, 17, "Portfolio-Bold", INK)
    c.linkURL(PUBLIC_FOLDER_URL, (337, 118, 705, 190), relative=0)
    c.showPage()


def formats(c):
    draw_title(c, "Форматы работы", None, 3, dark=True)
    draw_text(
        c,
        "Коммерческий рекламный и промо-контент, а также видео для личных целей: поздравления, памятные ролики для выпускников и другие эмоциональные истории.",
        44,
        PAGE_H - 205,
        12,
        "Portfolio",
        colors.HexColor("#c8bfb2"),
        16,
        680,
    )
    cards = [
        ("Social-first", "Reels, shorts и видеоафиши", "Короткие ролики для первого касания: анонсы, обложки, промо, вертикальные видео под соцсети."),
        ("Brand worlds", "AI-сериалы и брендовые вселенные", "Серийный контент с единым визуальным языком, персонажами, настроением и узнаваемостью."),
        ("Event & personal", "Промо и личные видео", "Видеоупаковка мероприятий, фестивалей, поздравлений, выпускных и памятных историй."),
    ]
    x = 42
    y = PAGE_H - 360
    w = (PAGE_W - 108) / 3
    for idx, (label, title, body) in enumerate(cards):
        cx = x + idx * (w + 12)
        fill = [colors.HexColor("#1f1d1a"), colors.HexColor("#203734"), colors.HexColor("#4d462e")][idx]
        rounded_rect(c, cx, y, w, 132, fill)
        draw_text(c, label.upper(), cx + 18, y + 100, 8.5, "Portfolio-Bold", GOLD)
        draw_text(c, title, cx + 18, y + 74, 17, "Portfolio-Bold", WHITE, 19, w - 36)
        draw_text(c, body, cx + 18, y + 35, 10.5, "Portfolio", colors.HexColor("#e2d9cc"), 14, w - 36)

    rounded_rect(c, 42, 82, PAGE_W - 84, 76, colors.HexColor("#23211e"), colors.HexColor("#4b4640"))
    draw_text(c, "Что можно обсудить", 66, 126, 10, "Portfolio-Bold", GOLD)
    draw_text(
        c,
        "AI-ролик для соцсетей, видеоафишу, промо события, брендовый AI-сериал, mood film, поздравление или памятную видеоисторию.",
        66,
        104,
        13,
        "Portfolio",
        colors.HexColor("#e2d9cc"),
        17,
        PAGE_W - 132,
    )
    c.showPage()


WORKS = [
    ("Aurumix", "Reel / brand video", "Короткий брендовый ролик с акцентом на визуальное ощущение продукта.", "project-1.jpg", "/Проекты/Reel для Aurumix.mov"),
    ("МК по электро", "Motion poster / event", "Динамичная видеоафиша для анонса мастер-класса.", "project-2.jpg", "/Проекты/Афиша для МК по электро.mov"),
    ("Alya Prokach", "Announcement / social", "Афиша-анонс с фокусом на персону и настроение события.", "project-3.jpg", "/Проекты/Афиша-анонс для Alya Prokach.mov"),
    ("Чемпионат Стрелка", "Promo / competition", "Промо для чемпионата: темп, масштаб и визуальная драматургия.", "project-4.jpg", "/Проекты/Видео для чемпионата Стрелка (Москва,2026).mov"),
    ("Karnity, серия 1", "AI series / episode 01", "Старт брендового AI-сериала и визуального мира.", "project-5.jpg", "/Проекты/ИИ сериал для Karnity, серия 1.mp4"),
    ("Karnity, серия 2", "AI series / episode 02", "Продолжение серии с сохранением визуальной преемственности.", "project-6.jpg", "/Проекты/ИИ сериал для Karnity, серия 2.mov"),
    ("Karnity, серия 3", "AI series / episode 03", "Закрепление сериального формата и узнаваемости.", "project-7.jpg", "/Проекты/ИИ сериал для бренда Karnity. Серия 3.mov"),
    ("Видео для выпускников", "Memory video / personal", "Эмоциональный ролик для памятного события.", "project-8.jpg", "/Проекты/Памятное видео для выпускников.mov"),
    ("CDF-2026", "Promo / festival", "Промо для Cever Dance Forever: быстрая event-коммуникация.", "project-9.jpg", "/Проекты/Промо для CDF-2026.mov"),
    ("Фестиваль Летник", "Promo / Moscow 2026", "Летнее event-промо с городской атмосферой.", "project-10.jpg", "/Проекты/Промо-видео для фестиваля Летник( Москва, 2026).mov"),
    ("ketrinrin electro", "Motion poster / own project", "Собственный анонс мастер-класса в формате соцсетей.", "project-11.jpg", "/Проекты/афиша мк по электро для ketrinrin .mov"),
    ("GRLZ PWR BATTLE", "Promo / battle", "Энергичное промо для баттла с яркой event-идентичностью.", "project-12.jpg", "/Проекты/промо видео GRLZ PWR BATTLE .mov"),
    ("NEW G", "Promo / long version", "Развернутая версия промо-ролика для бренда.", "project-13.jpg", "/Проекты/промо видео для NEW G длинная версия.mov"),
    ("Hourses", "Art video / visual sketch", "Авторская зарисовка на границе fashion и dreamscape.", "creative-1.jpg", "/Творчество/Творческая зарисовка “Hourses”.mov"),
    ("Angel", "Art video / character mood", "Атмосферная работа с персонажем, светом и cinematic-образностью.", "creative-2.jpg", "/Творчество/Творческое видео “Angel”.mov"),
    ("New Year's Eve", "Art video / seasonal story", "Праздничная визуальная история с настроением ночного ожидания.", "creative-3.jpg", "/Творчество/Творческое видео “New Year’s Eve”.mp4"),
]

WORK_BY_TITLE = {work[0]: work for work in WORKS}


def work_card(c, work, x, y, w, h):
    title, meta, body, img_name, source_path = work
    rounded_rect(c, x, y, w, h, WHITE, LINE)
    img_h = h * 0.50
    img = crop_image(image_path(img_name), w - 16, img_h, f"pdf-{img_name}")
    c.drawImage(ImageReader(img), x + 8, y + h - img_h - 8, w - 16, img_h)
    text_y = y + h - img_h - 28
    text_y = draw_text(c, meta.upper(), x + 12, text_y, 7.2, "Portfolio-Bold", TEAL)
    text_y = draw_text(c, title, x + 12, text_y - 5, 13.5, "Portfolio-Bold", INK, 15, w - 24)
    draw_text(c, body, x + 12, min(text_y - 4, y + 43), 8.4, "Portfolio", MUTED, 10.5, w - 24, max_lines=2)
    draw_text(c, "Смотреть работу ->", x + 12, y + 15, 7.2, "Portfolio-Bold", TEAL)
    c.linkURL(work_url(source_path), (x, y, x + w, y + h), relative=0)


def works_page(c, works, title, subtitle, page_num):
    draw_title(c, title, None, page_num)
    cols = 3
    rows = 2
    gap = 12
    x0 = 42
    grid_y = 36
    card_w = (PAGE_W - 84 - gap * (cols - 1)) / cols
    card_h = 186
    for idx, work in enumerate(works):
        col = idx % cols
        row = idx // cols
        x = x0 + col * (card_w + gap)
        y = grid_y + (rows - 1 - row) * (card_h + gap)
        work_card(c, work, x, y, card_w, card_h)
    c.showPage()


def contacts(c):
    draw_title(c, "Буду рада сотрудничеству", None, 7, dark=True)
    draw_text(
        c,
        "Если вам нужен AI-ролик для бренда, события, личного проекта или визуальной кампании, напишите мне. Обсудим идею, формат, настроение и то, какой эффект должен произвести ролик.",
        44,
        PAGE_H - 205,
        12,
        "Portfolio",
        colors.HexColor("#c8bfb2"),
        16,
        700,
    )
    items = [
        ("Почта", "e.s.a.22@yandex.ru", "mailto:e.s.a.22@yandex.ru"),
        ("Instagram", "instagram.com/ketrin__rin", "https://www.instagram.com/ketrin__rin?igsh=MWwzc2g2a2ZrN2E0bg%3D%3D&utm_source=qr"),
        ("Telegram", "@ketrinrin", "https://t.me/ketrinrin"),
    ]
    y = PAGE_H - 330
    for label, value, url in items:
        rounded_rect(c, 48, y, 420, 56, colors.HexColor("#23211e"), colors.HexColor("#4b4640"))
        draw_text(c, label.upper(), 68, y + 35, 8.5, "Portfolio-Bold", GOLD)
        draw_text(c, value, 68, y + 16, 16, "Portfolio-Bold", WHITE)
        c.linkURL(url, (48, y, 468, y + 56), relative=0)
        y -= 72
    draw_text(c, "Портфолио и исходные работы:", 508, PAGE_H - 300, 10, "Portfolio-Bold", GOLD)
    draw_text(c, "disk.yandex.ru/d/xoXUtzBqId7gAg", 508, PAGE_H - 326, 18, "Portfolio-Bold", WHITE)
    c.linkURL("https://disk.yandex.ru/d/xoXUtzBqId7gAg", (508, PAGE_H - 340, 780, PAGE_H - 300), relative=0)
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
    c.setTitle("ketrinrin AI portfolio")
    cover(c)
    about(c)
    formats(c)
    cases = [
        WORK_BY_TITLE["Aurumix"],
        WORK_BY_TITLE["Чемпионат Стрелка"],
        WORK_BY_TITLE["Karnity, серия 1"],
        WORK_BY_TITLE["Karnity, серия 2"],
        WORK_BY_TITLE["Karnity, серия 3"],
        WORK_BY_TITLE["Фестиваль Летник"],
    ]
    dance_announcements = [
        WORK_BY_TITLE["Alya Prokach"],
        WORK_BY_TITLE["CDF-2026"],
        WORK_BY_TITLE["NEW G"],
        WORK_BY_TITLE["GRLZ PWR BATTLE"],
        WORK_BY_TITLE["ketrinrin electro"],
    ]
    creative_projects = [
        WORK_BY_TITLE["МК по электро"],
        WORK_BY_TITLE["Hourses"],
        WORK_BY_TITLE["Angel"],
        WORK_BY_TITLE["New Year's Eve"],
        WORK_BY_TITLE["Видео для выпускников"],
    ]
    works_page(c, cases, "Кейсы", "Коммерческие, event- и брендовые проекты: reels, промо, видеоафиши и AI-сериал.", 4)
    works_page(c, dance_announcements, "Анонсы танцевальных событий", "Видеоафиши и промо для танцевальных событий, фестивалей и баттлов.", 5)
    works_page(c, creative_projects, "Творческие проекты", "Авторские AI-видео, личные истории и экспериментальные визуальные зарисовки.", 6)
    contacts(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
