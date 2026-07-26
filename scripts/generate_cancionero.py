#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cancionero Pascua Joven San Isidro - version corregida
Cambios:
  1. ALMA MISIONERA: transposicion de Mi a SOL
     (Mi->SOL, Si7->RE7, Do#m->MIm, La->DO, Mi7->SOL7)
  16. SIEMPRE ME AMASTE: correccion de E a DO
     (el titulo decia DO pero los acordes estaban en Mi)
  Todas las canciones: acordes en todas las estrofas
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

W, H = A4
ML = 18 * mm
MR = W - 18 * mm
MT = H - 20 * mm
MB = 22 * mm
CHORD_COLOR = HexColor("#1a1acc")


class PDF:
    def __init__(self, fn):
        self.c = canvas.Canvas(fn, pagesize=A4)
        self.pn = 0
        self.y = 0
        self._pg()

    def _pg(self):
        if self.pn:
            self.c.showPage()
        self.pn += 1
        self.y = MT
        self.c.setFont("Courier", 7)
        self.c.setFillColorRGB(0, 0, 0)
        self.c.drawCentredString(W / 2, 13 * mm, str(self.pn))

    def _chk(self, h):
        if self.y - h < MB:
            self._pg()

    def title(self, t):
        self._chk(22)
        self.y -= 6
        self.c.setFont("Courier-Bold", 11)
        self.c.setFillColorRGB(0, 0, 0)
        self.c.drawString(ML, self.y, t)
        self.y -= 2
        self.c.setLineWidth(0.5)
        self.c.line(ML, self.y, MR, self.y)
        self.y -= 7

    def sec(self, t):
        self._chk(11)
        self.c.setFont("Courier-Bold", 8.5)
        self.c.setFillColorRGB(0, 0, 0)
        self.c.drawString(ML, self.y, t)
        self.y -= 10

    def ln(self, ch, ly):
        h = 10.5 + (9.5 if ch else 0)
        self._chk(h)
        if ch:
            self.c.setFont("Courier-Bold", 8.5)
            self.c.setFillColor(CHORD_COLOR)
            self.c.drawString(ML, self.y, ch)
            self.c.setFillColorRGB(0, 0, 0)
            self.y -= 9.5
        self.c.setFont("Courier", 8.5)
        self.c.setFillColorRGB(0, 0, 0)
        self.c.drawString(ML, self.y, ly)
        self.y -= 10.5

    def gap(self):
        self.y -= 5

    def save(self):
        self.c.save()


def song(p, num, name, items):
    """Render a song. Items are:
    - (chord_str, lyric_str): chord line above lyric
    - lyric_str (plain string): lyric only
    - None: blank gap between strophes
    - ("##", header): section header in bold
    """
    p.title(f"{num}. {name}")
    for x in items:
        if x is None:
            p.gap()
        elif isinstance(x, tuple) and x[0] == "##":
            p.sec(x[1])
        elif isinstance(x, tuple):
            p.ln(x[0], x[1])
        else:
            p.ln("", str(x))
    p.gap()
    p.gap()


# ============================================================
p = PDF("/sessions/gallant-gracious-franklin/mnt/outputs/Cancionero_corregido.pdf")

# Cover
p.c.setFont("Courier-Bold", 14)
p.c.setFillColorRGB(0, 0, 0)
p.c.drawCentredString(W / 2, H / 2 + 40, "CANCIONERO")
p.c.setFont("Courier-Bold", 10)
p.c.drawCentredString(W / 2, H / 2 + 20, "Seleccion personal")
p.c.setFont("Courier", 9)
p.c.drawCentredString(W / 2, H / 2, "(extraido de \"Cancionero con acordes\"")
p.c.drawCentredString(W / 2, H / 2 - 15, "Pascua Joven San Isidro)")
p._pg()

# ============================================================
# 1. ALMA MISIONERA
#    TRANSPOSICION: Mi->SOL, Si7->RE7, Do#m->MIm, La->DO, Mi7->SOL7
# ============================================================
song(p, 1, "ALMA MISIONERA  (G)", [
    ("G         D        Em", "Señor, toma mi vida nueva"),
    ("C          G", "antes de que la espera"),
    ("C          D", "desgaste años en mí."),
    ("G         D        Em", "Estoy dispuesto a lo que quieras"),
    ("C          G", "no importa lo que sea,"),
    ("C      G7 G G7", "tú llámame a servir."),
    None,
    ("G           D", "LLEVAME DONDE LOS HOMBRES"),
    ("Em         C", "NECESITEN TUS PALABRAS"),
    ("G       C        D", "NECESITEN MIS GANAS DE VIVIR."),
    ("G                 D", "DONDE FALTE LA ESPERANZA,"),
    ("Em            C", "DONDE TODO SEA TRISTE"),
    ("G    C    D G D", "SIMPLEMENTE POR NO SABER DE TI."),
    None,
    ("G         D        Em", "Te doy mi corazón sincero"),
    ("C          G", "para gritar sin miedo"),
    ("C          D", "lo hermoso que es tu amor"),
    ("G         D        Em", "Señor tengo alma misionera"),
    ("C          G", "condúceme a la tierra"),
    ("C      G7", "que tengo sed de vos."),
    None,
    ("G         D        Em", "Y así, en marcha iré cantando"),
    ("C          G", "por pueblos predicando"),
    ("C          D", "tu grandeza, Señor;"),
    ("G         D        Em", "tendré tus brazos sin cansancio"),
    ("C          G", "tu historia entre mis labios"),
    ("C      G7", "tu fuerza en la oración."),
])

# ============================================================
# 2. A TANTO AMOR (SOL / MI)
# ============================================================
song(p, 2, "A TANTO AMOR  (D, capo 3 = F)", [
    ("D                                    F#m", "Hecha un mar de lágrimas al verlo allí en la cruz,"),
    ("G                   D          A", "se acordó del niño que ella misma diera a luz."),
    ("Bm                        G", "Y entre el firmamento y su mirada de dolor,"),
    ("              D       A", "bien supo serle fiel a tanto amor."),
    None,
    ("D                                    F#m", "No rompió el silencio cuando el cielo se quebró,"),
    ("G                   D          A", "no volteó sus ojos cuando ya no respiró."),
    ("Bm                        G", "Se sintió caer pero así mismo no cayó,"),
    ("              D       A", "y amó a pesar de que todo se oscureció."),
    None,
    ("Bm", "Solo besos sus pies,"),
    ("G              A", "y a Dios se lo ofreció."),
    ("Bm", "Sin preguntar por qué,"),
    ("G              A", "a todos perdonó."),
    ("Bm", "Pues entendió el amor"),
    ("G              A", "que Jesús predicó,"),
    ("D", "que su hijo predicó."),
    ("Bm           G         D  A", "Ella entendió el amor que él enseñó."),
    None,
    ("D                                    F#m", "Entre la llovizna, la tristeza y el temor,"),
    ("G                   D          A", "lo tomó en sus brazos cuando ya no respiró."),
    ("Bm                        G", "Junto con su alma le traspasó el corazón,"),
    ("              D       A", "la espada que esa cruz todo lo consumó."),
    None,
    ("D                                    F#m", "No rompió el silencio cuando el cielo se quebró,"),
    ("G                   D          A", "no volteó sus ojos y el sepulcro se cerró."),
    ("Bm                        G", "Se sintió caer pero su fe permaneció,"),
    ("              D       A", "y amó a pesar de que el mundo lo entregó."),
    None,
    ("Bm", "Solo besos sus pies,"),
    ("G              A", "y a Dios se lo ofreció."),
    ("Bm", "Sin preguntar por qué,"),
    ("G              A", "a todos perdonó."),
    ("Bm", "Pues entendió el amor"),
    ("G              A", "que Jesús predicó,"),
    ("D", "que su hijo predicó."),
    ("Bm           G         D  A", "Ella entendió el amor que él enseñó."),
])

# ============================================================
# 3. CARA A CARA (SOL - LA)
# ============================================================
song(p, 3, "CARA A CARA  (A)", [
    ("    A          F#m", "Solamente una palabra,"),
    ("    A           F#m", "solamente una oración,"),
    ("        A            F#m         Bm  E", "cuando llegue a tu presencia, oh Señor."),
    ("        C#m", "No me importa en qué lugar"),
    ("      F#m    E        D", "de la mesa me hagas sentar,"),
    ("        D    D/C#    Bm           E    E7", "o el color de mi corona, si la llego a ganar."),
    None,
    ("    A          F#m", "Solamente una palabra,"),
    ("    A           F#m", "si es que aún me queda voz,"),
    ("        A            F#m         Bm  E", "y si logro articularla en tu presencia."),
    ("        C#m", "No te quiero hacer preguntas,"),
    ("      F#m    E        D", "sólo una petición,"),
    ("        D    D/C#    Bm           E    E7", "y si puede ser a solas, mucho mejor."),
    None,
    ("     D       E           C#m  F#m", "Sólo déjame mirarte cara a cara,"),
    ("     D            E           C#m  F#m", "y perderme como un niño en tu mirada,"),
    ("      D          E", "y que pase mucho tiempo,"),
    ("      C#m       F#m", "y que nadie diga nada,"),
    ("         D      D/C#  Bm           E    E7", "porque estoy viendo al Maestro cara a cara."),
    None,
    ("     D            E           C#m  F#m", "Que se ahogue mi recuerdo en tu mirada,"),
    ("     D            E            C#m  F#m", "quiero hablarte en silencio y sin palabras,"),
    ("      D          E", "y que pase mucho tiempo,"),
    ("      C#m       F#m", "y que nadie diga nada,"),
    ("         D    D/C#   Bm           E    E7", "sólo déjame mirarte cara a cara."),
    None,
    ("    A          F#m", "Solamente una palabra,"),
    ("    A           F#m", "solamente una oración,"),
    ("        A            F#m         Bm  E", "cuando llegue a tu presencia, oh Señor."),
    ("        C#m", "No me importa en qué lugar"),
    ("      F#m    E        D", "de la mesa me hagas sentar,"),
    ("        D    D/C#    Bm           E    E7", "o el color de mi corona, si la llego a ganar."),
    None,
    ("     D       E           C#m  F#m", "Sólo déjame mirarte cara a cara,"),
    ("     D            E           C#m  F#m", "aunque caiga derrotado en tu mirada,"),
    ("      D          E", "derrotado y desde el suelo,"),
    ("      C#m       F#m", "tembloroso y sin aliento,"),
    ("         D    D/C#   Bm           E    E7", "aún te seguiré mirando, mi Maestro."),
    None,
    ("     D          E              C#m  F#m", "Cuando caiga ante tus plantas de rodillas,"),
    ("     D       E             C#m  F#m", "déjame llorar pegado a tus heridas,"),
    ("      D          E", "y que pase mucho tiempo,"),
    ("      C#m       F#m", "y que nadie me lo impida,"),
    ("           D    D/C#    Bm           E  A", "que he esperado este momento toda mi vida."),
])

# ============================================================
# 4. CON VOS (LA) - Coro Pascua Joven San Isidro
# ============================================================
song(p, 4, "CON VOS  (A)", [
    ("A              E", "Te alejaste de mí"),
    ("    F#m             D", "Estás perdido, no encuentras sentido"),
    ("A              E", "Te avergüenza quien sos"),
    ("    F#m           D", "Estás dolido, te sentís vacío"),
    None,
    ("Bm          D", "Elegí buscarte"),
    ("F#m                  D", "Y llorar con vos, con tu corazón"),
    ("Bm              D", "Un corazón sediento"),
    ("             E", "Herido por el tiempo"),
    None,
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E          D", "Aquí yo te espero, no tengas miedo"),
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E", "Necesito verte"),
    ("D             E", "Elijo todo lo que sos"),
    ("A            E", "Quiero estar con vos"),
    ("F#m            D", "Quiero estar con vos"),
    None,
    ("A              E", "Cómo hacerte entender"),
    ("    F#m             D", "Lo mucho que te quiero, lo mucho que te espero"),
    ("A              E", "Te espero para abrazar"),
    ("    F#m          D", "Tu mundo entero, con mi amor sincero"),
    None,
    ("Bm          D", "No importa lo que hayas hecho"),
    ("F#m", "Mi amor no cambió"),
    ("D", "Escuchá mi voz"),
    ("Bm        D", "Una voz compasiva"),
    ("             E", "¡Vuelve a la vida!"),
    None,
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E          D", "Aquí yo te espero, no tengas miedo"),
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E", "Necesito verte"),
    ("D             E", "Elijo todo lo que sos"),
    ("A            E", "Quiero estar con vos"),
    ("F#m            D", "Quiero estar con vos"),
    None,
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E          D", "Aquí yo te espero, no tengas miedo"),
    ("A             E", "Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m            D", "Vuelve por favor (vuelve por favor)"),
    ("A           E", "Necesito verte"),
    ("D             E", "Elijo todo lo que sos"),
    ("A            E", "Quiero estar con vos"),
    ("F#m            D", "Quiero estar con vos"),
])

# ============================================================
# 5. ESTOY A LA PUERTA (Conozco tu corazón)
# ============================================================
song(p, 5, "ESTOY A LA PUERTA  (Conozco tu corazón)  (G)", [
    ("  G                       D", "Estoy a la puerta de tu corazón,"),
    ("   Em           Bm", "llamando todo el tiempo."),
    ("     C                Am", "Si escuchas mi voz y me abres tu puerta,"),
    ("     C   D7", "entraré y cenaré contigo."),
    None,
    ("  G                       D", "Estoy a la puerta de tu corazón,"),
    ("   Em           Bm", "llamando todo el tiempo."),
    ("     C                Am", "Si escuchas mi voz y me abres tu puerta,"),
    ("     C   D7", "entraré y cenaré contigo."),
    None,
    ("            G", "Porque yo conozco tu corazón,"),
    ("  Am                   C", "conozco tu realidad, sé todo de ti,"),
    ("          D7", "vengo a saciar tu necesidad."),
    None,
    ("            G", "Porque yo conozco tu corazón,"),
    ("  Am                   C", "conozco tu realidad, sé todo de ti,"),
    ("          D7", "vengo a saciar tu necesidad."),
    None,
    ("          G            Em", "Porque te amo, porque te amé,"),
    ("    C         Am        D7", "y te amaré con toda mi fuerza."),
    None,
    ("          G            Em", "Porque te amo, porque te amé,"),
    ("    C         Am        D7", "y te amaré con toda mi fuerza."),
    None,
    ("            G", "Porque yo conozco tu corazón,"),
    ("  Am                   C", "conozco tu realidad, sé todo de ti,"),
    ("          D7", "vengo a saciar tu necesidad."),
    None,
    ("            G", "Porque yo conozco tu corazón,"),
    ("  Am                   C", "conozco tu realidad, sé todo de ti,"),
    ("          D7", "vengo a saciar tu necesidad."),
    None,
    ("          G            Em", "Porque te amo, porque te amé,"),
    ("    C         Am        D7", "y te amaré con toda mi fuerza."),
    None,
    ("          G            Em", "Porque te amo, porque te amé,"),
    ("    C         Am        D7", "y te amaré con toda mi fuerza."),
    None,
    ("  G                 Am", "Conozco tu corazón, conozco tu realidad,"),
    ("   C                    D7", "sé todo de ti y en nadie más puedo ser feliz,"),
    ("        G", "sólo en ti."),
])

# ============================================================
# 7. DE CIRENE
# ============================================================
song(p, 6, "DE CIRENE  (E, capo 1)", [
    ("E         F#m         A         E", "Venías por aquel camino hacia mí,"),
    ("E              F#m         A", "en realidad nunca pensé cruzarte así,"),
    ("E          F#m       A         E", "bajo esa cruz la majestad del Hijo de David."),
    None,
    ("E               F#m         A", "Todo el pecado y la soberbia original"),
    ("E                            A", "sobre tus hombros a mi lado pasarán."),
    ("E              F#m          A", "Y de repente el Salvador cayó"),
    ("E           F#m", "y no sé si es que te puedo ayudar."),
    None,
    ("B          C#m       A         E", "Ayúdame a cargar tanto dolor."),
    ("B          C#m       A         E", "Ayúdame, necesitan de tu corazón."),
    ("B          C#m       A         E", "Pero, Señor no puedo, mira mi debilidad."),
    ("E         F#m          A         E", "Ayúdame y verás cómo la hago mía,"),
    ("E              A", "y mía es tu capacidad de amar."),
    None,
    ("E    F#m         A", "Los brazos se entrelazan para caminar,"),
    ("E         F#m       A", "tu aliento lastimado me va haciendo callar."),
    ("   B          F#m  A", "Y aunque nos griten voy entrando más,"),
    ("   E        F#m   A", "en nuestra intimidad."),
    None,
    ("       F#m       A", "¿Qué culpa hay en el hombre que merezca tu don?"),
    ("E      F#m     A", "¿Acaso dar la vida transforma un corazón?"),
    ("E      F#m     A         E", "Cuando llegamos a la cima entendí que es por amor."),
    None,
    ("B          C#m       A         E", "Ayúdame a cargar tanto dolor."),
    ("B          C#m       A         E", "Ayúdame, necesitan de tu corazón."),
    ("B          C#m       A         E", "Pero, Señor no puedo, mira mi debilidad."),
    ("E         F#m          A         E", "Ayúdame y verás cómo la hago mía,"),
    ("E              A", "y mía es tu capacidad de amar. (bis)"),
])

# ============================================================
# 10. EN MI GETSEMANI (MI)
# ============================================================
song(p, 7, "EN MI GETSEMANI  (E)", [
    ("E              C#m", "Para que mi amor no sea un sentimiento,"),
    ("       A                    B7", "tan solo un deslumbramiento pasajero."),
    ("G#              C#m", "Para no gastar las palabras más mías,"),
    ("       A          F#       B7", "ni vaciar de contenido mi 'te quiero'."),
    None,
    ("E              C#m", "Quiero hundir más hondo mi raíz en Ti,"),
    ("       A                    B7", "y cimentar en solidez este mi afecto."),
    ("G#              C#m", "Pues mi corazón, que es inquieto y es frágil,"),
    ("       A                 B7", "sólo acierta si se abraza a tu proyecto."),
    None,
    ("##", "[Coro]"),
    ("     E           B7", "Más allá de mis miedos,"),
    ("     C#m              A", "más allá de mi inseguridad,"),
    ("     F#                B7", "quiero darte mi respuesta;"),
    ("      E             B7     C#m", "aquí estoy para hacer tu voluntad,"),
    ("         C#m          A          B7", "para que mi amor sea decir que sí"),
    ("             E", "hasta el final."),
])

# ============================================================
# 11. EN LA PALMA DE SU MANO
# ============================================================
song(p, 8, "EN LA PALMA DE SU MANO  (D, capo 1 = Eb)", [
    ("D            G                   D    G", "Que el camino venga siempre a tu encuentro,"),
    ("Bm            G           A", "cuando no sepas más dónde buscar."),
    ("D                  G           D    G", "Que el viento sople siempre a tu espalda,"),
    ("Bm              G            A", "cuando no queden fuerzas para avanzar."),
    ("Bm        F#m           G              D", "Y que la verdad guíe tus pensamientos y tus actos,"),
    ("G                A           D   G", "y que Dios te lleve en la palma de su mano."),
    None,
    ("##", "[Rasgueo]"),
    ("D               G           D   G", "Que el sol te dé siempre en la cara,"),
    ("Bm           G         A", "y hará que tu sonrisa brille más."),
    ("D           G                  D    G", "Que la lluvia caiga siempre en tu campo,"),
    ("Bm            G      A", "y que le pierdas el miedo a llorar."),
    ("Bm                F#m       G             D", "Y que las personas que quieras permanezcan a tu lado,"),
    ("G                A           D", "y que Dios te lleve en la palma de su mano."),
    None,
    ("Bm            F#m   G                 D", "Y hasta que volvamos a vernos, cuídate mi hermano,"),
    ("G                A           D", "y que Dios te lleve en la palma de su mano."),
    ("G                A           Bm", "Y que Dios te lleve en la palma de su mano,"),
    ("G                A           D", "y que Dios te lleve en la palma de su mano."),
])

# ============================================================
# 14. PARA DARLO A LOS DEMÁS (DO)
# ============================================================
song(p, 9, "PARA DARLO A LOS DEMÁS  (C)", [
    ("C          G        Am", "A veces me siento alejado"),
    ("F            D7         G", "y la vergüenza no me deja ni hablar."),
    ("C          G        Am", "Y solo sé que me duele verte clavado"),
    ("F            D7         G", "porque me olvido de lo mucho que me amas."),
    None,
    ("Am   G   F", "Quiero volver a serte fiel."),
    ("Am   G   F   G7", "Quiero volver a serte fiel."),
    None,
    ("C            G       Am", "Toma de mí lo que te sirva"),
    ("       G           C", "para darlo a los demás."),
    ("       G        Am", "Toma de mí lo que te sirva,"),
    ("   G        Am", "no me guardo nada más."),
    None,
    ("   Em            F", "Hoy quiero ser tu instrumento,"),
    ("      G            Am", "predicar tu gran verdad,"),
    ("   Em              F", "la de tu palabra, la de tu cuerpo,"),
    ("    Bb                G       C", "la de tu amor eterno, la de amar al más pequeño."),
    None,
    ("C          G        Am", "Trato de encontrarte en mis hermanos"),
    ("F            D7         G", "pero se me hace imposible sin tu amor."),
    ("C          G        Am", "Soy débil y te pido que tus manos"),
    ("F            D7         G", "abran de par en par mi corazón."),
    None,
    ("Am   G   F", "Quiero volver a serte fiel."),
    ("Am   G   F   G7", "Quiero volver a serte fiel."),
    None,
    ("C            G       Am", "Toma de mí lo que te sirva"),
    ("       G           C", "para darlo a los demás."),
    ("       G        Am", "Toma de mí lo que te sirva,"),
    ("   G        Am", "no me guardo nada más."),
    None,
    ("   Em            F", "Hoy quiero ser tu instrumento,"),
    ("      G            Am", "predicar tu gran verdad,"),
    ("   Em              F", "la de tu palabra, la de tu cuerpo,"),
    ("    Bb                G       C", "la de tu amor eterno, la de amar al más pequeño."),
])

# ============================================================
# 16. SIEMPRE ME AMASTE (DO)
#     CORRECCION: los acordes estaban en Mi, el titulo decia DO
#     E->DO, A9->FA, C#m->LAm, F#m->REm, B7/B9->SOL7, Bm->REm
# ============================================================
song(p, 10, "SIEMPRE ME AMASTE  (E)", [
    ("E           A              E          A", "Puedo construir un muro imponente alrededor,"),
    ("E           A                E      A", "o ignorar la voz que pronuncia mi Señor."),
    None,
    ("C#m                       A", "Pero aunque me olvide de Ti,"),
    ("                 B          B7", "Tú no te olvidas de mí y vendrás,"),
    None,
    ("          E                    A", "y me gritarás que siempre me amarás,"),
    ("                    F#m", "que siempre me has amado,"),
    ("                  B        B7", "que siempre has estado a mi lado"),
    ("       C#m             A", "y que jamás quedaré separado."),
    ("             B", "Porque mi pecado"),
    ("                   B7         A", "con tu sangre y tu cruz has lavado."),
    None,
    ("E           A              E          A", "Puede hacerme creer el orgullo,"),
    ("E           A                E      A", "que me pertenezco y no soy tuyo."),
    None,
    ("C#m                       A", "Pero aunque me olvide de Ti,"),
    ("                 B          B7", "Tú no te olvidas de mí y vendrás,"),
    None,
    ("          E                    A", "y me gritarás que siempre me amarás,"),
    ("                    F#m", "que siempre me has amado,"),
    ("                  B        B7", "que siempre has estado a mi lado"),
    ("       C#m             A", "y que jamás quedaré separado."),
    ("             B", "Porque mi pecado"),
    ("                   B7         A", "con tu sangre y tu cruz has lavado."),
])

# ============================================================
# 20. DIME REY - Tono G
# ============================================================
song(p, 11, "DIME REY  (G)", [
    ("G                 D", "Hoy miraba señor tus heridas"),
    ("Em                    C", "Y el dolor que abarcaba esa cruz"),
    ("G                 D", "Con tus manos muy bien extendidas"),
    ("Em              C", "Abrazabas toda multitud"),
    None,
    ("G                 D", "Hoy miraba señor al soldado"),
    ("Em                    C", "Perforando con lanzas tus pies"),
    ("G                 D", "Y esos clavos muy bien sujetados"),
    ("Em              C", "Sostenian con odio tus pies"),
    None,
    ("##", "[Estribillo]"),
    ("G                 D", "Dime rey porque estás tan callado"),
    ("Em                    C", "Te latigaron con tanto furor"),
    ("G                 D", "Dime rey porque escondes el llanto"),
    ("Em              C", "Y perdonas aquel quien te mato"),
    None,
    ("G                 D", "Dime rey porque es tan necesario"),
    ("Em                    C", "Morir asi de esta forma tan cruel"),
    ("G                 D", "Dime rey como puedo ayudarte"),
    ("Em              C", "A soportar el dolor que tenes"),
    None,
    ("G                 D", "Hijo mio esa cruz tenebrosa"),
    ("Em                    C", "Me dolió y hasta sangre sudé"),
    ("G                 D", "Por amor a esas vidas perdidas"),
    ("Em              C", "Toda aquella maldad soporté"),
    None,
    ("G                D", "Mi mensaje de amor y justicia"),
    ("Em                    C", "Salvaria toda humanidad"),
    ("G                D", "Pero más me dolió todavia"),
    ("       Em               C", "Que no a todos les pudo llegar"),
    None,
    ("G                D", "Hoy miraba hijo mio esos niños"),
    ("Em                    C", "Morir asi, de esa forma tan cruel"),
    ("G                 D", "Hoy miraba toda la pobreza"),
    ("Em              C", "Sufriendo frio con hambre y con sed"),
    None,
    ("G                 D", "Y esos jóvenes tan lastimados"),
    ("Em                    C", "Equivocados pecando otra vez"),
    ("G                 D", "Me recuerdan aquel Viernes Santo"),
    ("Em              C", "Y ese dolor se repite otra vez"),
    None,
    ("Em                    C", "Animate que tú estás conmigo"),
    ("G                 D", "A expandir ese amor de tu fe"),
    ("Em              C", "Hijo mio ese fuego perdido"),
    ("G                 D", "Tú lo puedes volver a encender"),
    None,
    ("Em                    C", "Misiona, transforma"),
    ("Em                    C", "Esas almas que no pude entrar"),
    ("Em                    C", "Misiona, transforma"),
    ("G                D", "Corazones sedientos de paz"),
])

# ============================================================
# 22. PERFUME A TUS PIES - Tono D (capo 2 = E)
# ============================================================
song(p, 12, "PERFUME A TUS PIES  (D, capo 2 = E)", [
    ("D           A", "Cuando pienso en tu amor"),
    ("G", "y en tu fidelidad,"),
    ("A                      D", "no puedo hacer más que postrarme y adorar."),
    ("A", "Cuando pienso en como he sido"),
    ("G", "y hasta dónde me has traído,"),
    ("A", "me asombro de Ti."),
    None,
    ("Bm         A         G", "Y no me quiero conformar,"),
    ("Bm     A            G", "he probado y quiero más."),
    None,
    ("D                           A", "Yo quiero enamorarme más de Ti,"),
    ("                         Bm", "enséñame a amarte y a vivir"),
    ("                  A             G", "conforme a tu Justicia y tu verdad,"),
    ("                        D", "con mi vida quiero adorar."),
    ("                                A", "Con todo lo que tengo y lo que soy,"),
    ("                           Bm", "todo lo que he sido te lo doy."),
    ("             A       G", "Que mi vida sea para ti"),
    ("            A         Bm", "como un perfume a tus pies."),
    None,
    ("##", "A  G  Bm  A  G"),
    None,
    ("D                    A", "Cuando pienso en tu cruz"),
    ("G", "y en todo lo que has dado,"),
    ("A", "tu sangre por mí,"),
    ("D", "por llevar mi pecado."),
    ("A", "Cuando pienso en tu mano,"),
    ("G", "que hasta aquí hemos llegado"),
    ("A", "por tu fidelidad."),
    None,
    ("Bm         A         G", "Y no me quiero conformar,"),
    ("Bm     A            G", "he probado y quiero más."),
    None,
    ("D                           A", "Yo quiero enamorarme más de Ti,"),
    ("                         Bm", "enséñame a amarte y a vivir"),
    ("                  A             G", "conforme a tu Justicia y tu verdad,"),
    ("                        D", "con mi vida quiero adorar."),
    ("                                A", "Con todo lo que tengo y lo que soy,"),
    ("                           Bm", "todo lo que he sido te lo doy."),
    ("             A       G", "Que mi vida sea para ti"),
    ("            A             D", "como un perfume a tus pies."),
])

# ============================================================
# 23. TU ESTÁS AQUÍ
# ============================================================
song(p, 13, "TU ESTÁS AQUÍ  (G capo 1)", [
    ("G                        Em", "Aunque mis ojos no te puedan ver,"),
    ("C                   G    D", "Te puedo sentir, sé que estás aquí."),
    ("G                          Em", "Aunque mis manos no pueden tocar"),
    ("C                      G    D", "Tu rostro, señor, sé que estás aquí."),
    None,
    ("Em                        C", "Mi corazón puede sentir tu presencia,"),
    ("G                D", "Tú estás aquí, tú estás aquí."),
    ("Em               C", "Puedo sentir tu majestad,"),
    ("G                D", "Tú estás aquí, tú estás aquí."),
    None,
    ("G                        Em", "Aunque mis ojos no te puedan ver,"),
    ("C                   G    D", "Te puedo sentir, sé que estás aquí."),
    ("G                          Em", "Aunque mis manos no pueden tocar"),
    ("C                      G    D", "Tu rostro, señor, sé que estás aquí."),
    None,
    ("Em                        C", "Mi corazón puede mirar tu hermosura,"),
    ("G                D", "Tú estás aquí, tú estás aquí."),
    ("Em               C", "Puedo sentir tu gran amor,"),
    ("G                D", "Tú estás aquí, tú estás aquí."),
    None,
    ("G       D        Em", "Por su amor yo viviré,"),
    ("Em      D        G", "De su amor yo cantaré,"),
    ("G       D        Em", "Con mi Jesús caminaré,"),
    ("Em      C        D", "Porque Él murió por mí."),
    ("G       D        Em", "Por su amor yo viviré,"),
    ("Em      D        G", "De su amor yo cantaré,"),
    ("G       D        Em", "Con mi Jesús caminaré,"),
    ("Em      C", "Porque Él me amó a mí,"),
    ("D", "Lo seguiré. Lo seguiré. Lo seguiré. Lo seguiré."),
    None,
    ("G       D           Em", "Por su amor yo viviré  (puedo mirar tu hermosura)"),
    ("Em      D           G", "De su amor yo cantaré  (puedo sentir tu presencia)"),
    ("G       D        Em", "Con mi Jesús caminaré, porque Él murió por mí,"),
    ("D", "Lo seguiré."),
])

# ============================================================
# 26. TAN SÓLO HE VENIDO
# ============================================================
song(p, 14, "TAN SÓLO HE VENIDO  (G)", [
    ("G       D     Cadd9", "No he venido a pedirte,"),
    ("G       D     Cadd9", "como suelo, Señor."),
    ("G       D     Cadd9", "Si antes de yo clamarte,"),
    ("Em7       Cadd9    D7", "conoces mi petición."),
    None,
    ("G       D     Cadd9", "Solo quiero escucharte,"),
    ("G       D     Cadd9", "pon el tema, Señor."),
    ("G       D     Cadd9", "Descubrir Tu presencia,"),
    ("Em7     Cadd9     D7", "y dedicarte una canción."),
    None,
    ("         G", "Tan sólo he venido,"),
    ("  Bm7       Em", "a estar contigo,"),
    (" Bm7        C", "a ser tu amigo,"),
    ("Am           D7", "a compartir con mi Dios."),
    ("         G", "Y adorarte,"),
    ("  Bm7       Em", "y darte gracias,"),
    (" Bm7        C", "por siempre gracias,"),
    ("Am           D7        G", "por lo que has hecho, Señor, conmigo."),
    None,
    ("G     D    Cadd9", "Cuéntame de Tus obras,"),
    ("G     D      Cadd9", "¿qué hay de nuevo, Señor?"),
    ("G         D    Cadd9", "Y de paso pregunto,"),
    ("Em7         Cadd9      D7", "¿cómo pude estar sin Vos?"),
    None,
    ("G         D    Cadd9", "Solo quiero abrazarte,"),
    ("G  D      Cadd9", "bendecirte mi Dios."),
    ("G  D       Cadd9", "Meditar Tus silencios,"),
    ("Em7       Cadd9   D7", "y abrirte mi corazón."),
    None,
    ("         G", "Tan sólo he venido,"),
    ("  Bm7       Em", "a estar contigo,"),
    (" Bm7        C", "a ser tu amigo,"),
    ("Am           D7", "a compartir con mi Dios."),
    ("         G", "Y adorarte,"),
    ("  Bm7       Em", "y darte gracias,"),
    (" Bm7        C", "por siempre gracias,"),
    ("Am           D7", "por lo que has hecho, Señor."),
    None,
    ("         G", "He venido,"),
    ("  Bm7       Em", "a estar contigo,"),
    (" Bm7        C", "a ser tu amigo,"),
    ("Am           D7", "a compartir con mi Dios."),
    ("         G", "Y adorarte,"),
    ("  Bm7       Em", "y darte gracias,"),
    (" Bm7        C", "por siempre gracias,"),
    ("Am           D7        G", "por lo que has hecho, Señor, conmigo."),
    ("Am           D7        G", "Por lo que has hecho, Señor, conmigo."),
])

# ============================================================
# 27. DE TAL MANERA
# ============================================================
song(p, 15, "DE TAL MANERA  (G capo 1)", [
    ("G                     D", "De tal manera me amó,"),
    ("       C       Am       D", "Que su vida no escatimó."),
    ("G                 D", "Hasta el final él se entregó,"),
    ("         C          D     G", "Y a la muerte fue porque Él me amó."),
    None,
    ("G                     D", "De tal manera me amó,"),
    ("       C       Am       D", "Que no hay forma en que podré pagar."),
    ("G                 D", "El precio de su gran amor,"),
    ("         C          D", "Pero toda mi alma quiero dar."),
    None,
    ("G       D        Em", "Por su amor yo viviré,"),
    ("Em      D        G", "De su amor yo cantaré,"),
    ("G       D        Em", "Con mi Jesús caminaré,"),
    ("Em      C        D", "Porque Él me amó a mí."),
    None,
    ("G       D        Em", "Por su amor yo viviré,"),
    ("Em      D        G", "De su amor yo cantaré,"),
    ("G       D        Em", "Con mi Jesús caminaré,"),
    ("Em      C        D", "Porque Él murió por mí,"),
    ("D        G", "Le seguiré."),
])

# ============================================================
# 16. CANCIONES DEL ESPÍRITU SANTO / MARANATHÁ (Em - G, capo 1)
# ============================================================
song(p, 16, "CANCIONES DEL ESPÍRITU SANTO / MARANATHÁ  (Em - G, capo 1)", [
    ("##", "[Primera estrofa: arpegiada]"),
    None,
    ("Em                     D", "Espíritu de Dios, toma mi vida,"),
    ("        C        B7", "toma mi alma, toma mi ser."),
    ("Em              D", "Lléname con tu presencia,"),
    ("        C      B7", "con tu poder, lléname de ti."),
    ("Em              D", "Lléname con tu presencia,"),
    ("        C      B7   Em", "con tu poder, lléname de ti."),
    None,
    ("##", "[Desde aquí: rasgeo]"),
    None,
    ("Em                          D", "Enciéndeme señor, préndeme fuego quiero anunciarte,"),
    ("        C              B7", "morir por vos, lléname con tu presencia, con tu poder,"),
    ("Em", "lléname de ti."),
    None,
    ("##", "[Instrumental]  Em C D Em / G D Em C D"),
    None,
    ("Em", "Espíritu Santo, espíritu Santo,"),
    ("C   D   Em", "muévete en este lugar. (bis)"),
    None,
    ("Em          C", "Que haya paz, (que haya paz), que haya paz, (que haya paz),"),
    ("D       Em", "que haya paz en este lugar."),
    ("Em          C", "Que haya amor, que haya amor,"),
    ("D       Em", "que haya amor en este lugar."),
    ("Em          C", "Espíritu Santo, espíritu Santo,"),
    ("D       Em", "quédate en este lugar."),
    None,
    ("##", "[Instrumental]  Em C D Em / G D Em C D"),
    None,
    ("G    D   Em   C   D", "Ven espíritu de Dios, ven a mi ser, ven a mi vida,"),
    ("G", "ven espíritu de amor,"),
    ("D       Em          C         D", "ven a morar, ven hacia mí, ven espíritu de Dios, ven a mi ser,"),
    ("G           D    Em      C     D", "ven a mi vida, ven espíritu de amor, ven a morar, para maranathá."),
])

# ============================================================
# 36. NOS VEREMOS OTRA VEZ (MI) - Coro Pascua Joven
# ============================================================
song(p, 17, "NOS VEREMOS OTRA VEZ  (E)", [
    ("A         B          E", "Aunque te abraces a la luna,"),
    ("A         B          E", "aunque te acuestes con el sol,"),
    ("A         B       G#m          C#m", "no hay más estrellas que las que dejes brillar."),
    ("A         B          E", "tendrá el cielo tu color."),
    None,
    ("G#m     A        B    A", "No estés solo en esta lluvia,"),
    ("G#m     A        B    A", "no te entregues por favor."),
    ("E                    A", "Si debes ser fuerte en estos tiempos,"),
    ("E                    A", "para resistir la decepción,"),
    ("E                    A", "y quedar abierto, mente y alma,"),
    ("B   E", "yo estoy con vos."),
    None,
    ("A   B   G#m  C#m", "Si te hace falta quien te trate con amor,"),
    ("A   B   G#m  C#m", "si no tenés a quien brindar tu corazón,"),
    ("A   B   G#m  C#m", "si todo vuelve cuando más lo precisás,"),
    ("A   B   E", "nos veremos otra vez."),
    None,
    ("A         B          E", "Aunque te abraces a la luna,"),
    ("A         B          E", "aunque te acuestes con el sol,"),
    ("A         B       G#m          C#m", "no hay más estrellas que las que dejes brillar."),
    ("A         B          E", "tendrá el cielo tu color."),
    None,
    ("G#m     A        B    A", "No estés solo en esta lluvia,"),
    ("G#m     A        B    A", "no te entregues por favor."),
    ("E                    A", "Si debes ser fuerte en estos tiempos,"),
    ("E                    A", "para resistir la decepción,"),
    ("E                    A", "y quedar abierto, mente y alma,"),
    ("B   E", "yo estoy con vos."),
    None,
    ("A   B   G#m  C#m", "Si te hace falta quien te trate con amor,"),
    ("A   B   G#m  C#m", "si no tenés a quien brindar tu corazón,"),
    ("A   B   G#m  C#m", "si todo vuelve cuando más lo precisás,"),
    ("A   B   E", "nos veremos otra vez."),
])

# ============================================================
# 41. CINCO PANES Y DOS PECES (SOL)
# ============================================================
song(p, 18, "CINCO PANES Y DOS PECES  (G capo 2)", [
    ("G                          D    Em", "Yo soy un mendigo de tu gracia,"),
    ("                          C", "soy sólo un ladrón de tu amor."),
    ("G                          D    Em", "Perderte sería mi desgracia,"),
    ("                        C", "no te vayas nunca, mi Señor."),
    None,
    ("  C              D           G", "Señor tengo cinco panes y dos peces,"),
    ("C               D           G", "y veo tanta hambre a mi alrededor."),
    ("C                  D", "Lo pongo en tus manos,"),
    ("G            B7              Em", "dale de comer a mis hermanos,"),
    ("C               D           G", "aquí está tu siervo, mi Señor."),
    None,
    ("G                          D    Em", "Y cuando te pierdo pierdo la calma,"),
    ("                          C", "soy un débil que se protege en Dios."),
    ("G                          D    Em", "En tu amor se limpia toda mi alma,"),
    ("                          C", "soy un ambicioso, llename de Vos."),
    None,
    ("C                  D", "Lo pongo en tus manos,"),
    ("G            B7              Em", "dale de comer a mis hermanos,"),
    ("C               D           G", "aquí está tu siervo, mi Señor."),
])

# ============================================================
# 43. SALMO 17 (LA) - Coro Pascua Joven
# ============================================================
song(p, 19, "SALMO 17  (A)", [
    ("A            E           D", "Yo te amo, Señor, mi fortaleza,"),
    ("   Bm          D               A  E", "mi roca, mi baluarte, mi liberador."),
    ("A            E           D", "Eres la peña en que me amparo,"),
    ("      Bm         D            E", "mi escudo y mi fuerza, mi Salvador."),
    None,
    ("F#m                  C#m", "En el templo se escuchó mi voz,"),
    ("D                     A  E", "clamé por Ti en mi angustia."),
    ("F#m                   C#m", "Extendiste tu mano y no caí,"),
    ("D                     A    E", "tu poder del enemigo me libró."),
    None,
    ("A            E           D", "Las olas de la muerte me envolvían,"),
    ("   Bm          D               A  E", "me aguardaba la ruina, pero el Señor venció."),
    ("A            E           D", "Tú eres la luz que me ilumina,"),
    ("      Bm         D            E", "quien abre mis caminos, eres mi Dios."),
    None,
    ("F#m                  C#m", "En el templo se escuchó mi voz,"),
    ("D                     A  E", "clamé por Ti en mi angustia."),
    ("F#m                   C#m", "Extendiste tu mano y no caí,"),
    ("D                     A    E", "tu poder del enemigo me libró."),
    None,
    ("A            E           D", "Cuando yo invoqué tu Nombre,"),
    ("   Bm          D               A  E", "con mano poderosa me salvó tu amor."),
    ("A            E           D", "Son perfectos tus caminos,"),
    ("      Bm         D            E", "tus manos me sostienen, Tú eres mi Rey."),
    None,
    ("F#m                  C#m", "En el templo se escuchó mi voz,"),
    ("D                     A  E", "clamé por Ti en mi angustia."),
    ("F#m                   C#m", "Extendiste tu mano y no caí,"),
    ("D                     A    E", "tu poder del enemigo me libró."),
    ("F#m                   C#m", "Extendiste tu mano y no caí,"),
    ("D                     A    E", "tu poder del enemigo me libró."),
])

# ============================================================
# 45. MAR ADENTRO (MI) - Coro Pascua Joven
# ============================================================
song(p, 20, "MAR ADENTRO  (E)", [
    ("E           A          E", "Es hora de partir mar adentro,"),
    ("   B7", "y no voy a esperar."),
    ("E           A          E", "Él vendrá para ir mar adentro,"),
    ("   B7          E", "y lo voy a esperar."),
    None,
    ("E           A          E", "El ya está junto a mí,"),
    ("   B7", "y sus ojos derraman ternura."),
    ("E           A          E", "El espera mi 'sí',"),
    ("   B7          E", "y yo no quiero hacerlo esperar."),
    None,
    ("            E          A       E  B7", "Quiero sentir tu amor y volver a nacer,"),
    ("            C#m        A       E  B7", "quiero decirte: 'Ven, mi barca es tuya.'"),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A              E", "no temo navegar si está mi Dios."),
    None,
    ("E           A          E", "Quiero andar como vos"),
    ("   B7", "y ser pan que se deja comer."),
    ("E           A          E", "Quiero que los demás"),
    ("   B7          E", "vean en mí tu sonrisa, Señor."),
    None,
    ("E           A          E", "Quiero ser manantial,"),
    ("   B7", "ser bebida donde quiera que vaya."),
    ("E           A          E", "Quiero llevar tu luz"),
    ("   B7          E", "a este mundo que no habla de Dios."),
    None,
    ("            E          A       E  B7", "Quiero sentir tu amor y volver a nacer,"),
    ("            C#m        A       E  B7", "quiero decirte: 'Ven, mi barca es tuya.'"),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A              E", "no temo navegar si está mi Dios."),
    None,
    ("            E          A       E  B7", "Quiero sentir tu amor y volver a nacer,"),
    ("            C#m        A       E  B7", "quiero decirte: 'Ven, mi barca es tuya.'"),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A              E", "no temo navegar si está mi Dios."),
    None,
    ("            E          A       E  B7", "Quiero sentir tu amor y volver a nacer,"),
    ("            E          A       E  B7", "quiero sentir tu amor y volver a nacer,"),
    ("            C#m        A       E  B7", "quiero decirte: 'Ven, mi barca es tuya.'"),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A              E", "no temo navegar si está mi Dios."),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A              E", "no temo navegar si está mi Dios."),
    None,
    ("            E          A       E  B7", "Es tan inmenso el mar, pero yo voy con vos,"),
    ("         C#m  A    E", "no temo navegar,"),
    ("            B7", "si está mi Dios,"),
    ("            B7", "si está mi Dios,"),
    ("            B7", "si está mi Dios,"),
    ("            B7", "si está mi Dios,"),
    ("            E", "si está mi Dios!"),
])

# ============================================================
# 46. SAL Y LUZ (LA, capo 2 = SI)  - Maxi Larghi
# ============================================================
song(p, 21, "SAL Y LUZ  (A, capo 2 = B)  - Maxi Larghi", [
    ("A     Bm7", "Luz del mundo"),
    ("D                        A", "Deja de ocultarte en lo profundo"),
    ("A         Bm7", "Sal de la tierra"),
    ("D                       A", "Cuida tu sabor, nunca lo pierdas"),
    None,
    ("F#m  E        D", "Anuncia la palabra"),
    ("F#m   E          D", "Con obras, es tu vida la que habla"),
    ("F#m  E           D", "Ayuda a tus hermanos"),
    ("F#m        E       D", "Que el mundo necesita de tus manos"),
    None,
    ("       A    F#m      E", "Sal y luz, luz y sal"),
    ("   Bm           A          G", "Mezclado entre la gente está"),
    ("       E", "Jesús en la ciudad"),
    ("      A  F#m      E", "Buscarás la verdad"),
    ("      Bm            A", "No habrá noche en tu vida, será"),
    ("   G              E", "siempre un despertar"),
    None,
    ("A            Bm7", "Luz, si tú iluminas"),
    ("D                        A", "No puede ocultarse la ciudad sobre la cima"),
    ("A      Bm7", "Sal excelente"),
    ("D                               A", "Mirando hacia el cielo, con los pies en el presente"),
    None,
    ("F#m      E            D", "Y aunque quizás tropieces"),
    ("F#m     E          D", "No olvides que Jesús cayó tres veces"),
    ("F#m     E          D", "Levántate y camina"),
    ("F#m    E             D", "Que con tu andar el mundo se ilumina"),
    None,
    ("       A   F#m     E", "Sal y luz, luz y sal"),
    ("   C#m           A           G", "Mezclado entre la gente está"),
    ("        E", "Jesús en la ciudad"),
    ("      A F#m      E", "Buscarás la verdad"),
    ("     Bm            A", "No habrá noche en tu vida, será"),
    ("   G              E", "siempre un despertar"),
    None,
    ("E", "Si al cielo caminas, tu amor ilumina"),
    ("E", "Si al cielo caminas, tu amor ilumina"),
    ("E", "Si al cielo caminas, tu amor ilumina"),
    ("E", "Si al cielo caminas, tu amor ilumina"),
    ("E", "Si al cielo caminas, tu amor ilumina"),
    ("E", "Si al cielo caminas, tu amor ilumina"),
])

# ============================================================
# 51. BAJA / RENACE (REMIX) (MIm) - Coro de Jóvenes Inmaculada
# ============================================================
song(p, 22, "BAJA / RENACE (REMIX)  (Em)", [
    ("Em", "Baja hasta lo más hondo,"),
    ("C", "de nuestra condición."),
    ("Em", "Hasta lo más profundo"),
    ("C", "de nuestro corazón."),
    ("G            D", "Tú eres Rey, Hijo de Dios,"),
    ("Em       C  D", "Señor Jesús."),
    None,
    ("Em", "Ama hasta lo más hondo,"),
    ("C", "de nuestra condición."),
    ("Em", "Hasta lo más profundo"),
    ("C", "de nuestro corazón."),
    ("G            D", "Tú eres Rey, Hijo de Dios,"),
    ("Em       C  D", "Señor Jesús."),
    None,
    ("Em", "Libera hasta lo más hondo,"),
    ("C", "de nuestra condición."),
    ("Em", "Hasta lo más profundo"),
    ("C", "de nuestro corazón."),
    ("G            D", "Tú eres Rey, Hijo de Dios,"),
    ("Em       C  D", "Señor Jesús."),
    None,
    ("Em", "Sana hasta lo más hondo,"),
    ("C", "de nuestra condición."),
    ("Em", "Hasta lo más profundo"),
    ("C", "de nuestro corazón."),
    ("G            D", "Tú eres Rey, Hijo de Dios,"),
    ("Em       C  D", "Señor Jesús."),
    None,
    ("C       D        Em", "Ya no hay muerte, en Tu historia,"),
    ("C       D        Em", "solo vida, para contemplar Tu gloria."),
    None,
    ("C       D        Em", "Ya no hay muerte, en Tu historia,"),
    ("C       D        Em", "solo vida, para contemplar Tu gloria."),
    None,
    ("C       D        Em", "Aleluya, todo es posible para nosotros,"),
    ("C       D        G", "resucitó, Cristo nuestro Señor."),
    ("C       D        Em", "Él vive hoy, es nuestro amor y nuestra esperanza,"),
    ("C       D        G", "renace la vida y el corazón,"),
    ("C       D        Em", "renace la vida y el corazón."),
    None,
    ("C       D        Em", "Aleluya, todo es posible para nosotros,"),
    ("C       D        G", "resucitó, Cristo nuestro Señor."),
    ("C       D        Em", "Él vive hoy, es nuestro amor y nuestra esperanza,"),
    ("C       D        G", "renace la vida y el corazón,"),
    ("C       D        Em", "renace la vida y el corazón."),
])

# ============================================================
# 52. ROMPE ESAS CADENAS (REMIX) (MI) - Coro de Jóvenes Inmaculada
# ============================================================
song(p, 23, "ROMPE ESAS CADENAS (REMIX)  (E)", [
    ("E                    A", "Rompe esas cadenas, Espíritu"),
    ("E                 A", "esas que no dejan concentrar"),
    ("E                    A", "para que yo pueda rezar"),
    ("E   A", "en paz"),
    None,
    ("E                    A", "Que nada me impida estar acá"),
    ("E                    A", "Que nada me importe, nada más que"),
    ("E                         A", "sentirme protegido, acompañado"),
    ("              E  A", "amado y perdonado"),
    None,
    ("E  A    E           A", "Por eso ven, Espíritu Santo"),
    ("E  A    E           A", "Por eso ven, Espíritu Santo"),
    None,
    ("E                    A", "Solo Tu amor llena mi alma (solo Tu amor llena mi alma)"),
    ("E                      A", "Solo Tu luz alumbra mi corazón"),
    ("E                    A", "Solo Tu amor llena mi alma (solo Tu amor llena mi alma)"),
    ("E                      A", "Solo Tu luz alumbra mi corazón"),
    None,
    ("E                      A", "Iluminanos con Tu luz, Señor"),
    ("E                   A", "Y protegenos con Tu manto"),
    ("E  A    E           A", "Por eso ven, Espíritu Santo"),
    None,
    ("             E     B", "Santo Espíritu de Dios"),
    ("             C#m    A", "Santo Espíritu de Dios"),
    ("             E     B", "Santo Espíritu de Dios"),
    ("   C#m        A", "Infunde Tu amor"),
    None,
    ("E", "Ven dulce huésped del alma"),
    ("B", "Ven con Tu abrazo que sana"),
    ("C#m", "Ven dulce huésped del alma"),
    ("A", "En las tormentas, traes la calma"),
    None,
    ("             E     B", "Santo Espíritu de Dios"),
    ("             C#m    A", "Santo Espíritu de Dios"),
    ("             E     B", "Santo Espíritu de Dios"),
    ("   C#m        A", "Infunde Tu amor"),
    None,
    ("E", "Ven dulce huésped del alma"),
    ("B", "Ven con Tu abrazo que sana"),
    ("C#m", "Ven dulce huésped del alma"),
    ("A", "En las tormentas, traes la calma"),
    ("A", "En las tormentas, traes la calma"),
])

# ============================================================
# 53. VUELVE A DARME VIDA (SOL, capo 2 = LA)
# ============================================================
song(p, 24, "VUELVE A DARME VIDA  (G, capo 1 = Ab)", [
    ("G", "Recuerdo los tiempos antiguos,"),
    ("       D", "medito todas tus promesas."),
    ("   C              Am               G  D", "He visto Tu obrar y Tu espíritu soplar sobre mi."),
    None,
    ("G", "Amaba Tus mandatos,"),
    ("     D", "Tu discípulo yo era."),
    ("   C              Am             G  D", "Y no importaba que quisieras de mi, ni a dónde ir."),
    None,
    ("C", "Pero se enfrió mi corazón, me acostumbré a nombrarte,"),
    ("G", "hablar de Ti a los demás, pero ya no contigo."),
    ("C", "De manantial me convertí, en cisterna agrietada."),
    ("Am       D              G", "Mi alma en tierra, agostada, cansada y sin agua."),
    None,
    ("            G", "Y vuelve a darme vida en Tu costado abierto,"),
    ("           D", "de los manantiales de Tu amor eterno."),
    ("          C       Am", "Quemame por dentro, sopla con Tu aliento."),
    ("            G", "Y vuelve a darme vida en Tu costado abierto,"),
    ("           D", "de los manantiales de Tu amor eterno."),
    ("          C       Am", "Quemame por dentro, sopla con Tu aliento."),
    None,
    ("G    D", "Dame vida, dame amor."),
    ("C    G", "Quemame, con Tu fuego Señor."),
    ("G    D", "Dame vida, dame amor."),
    ("C    G", "Quemame, con Tu fuego Señor."),
    None,
    ("            G", "Y vuelve a darme vida en Tu costado abierto,"),
    ("           D", "de los manantiales de Tu amor eterno."),
    ("          C       Am", "Quemame por dentro, sopla con Tu aliento."),
    ("            G", "Y vuelve a darme vida en Tu costado abierto,"),
    ("           D", "de los manantiales de Tu amor eterno."),
    ("          C       Am", "Quemame por dentro, sopla con Tu aliento."),
    None,
    ("G    D", "Dame vida, dame amor."),
    ("C    G", "Quemame, con Tu fuego Señor."),
    ("G    D", "Dame vida, dame amor."),
    ("C    G", "Quemame, con Tu fuego Señor."),
])

# ============================================================
# 18. VIDA EN ABUNDANCIA (SOL)
# ============================================================
song(p, 25, "VIDA EN ABUNDANCIA  (G)", [
    ("G               C              D", "Los lirios del campo y las aves del cielo,"),
    ("G               C              D", "no se preocupan porque están en mis manos."),
    ("Em              C", "Tené confianza en mí,"),
    ("G               D", "acá estoy junto a vos."),
    None,
    ("G               C              D", "Amá lo que sos y tus circunstancias,"),
    ("G               C              D", "estoy con vos, con tu cruz en mi espalda."),
    ("Em              C", "todo terminará bien,"),
    ("G               D", "yo hago nuevas todas las cosas."),
    None,
    ("##", "[Pre-Estribillo]"),
    ("Em  C              G  D", "Yo vengo a traerte vida,"),
    ("Em  C              D", "vida en abundancia, en abundancia."),
    None,
    ("##", "[Estribillo]"),
    ("Em  C           G  D", "Yo soy el camino, la verdad y la vida,"),
    ("Em  C              D", "vida en abundancia, en abundancia."),
    None,
    ("G               C              D", "No hice al hombre para que esté solo,"),
    ("G               C              D", "caminen juntos como hermanos."),
    ("Em              C", "Sopórtense mutuamente,"),
    ("G               D", "ámense unos a otros."),
    None,
    ("G               C              D", "La felicidad de la vida eterna"),
    ("G               C              D", "empieza conmigo en la tierra."),
    ("Em              C", "Sentite vivo,"),
    ("G               D", "la fiesta del reino comienza acá."),
    None,
    ("##", "[Pre-Estribillo]"),
    ("Em  C              G  D", "Yo vengo a traerte vida,"),
    ("Em  C              D", "vida en abundancia, en abundancia."),
    None,
    ("##", "[Estribillo]"),
    ("Em  C           G  D", "Yo soy el camino, la verdad y la vida,"),
    ("Em  C              D", "vida en abundancia, en abundancia."),
    None,
    ("##", "[Pre-Estribillo]"),
    ("Em  C              G  D", "Yo vengo a traerte vida (yo vengo a traerte vida),"),
    ("Em  C              D", "vida en abundancia, en abundancia (vida en abundancia)."),
    None,
    ("##", "[Estribillo]"),
    ("Em  C           G  D", "Yo soy el camino, la verdad y la vida (yo soy el camino...),"),
    ("Em  C              D", "vida en abundancia, en abundancia (vida en abundancia)."),
])

# ============================================================
# 19. CRISTO REINA (REMIX) - Tono G
# ============================================================
song(p, 26, "CRISTO REINA (REMIX)  (G)", [
    ("##", "[Intro]  G  D  Em  C"),
    None,
    ("G                                  D", "Mi corazón quiere alabar, alabarte"),
    ("Em                           C", "Mi corazón quiere adorar, adorarte"),
    ("G                                  D", "Mi corazón quiere alabar, alabarte"),
    ("Em                           C", "Mi corazón quiere adorar, adorarte"),
    None,
    ("G     D", "Cristo reina, (reina reina Señor)"),
    ("Em    C", "Cristo reina, (aquí está Tu pueblo Jesús)"),
    ("G     D", "Cristo reina (te estamos esperando)"),
    ("Em      C", "Con poder (tuyo es el poder, es el poder)"),
    None,
    ("G                               D", "Vine a adorarte, vine a postrarme"),
    ("    Em                   C", "Vine a decir que eres mi Dios"),
    ("G                               D", "Solo Tú eres grande, solo Tú eres digno"),
    ("Em                           C", "Eres asombroso para mí"),
    ("        G          D", "Eres grande, eres digno"),
    ("Em                           C", "Eres asombroso para mí"),
    ("        G          D", "Eres grande, eres digno"),
    ("Em                           C", "Eres asombroso para mí"),
    None,
    ("           G", "Y me diste nombre"),
    ("           D", "Yo soy Tu niña"),
    ("                Em", "La niña de Tus ojos"),
    ("                   C", "Porque me amaste a mí"),
    None,
    ("G", "Te amo más que a mi vida"),
    ("D", "Te amo más que a mi vida"),
    ("Em                           C", "Te amo más que a mi vida, más"),
    None,
    ("           G", "Y me diste nombre (te amo más que a mi vida)"),
    ("           D", "Yo soy Tu niña (te amo más que a mi vida)"),
    ("                Em", "La niña de Tus ojos (te amo más que a mi vida)"),
    ("                   C", "Porque me amaste a mí (te amo más que a mi vida)"),
    ("           G", "Y me diste nombre (te amo más que a mi vida)"),
    ("           D", "Yo soy Tu niña (te amo más que a mi vida)"),
    ("                Em", "La niña de Tus ojos (te amo más que a mi vida)"),
    ("                   C", "Porque me amaste a mí (te amo más que a mi vida)"),
    None,
    ("G     D", "Cristo reina, (reina reina Señor)"),
    ("Em    C", "Cristo reina, (aquí está Tu pueblo Jesús)"),
    ("G     D", "Cristo reina (te estamos esperando)"),
    ("Em      C", "Con poder (tuyo es el poder, es el poder)"),
    None,
    ("##", "[modulación +2 → A]"),
    ("A     E", "Cristo reina, Cristo reina"),
    ("F#m    D", "Cristo reina, con poder"),
])

# ============================================================
# 47. LA NIÑA DE TUS OJOS (DO) - Daniel Calveti
# ============================================================
song(p, 27, "LA NIÑA DE TUS OJOS  (G)  - Daniel Calveti", [
    ("G                    D", "Me viste a mí cuando nadie me vio,"),
    ("Em                   C", "me amaste a mí cuando nadie me amó."),
    ("G                    D", "Me viste a mí cuando nadie me vio,"),
    ("Em                   C", "me amaste a mí cuando nadie me amó."),
    None,
    ("G                    D", "Y me diste nombre, yo soy tu niña,"),
    ("Em                   C", "la niña de Tus ojos, porque me amaste a mí."),
    ("G                    D", "Y me diste nombre, yo soy tu niña,"),
    ("Em                   C", "la niña de Tus ojos, porque me amaste a mí."),
    None,
    ("G       D", "Me amaste a mí,"),
    ("Em      C", "me amaste a mí,"),
    ("G       D", "me amaste a mí,"),
    ("Em      C", "porque me amaste a mí."),
    None,
    ("G", "Te amo más que a mi vida,"),
    ("D", "te amo más que a mi vida,"),
    ("Em      C", "te amo más que a mi vida, más."),
    ("G", "Te amo más que a mi vida,"),
    ("D", "te amo más que a mi vida,"),
    ("Em      C", "te amo más que a mi vida, más."),
    ("G", "Te amo más que a mi vida,"),
    ("D", "te amo más que a mi vida,"),
    ("Em      C", "te amo más que a mi vida, más."),
    ("G", "Te amo más que a mi vida,"),
    ("D", "te amo más que a mi vida,"),
    ("Em      C", "te amo más que a mi vida, más."),
    ("G", "Te amo más que a mi vida,"),
    ("D", "te amo más que a mi vida,"),
    ("Em      C", "te amo más que a mi vida, más."),
    None,
    ("G                    D", "Y me diste nombre, yo soy tu niña,"),
    ("Em                   C", "la niña de Tus ojos, porque me amaste a mí."),
    ("G                    D", "Y me diste nombre, yo soy tu niña,"),
    ("Em                   C", "la niña de Tus ojos, porque me amaste a mí, a mí."),
])

# ============================================================
# 28. EL QUE MUERE POR MÍ (SOL)
# ============================================================
song(p, 28, "EL QUE MUERE POR MÍ  (G)", [
    ("G                C", "Todo empezó en una cruz,"),
    ("             Em                   D", "donde un hombre sufrió y un Dios se entregó."),
    ("G                C", "Silenciosa, la muerte llegó,"),
    ("             Em                        D", "extinguiendo la luz, que en un grito se ahogó."),
    None,
    ("G                C", "Viendo su faz de dolor,"),
    ("         Em               D", "una madre lloró y su amigo calló."),
    ("G                   C", "Pero, siendo una entrega de amor,"),
    ("         Em        D       C", "su camino siguió y en algún otro lado"),
    ("D           G", "una luz se encendió."),
    None,
    ("C              D              Em", "Siendo hombre, amigo, esclavo y maestro,"),
    ("                          D         C", "siendo carga pesada, profesor y aprendiz,"),
    ("              D                      G   D", "entregó hasta su cuerpo en el pan y en la vid."),
    None,
    ("Em     C          G        D       Em", "Desde entonces lo he visto caminar a mi lado,"),
    ("      C            G      D       Em", "a ese Dios que se humilla y muere por mí."),
    ("      C           G         D       Em", "Es la barca en mi playa, el ruido del silencio,"),
    ("        C         G         D     Am", "que se acerca a su hijo y me abraza feliz,"),
    ("C                 D                 G", "que se acerca a su hijo y me abraza feliz."),
    None,
    ("##", "[Interludio: C  Em  D]"),
    None,
    ("G                  C", "Viendo un humilde calvario,"),
    ("              Em              D", "con rostro cansado soporta la cruz."),
    ("G                  C", "Y al verme rezando a sus pies,"),
    ("            Em     D          C", "se olvida de Él, me toma en sus brazos"),
    ("      D         G", "y me acoge otra vez."),
    None,
    ("C              D                  Em", "Siendo fuego, paloma, el agua y el viento."),
    ("                         D         C", "Siendo niño inocente, un Padre y pastor."),
    ("                D                    G   D", "Hoy acepta mi ofrenda, es mi vida, Señor."),
    None,
    ("##", "[Estribillo]"),
    ("C             D", "Y si ahora yo acepto esa cruz,"),
    ("Bm           Em        C    D", "es por esa persona, ese Dios,"),
    ("                  G    D", "es por Cristo, Jesús."),
    None,
    ("C             D", "Y si ahora yo acepto esa cruz,"),
    ("Bm           Em        C    D", "es por esa persona, ese Dios,"),
    ("                  G    D", "es por Cristo, Jesús."),
    None,
    ("C             D", "Y si ahora yo acepto esa cruz,"),
    ("Bm           Em        C    D", "es por esa persona, ese Dios,"),
    ("                  G    D", "es por Cristo, Jesús."),
])

# ============================================================
# 29. ALMA DE CRISTO (DO)
# ============================================================
song(p, 29, "ALMA DE CRISTO  (D)", [
    ("##", "[Intro: D - C - G - D  (x2)]"),
    None,
    ("D                C   G  D", "Alma de Cristo, santifícame."),
    ("                 C   G  D", "Cuerpo de Cristo, sálvame."),
    ("                 C   G  D", "Sangre de Cristo, embriágame."),
    ("                 C   G  D", "Agua de su Costado, lávame."),
    None,
    ("##", "[D - C - G - D  (x2)]"),
    None,
    ("D                C   G  D", "Pasión de Cristo, confórtame."),
    ("                 C   G  D", "Oh, buen Jesús, óyeme."),
    None,
    ("##", "[Estribillo (x2)]"),
    ("  Bm            G        D  A", "Dentro de tus llagas, escóndeme."),
    "No permitas que me aparte de Ti.",
    "Del maligno enemigo, defiéndeme.",
    "Y en la hora de mi muerte, llámame,",
    ("   Em", "y mándame ir a Ti,"),
    ("G                D          A", "para que con tus santos te alabe,"),
    ("        Em                     D", "por los siglos de los siglos. Amén."),
])

p.save()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            