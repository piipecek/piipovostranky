db jsem okopiroval z cernabila 19. 1. 2024

model evaluace bude mít:

ucitel: user_id
data_json: otazky a odpovedi v jsonu jako text
datum vytvoreni kodu
datum odeslani
kod
je_odevzdana


Možnosti forulářovej otázek jsou: 
otevrena
    otazka
    id (int)
    valaue
ciselna
    otazka
    id (int)
    max
    value
    text_min
    text_max
single
    otazka
    id (int)
    choices
    value
multiple
    otazka
    id (int)
    choices
    values


TODO:

sjednotit otázky, aby "dobrý" bylo vždy na jedné straně.
agregovaný výsledky
mít možnost upravit si formulář přes tím, než ho zveřejním.