#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

W, H = A4
ML = 18*mm; MR = W-18*mm; MT = H-20*mm; MB = 22*mm
CHORD_COLOR = HexColor("#1a1acc")

class PDF:
    def __init__(self,fn):
        self.c=canvas.Canvas(fn,pagesize=A4); self.pn=0; self.y=0; self._pg()
    def _pg(self):
        if self.pn: self.c.showPage()
        self.pn+=1; self.y=MT
        self.c.setFont("Courier",7); self.c.setFillColorRGB(0,0,0)
        self.c.drawCentredString(W/2,13*mm,str(self.pn))
    def _chk(self,h):
        if self.y-h<MB: self._pg()
    def title(self,t):
        self._chk(22); self.y-=6
        self.c.setFont("Courier-Bold",11); self.c.setFillColorRGB(0,0,0)
        self.c.drawString(ML,self.y,t); self.y-=2
        self.c.setLineWidth(0.5); self.c.line(ML,self.y,MR,self.y); self.y-=7
    def sec(self,t):
        self._chk(11); self.c.setFont("Courier-Bold",8.5)
        self.c.setFillColorRGB(0,0,0); self.c.drawString(ML,self.y,t); self.y-=10
    def ln(self,ch,ly):
        h=10.5+(9.5 if ch else 0); self._chk(h)
        if ch:
            self.c.setFont("Courier-Bold",8.5); self.c.setFillColor(CHORD_COLOR)
            self.c.drawString(ML,self.y,ch); self.c.setFillColorRGB(0,0,0); self.y-=9.5
        self.c.setFont("Courier",8.5); self.c.setFillColorRGB(0,0,0)
        self.c.drawString(ML,self.y,ly); self.y-=10.5
    def gap(self): self.y-=5
    def save(self): self.c.save()

def song(p,num,name,items):
    p.title(f"{num}. {name}")
    for x in items:
        if x is None: p.gap()
        elif isinstance(x,tuple) and x[0]=="##": p.sec(x[1])
        elif isinstance(x,tuple): p.ln(x[0],x[1])
        else: p.ln("",str(x))
    p.gap(); p.gap()

p = PDF("/sessions/gallant-gracious-franklin/mnt/outputs/Cancionero_seleccion.pdf")

# Cover
p.c.setFont("Courier-Bold",18); p.c.setFillColorRGB(1,1,1)
p.c.rect(0,0,W,H,fill=1,stroke=0)
p.c.setFillColorRGB(0.1,0.18,0.36)
p.c.rect(0,0,W,H,fill=1,stroke=0)
p.c.setFillColorRGB(1,1,1)
p.c.setFont("Courier-Bold",22)
p.c.drawCentredString(W/2,H/2+30,"CANCIONERO")
p.c.setFont("Courier-Bold",12)
p.c.drawCentredString(W/2,H/2+5,"Seleccion personal")
p.c.setFont("Courier",10)
p.c.drawCentredString(W/2,H/2-15,"Pascua Joven San Isidro")
p.c.setLineWidth(0.8); p.c.setStrokeColorRGB(1,1,1)
p.c.line(ML,H/2+45,MR,H/2+45)
p.c.line(ML,H/2-28,MR,H/2-28)
p._pg()

# INDICE
p.title("INDICE")
for line in [
    " 1. CON VOS  (A)",
    " 2. DIME REY  (G)",
    " 3. CANCIONES DEL ESPIRITU SANTO / MARANATHA  (Em, capo 1)",
    " 4. TU REINO ENTRE LOS VIVOS  (C)",
    " 5. EN LA PALMA DE SU MANO  (D, capo 1 = Eb)",
    " 6. PARA DARLO A LOS DEMAS  (C)",
    " 7. VIDA EN ABUNDANCIA  (G)",
    " 8. CRISTO REINA (REMIX)  (G)",
]:
    p.ln("",line)
p._pg()

# 1. CON VOS
song(p,1,"CON VOS  (A)",[
    ("A           E","Te alejaste de mí"),
    ("    F#m              D","Estás perdido, no encuentras sentido"),
    ("A               E","Te avergüenza quien sos"),
    ("    F#m         D","Estás dolido, te sentís vacío"),
    None,
    ("Bm          D","Elegí buscarte"),
    ("F#m                 D","Y llorar con vos, con tu corazón"),
    ("Bm              D","Un corazón sediento"),
    ("                E","Herido por el tiempo"),
    None,
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E           D","Aquí yo te espero, no tengas miedo"),
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E","Necesito verte"),
    ("D               E","Elijo todo lo que sos"),
    ("A               E","Quiero estar con vos"),
    ("F#m             D","Quiero estar con vos"),
    None,
    ("A                   E","Cómo hacerte entender"),
    ("    F#m                         D","Lo mucho que te quiero, lo mucho que te espero"),
    ("A               E","Te espero para abrazar"),
    ("    F#m                 D","Tu mundo entero, con mi amor sincero"),
    None,
    ("Bm                  D","No importa lo que hayas hecho"),
    ("F#m","Mi amor no cambió"),
    ("D","Escuchá mi voz"),
    ("Bm          D","Una voz compasiva"),
    ("                E","¡Vuelve a la vida!"),
    None,
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E           D","Aquí yo te espero, no tengas miedo"),
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E","Necesito verte"),
    ("D               E","Elijo todo lo que sos"),
    ("A               E","Quiero estar con vos"),
    ("F#m             D","Quiero estar con vos"),
    None,
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E           D","Aquí yo te espero, no tengas miedo"),
    ("A               E","Vuelve a casa hoy (vuelve a casa hoy)"),
    ("F#m             D","Vuelve por favor (vuelve por favor)"),
    ("A       E","Necesito verte"),
    ("D               E","Elijo todo lo que sos"),
    ("A               E","Quiero estar con vos"),
    ("F#m             D","Quiero estar con vos"),
])

# 2. DIME REY
song(p,2,"DIME REY  (G)",[
    ("G               D","Hoy miraba señor tus heridas"),
    ("Em                  C","Y el dolor que abarcaba esa cruz"),
    ("G               D","Con tus manos muy bien extendidas"),
    ("Em              C","Abrazabas toda multitud"),
    None,
    ("G               D","Hoy miraba señor al soldado"),
    ("Em                      C","Perforando con lanzas tus pies"),
    ("G                   D","Y esos clavos muy bien sujetados"),
    ("Em              C","Sostenian con odio tus pies"),
    None,
    ("##","[Estribillo]"),
    ("G               D","Dime rey porque estás tan callado"),
    ("Em                  C","Te latigaron con tanto furor"),
    ("G               D","Dime rey porque escondes el llanto"),
    ("Em              C","Y perdonas aquel quien te mato"),
    None,
    ("G               D","Dime rey porque es tan necesario"),
    ("Em                          C","Morir asi de esta forma tan cruel"),
    ("G               D","Dime rey como puedo ayudarte"),
    ("Em              C","A soportar el dolor que tenes"),
    None,
    ("G               D","Hijo mio esa cruz tenebrosa"),
    ("Em                  C","Me dolió y hasta sangre sudé"),
    ("G               D","Por amor a esas vidas perdidas"),
    ("Em              C","Toda aquella maldad soporté"),
    None,
    ("G               D","Mi mensaje de amor y justicia"),
    ("Em              C","Salvaria toda humanidad"),
    ("G               D","Pero más me dolió todavia"),
    ("    Em              C","Que no a todos les pudo llegar"),
    None,
    ("G               D","Hoy miraba hijo mio esos niños"),
    ("Em                          C","Morir asi, de esa forma tan cruel"),
    ("G               D","Hoy miraba toda la pobreza"),
    ("Em              C","Sufriendo frio con hambre y con sed"),
    None,
    ("G                   D","Y esos jóvenes tan lastimados"),
    ("Em              C","Equivocados pecando otra vez"),
    ("G               D","Me recuerdan aquel Viernes Santo"),
    ("Em              C","Y ese dolor se repite otra vez"),
    None,
    ("Em              C","Animate que tú estás conmigo"),
    ("G               D","A expandir ese amor de tu fe"),
    ("Em              C","Hijo mio ese fuego perdido"),
    ("G               D","Tú lo puedes volver a encender"),
    None,
    ("Em              C","Misiona, transforma"),
    ("Em              C","Esas almas que no pude entrar"),
    ("Em              C","Misiona, transforma"),
    ("G               D","Corazones sedientos de paz"),
])

# 3. CANCIONES DEL ESPÍRITU SANTO / MARANATHÁ
song(p,3,"CANCIONES DEL ESPIRITU SANTO / MARANATHA  (Em, capo 1)",[
    ("##","[Primera estrofa: arpegiada]"),
    ("Em              D","Espíritu de Dios, toma mi vida,"),
    ("    C           B7","toma mi alma, toma mi ser."),
    ("Em              D","Lléname con tu presencia,"),
    ("    C       B7","con tu poder, lléname de ti."),
    ("Em              D","Lléname con tu presencia,"),
    ("    C       B7  Em","con tu poder, lléname de ti."),
    None,
    ("##","[Desde aquí: rasgeo]"),
    ("Em                                  D","Enciéndeme señor, préndeme fuego quiero anunciarte,"),
    ("        C                       B7","morir por vos, lléname con tu presencia, con tu poder,"),
    ("Em","lléname de ti."),
    None,
    ("##","[Instrumental: Em C D Em / G D Em C D]"),
    None,
    ("Em","Espíritu Santo, espíritu Santo,"),
    ("C   D   Em","muévete en este lugar. (bis)"),
    None,
    ("Em              C","Que haya paz, (que haya paz), que haya paz, (que haya paz),"),
    ("D           Em","que haya paz en este lugar."),
    ("Em              C","Que haya amor, que haya amor,"),
    ("D           Em","que haya amor en este lugar."),
    ("Em              C","Espíritu Santo, espíritu Santo,"),
    ("D           Em","quédate en este lugar."),
    None,
    ("##","[Instrumental: Em C D Em / G D Em C D]"),
    None,
    ("G   D   Em  C   D","Ven espíritu de Dios, ven a mi ser, ven a mi vida,"),
    ("G","ven espíritu de amor,"),
    ("D           Em              C       D","ven a morar, ven hacia mí, ven espíritu de Dios, ven a mi ser,"),
    ("G       D   Em  C   D","ven a mi vida, ven espíritu de amor, ven a morar, para maranathá."),
])

# 4. TU REINO ENTRE LOS VIVOS
song(p,4,"TU REINO ENTRE LOS VIVOS  (C)",[
    ("C                    F","No permitas, Jesús, que muera"),
    ("C                        F","sin antes ver tu Reino entre los vivos."),
    ("Am       Em             F         C","Que no me vaya si alguien no te conociera."),
    ("Am             Em              F       G","Que me quede hasta que el mundo te haya oído."),
    None,
    ("F            G          C  C7","Maestro, qué bien estamos acá."),
    ("F              G              C  C7","Ay, si todos pudieran sentir tu paz."),
    ("F         G","Dejame quedarme y ser yo,"),
    ("Am       Em","por favor quedate y se Vos,"),
    ("F        G                C","dejame quedarme y llevar tu amor."),
    None,
    ("C                               F","Que al final de mis días pueda decir"),
    ("C                             F","que he peleado el buen combate hasta el fin;"),
    ("Am           Em          F    C","completé mi carrera, conservé mi fe."),
    ("Am       Em               F       G","La corona de justicia está preparada para mí."),
    None,
    ("F            G          C  C7","Maestro, qué bien estamos acá."),
    ("F              G              C  C7","Ay, si todos pudieran sentir tu paz."),
    ("F         G","Dejame quedarme y ser yo,"),
    ("Am       Em","por favor quedate y se Vos,"),
    ("F        G                C","dejame quedarme y llevar tu amor."),
])

# 5. EN LA PALMA DE SU MANO
song(p,5,"EN LA PALMA DE SU MANO  (D, capo 1 = Eb)",[
    ("D               G           D   G","Que el camino venga siempre a tu encuentro,"),
    ("Bm              G           A","cuando no sepas más dónde buscar."),
    ("D               G           D   G","Que el viento sople siempre a tu espalda,"),
    ("Bm              G           A","cuando no queden fuerzas para avanzar."),
    ("Bm      F#m         G               D","Y que la verdad guíe tus pensamientos y tus actos,"),
    ("G               A           D   G","y que Dios te lleve en la palma de su mano."),
    None,
    ("##","[Rasgueo]"),
    None,
    ("D               G           D   G","Que el sol te dé siempre en la cara,"),
    ("Bm              G           A","y hará que tu sonrisa brille más."),
    ("D               G           D   G","Que la lluvia caiga siempre en tu campo,"),
    ("Bm              G           A","y que le pierdas el miedo a llorar."),
    ("Bm      F#m         G                       D","Y que las personas que quieras permanezcan a tu lado,"),
    ("G               A               D","y que Dios te lleve en la palma de su mano."),
    None,
    ("Bm      F#m     G                   D","Y hasta que volvamos a vernos, cuídate mi hermano,"),
    ("G               A               D","y que Dios te lleve en la palma de su mano."),
    None,
    ("G               A               Bm","Y que Dios te lleve en la palma de su mano,"),
    ("G               A               D","y que Dios te lleve en la palma de su mano."),
])

# 6. PARA DARLO A LOS DEMÁS
song(p,6,"PARA DARLO A LOS DEMAS  (C)",[
    ("C           G       Am","A veces me siento alejado"),
    ("F           D7          G","y la vergüenza no me deja ni hablar."),
    ("C           G       Am","Y solo sé que me duele verte clavado"),
    ("F           D7          G","porque me olvido de lo mucho que me amas."),
    None,
    ("Am  G   F","Quiero volver a serte fiel."),
    ("Am  G   F   G7","Quiero volver a serte fiel."),
    None,
    ("C           G       Am","Toma de mí lo que te sirva"),
    ("        G           C","para darlo a los demás."),
    ("        G       Am","Toma de mí lo que te sirva,"),
    ("        G       Am","no me guardo nada más."),
    ("    Em          F","Hoy quiero ser tu instrumento,"),
    ("        G           Am","predicar tu gran verdad,"),
    ("    Em          F","la de tu palabra, la de tu cuerpo,"),
    ("    Bb              G           C","la de tu amor eterno, la de amar al más pequeño."),
    None,
    ("C           G       Am","Trato de encontrarte en mis hermanos"),
    ("F           D7          G","pero se me hace imposible sin tu amor."),
    ("C           G       Am","Soy débil y te pido que tus manos"),
    ("F           D7          G","abran de par en par mi corazón."),
    None,
    ("Am  G   F","Quiero volver a serte fiel."),
    ("Am  G   F   G7","Quiero volver a serte fiel."),
    None,
    ("C           G       Am","Toma de mí lo que te sirva"),
    ("        G           C","para darlo a los demás."),
    ("        G       Am","Toma de mí lo que te sirva,"),
    ("        G       Am","no me guardo nada más."),
    ("    Em          F","Hoy quiero ser tu instrumento,"),
    ("        G           Am","predicar tu gran verdad,"),
    ("    Em          F","la de tu palabra, la de tu cuerpo,"),
    ("    Bb              G           C","la de tu amor eterno, la de amar al más pequeño."),
])

# 7. VIDA EN ABUNDANCIA
song(p,7,"VIDA EN ABUNDANCIA  (G)",[
    ("G               C           D","Los lirios del campo y las aves del cielo,"),
    ("G               C           D","no se preocupan porque están en mis manos."),
    ("Em              C","Tené confianza en mí,"),
    ("G               D","acá estoy junto a vos."),
    None,
    ("G               C           D","Amá lo que sos y tus circunstancias,"),
    ("G               C           D","estoy con vos, con tu cruz en mi espalda."),
    ("Em              C","todo terminará bien,"),
    ("G               D","yo hago nuevas todas las cosas."),
    None,
    ("##","[Pre-Estribillo]"),
    ("Em  C               G   D","Yo vengo a traerte vida,"),
    ("Em  C               D","vida en abundancia, en abundancia."),
    None,
    ("##","[Estribillo]"),
    ("Em  C               G   D","Yo soy el camino, la verdad y la vida,"),
    ("Em  C               D","vida en abundancia, en abundancia."),
    None,
    ("G               C           D","No hice al hombre para que esté solo,"),
    ("G               C           D","caminen juntos como hermanos."),
    ("Em              C","Sopórtense mutuamente,"),
    ("G               D","ámense unos a otros."),
    None,
    ("G               C           D","La felicidad de la vida eterna"),
    ("G               C           D","empieza conmigo en la tierra."),
    ("Em              C","Sentite vivo,"),
    ("G               D","la fiesta del reino comienza acá."),
    None,
    ("##","[Pre-Estribillo]"),
    ("Em  C               G   D","Yo vengo a traerte vida,"),
    ("Em  C               D","vida en abundancia, en abundancia."),
    None,
    ("##","[Estribillo]"),
    ("Em  C               G   D","Yo soy el camino, la verdad y la vida,"),
    ("Em  C               D","vida en abundancia, en abundancia."),
    None,
    ("##","[Pre-Estribillo]"),
    ("Em  C               G   D","Yo vengo a traerte vida (yo vengo a traerte vida),"),
    ("Em  C               D","vida en abundancia, en abundancia (vida en abundancia)."),
    None,
    ("##","[Estribillo]"),
    ("Em  C               G   D","Yo soy el camino, la verdad y la vida (yo soy el camino...),"),
    ("Em  C               D","vida en abundancia, en abundancia (vida en abundancia)."),
])

# 8. CRISTO REINA (REMIX)
song(p,8,"CRISTO REINA (REMIX)  (G)",[
    ("##","[Intro] G D Em C"),
    None,
    ("G               D","Mi corazón quiere alabar, alabarte"),
    ("Em                      C","Mi corazón quiere adorar, adorarte"),
    ("G               D","Mi corazón quiere alabar, alabarte"),
    ("Em                      C","Mi corazón quiere adorar, adorarte"),
    None,
    ("G       D","Cristo reina, (reina reina Señor)"),
    ("Em      C","Cristo reina, (aquí está Tu pueblo Jesús)"),
    ("G       D","Cristo reina (te estamos esperando)"),
    ("Em      C","Con poder (tuyo es el poder, es el poder)"),
    None,
    ("G                   D","Vine a adorarte, vine a postrarme"),
    ("    Em                  C","Vine a decir que eres mi Dios"),
    ("G                       D","Solo Tú eres grande, solo Tú eres digno"),
    ("Em                      C","Eres asombroso para mí"),
    None,
    ("        G           D","Eres grande, eres digno"),
    ("Em                  C","Eres asombroso para mí"),
    ("        G           D","Eres grande, eres digno"),
    ("Em                  C","Eres asombroso para mí"),
    None,
    ("            G","Y me diste nombre"),
    ("            D","Yo soy Tu niña"),
    ("            Em","La niña de Tus ojos"),
    ("            C","Porque me amaste a mí"),
    None,
    ("G","Te amo más que a mi vida"),
    ("D","Te amo más que a mi vida"),
    ("Em              C","Te amo más que a mi vida, más"),
    None,
    ("            G","Y me diste nombre (te amo más que a mi vida)"),
    ("            D","Yo soy Tu niña (te amo más que a mi vida)"),
    ("            Em","La niña de Tus ojos (te amo más que a mi vida)"),
    ("            C","Porque me amaste a mí (te amo más que a mi vida)"),
    ("            G","Y me diste nombre (te amo más que a mi vida)"),
    ("            D","Yo soy Tu niña (te amo más que a mi vida)"),
    ("            Em","La niña de Tus ojos (te amo más que a mi vida)"),
    ("            C","Porque me amaste a mí (te amo más que a mi vida)"),
    None,
    ("G       D","Cristo reina, (reina reina Señor)"),
    ("Em      C","Cristo reina, (aquí está Tu pueblo Jesús)"),
    ("G       D","Cristo reina (te estamos esperando)"),
    ("Em      C","Con poder (tuyo es el poder, es el poder)"),
    None,
    ("##","[Modulación +2 → A]"),
    ("A       E","Cristo reina, Cristo reina"),
    ("F#m     D","Cristo reina, con poder"),
])

p.save()
print("OK")
