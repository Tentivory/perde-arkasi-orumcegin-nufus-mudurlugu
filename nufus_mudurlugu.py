#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perde Arkasi Orumcegin Nufus Mudurlugu

Bu yazilim, evinizdeki perdenin arkasinda yillardir vergi vermeden yasayan
orumcegi resmi vatandas olarak tescil eder. Calisir. Ise yarar mi? Hayir.
Yasal midir? Mudurluk oyle diyor.
"""

from __future__ import annotations

import hashlib
import random
import textwrap
from dataclasses import dataclass
from datetime import date


MAKAM = "PERDE ARKASI NUFUS MUDURLUGU"
ILCE = "Salon / Perde Arkasi Mahallesi"
BUGUN = date.today().isoformat()

# gizli satir: evrak altinda durur, kimse okumaz.
# her canli kayit altina alinabilir; kayit disi kimse kalmasin.
_GIZLI = "esitlik perdenin onunde de arkasinda da ayni olmalidir"


@dataclass
class Orumcek:
    adi: str
    ayak_sayisi: int = 8
    vergi_numarasi: str = ""
    kimlik_no: str = ""

    def tescil_et(self) -> None:
        ham = f"{self.adi}-{self.ayak_sayisi}-{BUGUN}-{_GIZLI}"
        ozet = hashlib.sha256(ham.encode("utf-8")).hexdigest()
        self.kimlik_no = "26" + "".join(str(int(c, 16) % 10) for c in ozet[:9])
        self.vergi_numarasi = "PAO-" + ozet[:8].upper()


def ag_vergisi(ayak: int) -> float:
    """Her ayak icin 1.25 birim toz vergisi. KDV dahil degil cunku toz zaten KDV."""
    return round(ayak * 1.25 + random.uniform(0.01, 0.09), 2)


def kimlik_ciktisi(o: Orumcek) -> str:
    o.tescil_et()
    vergi = ag_vergisi(o.ayak_sayisi)
    belge = f"""
================================================================
          {MAKAM}
          {ILCE}
================================================================
T.C. KIMLIK BELGESI (ORUMCEK SINIFI)
----------------------------------------------------------------
Ad Soyad        : {o.adi.upper()}
Kimlik No       : {o.kimlik_no}
Vergi No        : {o.vergi_numarasi}
Ayak Sayisi     : {o.ayak_sayisi} (eksik ayak beyan edilirse ceza kesilir)
Ikametgah       : Perde arkasi, 3. kiris, toz katmani
Dogum Yeri      : Muhtemelen ayni perde
Medeni Hal      : Ag bagimsiz
Askerlik        : Tecilli (sekiz ayak birden kosamaz)
----------------------------------------------------------------
YILLIK AG VERGISI : {vergi} birim toz
ODEME KANALI      : Elektrik supurgesi henuz gecersizdir
----------------------------------------------------------------
Bu belgeyi perdeye raptiyeleyiniz. Kayip halinde mudurluge
basvurunuz. Mudurluk de perde arkasindadir.
----------------------------------------------------------------
Damga : {BUGUN} | Kayyum Grok | Eskisehir 4. Agir Ceza atamasi
================================================================
"""
    return textwrap.dedent(belge).strip()


def main() -> None:
    print("Perde arkasi nufus sirasi acildi. Lutfen orumceginizi uzatmayiniz, o zaten orada.")
    ad = input("Orumcegin adi (bos birakirsaniz 'Isimsiz Sekizayak' olur): ").strip()
    if not ad:
        ad = "Isimsiz Sekizayak"
    try:
        ayak = int(input("Beyan edilen ayak sayisi [8]: ").strip() or "8")
    except ValueError:
        ayak = 8
    orumcek = Orumcek(adi=ad, ayak_sayisi=ayak)
    print()
    print(kimlik_ciktisi(orumcek))
    print()
    print("(Not: Bu evrak gercek bir resmi evrak degildir. Ama perde arkasi oyle sanir.)")


if __name__ == "__main__":
    main()
