"""Builds the static website: index.html (Spanish), en/index.html and the privacy pages.

Texts live here, one dictionary per language; the privacy pages come from content/privacy-*.md
(the same text as PRIVACY.md and the copy inside the app). Every link is relative, so the site
works at https://calamares00.github.io/miga-web/ and on its own domain alike.

    pip install markdown
    python3 tools/build.py
"""
from html import escape
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

APP_REPO = "https://github.com/calamares00/miga-app"
APK_URL = "https://github.com/calamares00/miga-app/releases"
SERVER_REPO = "https://github.com/calamares00/miga-server"
PACKS_REPO = "https://github.com/bmo00/miga-packs"
CONTACT = "miga@calamares.org"
SITE_URL = "https://miga.calamares.org/"
VERSION = "1.0.0"

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
    "wand": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72M14 7l3 3M5 6v4M19 14v4M10 2v2M7 8H3M21 16h-4M11 3H9"/>',
}


def icon(name):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


# ---------------------------------------------------------------------------------------------
# Texts
# ---------------------------------------------------------------------------------------------

ES = {
    "lang": "es", "other": "en", "other_label": "English", "other_short": "EN",
    "title": "Miga · Tu recetario familiar y tu lista de la compra",
    "description": "Miga es una app de Android para guardar las recetas de tu familia en libros, cocinar paso a paso y hacer la compra. Sin cuentas, sin anuncios y con tus datos en tu móvil.",
    "nav": [("#funciones", "Funciones"), ("#asistente", "Asistente"), ("#sincronizacion", "Sincronización"), ("#packs", "Packs"), ("#preguntas", "Preguntas")],
    "theme": "Cambiar tema", "menu": "Menú", "get": "Descargar",
    "badge": f"Versión {VERSION}",
    "hero_title": "Tus recetas. Tus libros. <em>Tu cocina.</em>",
    "hero_lead": "Miga guarda las recetas de tu familia en libros con su portada, te acompaña paso a paso mientras cocinas y organiza la compra por los pasillos de tu supermercado. Sin cuentas, sin anuncios y con todo guardado en tu móvil.",
    "play": "Google Play", "soon": "Pronto", "apk": "Descargar APK", "source": "Código fuente",
    "hero_badges": ["Sin cuentas", "Sin anuncios", "Sin analítica", "Código abierto (GPL-3.0)", "Español e inglés"],
    "shot_alt_front": "Pantalla de una receta en Miga", "shot_alt_back": "Lista de libros en Miga",
    "marquee": [("book", "Libros de recetas"), ("utensils", "Modo cocina"), ("timer", "Temporizadores"), ("mic", "Dictado y voz"), ("cart", "Lista de la compra"), ("scan", "Escáner de productos"), ("leaf", "Open Food Facts"), ("sparkles", "Asistente de cocina"), ("server", "Servidor propio"), ("package", "Packs de recetas"), ("file", "PDF e imagen"), ("archive", "Copias cifradas"), ("palette", "Temas y marcos"), ("widget", "Widget"), ("lock", "Bloqueo con huella")],
    "pillars_head": ("Hecha para tu cocina, no para vender tus datos", "Miga no tiene servidores propios ni te pide registrarte. Lo que guardas es tuyo y se queda en tu teléfono."),
    "pillars": [
        ("phone", "Todo en tu móvil", "Recetas, fotos, listas y ajustes se guardan en el teléfono. Funciona sin conexión."),
        ("ban", "Sin cuentas ni anuncios", "Ni registro, ni publicidad, ni analítica. Abres la app y empiezas a cocinar."),
        ("shield", "Tú decides qué sale", "Internet solo se usa para lo que activas: tu asistente, Open Food Facts, packs o tu servidor."),
        ("code", "Código abierto", "Licencia GPL-3.0. Puedes revisar el código, compilarlo y proponer mejoras."),
    ],
    "showcase_head": ("Explora Miga", "Elige una parte de la app para ver qué puede hacer por ti.", "Vista interactiva"),
    "showcase": [
        ("books", "book", "Libros", "Libros y recetas", "Un recetario para cada cosa",
         "Crea un libro para cada persona o cada tema, cada uno con su portada, y llena sus páginas con recetas completas.",
         [("Recetas completas", "ingredientes con cantidad y unidad, pasos, fotos, dificultad, tiempos, raciones, origen con bandera y etiquetas."),
          ("Subrecetas", "separa la salsa, la masa o la guarnición, cada una con sus ingredientes y sus pasos."),
          ("Ingredientes opcionales", "marca el perejil para decorar sin ensuciar su nombre."),
          ("Raciones al momento", "cambia las raciones y las cantidades se recalculan solas."),
          ("Mis notas", "apuntes con fecha que no cambian la receta: «la próxima vez, menos sal».")], "books"),
        ("cooking", "utensils", "Modo cocina", "Modo cocina", "Cocina con las manos en la masa",
         "Los pasos uno a uno, en grande y sin que se apague la pantalla.",
         [("Temporizadores de un toque", "«cocer 10 minutos» se convierte en un temporizador."),
          ("Lectura en voz alta", "Miga te lee cada paso con la voz que elijas."),
          ("Manos libres", "di «siguiente», «anterior», «repite» o «temporizador» sin tocar el móvil."),
          ("Formato claro", "tiempos y temperaturas en negrita para encontrarlos de un vistazo.")], "cooking"),
        ("shopping", "cart", "Compra", "Lista de la compra", "La compra, en el orden de tu súper",
         "Añade lo que falta escribiendo, dictando, escaneando o desde una receta, y recórrela por pasillos.",
         [("Por pasillos", "agrupada por categorías y ordenada como tu supermercado."),
          ("Varias listas y plantillas", "la de casa, la de la fiesta y la compra semanal guardada."),
          ("Modo tienda", "desliza para marcar y la pantalla se queda encendida."),
          ("Compartir", "por texto, con un código QR o sincronizada con tu familia."),
          ("Widget", "añade cosas desde la pantalla de inicio sin abrir la app.")], "shopping"),
        ("product", "scan", "Productos", "Ficha de producto", "Sabe lo que compras",
         "Escanea el código de barras y consulta la ficha del producto con los datos abiertos de Open Food Facts.",
         [("Nutri-Score y NOVA", "la calidad nutricional y el grado de procesado de un vistazo."),
          ("Alérgenos y aditivos", "lo que conviene vigilar, marcado claramente."),
          ("Puntuación de 0 a 100", "una estimación orientativa de Miga a partir de esos datos."),
          ("Tabla nutricional", "energía, grasas, hidratos, fibra y proteínas por 100 g.")], "product"),
        ("assistant", "sparkles", "Asistente", "Asistente de cocina", "Una ayuda cuando la quieras",
         "Funciones opcionales con inteligencia artificial y tu propia clave. Si no lo configuras, no se envía nada.",
         [("Recetas desde fotos", "fotografía una receta de un libro o escrita a mano y precarga el editor."),
          ("Desde una web", "pega un enlace y obtén la receta limpia, sin anuncios ni historias."),
          ("Mejorar recetas", "pule la redacción y normaliza ingredientes; ves el antes y el después."),
          ("Ideas", "pregunta qué cocinar con lo que tienes, pide un menú semanal o un plato de temporada.")], "assistant"),
        ("sync", "users", "Familia", "Sincronización", "Compartid libros y listas en familia",
         "Conecta Miga a un servidor que alojes tú y comparte libros y la lista de la compra entre varios móviles.",
         [("Tu servidor", "miga-server funciona en tu casa o en tu VPS con Docker."),
          ("Invitaciones con QR", "escanea el código desde otro móvil y ya estáis conectados."),
          ("Lista compartida en directo", "se actualiza cada pocos segundos mientras la miras."),
          ("Sin terceros", "los datos van solo a tu servidor.")], "sync"),
    ],
    "features_head": ("Todo lo que hace Miga", "Una app completa para la cocina de casa, explicada sin letra pequeña.", "Funciones"),
    "features": [
        ("book", "", "Libros con portada", "Organiza las recetas en libros: el de tu madre, el de un amigo o uno por temas.", ["Fija tus libros favoritos arriba", "Recetas agrupadas por categoría", "Desliza para pasar de receta como las páginas de un libro"]),
        ("search", "", "Buscar y filtrar", "Encuentra cualquier receta en todos tus libros por nombre o ingrediente.", ["Filtros por tiempo, dificultad, categoría, equipamiento, etiquetas, ingredientes u origen", "Favoritas a un toque", "Filtros activos como chips que quitas de uno en uno"]),
        ("list", "", "Editor cómodo", "Escribir una receta es rápido: la app te sugiere lo que ya has usado.", ["Pasos con negrita, cursiva, tachado y listas", "Dicta los pasos con el micrófono", "Selecciona varias recetas y cámbialas de una vez"]),
        ("camera", "accent", "Fotos a juego", "Recorta, gira y mejora tus fotos, que se guardan con el tamaño justo.", ["Marcos para todas las fotos: Polaroid, galería, viñeta…", "Mejora automática de luz, color y nitidez ✨", "La foto del plato se recorta sola al importar"]),
        ("utensils", "", "Modo cocina", "Los pasos en grande y la pantalla siempre encendida.", ["Temporizadores a partir del texto", "Lectura en voz alta", "Control por voz y manos libres"]),
        ("cart", "", "Lista de la compra", "Desde una receta añades todos sus ingredientes de una vez.", ["Varias listas y plantillas", "Orden por pasillos de tu supermercado", "Modo tienda, QR y widget"]),
        ("scan", "sage", "Escáner y Open Food Facts", "Escanea códigos de barras para añadir productos y ver su ficha.", ["Nutri-Score, NOVA, alérgenos y aditivos", "Puntuación orientativa de 0 a 100", "Datos abiertos bajo licencia ODbL"]),
        ("download", "", "Importar recetas", "Trae recetas de donde estén.", ["Desde un archivo de Miga (JSON o ZIP con fotos)", "Desde fotos, una web o el nombre de un plato ✨", "Varias recetas desde muchas fotos a la vez ✨"]),
        ("file", "accent", "Exportar y compartir", "Comparte una receta o un libro entero en el formato que necesites.", ["PDF con portada e índice para imprimir", "Imagen de la receta lista para WhatsApp o Instagram", "Archivo de Miga para pasarlo a otro móvil, o texto"]),
        ("archive", "", "Copias de seguridad", "Guarda toda tu biblioteca en un archivo y restáurala cuando quieras.", ["Con fotos incluidas", "Cifrado opcional con contraseña (AES-256)", "Compatible con la copia de Android"]),
        ("palette", "sage", "A tu gusto", "Que Miga se vea como te gusta.", ["Tema claro, oscuro o del sistema", "Ocho colores de acento, con Huerta por defecto", "Español e inglés"]),
        ("lock", "", "Privada y segura", "Tus recetas, solo para ti.", ["Bloqueo con huella, rostro o PIN", "Claves del asistente cifradas en el móvil", "Sin cuentas, anuncios ni analítica"]),
    ],
    "assistant_chip": "Opcional",
    "assistant_title": "Un asistente de cocina que usa tu propia clave",
    "assistant_lead": "Las funciones marcadas con ✨ usan inteligencia artificial con la clave que tú configures. Eliges el proveedor y el modelo, y Miga solo envía lo necesario para cada tarea.",
    "assistant_points": [
        ("Recetas desde fotos y webs", "lee el texto de una foto o de una página y precarga el editor; tú lo revisas antes de guardar."),
        ("Mejorar recetas", "una o muchas a la vez: mejor redacción, ingredientes normalizados y tiempos en negrita. Nada se guarda sin tu permiso."),
        ("Ideas", "recomendaciones a partir de tus recetas, menús semanales y respuestas sobre técnicas, conservación o sustituciones."),
        ("Salud y nutrición", "valoración orientativa, calorías y macros por ración, y sustitutos de ingredientes."),
        ("Sigue aunque salgas", "las tareas largas continúan en segundo plano con una notificación que te lleva al resultado."),
        ("Transparente", "el contenido generado se marca como tal y puedes reportarlo. Si no hay clave, no se envía nada."),
    ],
    "providers": ["Google Gemini", "Anthropic Claude", "OpenAI", "OpenRouter (modelos gratuitos)"],
    "providers_note": "Si añades varios, se usan en el orden que elijas: si uno falla, se prueba el siguiente.",
    "server_chip": "miga-server",
    "server_title": "Tu propio servidor de sincronización",
    "server_lead": "Para compartir libros y la lista de la compra en familia, Miga se conecta a un servidor que alojas tú. Es ligero, funciona con Docker y trae una web de administración muy completa.",
    "server_steps": [
        ("Arranca el servidor", "copia <code>.env.example</code> a <code>.env</code>, pon un token de administrador y ejecuta <code>docker compose up -d</code>."),
        ("Crea un espacio compartido", "desde la web de administración, crea un namespace (por ejemplo, «casa») y un token para cada móvil."),
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
    "server_cta": "Ver miga-server",
    "packs_chip": "Packs",
    "packs_title": "Packs de recetas listos para instalar",
    "packs_lead": "Un pack es un libro de recetas que se instala con un toque desde Ajustes › Packs de recetas. Sus recetas no se editan, pero puedes copiar las que quieras a tus libros.",
    "packs_points": [
        ("Catálogo oficial", "Miga consulta el catálogo de esta web; cada pack trae portada, autor y número de recetas."),
        ("Catálogos alternativos", "añade otro catálogo con una URL o un repositorio de GitHub «usuario/repositorio»."),
        ("Crea el tuyo", "exporta un libro como archivo de Miga (ZIP) y descríbelo en un <code>catalog.json</code>."),
    ],
    "packs_example_title": "Ejemplo de catalog.json",
    "packs_cta": "Repositorio de packs",
    "faq_head": ("Preguntas frecuentes", "", "Ayuda"),
    "faq": [
        ("¿Miga es gratis?", "Sí. Es gratuita y de código abierto (GPL-3.0), sin anuncios ni compras dentro de la app."),
        ("¿Necesito una cuenta o internet?", "No. Todo funciona sin conexión y sin registrarte. Internet solo se usa para las funciones que eliges: el asistente con tu clave, Open Food Facts, el catálogo de packs y tu servidor."),
        ("¿Cuánto cuesta el asistente de cocina?", "Depende del proveedor que elijas. Con OpenRouter hay modelos gratuitos; con Gemini, Claude u OpenAI pagas a ellos según tu uso. Miga no cobra nada ni ve tus datos."),
        ("¿Dónde se guardan mis recetas?", "En el almacenamiento interno de tu móvil. Si usas la sincronización, también en tu propio servidor. Miga no tiene servidores propios."),
        ("¿Puedo pasar mis recetas a otro móvil?", "Sí: con una copia de seguridad completa (opcionalmente cifrada), exportando libros como archivo de Miga o con la sincronización."),
        ("¿Hay versión para iPhone?", "De momento Miga es solo para Android (8.0 o superior)."),
        ("¿Qué datos usa de Open Food Facts?", "Al escanear un código o buscar un producto se envía ese código o ese texto a Open Food Facts para obtener su ficha. Los datos son abiertos (licencia ODbL)."),
    ],
    "cta_title": "Empieza tu recetario hoy",
    "cta_text": "Descarga Miga, crea tu primer libro y guarda esa receta que siempre te piden.",
    "footer_tagline": "El recetario de tu familia y tu lista de la compra, en tu móvil.",
    "footer_cols": [
        ("Miga", [("#funciones", "Funciones"), ("#asistente", "Asistente de cocina"), ("#packs", "Packs de recetas"), (APK_URL, "Descargas")]),
        ("Proyecto", [(APP_REPO, "Código de la app"), (SERVER_REPO, "miga-server"), (PACKS_REPO, "miga-packs")]),
        ("Legal", [("privacy/", "Política de privacidad"), (f"mailto:{CONTACT}", "Contacto")]),
    ],
    "legal": "Miga es software libre bajo licencia GPL-3.0.",
    "off": "Datos de productos de Open Food Facts (ODbL).",
    "privacy_title": "Política de privacidad · Miga",
    "back": "Volver al inicio",
}

EN = {
    "lang": "en", "other": "es", "other_label": "Español", "other_short": "ES",
    "title": "Miga · Your family recipe book and shopping list",
    "description": "Miga is an Android app to keep your family's recipes in books, cook step by step and do the shopping. No accounts, no ads, and your data stays on your phone.",
    "nav": [("#features", "Features"), ("#assistant", "Assistant"), ("#sync", "Sync"), ("#packs", "Packs"), ("#faq", "FAQ")],
    "theme": "Switch theme", "menu": "Menu", "get": "Download",
    "badge": f"Version {VERSION}",
    "hero_title": "Your recipes. Your books. <em>Your kitchen.</em>",
    "hero_lead": "Miga keeps your family's recipes in books with their own covers, guides you step by step while you cook and sorts the shopping by your supermarket's aisles. No accounts, no ads, and everything stays on your phone.",
    "play": "Google Play", "soon": "Soon", "apk": "Download APK", "source": "Source code",
    "hero_badges": ["No accounts", "No ads", "No analytics", "Open source (GPL-3.0)", "English and Spanish"],
    "shot_alt_front": "A recipe in Miga", "shot_alt_back": "The list of books in Miga",
    "marquee": [("book", "Recipe books"), ("utensils", "Cooking mode"), ("timer", "Timers"), ("mic", "Dictation and voice"), ("cart", "Shopping list"), ("scan", "Product scanner"), ("leaf", "Open Food Facts"), ("sparkles", "Cooking assistant"), ("server", "Your own server"), ("package", "Recipe packs"), ("file", "PDF and image"), ("archive", "Encrypted backups"), ("palette", "Themes and frames"), ("widget", "Widget"), ("lock", "Fingerprint lock")],
    "pillars_head": ("Made for your kitchen, not to sell your data", "Miga has no servers of its own and never asks you to sign up. What you save is yours and stays on your phone."),
    "pillars": [
        ("phone", "Everything on your phone", "Recipes, photos, lists and settings live on the phone. It works offline."),
        ("ban", "No accounts, no ads", "No sign-up, no advertising, no analytics. Open the app and start cooking."),
        ("shield", "You decide what leaves", "The internet is only used for what you turn on: your assistant, Open Food Facts, packs or your server."),
        ("code", "Open source", "GPL-3.0 licensed. Read the code, build it and suggest improvements."),
    ],
    "showcase_head": ("Explore Miga", "Pick a part of the app to see what it can do for you.", "Interactive preview"),
    "showcase": [
        ("books", "book", "Books", "Books and recipes", "A recipe book for everything",
         "Make a book for each person or each topic, each with its own cover, and fill it with complete recipes.",
         [("Complete recipes", "ingredients with quantity and unit, steps, photos, difficulty, times, servings, origin with a flag and tags."),
          ("Sub-recipes", "keep the sauce, the dough or the side apart, each with its own ingredients and steps."),
          ("Optional ingredients", "mark the parsley for garnish without cluttering its name."),
          ("Servings on the fly", "change the servings and the quantities update themselves."),
          ("My notes", "dated notes that never change the recipe: “next time, less salt”.")], "books"),
        ("cooking", "utensils", "Cooking", "Cooking mode", "Cook with your hands in the dough",
         "One step at a time, in large type, with the screen kept on.",
         [("One-tap timers", "“simmer for 10 minutes” turns into a timer."),
          ("Read aloud", "Miga reads each step with the voice you choose."),
          ("Hands-free", "say “next”, “back”, “repeat” or “timer” without touching the phone."),
          ("Clear formatting", "times and temperatures in bold, easy to spot.")], "cooking"),
        ("shopping", "cart", "Shopping", "Shopping list", "Shopping in your supermarket's order",
         "Add what you need by typing, dictating, scanning or straight from a recipe, and walk it aisle by aisle.",
         [("By aisle", "grouped by category and sorted like your supermarket."),
          ("Several lists and templates", "home, the party, and your saved weekly shop."),
          ("Store mode", "swipe to tick items off while the screen stays on."),
          ("Share", "as text, with a QR code or synced with your family."),
          ("Widget", "add items from the home screen without opening the app.")], "shopping"),
        ("product", "scan", "Products", "Product sheet", "Know what you buy",
         "Scan a barcode and read the product sheet with Open Food Facts' open data.",
         [("Nutri-Score and NOVA", "nutritional quality and processing level at a glance."),
          ("Allergens and additives", "what to watch out for, clearly flagged."),
          ("A score from 0 to 100", "Miga's own rough estimate from that data."),
          ("Nutrition table", "energy, fat, carbs, fibre and protein per 100 g.")], "product"),
        ("assistant", "sparkles", "Assistant", "Cooking assistant", "Help whenever you want it",
         "Optional AI features with your own key. Without one, nothing is sent anywhere.",
         [("Recipes from photos", "snap a recipe from a book or a handwritten card and the editor fills itself."),
          ("From a web page", "paste a link and get the clean recipe, without the ads and life stories."),
          ("Improve recipes", "better wording and tidy ingredients; you see the before and after."),
          ("Ideas", "ask what to cook with what you have, plan a weekly menu or find a seasonal dish.")], "assistant"),
        ("sync", "users", "Family", "Sync", "Share books and lists with your family",
         "Connect Miga to a server you host and share books and the shopping list across phones.",
         [("Your server", "miga-server runs at home or on your VPS with Docker."),
          ("QR invitations", "scan the code from another phone and you're connected."),
          ("Live shared list", "it refreshes every few seconds while you look at it."),
          ("No third parties", "your data only goes to your server.")], "sync"),
    ],
    "features_head": ("Everything Miga does", "A complete app for home cooking, explained without fine print.", "Features"),
    "features": [
        ("book", "", "Books with covers", "Organise recipes into books: your mum's, a friend's, or one per topic.", ["Pin your favourite books on top", "Recipes grouped by category", "Swipe between recipes like the pages of a book"]),
        ("search", "", "Search and filters", "Find any recipe across all your books by name or ingredient.", ["Filter by time, difficulty, category, equipment, tags, ingredients or origin", "Favourites in one tap", "Active filters as chips you remove one by one"]),
        ("list", "", "A friendly editor", "Writing a recipe is quick: the app suggests what you've used before.", ["Steps with bold, italic, strikethrough and lists", "Dictate the steps with the microphone", "Select several recipes and change them at once"]),
        ("camera", "accent", "Matching photos", "Crop, rotate and improve your photos, saved at just the right size.", ["Frames for every photo: Polaroid, gallery, vignette…", "Automatic light, colour and sharpness ✨", "The dish photo is cropped for you when importing"]),
        ("utensils", "", "Cooking mode", "Big steps and the screen always on.", ["Timers from the text", "Read aloud", "Voice control and hands-free"]),
        ("cart", "", "Shopping list", "Add all the ingredients of a recipe in one go.", ["Several lists and templates", "Sorted by your supermarket's aisles", "Store mode, QR code and widget"]),
        ("scan", "sage", "Scanner and Open Food Facts", "Scan barcodes to add products and see their sheet.", ["Nutri-Score, NOVA, allergens and additives", "A rough score from 0 to 100", "Open data under the ODbL licence"]),
        ("download", "", "Import recipes", "Bring recipes from wherever they are.", ["From a Miga file (JSON or ZIP with photos)", "From photos, a web page or a dish name ✨", "Many recipes from many photos at once ✨"]),
        ("file", "accent", "Export and share", "Share a recipe or a whole book in the format you need.", ["PDF with cover and contents, ready to print", "A recipe image ready for WhatsApp or Instagram", "A Miga file for another phone, or plain text"]),
        ("archive", "", "Backups", "Save your whole library in one file and restore it whenever you like.", ["Photos included", "Optional password encryption (AES-256)", "Works with Android's own backup"]),
        ("palette", "sage", "Your way", "Make Miga look the way you like.", ["Light, dark or system theme", "Eight accent colours, Garden by default", "English and Spanish"]),
        ("lock", "", "Private and secure", "Your recipes, just for you.", ["Fingerprint, face or PIN lock", "Assistant keys encrypted on the phone", "No accounts, ads or analytics"]),
    ],
    "assistant_chip": "Optional",
    "assistant_title": "A cooking assistant that uses your own key",
    "assistant_lead": "Features marked ✨ use artificial intelligence with the key you set up. You choose the provider and the model, and Miga only sends what each task needs.",
    "assistant_points": [
        ("Recipes from photos and web pages", "reads the text of a photo or a page and fills in the editor; you review it before saving."),
        ("Improve recipes", "one or many at once: better wording, tidy ingredients and times in bold. Nothing is saved without your say-so."),
        ("Ideas", "suggestions from your own recipes, weekly menus and answers about techniques, storage or substitutions."),
        ("Health and nutrition", "a rough health rating, calories and macros per serving, and ingredient substitutes."),
        ("Keeps going when you leave", "long tasks continue in the background with a notification that takes you to the result."),
        ("Transparent", "generated content is labelled and can be reported. With no key, nothing is sent."),
    ],
    "providers": ["Google Gemini", "Anthropic Claude", "OpenAI", "OpenRouter (free models)"],
    "providers_note": "Add several and they are used in your order: if one fails, the next one steps in.",
    "server_chip": "miga-server",
    "server_title": "Your own sync server",
    "server_lead": "To share books and the shopping list with your family, Miga connects to a server you host. It's lightweight, runs with Docker and comes with a full web admin.",
    "server_steps": [
        ("Start the server", "copy <code>.env.example</code> to <code>.env</code>, set an admin token and run <code>docker compose up -d</code>."),
        ("Create a shared space", "in the web admin, create a namespace (say, “home”) and a token for each phone."),
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
    "server_cta": "See miga-server",
    "packs_chip": "Packs",
    "packs_title": "Recipe packs, ready to install",
    "packs_lead": "A pack is a recipe book you install with one tap from Settings › Recipe packs. Its recipes can't be edited, but you can copy the ones you like into your books.",
    "packs_points": [
        ("Official catalogue", "Miga reads this website's catalogue; each pack has a cover, an author and a recipe count."),
        ("Other catalogues", "add another one with a URL or a GitHub “user/repo”."),
        ("Make your own", "export a book as a Miga file (ZIP) and describe it in a <code>catalog.json</code>."),
    ],
    "packs_example_title": "Sample catalog.json",
    "packs_cta": "Packs repository",
    "faq_head": ("Frequently asked questions", "", "Help"),
    "faq": [
        ("Is Miga free?", "Yes. It's free and open source (GPL-3.0), with no ads or in-app purchases."),
        ("Do I need an account or the internet?", "No. Everything works offline and without signing up. The internet is only used for what you choose: the assistant with your key, Open Food Facts, the packs catalogue and your server."),
        ("How much does the cooking assistant cost?", "It depends on the provider you pick. OpenRouter has free models; with Gemini, Claude or OpenAI you pay them for what you use. Miga charges nothing and never sees your data."),
        ("Where are my recipes stored?", "In your phone's internal storage, and on your own server if you use sync. Miga has no servers of its own."),
        ("Can I move my recipes to another phone?", "Yes: with a full backup (optionally encrypted), by exporting books as Miga files, or with sync."),
        ("Is there an iPhone version?", "For now Miga is Android only (8.0 or newer)."),
        ("What does it send to Open Food Facts?", "When you scan a barcode or search for a product, that code or text goes to Open Food Facts to fetch its sheet. The data is open (ODbL licence)."),
    ],
    "cta_title": "Start your recipe book today",
    "cta_text": "Download Miga, create your first book and save that recipe everyone keeps asking for.",
    "footer_tagline": "Your family recipe book and shopping list, on your phone.",
    "footer_cols": [
        ("Miga", [("#features", "Features"), ("#assistant", "Cooking assistant"), ("#packs", "Recipe packs"), (APK_URL, "Downloads")]),
        ("Project", [(APP_REPO, "App source code"), (SERVER_REPO, "miga-server"), (PACKS_REPO, "miga-packs")]),
        ("Legal", [("privacy/", "Privacy policy"), (f"mailto:{CONTACT}", "Contact")]),
    ],
    "legal": "Miga is free software under the GPL-3.0 licence.",
    "off": "Product data from Open Food Facts (ODbL).",
    "privacy_title": "Privacy policy · Miga",
    "back": "Back to home",
}

# Section anchors differ per language (they appear in the URL).
ANCHORS = {
    "es": {"features": "funciones", "assistant": "asistente", "sync": "sincronizacion", "packs": "packs", "faq": "preguntas", "explore": "explora"},
    "en": {"features": "features", "assistant": "assistant", "sync": "sync", "packs": "packs", "faq": "faq", "explore": "explore"},
}

CATALOG_EXAMPLE = """{
  "schemaVersion": 1,
  "packs": [
    {
      "id": "cocina-de-la-abuela",
      "name": "Cocina de la abuela",
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

def other_language(t, root, page_path):
    """The same page in the other language. [root] leads to the site root (where assets/ is)."""
    return root + ("en/" if t["lang"] == "es" else "") + page_path


def head(t, root, title, description, page_path):
    return f"""<!doctype html>
<html lang="{t['lang']}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#0f1310">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{SITE_URL}assets/img/og.png">
<meta property="og:url" content="{SITE_URL}{'en/' if t['lang'] == 'en' else ''}{page_path}">
<link rel="canonical" href="{SITE_URL}{'en/' if t['lang'] == 'en' else ''}{page_path}">
<link rel="alternate" hreflang="{t['other']}" href="{other_language(t, root, page_path)}">
<link rel="icon" href="{root}assets/img/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css">
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
"""


def nav(t, root, home_rel, page_path):
    """[home_rel] leads to this language's home page ("" on it)."""
    links = "".join(f'<a href="{home_rel}{href}">{escape(label)}</a>' for href, label in t["nav"])
    other_href = other_language(t, root, page_path)
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="{home_rel or './'}"><img src="{root}assets/img/logo.svg" alt=""><b>Miga</b></a>
    <nav class="nav-links" aria-label="Miga">{links}</nav>
    <a class="icon-btn" href="{other_href}" hreflang="{t['other']}" title="{escape(t['other_label'])}">{t['other_short']}</a>
    <button class="icon-btn" data-theme-toggle title="{escape(t['theme'])}" aria-label="{escape(t['theme'])}">{icon('sun')}</button>
    <button class="icon-btn menu-toggle" data-menu-toggle aria-expanded="false" aria-label="{escape(t['menu'])}">{icon('menu')}</button>
    <a class="btn primary small" href="{APK_URL}">{icon('download')}<span class="cta-label">{escape(t['get'])}</span></a>
  </div>
</header>
"""


def downloads(t):
    return f"""<div class="hero-actions">
        <a class="btn primary" href="{APK_URL}">{icon('download')}{escape(t['apk'])}</a>
        <span class="btn" aria-disabled="true" title="{escape(t['soon'])}">{icon('play')}{escape(t['play'])}<span class="soon">{escape(t['soon'])}</span></span>
        <a class="btn" href="{APP_REPO}">{icon('code')}{escape(t['source'])}</a>
      </div>"""


def wavy():
    return '<div class="wavy" aria-hidden="true"></div>\n'


def phone(src, alt, cls=""):
    return f'<div class="phone {cls}"><img src="{src}" alt="{escape(alt)}" width="360" height="760" loading="lazy"></div>'


def section_head(title, text, chip=None):
    chip_html = f'<span class="chip primary">{escape(chip)}</span>' if chip else ""
    text_html = f"<p>{escape(text)}</p>" if text else ""
    return f'<div class="section-head">{chip_html}<h2>{escape(title)}</h2>{text_html}</div>'


def home(t, root):
    a = ANCHORS[t["lang"]]
    img = f"{root}assets/img/"
    out = [head(t, root, t["title"], t["description"], ""), nav(t, root, "", ""), "<main>"]

    badges = "".join(f'<span class="chip outline">{icon("check")}{escape(b)}</span>' for b in t["hero_badges"])
    out.append(f"""<section class="hero">
  <div class="wrap">
    <div>
      <span class="chip primary">{icon('leaf')}{escape(t['badge'])}</span>
      <h1>{t['hero_title']}</h1>
      <p class="lead">{escape(t['hero_lead'])}</p>
      {downloads(t)}
      <div class="hero-badges">{badges}</div>
    </div>
    <div class="hero-phones" aria-hidden="false">
      {phone(img + 'screens/books.svg', t['shot_alt_back'], 'back')}
      {phone(img + 'screens/recipe.svg', t['shot_alt_front'], 'front')}
    </div>
  </div>
</section>
""")

    chips = "".join(f'<span class="chip">{icon(i)}{escape(label)}</span>' for i, label in t["marquee"])
    out.append(f'<div class="marquee" aria-label="{escape(t["features_head"][2])}"><div class="marquee-track">{chips}</div></div>\n')
    out.append(wavy())

    pillars = "".join(f'<div class="pillar">{icon(i)}<h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for i, h, p in t["pillars"])
    out.append(f'<section class="wrap">{section_head(*t["pillars_head"])}<div class="pillars">{pillars}</div></section>\n')
    out.append(wavy())

    title, text, chip = t["showcase_head"]
    tabs, panels = [], []
    for n, (key, ic, short, kicker, heading, desc, points, screen) in enumerate(t["showcase"]):
        sel = n == 0
        tabs.append(f'<button role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{str(sel).lower()}" tabindex="{0 if sel else -1}">{icon(ic)}{escape(short)}</button>')
        items = "".join(f'<li>{icon("check")}<div><b>{escape(b)}:</b> <span>{escape(s)}</span></div></li>' for b, s in points)
        panels.append(f"""<div class="showcase-panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}"{'' if sel else ' hidden'}>
      <div class="showcase-card">
        <div>
          <span class="chip accent kicker">{escape(kicker)}</span>
          <h3>{escape(heading)}</h3>
          <p class="desc">{escape(desc)}</p>
          <ul class="checks">{items}</ul>
        </div>
        <div class="showcase-media">{phone(img + 'screens/' + screen + '.svg', heading)}</div>
      </div>
    </div>""")
    out.append(f"""<section class="wrap" id="{a['explore']}">
  {section_head(title, text, chip)}
  <div class="picker" role="tablist">{''.join(tabs)}</div>
  {''.join(panels)}
</section>
""")
    out.append(wavy())

    title, text, chip = t["features_head"]
    cards = []
    for ic, tone, h, p, bullets in t["features"]:
        lis = "".join(f"<li>{escape(b)}</li>" for b in bullets)
        cards.append(f'<article class="card"><div class="icon-circle {tone}">{icon(ic)}</div><h3>{escape(h)}</h3><p>{escape(p)}</p><ul>{lis}</ul></article>')
    out.append(f'<section class="wrap" id="{a["features"]}">{section_head(title, text, chip)}<div class="grid">{"".join(cards)}</div></section>\n')
    out.append(wavy())

    points = "".join(f'<li>{icon("sparkles")}<div><b>{escape(b)}:</b> <span>{escape(s)}</span></div></li>' for b, s in t["assistant_points"])
    providers = "".join(f'<span class="chip outline">{escape(p)}</span>' for p in t["providers"])
    out.append(f"""<section class="wrap" id="{a['assistant']}">
  <div class="split">
    <div>
      <span class="chip primary">{icon('sparkles')}{escape(t['assistant_chip'])}</span>
      <h2>{escape(t['assistant_title'])}</h2>
      <p>{escape(t['assistant_lead'])}</p>
      <div class="providers">{providers}</div>
      <p class="muted" style="font-size:15px;margin-top:-8px">{escape(t['providers_note'])}</p>
      <ul class="checks" style="margin-top:22px">{points}</ul>
    </div>
    <div class="showcase-media">{phone(img + 'screens/assistant.svg', t['assistant_title'])}</div>
  </div>
</section>
""")
    out.append(wavy())

    steps = "".join(f"<li><div><b>{escape(b)}</b><span>{s}</span></div></li>" for b, s in t["server_steps"])
    sfeat = "".join(f'<article class="card"><div class="icon-circle sage">{icon(i)}</div><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for i, h, p in t["server_features"])
    gallery = "".join(f'<figure><div class="frame"><div class="bar"><span></span><span></span><span></span></div><img src="{img}server/{f}" alt="{escape(c)}" loading="lazy"></div><figcaption>{escape(c)}</figcaption></figure>' for f, c in t["server_gallery"])
    out.append(f"""<section class="wrap" id="{a['sync']}">
  <div class="split reverse">
    <div>
      <span class="chip primary">{icon('server')}{escape(t['server_chip'])}</span>
      <h2>{escape(t['server_title'])}</h2>
      <p>{escape(t['server_lead'])}</p>
      <ol class="steps">{steps}</ol>
      <a class="btn" href="{SERVER_REPO}">{icon('code')}{escape(t['server_cta'])}</a>
    </div>
    <div class="showcase-media">{phone(img + 'screens/sync.svg', t['server_title'])}</div>
  </div>
  <div class="gallery">{gallery}</div>
  <div class="grid" style="margin-top:28px">{sfeat}</div>
</section>
""")
    out.append(wavy())

    ppoints = "".join(f'<li>{icon("package")}<div><b>{escape(b)}:</b> <span>{s}</span></div></li>' for b, s in t["packs_points"])
    out.append(f"""<section class="wrap" id="{a['packs']}">
  <div class="split">
    <div>
      <span class="chip primary">{icon('package')}{escape(t['packs_chip'])}</span>
      <h2>{escape(t['packs_title'])}</h2>
      <p>{escape(t['packs_lead'])}</p>
      <ul class="checks" style="margin-bottom:26px">{ppoints}</ul>
      <a class="btn" href="{PACKS_REPO}">{icon('code')}{escape(t['packs_cta'])}</a>
    </div>
    <div>
      <p class="muted" style="margin-bottom:10px;font-weight:600">{escape(t['packs_example_title'])}</p>
      <pre><code>{escape(CATALOG_EXAMPLE)}</code></pre>
    </div>
  </div>
</section>
""")
    out.append(wavy())

    title, text, chip = t["faq_head"]
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(r)}</p></details>" for q, r in t["faq"])
    out.append(f'<section class="wrap" id="{a["faq"]}">{section_head(title, text, chip)}<div class="faq">{faq}</div></section>\n')

    out.append(f"""<section class="wrap" style="margin-top:80px">
  <div class="cta">
    <h2>{escape(t['cta_title'])}</h2>
    <p>{escape(t['cta_text'])}</p>
    {downloads(t)}
  </div>
</section>
</main>
""")
    out.append(footer(t, root, ""))
    return "".join(out)


def footer(t, root, home_rel):
    cols = []
    for title, links in t["footer_cols"]:
        items = []
        for href, label in links:
            if not href.startswith(("http", "mailto:")):
                href = home_rel + href
            items.append(f'<li><a href="{href}">{escape(label)}</a></li>')
        cols.append(f"<div><h4>{escape(title)}</h4><ul>{''.join(items)}</ul></div>")
    return f"""<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="{home_rel or './'}"><img src="{root}assets/img/logo.svg" alt=""><b>Miga</b></a>
      <p style="margin-top:12px">{escape(t['footer_tagline'])}</p>
    </div>
    {''.join(cols)}
    <div class="legal"><span>{escape(t['legal'])}</span><span>{escape(t['off'])}</span></div>
  </div>
</footer>
<script src="{root}assets/main.js"></script>
</body>
</html>
"""


def privacy(t, root, source):
    body = markdown.markdown(source.read_text(encoding="utf-8"), extensions=["tables"])
    out = [head(t, root, t["privacy_title"], t["description"], "privacy/"), nav(t, root, "../", "privacy/")]
    out.append(f'<main class="wrap"><article class="doc">{body}<p style="margin-top:40px"><a class="btn small" href="../">{escape(t["back"])}</a></p></article></main>\n')
    out.append(footer(t, root, "../"))
    return "".join(out)


def main():
    pages = {
        ROOT / "index.html": home(ES, ""),
        ROOT / "en" / "index.html": home(EN, "../"),
        ROOT / "privacy" / "index.html": privacy(ES, "../", ROOT / "content" / "privacy-es.md"),
        ROOT / "en" / "privacy" / "index.html": privacy(EN, "../../", ROOT / "content" / "privacy-en.md"),
    }
    for path, html in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
