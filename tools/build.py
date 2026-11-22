"""Builds the static website: index.html (Spanish), en/index.html and the privacy pages.

Texts live here, one dictionary per language; the privacy pages come from content/privacy-*.md
(the same text as PRIVACY.md and the copy inside the app). Every link is relative, so the site
works at https://calamares00.github.io/miga-web/ and on its own domain alike.

    pip install markdown
    python3 tools/build.py
"""
import hashlib
import json
import unicodedata
from html import escape
from pathlib import Path
from urllib.parse import quote

import markdown

ROOT = Path(__file__).resolve().parent.parent

PACKS_REPO = "https://github.com/calamares00/miga-packs"
SERVER_REPO = "https://github.com/calamares00/miga-server"
SERVER_IMAGE = "ghcr.io/calamares00/miga-server:latest"
PLAY_URL = "https://play.google.com/store/apps/details?id=org.calamares.miga"
# False while Miga is in closed testing on Google Play: its store page only opens for testers, so
# the site asks people to join the beta by email instead. Set to True once it is in production.
PLAY_PUBLIC = False
CONTACT = "miga@calamares.org"
SITE_URL = "https://miga.calamares.org/"
YEAR = 2026

ICONS = {
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M7 8v8M11 8v8M15 8v8M18 8v8"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
    "timer": '<path d="M10 2h4M12 14l3-3"/><circle cx="12" cy="14" r="8"/>',
    "sparkles": '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.13a.5.5 0 0 1 .96 0L14.06 8.5A2 2 0 0 0 15.5 9.94l6.13 1.58a.5.5 0 0 1 0 .96L15.5 14.06a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z"/><path d="M20 3v4M22 5h-4"/>',
    "server": '<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><path d="M6 6h.01M6 18h.01"/>',
    "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M9 13h6M9 17h6"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/>',
    "palette": '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.65-.75 1.65-1.69 0-.44-.18-.84-.44-1.13-.29-.29-.44-.65-.44-1.13a1.64 1.64 0 0 1 1.67-1.67h2c3.05 0 5.56-2.5 5.56-5.55C21.97 6.01 17.46 2 12 2z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "archive": '<rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8M10 12h4"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "play": '<path d="m6 3 14 9-14 9V3z"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "volume": '<path d="M11 4.7a.7.7 0 0 0-1.2-.5L6.4 7.6A1.4 1.4 0 0 1 5.4 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.4a1.4 1.4 0 0 1 1 .4l3.4 3.4a.7.7 0 0 0 1.2-.5z"/><path d="M16 9a5 5 0 0 1 0 6M19.4 18.4a9 9 0 0 0 0-12.7"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "widget": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "table": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "ban": '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    "phone": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
    "wheat": '<path d="M2 22 16 8"/><path d="M3.47 12.53 5 11l1.53 1.53a3.5 3.5 0 0 1 0 4.94L5 19l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M7.47 8.53 9 7l1.53 1.53a3.5 3.5 0 0 1 0 4.94L9 15l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M11.47 4.53 13 3l1.53 1.53a3.5 3.5 0 0 1 0 4.94L13 11l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M20 2h2v2a4 4 0 0 1-4 4h-2V6a4 4 0 0 1 4-4Z"/>',
    "wand": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72M14 7l3 3M5 6v4M19 14v4M10 2v2M7 8H3M21 16h-4M11 3H9"/>',
}


def asset_version(name):
    """A short hash of an asset, added to its URL so browsers never mix a new page with an old cached copy."""
    return hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:10]


def icon(name):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


# ---------------------------------------------------------------------------------------------
# Texts
# ---------------------------------------------------------------------------------------------

ES = {
    "lang": "es", "other": "en", "other_label": "English", "other_short": "EN",
    "title": "Miga · Tu recetario familiar y tu lista de la compra",
    "description": "Miga es una app de Android para guardar las recetas de tu familia en libros, cocinar paso a paso y hacer la compra. Sin cuentas, sin anuncios y con tus datos en tu móvil.",
    "nav": [("features", "Funciones"), ("health", "Salud"), ("assistant", "Asistente"), ("sync", "Familia"), ("packs", "Packs"), ("faq", "Preguntas")],
    "theme": "Cambiar tema", "menu": "Menú", "get": "Descargar", "get_beta": "Probar la beta",
    "badge": "Disponible en Google Play", "badge_beta": "Beta cerrada en Google Play",
    "hero_title": "Tus recetas. Tus libros. <em>Tu cocina.</em>",
    "hero_lead": "Miga guarda las recetas de tu familia en libros con su portada, te acompaña paso a paso mientras cocinas, te avisa de los alérgenos que te importan y organiza la compra por los pasillos de tu supermercado. Sin cuentas, sin anuncios y con todo guardado en tu móvil.",
    "play": "Google Play", "soon": "Pronto", "beta": "Apúntate a la beta",
    "beta_note": "Miga está en pruebas en Google Play. Escríbenos desde el correo de tu cuenta de Google y te enviamos la invitación.",
    "beta_subject": "Quiero probar Miga",
    "beta_body": "Hola, quiero probar la beta de Miga. El correo de mi cuenta de Google es: ",
    "hero_badges": ["Sin cuentas", "Sin anuncios", "Sin analítica", "Funciona sin conexión", "Español e inglés"],
    "shot_alt_front": "Pantalla de una receta en Miga", "shot_alt_back": "Lista de libros en Miga",
    "marquee": [("book", "Libros de recetas"), ("utensils", "Modo cocina"), ("timer", "Temporizadores"), ("mic", "Dictado y voz"), ("cart", "Lista de la compra"), ("scan", "Escáner de productos"), ("leaf", "Open Food Facts"), ("sparkles", "Asistente de cocina"), ("server", "Servidor propio"), ("package", "Packs de recetas"), ("shield", "Alérgenos"), ("wheat", "Modo celíacos"), ("pulse", "Raciones de hidratos"), ("bulb", "Consejos de cocina"), ("file", "PDF e imagen"), ("archive", "Copias cifradas"), ("palette", "Temas y marcos"), ("widget", "Widget"), ("lock", "Bloqueo con huella")],
    "pillars_head": ("Hecha para tu cocina, no para vender tus datos", "Miga no tiene servidores propios ni te pide registrarte. Lo que guardas es tuyo y se queda en tu teléfono."),
    "pillars": [
        ("phone", "Todo en tu móvil", "Recetas, fotos, listas y ajustes se guardan en el teléfono. Funciona sin conexión."),
        ("ban", "Sin cuentas ni anuncios", "Ni registro, ni publicidad, ni analítica. Abres la app y empiezas a cocinar."),
        ("shield", "Tú decides qué sale", "Internet solo se usa para lo que activas: tu asistente, Open Food Facts, packs o tu servidor."),
        ("users", "Para toda la familia", "Comparte libros y la lista de la compra con tu propio servidor, sin nadie en medio."),
    ],
    "showcase_head": ("Explora Miga", "Elige una parte de la app para verla tal cual es: estas pantallas son de la app de verdad.", "Vista interactiva"),
    "showcase": [
        ("books", "book", "Libros", "Libros y recetas", "Un recetario para cada cosa",
         "Crea un libro para cada persona o cada tema, cada uno con su portada, y llena sus páginas con recetas completas.",
         [("Recetas completas", "ingredientes con cantidad y unidad, pasos, fotos, dificultad, tiempos, raciones, origen con bandera y etiquetas."),
          ("Subrecetas", "separa la salsa, la masa o la guarnición, cada una con sus ingredientes y sus pasos."),
          ("Ingredientes opcionales", "marca el perejil para decorar sin ensuciar su nombre."),
          ("Packs de recetas", "libros listos para instalar, con cocinas del mundo, arroces, panadería, Thermomix y más."),
          ("Consejo del día", "un truco de cocina cada día y cientos más que funcionan sin conexión.")], "books"),
        ("recipe", "list", "Recetas", "La receta", "Todo claro de un vistazo",
         "Tiempo, raciones y dificultad en una línea; los ingredientes, escritos como los dirías.",
         [("Ingredientes naturales", "«½ vaso de vino», «2 dientes de ajo»: sin tablas ni columnas."),
          ("Raciones al momento", "cambia las raciones y las cantidades se recalculan solas."),
          ("Alérgenos calculados", "los 14 de la ley europea y la lactosa, a partir de los ingredientes."),
          ("Consejos para esta receta", "si un truco ayuda con sus ingredientes o pasos, aparece ahí mismo."),
          ("Mis notas", "apuntes con fecha que no cambian la receta: «la próxima vez, menos sal».")], "recipe"),
        ("cooking", "utensils", "Modo cocina", "Modo cocina", "Cocina con las manos en la masa",
         "Los pasos uno a uno, en grande y sin que se apague la pantalla.",
         [("Temporizadores de un toque", "«cocer 10 minutos» se convierte en un temporizador; puedes tener varios y siguen aunque salgas."),
          ("Lectura en voz alta", "Miga te lee cada paso con la voz que elijas."),
          ("Manos libres", "di «siguiente», «anterior», «repite» o «temporizador» sin tocar el móvil."),
          ("Formato claro", "tiempos y temperaturas resaltados para encontrarlos de un vistazo.")], "cook_mode"),
        ("shopping", "cart", "Compra", "Lista de la compra", "La compra, en el orden de tu súper",
         "Añade lo que falta escribiendo, dictando, escaneando o desde una receta, y recórrela por pasillos.",
         [("Por pasillos", "escribe «limones» o «leche» como siempre y cada cosa va a su pasillo."),
          ("Varias listas y plantillas", "la de casa, la de la fiesta y la compra semanal guardada."),
          ("Modo tienda", "desliza para marcar y la pantalla se queda encendida."),
          ("Compartir", "por texto, con un código QR o sincronizada con tu familia."),
          ("Ficha del producto", "escanea el código de barras y mira Nutri-Score, NOVA, alérgenos y aditivos (Open Food Facts).")], "shopping"),
        ("health", "shield", "Salud", "Alérgenos y salud", "Cocina para quien tienes en la mesa",
         "Miga calcula los alérgenos de cada receta y te ayuda con la celiaquía y con las raciones de hidratos. Todo opcional y sin el asistente.",
         [("Solo los tuyos", "marca tus alergias e intolerancias y cada receta dice «Lleva huevo» o «Sin tus alérgenos»."),
          ("Filtros", "busca «Sin huevo», «Sin ingredientes con gluten» o recetas para celíacos."),
          ("Modo celíacos", "qué comprar certificado y cómo evitar la contaminación cruzada."),
          ("Raciones de hidratos", "cuántas lleva cada receta por persona y cuánto servirte según tu plan.")], "filters"),
        ("assistant", "sparkles", "Asistente", "Asistente de cocina", "Una ayuda cuando la quieras",
         "Funciones opcionales con inteligencia artificial y tu propia clave. Si no lo configuras, no se envía nada.",
         [("Recetas desde fotos", "fotografía una receta de un libro o escrita a mano y precarga el editor."),
          ("Desde una web, Instagram o YouTube", "pega un enlace o comparte un vídeo y obtén la receta limpia, sin anuncios ni historias."),
          ("Mejorar recetas", "pule la redacción y normaliza ingredientes; ves el antes y el después."),
          ("Ideas", "pregunta qué cocinar con lo que tienes, pide un menú semanal o un plato de temporada.")], "new_recipe"),
        ("sync", "users", "Familia", "Sincronización", "Compartid libros y listas en familia",
         "Conecta Miga a un servidor que alojes tú y comparte libros y la lista de la compra entre varios móviles.",
         [("Tu servidor", "miga-server funciona en tu casa o en tu VPS con Docker."),
          ("Invitaciones con QR", "escanea el código desde otro móvil y ya estáis conectados."),
          ("Lista compartida en directo", "se actualiza cada pocos segundos mientras la miras."),
          ("Sin terceros", "los datos van solo a tu servidor.")], "server/mobile.png"),
    ],
    "features_head": ("Todo lo que hace Miga", "Una app completa para la cocina de casa, explicada sin letra pequeña.", "Funciones"),
    "features": [
        ("book", "", "Libros con portada", "Organiza las recetas en libros: el de tu madre, el de un amigo o uno por temas.", ["Fija tus libros favoritos arriba", "Recetas agrupadas por categoría", "Desliza para pasar de receta como las páginas de un libro"]),
        ("search", "", "Buscar y filtrar", "Encuentra cualquier receta en todos tus libros por nombre o ingrediente.", ["Filtros por tiempo, dificultad, categoría, ingredientes, origen y alérgenos", "«¿Qué cocino con lo que tengo?» con lo que hay en tu despensa", "Búsquedas guardadas y recientes"]),
        ("list", "", "Editor cómodo", "Escribir una receta es rápido: pestañas para cada parte y sugerencias de lo que ya has usado.", ["Escribe «200 g de patatas» y Miga separa cantidad, unidad y nombre", "Pasos con negrita, cursiva y listas, o dictados", "Selecciona varias recetas y cámbialas de una vez"]),
        ("camera", "accent", "Fotos a juego", "Recorta, gira y mejora tus fotos, que se guardan con el tamaño justo.", ["Marcos para todas las fotos: Polaroid, galería, viñeta…", "Mejora automática de luz, color y nitidez ✨", "La foto del plato se recorta sola al importar"]),
        ("utensils", "", "Modo cocina", "Los pasos en grande y la pantalla siempre encendida.", ["Varios temporizadores que siguen aunque salgas de la app", "Lectura en voz alta", "Control por voz y manos libres"]),
        ("cart", "", "Lista de la compra", "Desde una receta añades todos sus ingredientes de una vez.", ["Varias listas y plantillas", "Orden por pasillos de tu supermercado", "Modo tienda, QR y widget"]),
        ("scan", "sage", "Escáner y Open Food Facts", "Escanea códigos de barras para añadir productos y ver su ficha.", ["Nutri-Score, NOVA, alérgenos y aditivos", "Puntuación orientativa de 0 a 100", "Datos abiertos bajo licencia ODbL"]),
        ("download", "", "Importar recetas", "Trae recetas de donde estén.", ["Desde una web, un reel de Instagram o un vídeo de YouTube, con su foto y sin necesitar el asistente", "Desde un archivo de Miga o un enlace compartido", "Desde fotos o el nombre de un plato, incluso varias a la vez ✨"]),
        ("shield", "accent", "Alérgenos e intolerancias", "Los 14 alérgenos de la ley europea y la lactosa, calculados con los ingredientes.", ["Muestra todos, solo los tuyos o ninguno", "Aviso en las listas y búsquedas sin tus alérgenos", "Modo celíacos con lo que hay que comprar certificado"]),
        ("pulse", "sage", "Raciones de hidratos", "Para quien cuenta raciones (por ejemplo, con diabetes). Opcional.", ["Raciones por persona en cada receta", "Tu plan por comidas y grupos de alimentos", "«Ajustar a mi comida»: cuánto servirte y qué añadir"]),
        ("heart", "accent", "Favoritos con tus canales y webs", "Sigue canales de YouTube, perfiles de Instagram y webs de recetas.", ["Sus últimos vídeos, reels y recetas, con lo nuevo marcado", "«Ver más recetas» y buscador en muchas webs", "Guarda lo que quieras cocinar e impórtalo con un toque"]),
        ("bulb", "", "Consejos de cocina", "Trucos cortos para cocinar mejor, sin conexión.", ["Un consejo del día en la biblioteca", "Consejos para cada receta según sus ingredientes", "Guárdalos y compártelos"]),
        ("file", "accent", "Exportar y compartir", "Comparte una receta o un libro entero en el formato que necesites.", ["Enlace cifrado que caduca a los 7 días", "PDF con portada e índice, o imagen para WhatsApp e Instagram", "Archivo de Miga para pasarlo a otro móvil, o texto"]),
        ("archive", "", "Copias de seguridad", "Guarda toda tu biblioteca en un archivo y restáurala cuando quieras.", ["Con fotos incluidas", "Cifrado opcional con contraseña (AES-256)", "Compatible con la copia de Android"]),
        ("palette", "sage", "A tu gusto", "Que Miga se vea como te gusta.", ["Tema claro, oscuro o del sistema", "Ocho colores de acento, con Huerta por defecto", "Español e inglés"]),
        ("lock", "", "Privada y segura", "Tus recetas, solo para ti.", ["Bloqueo con huella, rostro o PIN", "Claves del asistente cifradas en el móvil", "Sin cuentas, anuncios ni analítica"]),
    ],
    "pages": {
        "features": ("Funciones", "Todo lo que hace Miga: libros de recetas, modo cocina, lista de la compra por pasillos, escáner, importar recetas, copias de seguridad y más.", "Funciones", "Todo lo que hace Miga", "Una app completa para la cocina de casa, explicada sin letra pequeña y con capturas de la app de verdad."),
        "health": ("Salud", "Alérgenos, modo celíacos y raciones de hidratos en Miga: orientativo, sin el asistente y sin conexión.", "Salud · Opcional", "Alérgenos, celiaquía y raciones de hidratos", "Miga lee los ingredientes de cada receta, sin el asistente y sin conexión, y te dice lo que importa para tu familia."),
        "assistant": ("Asistente de cocina", "El asistente de cocina de Miga: recetas desde fotos, webs, Instagram y YouTube, mejorar recetas e ideas, con tu propia clave y el proveedor que elijas.", "Asistente · Opcional", "Un asistente de cocina que usa tu propia clave", "Las funciones marcadas con ✨ usan inteligencia artificial con la clave que tú configures. Eliges el proveedor y el modelo, y Miga solo envía lo necesario para cada tarea."),
        "sync": ("Familia y sincronización", "Comparte libros y la lista de la compra en familia con miga-server, un servidor de sincronización que alojas tú con Docker.", "miga-server", "Tu propio servidor de sincronización", "Para compartir libros y la lista de la compra en familia, Miga se conecta a un servidor que alojas tú. Es ligero, funciona con Docker y trae una web de administración muy completa."),
        "packs": ("Packs de recetas", "Packs de recetas para Miga: libros listos para instalar con cocinas del mundo, arroces, panadería, Thermomix y más.", "Packs", "Packs de recetas listos para instalar", "Un pack es un libro de recetas que se instala con un toque desde Ajustes › Packs de recetas. Sus recetas no se editan, pero puedes copiar las que quieras a tus libros."),
        "faq": ("Preguntas frecuentes", "Respuestas sobre Miga: precio, privacidad, el asistente de cocina, alérgenos, importar recetas de webs, Instagram y YouTube, y más.", "Ayuda", "Preguntas frecuentes", "Lo que más nos preguntan. ¿No está tu duda? Escríbenos."),
    },
    "home_label": "Inicio", "skip": "Saltar al contenido", "breadcrumb": "Ruta de navegación",
    "prev": "Anterior", "next": "Siguiente", "more": "Ver más", "page_nav": "Más secciones",
    "discover_head": ("Descubre Miga", "Cada parte de la app en su página, con capturas reales.", "Secciones"),
    "discover": {
        "features": ("shopping", "Libros, modo cocina, la compra por pasillos, el escáner, copias y todo lo demás."),
        "health": ("recipe_health", "Tus alérgenos, el modo celíacos y las raciones de hidratos."),
        "assistant": ("share_instagram", "Recetas desde fotos, webs, Instagram y YouTube, ideas y mejoras, con tu clave."),
        "sync": ("server/mobile.png", "Libros y lista de la compra compartidos con tu propio servidor."),
        "packs": ("books", "Libros de recetas listos para instalar con un toque."),
        "faq": ("search", "Precio, privacidad, alergias, iPhone… lo que más nos preguntan."),
    },
    "news_chip": "Novedad",
    "news_title": "Recetas de Instagram y YouTube",
    "news_text": "Comparte un reel o un vídeo con Miga y guárdalo como una receta más: con su foto, y si el texto no la trae, el asistente escucha o ve el vídeo.",
    "insta_chip": "Novedad",
    "insta_title": "Recetas de Instagram y YouTube, en tu libro",
    "insta_lead": "¿Has visto una receta en un reel o en un vídeo? Compártela con Miga o pega su enlace y queda guardada como una receta más, con su foto y el autor en las notas.",
    "insta_points": [
        ("Sin el asistente", "si el texto de la publicación trae los ingredientes y los pasos, Miga los lee directamente."),
        ("Escucha el vídeo ✨", "si el texto no trae la receta, el asistente escucha el vídeo: Gemini oye el audio y OpenAI, Groq o Mistral lo transcriben. Revisa las cantidades."),
        ("Desde Instagram", "toca Compartir en el reel, elige Miga y di en qué libro guardarla."),
        ("La foto buena", "a tamaño completo y sin el botón de reproducir del vídeo."),
        ("YouTube", "la receta de la descripción o de la web del autor que enlaza; si no está, Gemini ve el vídeo: lo que se dice y lo que sale escrito en pantalla."),
    ],
    "insta_shots": [("share_instagram", "Compartir un reel con Miga"), ("new_recipe", "Nueva receta desde una web o Instagram")],
    "health_gallery": [("health_settings", "Ajustes de salud"), ("filters", "Filtros sin tus alérgenos"), ("recipe_health", "Alérgenos e hidratos de una receta"), ("fit_meal", "Ajustar a mi comida")],
    "assistant_more": "Ideas y mejoras",
    "assistant_chip": "Opcional",
    "assistant_title": "Un asistente de cocina que usa tu propia clave",
    "assistant_lead": "Las funciones marcadas con ✨ usan inteligencia artificial con la clave que tú configures. Eliges el proveedor y el modelo, y Miga solo envía lo necesario para cada tarea.",
    "assistant_points": [
        ("Recetas desde fotos y webs", "lee el texto de una foto o de una página y precarga el editor; al importar de una web, también la pule. Tú lo revisas antes de guardar."),
        ("Recetas de vídeos", "si un reel de Instagram o un vídeo de YouTube no trae la receta en el texto, la saca del vídeo: lo que se dice y, en YouTube con Gemini, lo que sale escrito en pantalla."),
        ("Mejorar recetas", "una o muchas a la vez: mejor redacción, ingredientes normalizados y tiempos en negrita. Nada se guarda sin tu permiso."),
        ("Ideas", "recomendaciones a partir de tus recetas, menús semanales y respuestas sobre técnicas, conservación o sustituciones."),
        ("Salud y nutrición", "valoración orientativa, calorías y macros por ración, y sustitutos de ingredientes."),
        ("Sigue aunque salgas", "las tareas largas continúan en segundo plano con una notificación que te lleva al resultado."),
        ("Fácil de configurar", "«Conectar con OpenRouter» crea la clave por ti; con el resto, «Conseguir clave» y «Probar conexión»."),
        ("Transparente", "el contenido generado se marca como tal y puedes reportarlo. Si no hay clave, no se envía nada."),
    ],
    "health_chip": "Opcional",
    "health_title": "Alérgenos, celiaquía y raciones de hidratos",
    "health_lead": "Miga lee los ingredientes de cada receta, sin el asistente y sin conexión, y te dice lo que importa para tu familia. En Ajustes › Salud eliges qué ver.",
    "health_points": [
        ("14 alérgenos y lactosa", "los que la ley europea obliga a declarar. «Contiene» o «Puede contener» según el producto que compres, con la explicación al tocar el aviso."),
        ("Solo lo tuyo", "todos los alérgenos, solo los tuyos o ninguno; avisos en las listas y búsquedas que empiezan sin ellos."),
        ("Celíacos", "qué ingredientes llevan gluten, cuáles comprar certificados y cómo evitar la contaminación cruzada."),
        ("Raciones de hidratos", "cuántas raciones lleva cada receta por persona (10 g por ración, o la que te indiquen)."),
        ("Ajustar a mi comida", "con tu plan de raciones por grupos, cuánto servirte y qué añadir para completar esa comida, en medidas caseras."),
    ],
    "health_note": "Es orientativo: revisa siempre la etiqueta de cada producto y sigue la pauta de tu equipo médico.",
    "gallery_head": ("Así es Miga por dentro", "Pantallas de la app tal cual, con recetas de los packs.", "Capturas"),
    "gallery": [("books", "Tu biblioteca"), ("recipe", "Una receta"), ("cook_mode", "Modo cocina"), ("shopping", "La compra por pasillos"), ("search", "Buscar recetas"), ("health_settings", "Ajustes de salud"), ("recipe_health", "Alérgenos e hidratos"), ("fit_meal", "Ajustar a mi comida"), ("ideas", "Ideas del asistente"), ("recipe_dark", "Tema oscuro")],
    "providers": ["Google Gemini", "Anthropic Claude", "OpenAI", "DeepSeek", "Mistral", "Groq", "OpenRouter (modelos gratuitos)", "Compatible con OpenAI (Ollama, LM Studio…)"],
    "providers_note": "Si añades varios, se usan en el orden que elijas: si uno falla, se prueba el siguiente.",
    "server_chip": "miga-server",
    "server_title": "Tu propio servidor de sincronización",
    "server_lead": "Para compartir libros y la lista de la compra en familia, Miga se conecta a un servidor que alojas tú. Es ligero, funciona con Docker y trae una web de administración muy completa.",
    "server_steps": [
        ("Arranca el servidor", "guarda el <code>docker-compose.yml</code> de abajo, cambia el token de administrador por una cadena larga y aleatoria (por ejemplo, la salida de <code>openssl rand -base64 32</code>) y ejecuta <code>docker compose up -d</code>."),
        ("Crea un espacio compartido", "desde la web de administración (<code>http://tu-servidor:8080/ui</code>), crea un namespace (por ejemplo, «casa») y un token para cada móvil."),
        ("Conecta la app", "en Ajustes › Servidor de sincronización, añade la conexión. El resto de la familia se une escaneando un QR."),
    ],
    "server_features": [
        ("users", "Espacios privados", "cada namespace lo comparten los móviles que tú decidas, con un token por dispositivo que puedes revocar."),
        ("refresh", "Sincronización fiable", "libros, recetas, fotos y listas, con «la última edición gana» aunque los relojes no coincidan."),
        ("table", "Administración web", "edita recetas en una tabla como en una hoja de cálculo, cambia muchas a la vez o usa el editor completo."),
        ("file", "PDF desde el navegador", "descarga una receta o un libro entero con el mismo diseño que la app, en español o inglés."),
        ("archive", "Copias automáticas", "una copia diaria con rotación, y copias y descargas con un clic."),
        ("lock", "Sin dependencias externas", "una sola imagen Docker con SQLite; ponla detrás de un proxy con TLS para usarla fuera de casa."),
    ],
    "server_gallery": [("table.png", "Recetas en modo tabla, con acciones sobre varias a la vez"), ("editor-dark.png", "Editor de recetas en modo oscuro"), ("grid.png", "Vista de cuadrícula con fotos"), ("mobile.png", "También funciona en el móvil")],
    "server_compose_note": "Con este archivo basta: la imagen trae todo lo necesario y los datos se guardan en el volumen <code>miga-data</code>.",
    "admin_token_placeholder": "cambia-esto-por-un-token-largo",
    "server_cta": "Ver miga-server",
    "server_admin_title": "La web de administración",
    "packs_chip": "Packs",
    "packs_title": "Packs de recetas listos para instalar",
    "packs_lead": "Un pack es un libro de recetas que se instala con un toque desde Ajustes › Packs de recetas. Sus recetas no se editan, pero puedes copiar las que quieras a tus libros.",
    "packs_points": [
        ("Catálogo oficial", "Miga consulta el catálogo de esta web; cada pack trae su portada, su autor y una descripción."),
        ("Catálogos alternativos", "añade otro catálogo con una URL o un repositorio de GitHub «usuario/repositorio»."),
        ("Crea el tuyo", "exporta un libro como archivo de Miga (ZIP) y descríbelo en un <code>catalog.json</code>."),
    ],
    "packs_example_title": "Ejemplo de catalog.json",
    "packs_cta": "Repositorio de packs",
    "packs_available": "Packs disponibles",
    "faq_head": ("Preguntas frecuentes", "", "Ayuda"),
    "faq_beta": ("¿Cómo consigo Miga?", f"Ahora mismo está en pruebas cerradas en Google Play. Escríbenos a {CONTACT} desde el correo de tu cuenta de Google y te enviamos la invitación. Pronto estará disponible para todo el mundo."),
    "faq": [
        ("¿Miga es gratis?", "Sí. Es gratuita, sin anuncios ni compras dentro de la app."),
        ("¿Necesito una cuenta o internet?", "No. Todo funciona sin conexión y sin registrarte. Internet solo se usa para las funciones que eliges: el asistente con tu clave, Open Food Facts, el catálogo de packs y tu servidor."),
        ("¿Cuánto cuesta el asistente de cocina?", "Depende del proveedor que elijas. Con OpenRouter hay modelos gratuitos; con Groq hay una capa gratuita y con un modelo en tu propio ordenador (Ollama, LM Studio) no pagas nada; con Gemini, Claude, OpenAI, DeepSeek o Mistral pagas a ellos según tu uso. Miga no cobra nada ni ve tus datos."),
        ("¿Dónde se guardan mis recetas?", "En el almacenamiento interno de tu móvil. Si usas la sincronización, también en tu propio servidor. Miga no tiene servidores propios."),
        ("¿Puedo pasar mis recetas a otro móvil?", "Sí: con una copia de seguridad completa (opcionalmente cifrada), exportando libros como archivo de Miga o con la sincronización."),
        ("¿Sirve si tengo alergias, celiaquía o diabetes?", "Miga calcula los alérgenos y las raciones de hidratos a partir de los ingredientes para ayudarte a elegir y a organizarte, pero es orientativo: no puede ver las marcas ni las etiquetas. Revisa siempre la etiqueta de cada producto y sigue la pauta de tu equipo médico."),
        ("¿Puedo guardar recetas de webs?", "Sí. Pega el enlace y Miga lee la receta con su foto, tiempos y raciones, sin necesitar el asistente: casi todas las webs de recetas usan un formato estándar. Con el asistente configurado, además la pule."),
        ("¿Y webs de recetas?", "También. En Favoritos, pega una web de cocina o una de sus secciones (por ejemplo, su página de recetas) y verás sus últimas recetas con foto. En muchas webs puedes ver más recetas hacia atrás y buscar una concreta. Se importan con un toque, sin el asistente cuando la web trae la receta en el formato estándar."),
        ("¿Puedo seguir a mis cocineros de YouTube e Instagram?", "Sí. En Favoritos, pega el enlace de un canal de YouTube o de un perfil de Instagram (o compártelo con Miga) y verás sus últimos vídeos y reels: 15 en YouTube y 6 en Instagram. Guarda los que te gusten e impórtalos como receta. Miga los consulta directamente, sin cuenta; las cuentas privadas no se pueden seguir."),
        ("¿Y recetas de YouTube?", "Sí. Pega el enlace de un vídeo o un Short, o compártelo desde YouTube con Miga. Si la descripción trae la receta o enlaza a la web del autor, Miga la importa de ahí; si no, Gemini puede ver el vídeo (lo que se dice y lo que sale escrito en pantalla). Los demás asistentes solo leen la descripción."),
        ("¿Y recetas de Instagram?", "Sí. Pega el enlace de una publicación o un reel, o compártelo desde Instagram con Miga. Si el texto trae los ingredientes y los pasos, Miga los lee sin el asistente; si no, el asistente lee el texto o escucha el vídeo (con Gemini, OpenAI, Groq o Mistral). Las publicaciones privadas no se pueden importar."),
        ("¿Hay versión para iPhone?", "De momento Miga es solo para Android (8.0 o superior)."),
        ("¿Qué datos usa de Open Food Facts?", "Al escanear un código o buscar un producto se envía ese código o ese texto a Open Food Facts para obtener su ficha. Los datos son abiertos (licencia ODbL)."),
    ],
    "cta_title": "Empieza tu recetario hoy",
    "cta_text": "Descarga Miga, crea tu primer libro y guarda esa receta que siempre te piden.",
    "cta_text_beta": "Apúntate a la beta, crea tu primer libro y guarda esa receta que siempre te piden.",
    "footer_tagline": "El recetario de tu familia y tu lista de la compra, en tu móvil.",
    "footer_cols": [
        ("Miga", [("features", "Funciones"), ("health", "Salud"), ("assistant", "Asistente de cocina"), ("faq", "Preguntas frecuentes")]),
        ("Más", [("sync", "Servidor de sincronización"), ("packs", "Packs de recetas"), (SERVER_REPO, "miga-server"), (PACKS_REPO, "miga-packs")]),
        ("Legal", [("privacy", "Política de privacidad"), (f"mailto:{CONTACT}", "Contacto")]),
    ],
    "legal": f"© {YEAR} Calamares. Las recetas de los packs se publican bajo CC BY 4.0.",
    "off": "Datos de productos de Open Food Facts (ODbL).",
    "privacy_title": "Política de privacidad · Miga",
    "back": "Volver al inicio",
}

EN = {
    "lang": "en", "other": "es", "other_label": "Español", "other_short": "ES",
    "title": "Miga · Your family recipe book and shopping list",
    "description": "Miga is an Android app to keep your family's recipes in books, cook step by step and do the shopping. No accounts, no ads, and your data stays on your phone.",
    "nav": [("features", "Features"), ("health", "Health"), ("assistant", "Assistant"), ("sync", "Family"), ("packs", "Packs"), ("faq", "FAQ")],
    "theme": "Switch theme", "menu": "Menu", "get": "Download", "get_beta": "Try the beta",
    "badge": "Available on Google Play", "badge_beta": "Closed beta on Google Play",
    "hero_title": "Your recipes. Your books. <em>Your kitchen.</em>",
    "hero_lead": "Miga keeps your family's recipes in books with their own covers, guides you step by step while you cook, flags the allergens that matter to you and sorts the shopping by your supermarket's aisles. No accounts, no ads, and everything stays on your phone.",
    "play": "Google Play", "soon": "Soon", "beta": "Join the beta",
    "beta_note": "Miga is in testing on Google Play. Email us from your Google account's address and we'll send you an invitation.",
    "beta_subject": "I'd like to try Miga",
    "beta_body": "Hi, I'd like to try the Miga beta. My Google account's email is: ",
    "hero_badges": ["No accounts", "No ads", "No analytics", "Works offline", "English and Spanish"],
    "shot_alt_front": "A recipe in Miga", "shot_alt_back": "The list of books in Miga",
    "marquee": [("book", "Recipe books"), ("utensils", "Cooking mode"), ("timer", "Timers"), ("mic", "Dictation and voice"), ("cart", "Shopping list"), ("scan", "Product scanner"), ("leaf", "Open Food Facts"), ("sparkles", "Cooking assistant"), ("server", "Your own server"), ("package", "Recipe packs"), ("shield", "Allergens"), ("wheat", "Coeliac mode"), ("pulse", "Carb portions"), ("bulb", "Cooking tips"), ("file", "PDF and image"), ("archive", "Encrypted backups"), ("palette", "Themes and frames"), ("widget", "Widget"), ("lock", "Fingerprint lock")],
    "pillars_head": ("Made for your kitchen, not to sell your data", "Miga has no servers of its own and never asks you to sign up. What you save is yours and stays on your phone."),
    "pillars": [
        ("phone", "Everything on your phone", "Recipes, photos, lists and settings live on the phone. It works offline."),
        ("ban", "No accounts, no ads", "No sign-up, no advertising, no analytics. Open the app and start cooking."),
        ("shield", "You decide what leaves", "The internet is only used for what you turn on: your assistant, Open Food Facts, packs or your server."),
        ("users", "For the whole family", "Share books and the shopping list through your own server, with no one in between."),
    ],
    "showcase_head": ("Explore Miga", "Pick a part of the app to see it as it is: these are screens of the real app.", "Interactive preview"),
    "showcase": [
        ("books", "book", "Books", "Books and recipes", "A recipe book for everything",
         "Make a book for each person or each topic, each with its own cover, and fill it with complete recipes.",
         [("Complete recipes", "ingredients with quantity and unit, steps, photos, difficulty, times, servings, origin with a flag and tags."),
          ("Sub-recipes", "keep the sauce, the dough or the side apart, each with its own ingredients and steps."),
          ("Optional ingredients", "mark the parsley for garnish without cluttering its name."),
          ("Recipe packs", "ready-made books to install: world cuisines, rice dishes, baking, Thermomix and more."),
          ("Tip of the day", "a cooking tip every day and hundreds more that work offline.")], "books"),
        ("recipe", "list", "Recipes", "The recipe", "Everything clear at a glance",
         "Time, servings and difficulty in one line; ingredients written the way you'd say them.",
         [("Natural ingredients", "“½ glass of wine”, “2 cloves garlic”: no tables or columns."),
          ("Servings on the fly", "change the servings and the quantities update themselves."),
          ("Allergens worked out", "the 14 of EU law plus lactose, from the ingredients."),
          ("Tips for this recipe", "if a tip helps with its ingredients or steps, it shows up right there."),
          ("My notes", "dated notes that never change the recipe: “next time, less salt”.")], "recipe"),
        ("cooking", "utensils", "Cooking", "Cooking mode", "Cook with your hands in the dough",
         "One step at a time, in large type, with the screen kept on.",
         [("One-tap timers", "“simmer for 10 minutes” turns into a timer; run several and they keep going when you leave."),
          ("Read aloud", "Miga reads each step with the voice you choose."),
          ("Hands-free", "say “next”, “back”, “repeat” or “timer” without touching the phone."),
          ("Clear formatting", "times and temperatures highlighted, easy to spot.")], "cook_mode"),
        ("shopping", "cart", "Shopping", "Shopping list", "Shopping in your supermarket's order",
         "Add what you need by typing, dictating, scanning or straight from a recipe, and walk it aisle by aisle.",
         [("By aisle", "write “lemons” or “milk” as usual and each item goes to its aisle."),
          ("Several lists and templates", "home, the party, and your saved weekly shop."),
          ("Store mode", "swipe to tick items off while the screen stays on."),
          ("Share", "as text, with a QR code or synced with your family."),
          ("Product sheet", "scan a barcode to see Nutri-Score, NOVA, allergens and additives (Open Food Facts).")], "shopping"),
        ("health", "shield", "Health", "Allergens and health", "Cook for whoever is at your table",
         "Miga works out each recipe's allergens and helps with coeliac disease and carbohydrate portions. All optional, without the assistant.",
         [("Only yours", "mark your allergies and intolerances and each recipe says “Has egg” or “None of your allergens”."),
          ("Filters", "search “No eggs”, “No gluten ingredients” or recipes for coeliacs."),
          ("Coeliac mode", "what to buy certified and how to avoid cross-contact."),
          ("Carb portions", "how many each recipe has per serving and how much to take for your plan.")], "filters"),
        ("assistant", "sparkles", "Assistant", "Cooking assistant", "Help whenever you want it",
         "Optional AI features with your own key. Without one, nothing is sent anywhere.",
         [("Recipes from photos", "snap a recipe from a book or a handwritten card and the editor fills itself."),
          ("From a website, Instagram or YouTube", "paste a link or share a video and get the clean recipe, without the ads and life stories."),
          ("Improve recipes", "better wording and tidy ingredients; you see the before and after."),
          ("Ideas", "ask what to cook with what you have, plan a weekly menu or find a seasonal dish.")], "new_recipe"),
        ("sync", "users", "Family", "Sync", "Share books and lists with your family",
         "Connect Miga to a server you host and share books and the shopping list across phones.",
         [("Your server", "miga-server runs at home or on your VPS with Docker."),
          ("QR invitations", "scan the code from another phone and you're connected."),
          ("Live shared list", "it refreshes every few seconds while you look at it."),
          ("No third parties", "your data only goes to your server.")], "server/mobile.png"),
    ],
    "features_head": ("Everything Miga does", "A complete app for home cooking, explained without fine print.", "Features"),
    "features": [
        ("book", "", "Books with covers", "Organise recipes into books: your mum's, a friend's, or one per topic.", ["Pin your favourite books on top", "Recipes grouped by category", "Swipe between recipes like the pages of a book"]),
        ("search", "", "Search and filters", "Find any recipe across all your books by name or ingredient.", ["Filter by time, difficulty, category, ingredients, origin and allergens", "“What can I cook?” with what's in your pantry", "Saved and recent searches"]),
        ("list", "", "A friendly editor", "Writing a recipe is quick: tabs for each part and suggestions from what you've used before.", ["Type “200 g potatoes” and Miga splits amount, unit and name", "Steps with bold, italic and lists, or dictated", "Select several recipes and change them at once"]),
        ("camera", "accent", "Matching photos", "Crop, rotate and improve your photos, saved at just the right size.", ["Frames for every photo: Polaroid, gallery, vignette…", "Automatic light, colour and sharpness ✨", "The dish photo is cropped for you when importing"]),
        ("utensils", "", "Cooking mode", "Big steps and the screen always on.", ["Several timers that keep going when you leave the app", "Read aloud", "Voice control and hands-free"]),
        ("cart", "", "Shopping list", "Add all the ingredients of a recipe in one go.", ["Several lists and templates", "Sorted by your supermarket's aisles", "Store mode, QR code and widget"]),
        ("scan", "sage", "Scanner and Open Food Facts", "Scan barcodes to add products and see their sheet.", ["Nutri-Score, NOVA, allergens and additives", "A rough score from 0 to 100", "Open data under the ODbL licence"]),
        ("download", "", "Import recipes", "Bring recipes from wherever they are.", ["From a web page, an Instagram reel or a YouTube video, with its photo, no assistant needed", "From a Miga file or a shared link", "From photos or a dish name, even several at once ✨"]),
        ("shield", "accent", "Allergens and intolerances", "The 14 allergens of EU law plus lactose, worked out from the ingredients.", ["Show all, only yours or none", "Warnings in lists and searches without your allergens", "Coeliac mode with what to buy certified"]),
        ("pulse", "sage", "Carbohydrate portions", "For those who count portions (with diabetes, for instance). Optional.", ["Portions per serving on every recipe", "Your plan by meals and food groups", "“Fit to my meal”: how much to take and what to add"]),
        ("heart", "accent", "Favourites with your channels and websites", "Follow cooking channels on YouTube, profiles on Instagram and recipe websites.", ["Their latest videos, reels and recipes, with what is new marked", "\"More recipes\" and a search on many websites", "Save what you want to cook and import it in one tap"]),
        ("bulb", "", "Cooking tips", "Short tips to cook better, offline.", ["A tip of the day in the library", "Tips for each recipe from its ingredients", "Save and share them"]),
        ("file", "accent", "Export and share", "Share a recipe or a whole book in the format you need.", ["An encrypted link that expires in 7 days", "PDF with cover and contents, or an image for WhatsApp and Instagram", "A Miga file for another phone, or plain text"]),
        ("archive", "", "Backups", "Save your whole library in one file and restore it whenever you like.", ["Photos included", "Optional password encryption (AES-256)", "Works with Android's own backup"]),
        ("palette", "sage", "Your way", "Make Miga look the way you like.", ["Light, dark or system theme", "Eight accent colours, Garden by default", "English and Spanish"]),
        ("lock", "", "Private and secure", "Your recipes, just for you.", ["Fingerprint, face or PIN lock", "Assistant keys encrypted on the phone", "No accounts, ads or analytics"]),
    ],
    "pages": {
        "features": ("Features", "Everything Miga does: recipe books, cooking mode, a shopping list sorted by aisle, barcode scanner, recipe import, backups and more.", "Features", "Everything Miga does", "A complete app for home cooking, explained without small print and with screens of the real app."),
        "health": ("Health", "Allergens, coeliac mode and carbohydrate portions in Miga: a guide, without the assistant and offline.", "Health · Optional", "Allergens, coeliac disease and carbohydrate portions", "Miga reads the ingredients of every recipe, without the assistant and offline, and tells you what matters to your family."),
        "assistant": ("Cooking assistant", "Miga's cooking assistant: recipes from photos, websites, Instagram and YouTube, polishing recipes and ideas, with your own key and the provider you choose.", "Assistant · Optional", "A cooking assistant that uses your own key", "Features marked with ✨ use artificial intelligence with the key you set up. You choose the provider and the model, and Miga only sends what each task needs."),
        "sync": ("Family and sync", "Share books and the shopping list with your family through miga-server, a sync server you host yourself with Docker.", "miga-server", "Your own sync server", "To share books and the shopping list with your family, Miga connects to a server you host yourself. It's lightweight, runs on Docker and comes with a full admin website."),
        "packs": ("Recipe packs", "Recipe packs for Miga: ready-made books to install with world cuisines, rice dishes, baking, Thermomix and more.", "Packs", "Recipe packs ready to install", "A pack is a recipe book you install with one tap from Settings › Recipe packs. Its recipes can't be edited, but you can copy any of them to your books."),
        "faq": ("FAQ", "Answers about Miga: price, privacy, the cooking assistant, allergens, importing recipes from websites, Instagram and YouTube, and more.", "Help", "Frequently asked questions", "What people ask us most. Question not here? Email us."),
    },
    "home_label": "Home", "skip": "Skip to content", "breadcrumb": "Breadcrumb",
    "prev": "Previous", "next": "Next", "more": "See more", "page_nav": "More sections",
    "discover_head": ("Discover Miga", "Each part of the app on its own page, with real screens.", "Sections"),
    "discover": {
        "features": ("shopping", "Books, cooking mode, shopping by aisle, the scanner, backups and everything else."),
        "health": ("recipe_health", "Your allergens, coeliac mode and carbohydrate portions."),
        "assistant": ("share_instagram", "Recipes from photos, websites, Instagram and YouTube, ideas and polishing, with your key."),
        "sync": ("server/mobile.png", "Books and the shopping list shared through your own server."),
        "packs": ("books", "Recipe books ready to install with one tap."),
        "faq": ("search", "Price, privacy, allergies, iPhone… what people ask most."),
    },
    "news_chip": "New",
    "news_title": "Recipes from Instagram and YouTube",
    "news_text": "Share a reel or a video to Miga and keep it as just another recipe: with its photo, and if the text doesn't have it, the assistant listens to or watches the video.",
    "insta_chip": "New",
    "insta_title": "Instagram and YouTube recipes, in your book",
    "insta_lead": "Saw a recipe in a reel or a video? Share it to Miga or paste its link and it's saved as just another recipe, with its photo and the author in the notes.",
    "insta_points": [
        ("No assistant needed", "if the post's caption has the ingredients and steps, Miga reads them directly."),
        ("Listens to the video ✨", "if the caption has no recipe, the assistant listens to the video: Gemini hears the audio, and OpenAI, Groq or Mistral transcribe it. Check the quantities."),
        ("From Instagram", "tap Share on the reel, choose Miga and pick the book to save it in."),
        ("The right photo", "full size and without the video's play button."),
        ("YouTube", "the recipe in the description or on the author's website it links to; if it is not there, Gemini watches the video: what is said and what is written on screen."),
    ],
    "insta_shots": [("share_instagram", "Sharing a reel to Miga"), ("new_recipe", "New recipe from a website or Instagram")],
    "health_gallery": [("health_settings", "Health settings"), ("filters", "Filters without your allergens"), ("recipe_health", "A recipe's allergens and carbs"), ("fit_meal", "Fit to my meal")],
    "assistant_more": "Ideas and polishing",
    "assistant_chip": "Optional",
    "assistant_title": "A cooking assistant that uses your own key",
    "assistant_lead": "Features marked ✨ use artificial intelligence with the key you set up. You choose the provider and the model, and Miga only sends what each task needs.",
    "assistant_points": [
        ("Recipes from photos and web pages", "reads the text of a photo or a page and fills in the editor; from a web page it also polishes it. You review it before saving."),
        ("Recipes from videos", "if an Instagram reel or a YouTube video has no recipe in its text, it takes it from the video: what is said and, on YouTube with Gemini, what is written on screen."),
        ("Improve recipes", "one or many at once: better wording, tidy ingredients and times in bold. Nothing is saved without your say-so."),
        ("Ideas", "suggestions from your own recipes, weekly menus and answers about techniques, storage or substitutions."),
        ("Health and nutrition", "a rough health rating, calories and macros per serving, and ingredient substitutes."),
        ("Keeps going when you leave", "long tasks continue in the background with a notification that takes you to the result."),
        ("Easy to set up", "“Connect with OpenRouter” creates the key for you; for the others, “Get a key” and “Test connection”."),
        ("Transparent", "generated content is labelled and can be reported. With no key, nothing is sent."),
    ],
    "health_chip": "Optional",
    "health_title": "Allergens, coeliac disease and carb portions",
    "health_lead": "Miga reads each recipe's ingredients, without the assistant and offline, and tells you what matters to your family. You choose what to see in Settings › Health.",
    "health_points": [
        ("14 allergens and lactose", "those EU law requires to be declared. “Has” or “May have” depending on the product you buy, explained when you tap the warning."),
        ("Only yours", "all allergens, only yours or none; warnings in lists and searches that start without them."),
        ("Coeliacs", "which ingredients have gluten, which to buy certified and how to avoid cross-contact."),
        ("Carb portions", "how many portions each recipe has per serving (10 g per portion, or the one you were given)."),
        ("Fit to my meal", "with your portion plan by food groups, how much to take and what to add to complete that meal, in kitchen measures."),
    ],
    "health_note": "It is a guide: always check each product's label and follow your care team's advice.",
    "gallery_head": ("Inside Miga", "Screens of the app as they are, with recipes from the packs.", "Screenshots"),
    "gallery": [("books", "Your library"), ("recipe", "A recipe"), ("cook_mode", "Cooking mode"), ("shopping", "Shopping by aisle"), ("search", "Search recipes"), ("health_settings", "Health settings"), ("recipe_health", "Allergens and carbs"), ("fit_meal", "Fit to my meal"), ("ideas", "Assistant ideas"), ("recipe_dark", "Dark theme")],
    "providers": ["Google Gemini", "Anthropic Claude", "OpenAI", "DeepSeek", "Mistral", "Groq", "OpenRouter (free models)", "OpenAI-compatible (Ollama, LM Studio…)"],
    "providers_note": "Add several and they are used in your order: if one fails, the next one steps in.",
    "server_chip": "miga-server",
    "server_title": "Your own sync server",
    "server_lead": "To share books and the shopping list with your family, Miga connects to a server you host. It's lightweight, runs with Docker and comes with a full web admin.",
    "server_steps": [
        ("Start the server", "save the <code>docker-compose.yml</code> below, replace the admin token with a long random string (for example, the output of <code>openssl rand -base64 32</code>) and run <code>docker compose up -d</code>."),
        ("Create a shared space", "in the web admin (<code>http://your-server:8080/ui</code>), create a namespace (say, “home”) and a token for each phone."),
        ("Connect the app", "in Settings › Sync server, add the connection. The rest of the family joins by scanning a QR code."),
    ],
    "server_features": [
        ("users", "Private spaces", "each namespace is shared by the phones you choose, with one revocable token per device."),
        ("refresh", "Reliable sync", "books, recipes, photos and lists, last edit wins even when clocks disagree."),
        ("table", "Web admin", "edit recipes in a spreadsheet-like table, change many at once or use the full editor."),
        ("file", "PDF from the browser", "download a recipe or a whole book with the app's design, in English or Spanish."),
        ("archive", "Automatic backups", "a daily backup with rotation, plus one-click backups and downloads."),
        ("lock", "No external dependencies", "one Docker image with SQLite; put it behind a TLS proxy to use it away from home."),
    ],
    "server_gallery": [("table.png", "Recipes in table mode, with bulk actions"), ("editor-dark.png", "The recipe editor in dark mode"), ("grid.png", "Grid view with photos"), ("mobile.png", "It works on phones too")],
    "server_compose_note": "That file is all you need: the image has everything inside and the data lives in the <code>miga-data</code> volume.",
    "admin_token_placeholder": "replace-with-a-long-token",
    "server_cta": "See miga-server",
    "server_admin_title": "The admin website",
    "packs_chip": "Packs",
    "packs_title": "Recipe packs, ready to install",
    "packs_lead": "A pack is a recipe book you install with one tap from Settings › Recipe packs. Its recipes can't be edited, but you can copy the ones you like into your books.",
    "packs_points": [
        ("Official catalogue", "Miga reads this website's catalogue; each pack has a cover, an author and a description."),
        ("Other catalogues", "add another one with a URL or a GitHub “user/repo”."),
        ("Make your own", "export a book as a Miga file (ZIP) and describe it in a <code>catalog.json</code>."),
    ],
    "packs_example_title": "Sample catalog.json",
    "packs_cta": "Packs repository",
    "packs_available": "Available packs",
    "faq_head": ("Frequently asked questions", "", "Help"),
    "faq_beta": ("How do I get Miga?", f"Right now it's in closed testing on Google Play. Email {CONTACT} from your Google account's address and we'll send you an invitation. It will be open to everyone soon."),
    "faq": [
        ("Is Miga free?", "Yes. It's free, with no ads or in-app purchases."),
        ("Do I need an account or the internet?", "No. Everything works offline and without signing up. The internet is only used for what you choose: the assistant with your key, Open Food Facts, the packs catalogue and your server."),
        ("How much does the cooking assistant cost?", "It depends on the provider you pick. OpenRouter has free models; Groq has a free tier and a model on your own computer (Ollama, LM Studio) costs nothing; with Gemini, Claude, OpenAI, DeepSeek or Mistral you pay them for what you use. Miga charges nothing and never sees your data."),
        ("Where are my recipes stored?", "In your phone's internal storage, and on your own server if you use sync. Miga has no servers of its own."),
        ("Can I move my recipes to another phone?", "Yes: with a full backup (optionally encrypted), by exporting books as Miga files, or with sync."),
        ("Does it help with allergies, coeliac disease or diabetes?", "Miga works out allergens and carbohydrate portions from the ingredients to help you choose and plan, but it is a guide: it cannot see brands or labels. Always check each product's label and follow your care team's advice."),
        ("Can I save recipes from websites?", "Yes. Paste the link and Miga reads the recipe with its photo, times and servings, no assistant needed: almost every recipe site uses a standard format. With the assistant set up, it also polishes it."),
        ("And recipe websites?", "Those too. In Favourites, paste a cooking website or one of its sections (its recipes page, for example) and you will see its latest recipes with photos. On many websites you can go back to older recipes and search for a particular one. They are imported in one tap, without the assistant when the website uses the standard recipe format."),
        ("Can I follow my favourite cooks on YouTube and Instagram?", "Yes. In Favourites, paste the link to a YouTube channel or an Instagram profile (or share it to Miga) and you will see their latest videos and reels: 15 on YouTube and 6 on Instagram. Save the ones you like and import them as recipes. Miga reads them directly, without an account; private accounts cannot be followed."),
        ("What about recipes from YouTube?", "Yes. Paste the link to a video or a Short, or share it from YouTube to Miga. If the description has the recipe or links to the author's website, Miga imports it from there; otherwise Gemini can watch the video (what is said and what is written on screen). The other assistants only read the description."),
        ("What about recipes from Instagram?", "Yes. Paste the link to a post or reel, or share it from Instagram to Miga. If the caption has the ingredients and steps, Miga reads them without the assistant; otherwise the assistant reads the caption or listens to the video (with Gemini, OpenAI, Groq or Mistral). Private posts cannot be imported."),
        ("Is there an iPhone version?", "For now Miga is Android only (8.0 or newer)."),
        ("What does it send to Open Food Facts?", "When you scan a barcode or search for a product, that code or text goes to Open Food Facts to fetch its sheet. The data is open (ODbL licence)."),
    ],
    "cta_title": "Start your recipe book today",
    "cta_text": "Download Miga, create your first book and save that recipe everyone keeps asking for.",
    "cta_text_beta": "Join the beta, create your first book and save that recipe everyone keeps asking for.",
    "footer_tagline": "Your family recipe book and shopping list, on your phone.",
    "footer_cols": [
        ("Miga", [("features", "Features"), ("health", "Health"), ("assistant", "Cooking assistant"), ("faq", "FAQ")]),
        ("More", [("sync", "Sync server"), ("packs", "Recipe packs"), (SERVER_REPO, "miga-server"), (PACKS_REPO, "miga-packs")]),
        ("Legal", [("privacy", "Privacy policy"), (f"mailto:{CONTACT}", "Contact")]),
    ],
    "legal": f"© {YEAR} Calamares. Recipes in the packs are published under CC BY 4.0.",
    "off": "Product data from Open Food Facts (ODbL).",
    "privacy_title": "Privacy policy · Miga",
    "back": "Back to home",
}

# Pages and their folders in each language (they appear in the URL), in the order of the menu.
PAGES = {
    "home": {"es": "", "en": ""},
    "features": {"es": "funciones/", "en": "features/"},
    "health": {"es": "salud/", "en": "health/"},
    "assistant": {"es": "asistente/", "en": "assistant/"},
    "sync": {"es": "familia/", "en": "family/"},
    "packs": {"es": "packs/", "en": "packs/"},
    "faq": {"es": "preguntas/", "en": "faq/"},
    "privacy": {"es": "privacy/", "en": "privacy/"},
}
SECTIONS = ["features", "health", "assistant", "sync", "packs", "faq"]

# Anchors of the old one-page site, still in shared links: the home page sends them to their page.
LEGACY_ANCHORS = {
    "es": {"funciones": "features", "capturas": "features", "salud": "health", "asistente": "assistant", "sincronizacion": "sync", "packs": "packs", "preguntas": "faq"},
    "en": {"features": "features", "screenshots": "features", "health": "health", "assistant": "assistant", "sync": "sync", "packs": "packs", "faq": "faq"},
}
DOWNLOAD_ANCHOR = {"es": "descargar", "en": "download"}
EXPLORE_ANCHOR = {"es": "explora", "en": "explore"}
INSTAGRAM_ANCHOR = "instagram"

# Where each tab of the home page's showcase is told in full.
SHOWCASE_PAGE = {"books": "features", "recipe": "features", "cooking": "features", "shopping": "features", "health": "health", "assistant": "assistant", "sync": "sync"}


COMPOSE = """services:
  miga-server:
    image: {image}
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      MIGA_ADMIN_TOKEN: "{token}"
    volumes:
      - miga-data:/data

volumes:
  miga-data:"""

CATALOG_EXAMPLE = """{
  "schemaVersion": 1,
  "packs": [
    {
      "id": "cocina-de-la-abuela",
      "name": "Cocina de la abuela",
      "series": "Cocina de siempre",
      "author": "Ana",
      "authorGithub": "ana",
      "description": "Guisos, potajes y postres de siempre.",
      "coverImageUrl": "covers/abuela.jpg",
      "latestVersion": 1,
      "recipeCount": 24,
      "downloadUrl": "zips/abuela.zip"
    }
  ]
}"""


# ---------------------------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------------------------

class Page:
    """Where a page is: its language texts [t], its [key] in PAGES and the relative paths from it to
    the site root ([root], where assets/ is) and to its language's home page ([home])."""

    def __init__(self, t, key):
        self.t, self.key, self.lang = t, key, t["lang"]
        self.path = PAGES[key][self.lang]
        depth = self.path.count("/") + (1 if self.lang == "en" else 0)
        self.root = "../" * depth
        self.home = "../" * self.path.count("/")
        self.img = f"{self.root}assets/img/"

    def link(self, key, anchor=""):
        """Relative link to another page of the same language."""
        href = (self.home + PAGES[key][self.lang]) or "./"
        return href + (f"#{anchor}" if anchor else "")

    def other_language(self):
        other = "es" if self.lang == "en" else "en"
        return (self.root + ("en/" if other == "en" else "") + PAGES[self.key][other]) or "./"


def page_url(lang, page_path):
    return f"{SITE_URL}{'en/' if lang == 'en' else ''}{page_path}"


def structured_data(t):
    """schema.org description of the app, so search engines can show it as an app result."""
    data = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Miga",
        "description": t["description"],
        "url": page_url(t["lang"], ""),
        "image": f"{SITE_URL}assets/img/og.png",
        "operatingSystem": "Android 8.0+",
        "applicationCategory": "LifestyleApplication",
        "inLanguage": ["es", "en"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
    }
    if PLAY_PUBLIC:
        data["installUrl"] = PLAY_URL
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def breadcrumb_data(pg, name):
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Miga", "item": page_url(pg.lang, "")},
            {"@type": "ListItem", "position": 2, "name": name, "item": page_url(pg.lang, pg.path)},
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def head(pg, title, description, extra=""):
    t, root = pg.t, pg.root
    alternates = "".join(f'<link rel="alternate" hreflang="{lang}" href="{page_url(lang, PAGES[pg.key][lang])}">\n' for lang in ("es", "en"))
    url = page_url(t["lang"], pg.path)
    return f"""<!doctype html>
<html lang="{t['lang']}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#0f1310">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Miga">
<meta property="og:locale" content="{'es_ES' if t['lang'] == 'es' else 'en_GB'}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{SITE_URL}assets/img/og.png">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
{alternates}<link rel="alternate" hreflang="x-default" href="{page_url('es', PAGES[pg.key]['es'])}">
{extra}<link rel="icon" href="{root}assets/img/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css?v={asset_version('style.css')}">
<script>
  // Saved theme, else the system's, before the first paint.
  (function () {{
    var theme = null;
    try {{ theme = localStorage.getItem('miga-theme'); }} catch (e) {{}}
    if (!theme) theme = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
  }})();
</script>
</head>
<body>
<a class="skip" href="#main">{escape(t['skip'])}</a>
"""


def nav(pg):
    t = pg.t
    current = ' aria-current="page"'
    links = "".join(f'<a href="{pg.link(key)}"{current if key == pg.key else ""}>{escape(label)}</a>' for key, label in t["nav"])
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="{pg.link('home')}"{current if pg.key == 'home' else ''}><img src="{pg.root}assets/img/logo.svg" alt=""><b>Miga</b></a>
    <nav class="nav-links" id="menu" aria-label="Miga">{links}</nav>
    <a class="icon-btn" href="{pg.other_language()}" hreflang="{t['other']}" lang="{t['other']}" title="{escape(t['other_label'])}">{t['other_short']}</a>
    <button class="icon-btn" data-theme-toggle title="{escape(t['theme'])}" aria-label="{escape(t['theme'])}">{icon('sun')}</button>
    <button class="icon-btn menu-toggle" data-menu-toggle aria-controls="menu" aria-expanded="false" aria-label="{escape(t['menu'])}">{icon('menu')}</button>
    <a class="btn primary small" href="#{DOWNLOAD_ANCHOR[pg.lang]}">{icon('download')}<span class="cta-label">{escape(t['get'] if PLAY_PUBLIC else t['get_beta'])}</span></a>
  </div>
</header>
"""


def beta_mail(t):
    return f"mailto:{CONTACT}?subject={quote(t['beta_subject'])}&body={quote(t['beta_body'])}"


def downloads(t):
    if PLAY_PUBLIC:
        return f"""<div class="hero-actions">
        <a class="btn primary" href="{PLAY_URL}">{icon('play')}{escape(t['play'])}</a>
      </div>"""
    return f"""<div class="hero-actions">
        <a class="btn primary" href="{escape(beta_mail(t))}">{icon('mail')}{escape(t['beta'])}</a>
        <span class="btn" aria-disabled="true" title="{escape(t['soon'])}">{icon('play')}{escape(t['play'])}<span class="soon">{escape(t['soon'])}</span></span>
      </div>
      <p class="beta-note">{escape(t['beta_note'])}</p>"""


def pack_cards(t, img):
    """The packs of the official catalogue in this page's language, grouped by series (the largest
    first), with covers kept in assets/."""
    catalog = json.loads((ROOT / "packs" / "catalog.json").read_text(encoding="utf-8"))
    series = {}
    for pack in catalog["packs"]:
        if pack.get("language", "es") != t["lang"]:
            continue
        if not (ROOT / "assets" / "img" / "packs" / f"{pack['id']}.jpg").exists():
            raise SystemExit(f"Missing assets/img/packs/{pack['id']}.jpg: copy packs/{pack['id']}/cover.jpg from miga-packs")
        series.setdefault(pack.get("series") or "", []).append(f"""<article class="pack">
        <img src="{img}packs/{pack['id']}.jpg" alt="" width="720" height="720" loading="lazy">
        <div><h4>{escape(pack['name'])}</h4>
        <p>{escape(pack['description'])}</p></div>
      </article>""")
    groups = sorted(series.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    def anchor(name):
        plain = unicodedata.normalize("NFD", name.lower()).encode("ascii", "ignore").decode()
        return "serie-" + "-".join("".join(c if c.isalnum() else " " for c in plain).split())
    # Jump links to each series: the list is long, above all on a phone.
    jumps = "".join(f'<a class="chip outline" href="#{anchor(name)}">{escape(name)} · {len(cards)}</a>' for name, cards in groups if name)
    return (f'<nav class="series-nav" aria-label="{escape(t["packs_available"])}">{jumps}</nav>' if jumps else "") + "".join(
        (f'<h3 class="pack-series" id="{anchor(name)}">{escape(name)}</h3>' if name else "") + f'<div class="packs">{"".join(cards)}</div>'
        for name, cards in groups
    )


def wavy():
    return '<div class="wavy" aria-hidden="true"></div>\n'


def phone(src, alt, cls=""):
    return f'<div class="phone {cls}"><img src="{src}" alt="{escape(alt)}" width="360" height="781" loading="lazy"></div>'


def section_head(title, text, chip=None):
    chip_html = f'<span class="chip primary">{escape(chip)}</span>' if chip else ""
    text_html = f"<p>{escape(text)}</p>" if text else ""
    return f'<div class="section-head">{chip_html}<h2>{escape(title)}</h2>{text_html}</div>'


def screen(img, t, name):
    """A real screenshot of the app in the page's language (see tools/screens.py), or another image."""
    return img + (name if "/" in name else f"screens/{t['lang']}/{name}.webp")


def page_hero(pg):
    """Title block of a section page: breadcrumb, chip, heading and introduction."""
    t = pg.t
    name, _, chip, title, lead = t["pages"][pg.key]
    return f"""<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="{escape(t['breadcrumb'])}"><ol><li><a href="{pg.link('home')}">{escape(t['home_label'])}</a></li><li><span aria-current="page">{escape(name)}</span></li></ol></nav>
    <span class="chip primary">{escape(chip)}</span>
    <h1>{escape(title)}</h1>
    <p class="lead">{escape(lead)}</p>
  </div>
</section>
"""


def pager(pg):
    """Links to the previous and next sections, so the site reads like the old long page did."""
    t = pg.t
    i = SECTIONS.index(pg.key)
    labels = dict(t["nav"])
    parts = []
    if i > 0:
        prev = SECTIONS[i - 1]
        parts.append(f'<a class="prev" href="{pg.link(prev)}" rel="prev"><small>← {escape(t["prev"])}</small><b>{escape(t["pages"][prev][0])}</b></a>')
    if i < len(SECTIONS) - 1:
        nxt = SECTIONS[i + 1]
        parts.append(f'<a class="next" href="{pg.link(nxt)}" rel="next"><small>{escape(t["next"])} →</small><b>{escape(t["pages"][nxt][0])}</b></a>')
    others = "".join(f'<a href="{pg.link(k)}">{escape(labels[k])}</a>' for k in SECTIONS if k != pg.key)
    return f"""<nav class="wrap pager" aria-label="{escape(t['page_nav'])}">
  <div class="pager-steps">{''.join(parts)}</div>
  <div class="pager-all">{others}</div>
</nav>
"""


def cta(pg):
    t = pg.t
    return f"""<section class="wrap get" id="{DOWNLOAD_ANCHOR[pg.lang]}">
  <div class="cta">
    <h2>{escape(t['cta_title'])}</h2>
    <p>{escape(t['cta_text'] if PLAY_PUBLIC else t['cta_text_beta'])}</p>
    {downloads(t)}
  </div>
</section>
"""


def checks(points, ic, raw=False):
    return "".join(f'<li>{icon(ic)}<div><b>{escape(b)}:</b> <span>{s if raw else escape(s)}</span></div></li>' for b, s in points)


def strip(pg, shots):
    figures = "".join(f'<figure>{phone(screen(pg.img, pg.t, name), caption)}<figcaption>{escape(caption)}</figcaption></figure>' for name, caption in shots)
    return f'<div class="screens-strip" tabindex="0" role="group">{figures}</div>'


def section_page(pg, content):
    t = pg.t
    name, description = t["pages"][pg.key][:2]
    out = [head(pg, f"{name} · Miga", description, breadcrumb_data(pg, name)), nav(pg), '<main id="main">', page_hero(pg)]
    out.append(content)
    out.append(pager(pg))
    out.append(cta(pg))
    out.append("</main>\n")
    out.append(footer(pg))
    return "".join(out)


def home(t):
    pg = Page(t, "home")
    img = pg.img
    legacy = json.dumps({anchor: pg.link(key) for anchor, key in LEGACY_ANCHORS[t["lang"]].items()})
    out = [head(pg, t["title"], t["description"], structured_data(t)), nav(pg), f'<main id="main" data-legacy-anchors=\'{legacy}\'>']

    badges = "".join(f'<span class="chip outline">{icon("check")}{escape(b)}</span>' for b in t["hero_badges"])
    out.append(f"""<section class="hero">
  <div class="wrap">
    <div>
      <span class="chip primary">{icon('leaf')}{escape(t['badge'] if PLAY_PUBLIC else t['badge_beta'])}</span>
      <h1>{t['hero_title']}</h1>
      <p class="lead">{escape(t['hero_lead'])}</p>
      {downloads(t)}
      <div class="hero-badges">{badges}</div>
    </div>
    <div class="hero-phones">
      {phone(screen(img, t, 'books'), t['shot_alt_back'], 'back')}
      {phone(screen(img, t, 'recipe'), t['shot_alt_front'], 'front')}
    </div>
  </div>
</section>
""")

    chips = "".join(f'<span class="chip">{icon(i)}{escape(label)}</span>' for i, label in t["marquee"])
    out.append(f'<div class="marquee" aria-label="{escape(t["features_head"][2])}"><div class="marquee-track">{chips}</div></div>\n')

    out.append(f"""<section class="wrap news">
  <a class="news-card" href="{pg.link('assistant', INSTAGRAM_ANCHOR)}">
    <img src="{screen(img, t, 'share_instagram')}" alt="" width="360" height="781" loading="lazy">
    <div><span class="chip accent">{icon('sparkles')}{escape(t['news_chip'])}</span><h2>{escape(t['news_title'])}</h2><p>{escape(t['news_text'])}</p><span class="more">{escape(t['more'])} →</span></div>
  </a>
</section>
""")
    out.append(wavy())

    pillars = "".join(f'<div class="pillar">{icon(i)}<h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for i, h, p in t["pillars"])
    out.append(f'<section class="wrap">{section_head(*t["pillars_head"])}<div class="pillars">{pillars}</div></section>\n')
    out.append(wavy())

    title, text, chip = t["showcase_head"]
    tabs, panels = [], []
    for n, (key, ic, short, kicker, heading, desc, points, shot) in enumerate(t["showcase"]):
        sel = n == 0
        tabs.append(f'<button role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{str(sel).lower()}" tabindex="{0 if sel else -1}">{icon(ic)}{escape(short)}</button>')
        items = "".join(f'<li>{icon("check")}<div><b>{escape(b)}:</b> <span>{escape(s)}</span></div></li>' for b, s in points)
        target = SHOWCASE_PAGE[key]
        panels.append(f"""<div class="showcase-panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}"{'' if sel else ' hidden'}>
      <div class="showcase-card">
        <div>
          <span class="chip accent kicker">{escape(kicker)}</span>
          <h3>{escape(heading)}</h3>
          <p class="desc">{escape(desc)}</p>
          <ul class="checks">{items}</ul>
          <a class="btn small" href="{pg.link(target)}">{escape(t['more'])}: {escape(t['pages'][target][0])} →</a>
        </div>
        <div class="showcase-media">{phone(screen(img, t, shot), heading)}</div>
      </div>
    </div>""")
    out.append(f"""<section class="wrap" id="{EXPLORE_ANCHOR[t['lang']]}">
  {section_head(title, text, chip)}
  <div class="picker" role="tablist">{''.join(tabs)}</div>
  {''.join(panels)}
</section>
""")
    out.append(wavy())

    title, text, chip = t["discover_head"]
    cards = []
    for key in SECTIONS:
        shot, blurb = t["discover"][key]
        name = t["pages"][key][0]
        cards.append(f"""<a class="dcard" href="{pg.link(key)}">
      <div class="dcard-shot"><img src="{screen(img, t, shot)}" alt="" loading="lazy" width="360" height="781"></div>
      <div class="dcard-text"><h3>{escape(name)}</h3><p>{escape(blurb)}</p><span class="more">{escape(t['more'])} →</span></div>
    </a>""")
    out.append(f'<section class="wrap" id="{"secciones" if t["lang"] == "es" else "sections"}">{section_head(title, text, chip)}<div class="discover">{"".join(cards)}</div></section>\n')

    out.append(cta(pg))
    out.append("</main>\n")
    out.append(footer(pg))
    return "".join(out)


def features_page(t):
    pg = Page(t, "features")
    title, text, _ = t["gallery_head"]
    cards = []
    for ic, tone, h, p, bullets in t["features"]:
        lis = "".join(f"<li>{escape(b)}</li>" for b in bullets)
        cards.append(f'<article class="card"><div class="icon-circle {tone}">{icon(ic)}</div><h3>{escape(h)}</h3><p>{escape(p)}</p><ul>{lis}</ul></article>')
    content = f"""<section class="wrap" aria-labelledby="capturas"><div class="section-head"><h2 id="capturas">{escape(title)}</h2><p>{escape(text)}</p></div>{strip(pg, t['gallery'])}</section>
{wavy()}<section class="wrap" aria-label="{escape(t['pages']['features'][0])}"><div class="grid">{''.join(cards)}</div></section>
"""
    return section_page(pg, content)


def health_page(t):
    pg = Page(t, "health")
    img = pg.img
    content = f"""<section class="wrap">
  <div class="split reverse">
    <div>
      <ul class="checks">{checks(t['health_points'], 'shield')}</ul>
      <p class="note">{escape(t['health_note'])}</p>
    </div>
    <div class="showcase-media duo">{phone(screen(img, t, 'recipe_health'), t['health_gallery'][2][1])}{phone(screen(img, t, 'fit_meal'), t['health_gallery'][3][1], 'second')}</div>
  </div>
</section>
{wavy()}<section class="wrap">{strip(pg, t['health_gallery'])}</section>
"""
    return section_page(pg, content)


def assistant_page(t):
    pg = Page(t, "assistant")
    img = pg.img
    providers = "".join(f'<span class="chip outline">{escape(p)}</span>' for p in t["providers"])
    insta = "".join(phone(screen(img, t, name), caption, "second" if n else "") for n, (name, caption) in enumerate(t["insta_shots"]))
    content = f"""<section class="wrap">
  <div class="split">
    <div>
      <div class="providers">{providers}</div>
      <p class="note">{escape(t['providers_note'])}</p>
      <ul class="checks">{checks(t['assistant_points'], 'sparkles')}</ul>
    </div>
    <div class="showcase-media">{phone(screen(img, t, 'ideas'), t['assistant_more'])}</div>
  </div>
</section>
{wavy()}<section class="wrap" id="{INSTAGRAM_ANCHOR}">
  <div class="split reverse">
    <div>
      <span class="chip accent">{icon('sparkles')}{escape(t['insta_chip'])}</span>
      <h2>{escape(t['insta_title'])}</h2>
      <p>{escape(t['insta_lead'])}</p>
      <ul class="checks">{checks(t['insta_points'], 'check')}</ul>
    </div>
    <div class="showcase-media duo">{insta}</div>
  </div>
</section>
"""
    return section_page(pg, content)


def sync_page(t):
    pg = Page(t, "sync")
    img = pg.img
    steps = "".join(f"<li><div><b>{escape(b)}</b><span>{s}</span></div></li>" for b, s in t["server_steps"])
    sfeat = "".join(f'<article class="card"><div class="icon-circle sage">{icon(i)}</div><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for i, h, p in t["server_features"])
    gallery = "".join(f'<figure><div class="frame"><div class="bar"><span></span><span></span><span></span></div><img src="{img}server/{f}" alt="{escape(c)}" loading="lazy"></div><figcaption>{escape(c)}</figcaption></figure>' for f, c in t["server_gallery"])
    content = f"""<section class="wrap">
  <div class="split reverse">
    <div>
      <ol class="steps">{steps}</ol>
      <a class="btn" href="{SERVER_REPO}">{icon('code')}{escape(t['server_cta'])}</a>
    </div>
    <div class="showcase-media">{phone(screen(img, t, 'server/mobile.png'), t['server_title'])}</div>
  </div>
  <div class="compose">
    <p class="muted"><b>docker-compose.yml</b> · {t['server_compose_note']}</p>
    <pre><code>{escape(COMPOSE.format(image=SERVER_IMAGE, token=t['admin_token_placeholder']))}</code></pre>
  </div>
</section>
{wavy()}<section class="wrap">
  <h2 class="subhead">{escape(t['server_admin_title'])}</h2>
  <div class="gallery">{gallery}</div>
  <div class="grid" style="margin-top:28px">{sfeat}</div>
</section>
"""
    return section_page(pg, content)


def packs_page(t):
    pg = Page(t, "packs")
    content = f"""<section class="wrap">
  <div class="split">
    <div>
      <ul class="checks">{checks(t['packs_points'], 'package', raw=True)}</ul>
      <a class="btn" href="{PACKS_REPO}">{icon('package')}{escape(t['packs_cta'])}</a>
    </div>
    <div>
      <p class="muted" style="margin-bottom:10px;font-weight:600">{escape(t['packs_example_title'])}</p>
      <pre><code>{escape(CATALOG_EXAMPLE)}</code></pre>
    </div>
  </div>
</section>
{wavy()}<section class="wrap">
  <h2 class="subhead">{escape(t['packs_available'])}</h2>
  {pack_cards(t, pg.img)}
</section>
"""
    return section_page(pg, content)


def faq_page(t):
    pg = Page(t, "faq")
    questions = t["faq"] if PLAY_PUBLIC else [t["faq_beta"], *t["faq"]]
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(r)}</p></details>" for q, r in questions)
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in questions],
    }
    content = f"""<section class="wrap"><div class="faq">{faq}</div>
  <p class="faq-contact">{icon('mail')}<a href="mailto:{CONTACT}">{CONTACT}</a></p>
</section>
<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>
"""
    return section_page(pg, content)


def footer(pg):
    t = pg.t
    cols = []
    for title, links in t["footer_cols"]:
        items = []
        for href, label in links:
            if href in PAGES:
                href = pg.link(href)
            items.append(f'<li><a href="{href}">{escape(label)}</a></li>')
        cols.append(f"<div><h2>{escape(title)}</h2><ul>{''.join(items)}</ul></div>")
    return f"""<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="{pg.link('home')}"><img src="{pg.root}assets/img/logo.svg" alt=""><b>Miga</b></a>
      <p style="margin-top:12px">{escape(t['footer_tagline'])}</p>
    </div>
    {''.join(cols)}
    <div class="legal"><span>{escape(t['legal'])}</span><span>{escape(t['off'])}</span></div>
  </div>
</footer>
<script src="{pg.root}assets/main.js?v={asset_version('main.js')}"></script>
</body>
</html>
"""


def privacy(t, source):
    pg = Page(t, "privacy")
    body = markdown.markdown(source.read_text(encoding="utf-8"), extensions=["tables"])
    out = [head(pg, t["privacy_title"], t["description"]), nav(pg)]
    out.append(f'<main id="main"><article class="wrap doc">{body}<p style="margin-top:40px"><a class="btn small" href="{pg.link("home")}">{escape(t["back"])}</a></p></article>\n{cta(pg)}</main>\n')
    out.append(footer(pg))
    return "".join(out)


def main():
    builders = {"home": home, "features": features_page, "health": health_page, "assistant": assistant_page,
                "sync": sync_page, "packs": packs_page, "faq": faq_page}
    pages = {}
    for t in (ES, EN):
        base = ROOT / ("en" if t["lang"] == "en" else "")
        for key, build in builders.items():
            pages[base / PAGES[key][t["lang"]] / "index.html"] = build(t)
        pages[base / "privacy" / "index.html"] = privacy(t, ROOT / "content" / f"privacy-{t['lang']}.md")
    urls = "".join(f"  <url><loc>{page_url(lang, PAGES[key][lang])}</loc></url>\n" for key in PAGES for lang in ("es", "en"))
    pages[ROOT / "sitemap.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    pages[ROOT / "robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n"
    for path, html in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
