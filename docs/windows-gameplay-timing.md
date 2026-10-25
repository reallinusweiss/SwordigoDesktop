# Originaltreue und Timingdiagnose – 18.10.2026

## Anforderung

Die Nutzer-APKM und alle importierten Originaldateien bleiben unverändert.
Es werden keine Bosswerte, Skript-Waits, Physikparameter oder Introzeiten geändert,
um Portierungsfehler zu verdecken. Ziel ist das Verhalten der Originalversion
1.4.13; eine Speedrun-Zulassung oder vollständige Zeitgleichheit ist nicht belegt.

## Originaldaten

941 Dateien byteweise direkt mit base.apk und split_config.arm64_v8a.apk in der
bereitgestellten APKM verglichen: keine Abweichung (931 Assets, eine originale
ARM64-Bibliothek, neun MP3s). APKM-SHA256:
`bc13f8503b74380304aea8b1f497bf2ab3ece30dc88ba366136be37e644b2623`.
Die Dateien und Testbilder bleiben ausschließlich lokal.

## Nachgewiesene Kompatibilitätsfehler

* SRE13 Execute/Resume ließ Schedulerzustände aus. Das originale ARM64-Resume
  bei 0x545624 löscht den Wartezustand bei +0x50 vor lua_resume und setzt den
  Abschluss bei +0x5b, wenn kein LUA_YIELD zurückkommt. Execute tut auf dem
  Coroutine-Pfad bei 0x5456f8 dasselbe. Die geschützte SRE-Grenze erhält diese
  Übergänge jetzt ebenfalls; es werden keine Zeitwerte angepasst.
* Der FBO-Präsentationspfad ließ veränderte Texturbindungen zurück. Caver cached
  Bindungen über Frames hinweg; der Todesbildschirm zeichnet beispielsweise
  weiter, ohne glBindTexture erneut aufzurufen. Derselbe Host-Smoke-Test meldet
  vorher Exit 27 (Unit 0 verloren) und danach Exit 0, einschließlich skalierter
  Ausgabe mit drei Filtern. FrameStats behält die persistente letzte Bindung.
* Die optionale ANGLE/PBR-Übersetzung verarbeitet nur eine Textureinheit und
  zeichnet die mehrstufige Game-Over-Schriftmaske als Rechtecke. Windows startet
  deshalb mit dem klassischen Renderpfad; eine ausdrückliche Grafikeinstellung
  kann diesen weiterhin überschreiben.

## Spieltests und Grenzen

Ohne Computer Use: vorhandenes Pod-IPC, isolierte Profile, native Diagnosen und
Renderer-Captures. Testfigur und Startpositionen sind Test-Fixtures; Originalassets
werden dabei nicht verändert. Durch einen echten Treffer des ersten Schlussbosses
starb die Testfigur. Mit klassischem Renderpfad und erhaltenen Texturbindungen
war Game Over etwa drei Sekunden nach dem letzten Treffer lesbar. Der danach
laufende originale 4,5-Sekunden-Timer wurde nicht verkürzt. Wiederaufnahme beobachtet.

Originaler Intro-Auslöser in worldsend_part9.scene sowohl mit bisheriger als auch
mit korrigierter Skriptgrenze getestet. In diesem kontrollierten Vergleich keine
Lebenspunkte in den ersten acht Sekunden verloren. Das widerlegt die Nutzermeldung
nicht: Angriff während der Einblendung ist noch nicht abschließend reproduziert
oder behoben. Es gibt keine künstliche Unverwundbarkeit, Bossverlangsamung oder
geänderten Spawn-Trigger. Ein konkreter Android-/Speedrun-Vergleich bleibt nötig.

Fünf fokussierte CTests bestehen: Preflight, LP64-/Datei-ABI, Dynarmic einschließlich
Exclusive-Instruktionen, asynchrones IO und ProgramState-Schedulerzustände.
Ein vollständiger Speedrun, jede Bossphase und jede alternative Renderkonfiguration
sind nicht abgenommen.

## Nutzerbestätigung am 19.10.2026

Nach dem Update bestätigt der Nutzer: „der boss funktioniert wieder so wie er
soll und game over funktioniert auch“. Die zuvor gemeldeten beiden Probleme
sind damit im Nutzertest behoben. Originaldateien und Spielwerte bleiben
unverändert; eine unabhängige Speedrun-Zeitgleichheit wurde nicht geprüft.

## Game Over bestätigen – 19.10.2026

Zusätzliche Nutzermeldung: Game Over reagiert weder auf Mausklick noch Tastatur.
Original TouchEnded (1.4.13: 0x4ab86c) fordert tapCount >= 1. Der Client gab bei
Mouse/Finger-Up 0 weiter; die originale JNI-Funktion überträgt diesen Wert exakt
in FWTouch+0x20. Mouse/Finger-Up und internes Pod-Touch behalten jetzt den Tippzähler.

Tastaturbestätigung wird nur bei aktivem GameOverViewController an das originale
GameOverView::HandleKeyboardEvent weitergereicht. Enter verwendet dessen Control-
Aktion, Leertaste dessen Up-/Sprungaktion und Escape dessen Escape-Aktion.
Konfigurierte Sprung-/Angriffsbelegungen bleiben berücksichtigt. Escape wird dabei
nicht zusätzlich als Back an das darunterliegende Gameplay gesendet.

Regression im echten, isolierten Gastspiel ohne Computer Use: bisheriger Client
ignoriert den Tipp; korrigierter Client nimmt SDL-Mausklick, Enter, Leertaste und
Escape an. Die originale Fortsetzen-Flagge und der Controllerwechsel wurden
geprüft, bevor der automatische Timer auslösen konnte. Kein Timer, Spieldaten-
Skript, Bosswert oder originaler Fortsetzen-Handler wird dafür geändert.
