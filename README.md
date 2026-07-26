# Cancionero — Pascua Joven San Isidro

Cancionero digital con 29 canciones para guitarra. Web app PWA + PDFs imprimibles.

🌐 **[Ver en vivo →](https://tomasitogh.github.io/cancionero-pjsi)**

---

## Estructura del proyecto

```
cancionero-pjsi/
├── index.html          ← estructura HTML de la SPA
├── style.css           ← todos los estilos (variables CSS, dark mode, componentes)
├── app.js              ← toda la lógica de la app (navegación, transposición, setlists)
├── songs_data.js       ← los datos de las 29 canciones (letra + acordes)
├── .gitignore
├── README.md
└── scripts/
    ├── generate_cancionero.py  ← genera el PDF completo (29 canciones)
    ├── generate_seleccion.py   ← genera el PDF de selección (8 canciones)
    ├── deploy.sh               ← sube cambios a GitHub Pages
    └── config.env.example      ← template de credenciales (no se commitea)
```

---

## Stack

**Web app** — HTML + CSS + JS vanilla, sin frameworks ni dependencias
- SPA con routing manual por estado (`S.view`)
- `localStorage` para colecciones, setlists, historial de transposición y dark mode
- CSS custom properties para theming claro/oscuro
- Touch events para swipe entre canciones en setlist
- PWA: instalable en home screen de iPhone
- URL sharing: `?col=iglesia&song=5` navega directo a la canción

**PDFs** — Python + [ReportLab](https://www.reportlab.com/)
- Fuente monoespaciada (Courier) para alinear acordes con letra
- Acordes en azul, portada oscura

**Deploy** — GitHub Pages (gratis, automático)

---

## Formato de los datos (`songs_data.js`)

```js
const SONGS = [
  {
    n: 1,           // número
    t: "Con Vos",   // título
    a: "Autor",     // autor (opcional)
    k: "A",         // tono (notación inglesa: A B C D E F G)
    c: null,        // capo (número o null)
    i: [            // ítems de letra/acordes
      { t: "l", c: "A    E    F#m   D", y: "primera línea de letra" },
      { t: "l", c: "",                  y: "línea sin acorde" },
      { t: "g" },                       // gap (espacio vertical)
      { t: "s", x: "Estribillo" },      // encabezado de sección
    ]
  },
]
```

Tipos de ítem (`t`): `"l"` línea con letra/acordes · `"g"` espacio · `"s"` título de sección

---

## Agregar una canción (workflow)

1. Editar `songs_data.js` — agregar el objeto al array `SONGS`
2. Abrir `index.html` en el navegador y verificar
3. Commitear y pushear:
   ```bash
   git add songs_data.js
   git commit -m "Agregar canción: Nombre"
   git push
   ```

En la práctica, esto lo hace Claude desde el chat. Ignacio aprueba → Claude edita y pushea.

---

## Setup inicial (una sola vez)

### 1. Clonar / abrir en VSCode
```bash
git clone https://github.com/tomasitogh/cancionero-pjsi.git
cd cancionero-pjsi
code .
```

### 2. Para que Claude pueda deployar automáticamente
Crear `scripts/config.env` (no se sube a GitHub):
```bash
GITHUB_TOKEN=ghp_tutoken...
GITHUB_USER=tomasitogh
GITHUB_REPO=cancionero-pjsi
```

### 3. GitHub Pages
En el repo de GitHub: **Settings → Pages → Branch: `main` → `/root` → Save**

URL resultante: `https://tomasitogh.github.io/cancionero-pjsi`

---

## Features de la app

- **Multi-colección**: "Iglesia / Pascua Joven San Isidro" built-in + colecciones de usuario
- **Transposición**: semitonos con memoria por canción, selector de tono, sugerencia de capo
- **Setlists**: crear, editar, reordenar, modo play con swipe
- **Dark mode** con persistencia
- **Auto-scroll** con velocidad configurable
- **Compartir por URL**: botón 🔗 copia link directo a la canción
- **PWA**: instalable en iPhone como app
