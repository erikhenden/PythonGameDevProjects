# 🎯 Turret Shooter

Et Python-basert top-down skytespill der du forsvarer en turret mot bølger av innkommende fiender.

---

## 🎮 Spillkonsept

Spilleren kontrollerer en turret plassert midt på skjermen. Fiender strømmer inn fra alle kanter og beveger seg mot turreten. Målet er å overleve så mange bølger som mulig ved å skyte ned fiendene før de når midten.

Spillet er bygget rundt én enkel, engasjerende kjerneloop:

```
Bølge starter → Fiender angriper → Spiller skyter → Bølge ryddes → Oppgrader → Gjenta
```

---

## 🗺️ Veikart

Prosjektet er delt inn i tre faser, fra enkel kjerne til et fullverdig spill.

### Fase 1 – Kjerne (MVP)
Den grunnleggende spillopplevelsen. Ingenting fancy – bare funksjonelt og gøy.

- [ ] Spillvindu og game loop med Pygame CE
- [ ] Turret i midten som roterer mot musepeker
- [ ] Enkel skytemekanikk (venstreklikk / automatisk)
- [ ] Én type fiende som beveger seg mot midten
- [ ] Bølgesystem med økende antall fiender
- [ ] HP-system for turret (spillet slutter når HP = 0)
- [ ] Poengsystem
- [ ] Game Over-skjerm med score

### Fase 2 – Variasjon og dybde
Gjør spillet mer engasjerende og gi spilleren valg.

- [ ] Flere fiendtyper (rask/svak, treg/sterk, splitter seg)
- [ ] Oppgraderingssystem mellom bølger (velg én av tre)
- [ ] Ressurser droppet av fiender
- [ ] Overheting / ammunisjonsbegrensning på turret
- [ ] Sprite-animasjoner
- [ ] Lydeffekter (pygame.mixer)

### Fase 3 – Polering og innhold
Gjør spillet spillklart for andre.

- [ ] Boss-fiender hver 5. bølge
- [ ] Highscore-lagring (JSON-fil)
- [ ] Startmeny og pausemeny
- [ ] Vanskelighetsgrader
- [ ] Balansering basert på spilltesting

---

## 🏗️ Teknisk stack

| Komponent      | Teknologi                 |
|----------------|--------------------------|
| Språk          | Python 3.11+              |
| Spillbibliotek | Pygame Community Edition  |
| Lyd            | pygame.mixer              |
| Datalagring    | JSON (highscores)         |

---

## 📁 Prosjektstruktur

```
turret_shooter/
│
├── __main__.py          # Inngangspunkt – starter spillet
├── game.py              # Game loop, tilstandshåndtering og koordinering
├── entities.py          # Spillobjekter: Turret, Bullet, Enemy
├── utils.py             # Hjelpefunksjoner: vektormatematikk, kollisjoner, konstanter
│
└── assets/
    ├── sprites/         # Bildefiler (.png) for turret, fiender, prosjektiler
    └── sounds/          # Lydfiler (.wav / .ogg) for skudd, treff, eksplosjon
```

### Filansvar

**`__main__.py`**
Inngangspunkt for spillet. Initialiserer Pygame og starter game loop.
```python
# Kjøres med: python -m turret_shooter
```

**`game.py`**
Hjertet i spillet. Håndterer game loop, bølgesystem, input og rendering.

**`entities.py`**
Inneholder alle spillobjekter som egne klasser: `Turret`, `Bullet` og `Enemy`.
Hver klasse har ansvar for sin egen oppdatering og tegning.

**`utils.py`**
Delte hjelpefunksjoner og konstanter som brukes på tvers av filene –
vektormatematikk, kollisjonsdeteksjon og spillparametere.

---

## 🔧 Kjernemekanikker forklart

### Turret-rotasjon
Turreten peker alltid mot musepekeren ved hjelp av `pygame.math.Vector2`:

```python
direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(turret.rect.center)
angle = -direction.angle_to(pygame.math.Vector2(1, 0))
```

### Bølgesystem
Bølger eskalerer gradvis i antall og hastighet:

```python
enemy_count = BASE_ENEMIES + wave * SCALE_FACTOR
enemy_speed = BASE_SPEED + wave * SPEED_INCREMENT
```

### Kollisjonsdeteksjon
Sirkelbasert kollisjon via `pygame.math.Vector2.distance_to()`:

```python
def circles_collide(a, b) -> bool:
    distance = pygame.math.Vector2(a.pos).distance_to(b.pos)
    return distance < (a.radius + b.radius)
```

---

## 🎯 Designprinsipper

**1. Enkelt først, komplekst etterpå**
Legg aldri til ny funksjonalitet før kjernen fungerer godt.

**2. Spilleren skal alltid føle seg akkurat på grensen**
Vanskelighetsgraden øker jevnt – aldri for lett, aldri for hardt.

**3. Responsivt og forutsigbart**
Kontrollene gjør alltid nøyaktig det spilleren forventer.

**4. Ren og lesbar kode**
Hver fil og klasse har ett tydelig ansvar. Kode skrives for å leses av mennesker.

---

## 🚀 Kom i gang

### Krav
- Python 3.11+
- Pygame Community Edition

### Installasjon

```bash
# Installer Pygame CE
pip install pygame-ce

# Klon prosjektet
git clone https://github.com/ditt-brukernavn/turret-shooter.git
cd turret-shooter

# Start spillet
python -m turret_shooter
```

---

## 📐 Spillparametere (Fase 1)

Disse verdiene defineres i `utils.py` og kan justeres for å balansere spillet:

| Parameter          | Standardverdi | Beskrivelse                   |
|--------------------|---------------|-------------------------------|
| `SCREEN_WIDTH`     | 800 px        | Bredde på spillvinduet        |
| `SCREEN_HEIGHT`    | 600 px        | Høyde på spillvinduet         |
| `FPS`              | 60            | Bilder per sekund             |
| `TURRET_HP`        | 100           | Startliv for turreten         |
| `BULLET_SPEED`     | 600 px/s      | Hastighet på prosjektiler     |
| `FIRE_RATE`        | 300 ms        | Tid mellom hvert skudd        |
| `BASE_ENEMIES`     | 5             | Antall fiender i bølge 1      |
| `SCALE_FACTOR`     | 2             | Ekstra fiender per bølge      |
| `BASE_ENEMY_SPEED` | 80 px/s       | Fiendehastighet i bølge 1     |
| `SPEED_INCREMENT`  | 5 px/s        | Ekstra fart per bølge         |
| `WAVE_PAUSE`       | 3000 ms       | Pause mellom bølger           |

---

## 📝 Lisens

MIT – gjør hva du vil med koden.
