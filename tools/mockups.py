"""Draws the illustrative phone screens of the website (assets/img/screens/*.svg).

They are stand-ins in the app's "Huerta" colours until real screenshots replace them: drop a PNG with
the same name next to them and point the HTML at it.

    python3 tools/mockups.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "screens"

W, H = 360, 760
GARDEN = "#2F7A57"
GARDEN_SOFT = "#D3EBDD"
TERRA = "#C1633D"
TERRA_SOFT = "#F5DFD4"
PAPER = "#F7F8F4"
CARD = "#FFFFFF"
CONT = "#EDF0EA"
CONT_HIGH = "#E1E5DE"
INK = "#1D2520"
INK_SOFT = "#5A645E"
OUTLINE = "#C6CCC4"
FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"


def text(x, y, s, size=14, color=INK, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')


def rect(x, y, w, h, fill, r=0, stroke=None):
    s = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>'


def chip(x, y, label, fill=CONT, color=INK_SOFT, w=None):
    w = w or (len(label) * 7.2 + 22)
    return rect(x, y, w, 26, fill, 13) + text(x + w / 2, y + 17.5, label, 12, color, 600, "middle"), w


def status_bar(dark=False):
    c = "#E5EAE6" if dark else INK
    return text(22, 26, "9:41", 13, c, 600) + text(W - 22, 26, "▮▮▮ 100%", 11, c, 500, "end")


def top_bar(title, dark=False, back=True):
    c = "#E5EAE6" if dark else INK
    out = ""
    if back:
        out += f'<path d="M30 62 l-8 8 8 8" stroke="{c}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    out += text(52 if back else 22, 76, title, 20, c, 700)
    return out


def dish(cx, cy, r, variant=0):
    """A stylised plate seen from above."""
    palettes = [("#F2C14E", "#E8A33D", "#7FAE5B"), ("#C94F3D", "#E07B5F", "#F4E1C1"), ("#E9D3A8", "#D9A95F", "#8DB360")]
    a, b, c = palettes[variant % 3]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" opacity="0.95"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.78}" fill="#F4F1EA"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.58}" fill="{a}"/>'
            f'<circle cx="{cx - r * 0.2}" cy="{cy - r * 0.15}" r="{r * 0.18}" fill="{b}"/>'
            f'<circle cx="{cx + r * 0.22}" cy="{cy + r * 0.12}" r="{r * 0.14}" fill="{b}"/>'
            f'<circle cx="{cx + r * 0.05}" cy="{cy - r * 0.3}" r="{r * 0.07}" fill="{c}"/>'
            f'<circle cx="{cx - r * 0.25}" cy="{cy + r * 0.25}" r="{r * 0.06}" fill="{c}"/>'
            f'<circle cx="{cx + r * 0.32}" cy="{cy - r * 0.18}" r="{r * 0.05}" fill="{c}"/>')


def phone(body, bg=PAPER, dark=False):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs><clipPath id="screen"><rect width="{W}" height="{H}" rx="38"/></clipPath>'
            f'<linearGradient id="photo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9C9A4"/><stop offset="1" stop-color="#5E8C61"/></linearGradient>'
            f'<linearGradient id="warm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9A47F"/><stop offset="1" stop-color="#B85C38"/></linearGradient></defs>'
            f'<g clip-path="url(#screen)">{rect(0, 0, W, H, bg)}{status_bar(dark)}{body}</g></svg>')


def nav_bar(active):
    items = [("Libros", 0), ("Buscar", 1), ("Compra", 2), ("Ajustes", 3)]
    out = rect(0, H - 74, W, 74, CARD) + f'<line x1="0" y1="{H - 74}" x2="{W}" y2="{H - 74}" stroke="{CONT_HIGH}"/>'
    for label, i in items:
        cx = 45 + i * 90
        if i == active:
            out += rect(cx - 30, H - 64, 60, 30, GARDEN_SOFT, 15)
        out += f'<circle cx="{cx}" cy="{H - 49}" r="7" fill="none" stroke="{GARDEN if i == active else INK_SOFT}" stroke-width="2"/>'
        out += text(cx, H - 18, label, 11, GARDEN if i == active else INK_SOFT, 600 if i == active else 500, "middle")
    return out


def books():
    body = top_bar("Mis libros", back=False)
    body += f'<circle cx="{W - 34}" cy="70" r="16" fill="{GARDEN_SOFT}"/>' + text(W - 34, 75, "✦", 14, GARDEN, 700, "middle")
    covers = [("Recetas de la abuela", "url(#warm)", 42), ("Postres", "#E9C46A", 18), ("Cocina del mundo", "url(#photo)", 27), ("Cenas rápidas", "#7FA7C9", 15)]
    for i, (name, fill, n) in enumerate(covers):
        x = 20 + (i % 2) * 165
        y = 106 + (i // 2) * 250
        body += rect(x, y, 155, 236, CARD, 20, CONT_HIGH)
        body += f'<clipPath id="c{i}"><rect x="{x}" y="{y}" width="155" height="170" rx="20"/></clipPath>'
        body += f'<g clip-path="url(#c{i})">{rect(x, y, 155, 190, fill)}{dish(x + 78, y + 86, 46, i)}</g>'
        if i == 0:
            body += f'<circle cx="{x + 134}" cy="{y + 20}" r="12" fill="{CARD}"/>' + text(x + 134, y + 25, "📌", 11, INK, 400, "middle")
        body += text(x + 14, y + 198, name if len(name) < 19 else name[:17] + "…", 14, INK, 700)
        body += text(x + 14, y + 220, f"{n} recetas", 12, INK_SOFT)
    body += rect(W - 150, H - 140, 130, 52, GARDEN, 18) + text(W - 85, H - 108, "+  Nueva receta", 14, "#FFFFFF", 700, "middle")
    return phone(body + nav_bar(0))


def recipe():
    body = f'<clipPath id="hero"><rect x="0" y="0" width="{W}" height="270"/></clipPath>'
    body += f'<g clip-path="url(#hero)">{rect(0, 0, W, 270, "url(#warm)")}{dish(W / 2, 150, 92, 0)}</g>'
    body += f'<circle cx="34" cy="62" r="18" fill="{CARD}" opacity="0.9"/><path d="M38 54 l-8 8 8 8" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    body += rect(0, 250, W, H - 250, PAPER, 26)
    body += text(22, 292, "Tortilla de patatas", 24, INK, 800)
    x = 22
    for label, fill, col in [("Fácil", "#D7ECC8", "#2E4A20"), ("40 min", CONT, INK_SOFT), ("4 raciones", CONT, INK_SOFT), ("España", TERRA_SOFT, TERRA)]:
        c, w = chip(x, 306, label, fill, col)
        body += c
        x += w + 8
    body += rect(22, 346, W - 44, 38, GARDEN_SOFT, 19) + text(W / 2, 370, "▶  Modo cocina", 14, GARDEN, 700, "middle")
    body += text(22, 414, "Ingredientes", 17, GARDEN, 700)
    items = [("500 g de patatas", False), ("6 huevos", False), ("1 cebolla", True), ("Aceite de oliva", False), ("Sal", False)]
    for i, (name, opt) in enumerate(items):
        y = 444 + i * 30
        body += f'<circle cx="30" cy="{y - 5}" r="3.5" fill="{GARDEN}"/>' + text(44, y, name, 14, INK)
        if opt:
            body += text(44 + len(name) * 7.4 + 6, y, "(opcional)", 13, INK_SOFT)
    body += text(22, 610, "Preparación", 17, GARDEN, 700)
    steps = [("1", "Pela y corta las patatas en", "láminas finas."), ("2", "Fríe a ", "fuego medio 20 minutos.")]
    y = 640
    for n, a, b in steps:
        body += text(22, y, n, 15, GARDEN, 800) + text(42, y, a, 14, INK)
        body += text(42, y + 20, b, 14, INK, 700 if n == "2" else 400)
        y += 52
    return phone(body)


def cooking():
    dark_bg = "#121513"
    body = top_bar("Paso 3 de 6", dark=True)
    body += rect(22, 98, W - 44, 6, "#2F3531", 3) + rect(22, 98, (W - 44) * 0.5, 6, "#6BBF93", 3)
    lines = ["Fríe las patatas", "a fuego medio", "durante 20 minutos,", "removiendo de vez", "en cuando."]
    for i, line in enumerate(lines):
        body += text(28, 190 + i * 40, line, 26, "#E5EAE6", 700 if i in (1, 2) else 500)
    body += rect(28, 430, 190, 64, "#1F3A2B", 32) + text(123, 471, "⏱  20:00", 24, "#6BBF93", 800, "middle")
    body += rect(28, 520, W - 56, 56, "#1C211E", 18) + f'<circle cx="60" cy="548" r="14" fill="#2F3531"/>'
    body += text(86, 545, "Manos libres activado", 13, "#E5EAE6", 600) + text(86, 563, "Di «siguiente», «repite» o «temporizador»", 11, "#A7B0AA")
    body += rect(28, H - 120, 140, 60, "#252B27", 30) + text(98, H - 83, "Anterior", 16, "#E5EAE6", 600, "middle")
    body += rect(W - 168, H - 120, 140, 60, "#6BBF93", 30) + text(W - 98, H - 83, "Siguiente", 16, dark_bg, 800, "middle")
    return phone(body, dark_bg, dark=True)


def shopping():
    body = top_bar("Lista de la compra", back=False)
    x = 22
    for label, active in [("Casa", True), ("Fiesta", False), ("Plantillas", False)]:
        c, w = chip(x, 94, label, GARDEN_SOFT if active else CONT, GARDEN if active else INK_SOFT)
        body += c
        x += w + 8
    groups = [("Fruta y verdura", [("Tomates", "1 kg", False), ("Cebollas", "3", True), ("Perejil", "", False)]),
              ("Lácteos y huevos", [("Huevos", "12", False), ("Leche", "2 L", True)]),
              ("Despensa", [("Aceite de oliva", "1 L", False), ("Harina", "500 g", False)])]
    y = 150
    for title, items in groups:
        body += text(22, y, title.upper(), 11, GARDEN, 700)
        y += 14
        body += rect(16, y, W - 32, len(items) * 46, CARD, 16, CONT_HIGH)
        for name, qty, done in items:
            box = f'<rect x="32" y="{y + 14}" width="18" height="18" rx="5" fill="{GARDEN if done else "none"}" stroke="{GARDEN if done else OUTLINE}" stroke-width="2"/>'
            if done:
                box += f'<path d="M36 {y + 23} l4 4 7-8" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            body += box + text(62, y + 28, name, 15, INK_SOFT if done else INK, 500)
            if done:
                body += f'<line x1="62" y1="{y + 23}" x2="{62 + len(name) * 7.6}" y2="{y + 23}" stroke="{INK_SOFT}" stroke-width="1.4"/>'
            if qty:
                body += text(W - 34, y + 28, qty, 13, INK_SOFT, 500, "end")
            y += 46
        y += 26
    body += rect(W - 84, H - 160, 64, 64, GARDEN, 20)
    body += f'<g stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M{W - 66} {H - 140} v-6 h6 M{W - 38} {H - 146} h6 v6 M{W - 66} {H - 116} v6 h6 M{W - 38} {H - 110} h6 v-6"/><path d="M{W - 62} {H - 128} h24"/></g>'
    return phone(body + nav_bar(2))


def product():
    body = top_bar("Ficha del producto")
    body += rect(22, 100, W - 44, 150, CARD, 20, CONT_HIGH)
    body += rect(38, 116, 90, 118, "#F4E9D8", 12) + rect(56, 132, 54, 86, "#E8C07A", 8) + text(83, 182, "AVENA", 10, "#7A5520", 800, "middle")
    body += text(144, 140, "Copos de avena", 17, INK, 700) + text(144, 162, "Marca blanca · 500 g", 12, INK_SOFT)
    body += rect(144, 182, 84, 46, "#E6F3EA", 12) + text(186, 202, "82", 20, GARDEN, 800, "middle") + text(186, 220, "/100", 10, GARDEN, 600, "middle")
    body += text(240, 202, "Excelente", 13, GARDEN, 700)
    body += text(22, 290, "Nutri-Score", 15, INK, 700)
    colors = ["#038141", "#85BB2F", "#FECB02", "#EE8100", "#E63E11"]
    for i, c in enumerate(colors):
        big = i == 0
        body += rect(22 + i * 46 - (4 if big else 0), 304 - (6 if big else 0), 42 + (8 if big else 0), 40 + (12 if big else 0), c, 10)
        body += text(43 + i * 46, 331, "ABCDE"[i], 18 if big else 15, "#fff", 800, "middle")
    body += text(22, 392, "Grupo NOVA", 15, INK, 700)
    body += rect(22, 404, 40, 48, "#038141", 10) + text(42, 435, "1", 22, "#fff", 800, "middle") + text(76, 428, "Alimento sin procesar", 13, INK_SOFT)
    body += text(22, 490, "Alérgenos", 15, INK, 700)
    c, w = chip(22, 502, "Gluten", TERRA_SOFT, TERRA)
    body += c
    body += text(22, 560, "Por 100 g", 15, INK, 700)
    rows = [("Energía", "372 kcal"), ("Grasas", "7 g"), ("Hidratos", "59 g"), ("Fibra", "10 g"), ("Proteínas", "13 g")]
    for i, (k, v) in enumerate(rows):
        y = 590 + i * 30
        body += text(22, y, k, 14, INK_SOFT) + text(W - 22, y, v, 14, INK, 600, "end")
        body += f'<line x1="22" y1="{y + 10}" x2="{W - 22}" y2="{y + 10}" stroke="{CONT_HIGH}"/>'
    return phone(body)


def assistant():
    body = top_bar("Ideas")
    body += text(W - 22, 76, "✦", 18, GARDEN, 700, "end")
    x, y = 22, 100
    for label, active in [("Cena", True), ("Saludable", True), ("De temporada", False), ("Air fryer", False)]:
        c, w = chip(x, y, label, GARDEN_SOFT if active else CONT, GARDEN if active else INK_SOFT)
        if x + w > W - 22:
            x, y = 22, y + 34
            c, w = chip(x, y, label, GARDEN_SOFT if active else CONT, GARDEN if active else INK_SOFT)
        body += c
        x += w + 8
    body += rect(W - 250, 186, 228, 46, GARDEN, 18) + text(W - 136, 214, "¿Qué ceno hoy con calabacín?", 12, "#fff", 600, "middle")
    body += rect(22, 250, W - 60, 300, CARD, 20, CONT_HIGH)
    lines = ["Con lo que tienes en tus libros te", "propongo dos platos ligeros:"]
    for i, l in enumerate(lines):
        body += text(38, 280 + i * 20, l, 13, INK)
    for i, (name, meta, v) in enumerate([("Calabacines rellenos", "35 min · Fácil", 2), ("Tortilla de calabacín", "25 min · Fácil", 0)]):
        y = 330 + i * 84
        body += rect(38, y, W - 92, 72, CONT, 14)
        body += f'<clipPath id="i{i}"><rect x="46" y="{y + 8}" width="56" height="56" rx="10"/></clipPath><g clip-path="url(#i{i})">{rect(46, y + 8, 56, 56, "url(#photo)")}{dish(74, y + 36, 26, v)}</g>'
        body += text(114, y + 32, name, 14, INK, 700) + text(114, y + 52, meta, 12, INK_SOFT)
    body += text(38, 522, "✦ Generado con IA · puede contener errores", 11, INK_SOFT)
    body += rect(22, H - 92, W - 44, 56, CARD, 28, OUTLINE) + text(46, H - 58, "Pregunta lo que quieras de cocina…", 14, INK_SOFT)
    body += f'<circle cx="{W - 52}" cy="{H - 64}" r="18" fill="{GARDEN}"/>' + f'<path d="M{W - 58} {H - 64} h12 m-5 -5 5 5 -5 5" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    return phone(body)


def sync():
    body = top_bar("Sincronización")
    body += rect(22, 100, W - 44, 118, CARD, 20, CONT_HIGH)
    body += f'<circle cx="52" cy="134" r="14" fill="{GARDEN_SOFT}"/>' + f'<path d="M46 134 l4 4 8-8" stroke="{GARDEN}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    body += text(76, 130, "Recetas de casa", 15, INK, 700) + text(76, 150, "miga.mi-casa.lan · al día", 12, INK_SOFT)
    c, w = chip(38, 172, "3 libros", CONT)
    body += c
    c2, w2 = chip(46 + w, 172, "Lista compartida", GARDEN_SOFT, GARDEN)
    body += c2
    body += text(22, 256, "Invitar a otro móvil", 15, INK, 700)
    body += rect(70, 274, 220, 220, CARD, 20, CONT_HIGH)
    import random
    rnd = random.Random(7)
    cell = 9
    for r in range(20):
        for col in range(20):
            corner = (r < 7 and col < 7) or (r < 7 and col > 12) or (r > 12 and col < 7)
            if corner:
                continue
            if rnd.random() < 0.45:
                body += rect(90 + col * cell, 294 + r * cell, cell, cell, INK)
    for (cx, cy) in [(90, 294), (90 + 13 * cell, 294), (90, 294 + 13 * cell)]:
        body += rect(cx, cy, 7 * cell, 7 * cell, INK, 6) + rect(cx + cell, cy + cell, 5 * cell, 5 * cell, CARD, 4) + rect(cx + 2 * cell, cy + 2 * cell, 3 * cell, 3 * cell, INK, 3)
    body += text(W / 2, 524, "Escanéalo desde Miga en el otro móvil", 12, INK_SOFT, 500, "middle")
    body += rect(22, 560, W - 44, 64, TERRA_SOFT, 18) + text(40, 588, "Tu servidor, tus datos", 14, TERRA, 700)
    body += text(40, 608, "Nada pasa por servidores de terceros.", 12, INK_SOFT)
    return phone(body)


SCREENS = {"books": books, "recipe": recipe, "cooking": cooking, "shopping": shopping,
           "product": product, "assistant": assistant, "sync": sync}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in SCREENS.items():
        (OUT / f"{name}.svg").write_text(draw(), encoding="utf-8")
        print("wrote", name)
