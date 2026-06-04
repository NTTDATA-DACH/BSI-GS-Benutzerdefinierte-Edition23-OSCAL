# Verbindlichkeit, Modalverben und Redaktionsstil

## Verbindlichkeits-Modalverben (Großbuchstaben)

In Großbuchstaben gesetzte Verben zeigen die Verbindlichkeit einer Anforderung. Maßgeblich ist die Schreibung in Versalien — dasselbe Wort in normaler Schreibung trägt **keine** normative Bedeutung.

| Formulierung | Verbindlichkeit |
|--------------|-----------------|
| MUSS / MÜSSEN; IST … ZU / SIND … ZU | Diese Anforderung muss unbedingt erfüllt werden. |
| DARF NICHT / DÜRFEN NICHT | Was hier beschrieben wird, darf in keinem Fall geschehen. |
| SOLLTE / SOLLTEN | Sollte normalerweise erfüllt werden; Abweichung nur in begründeten, dokumentierten Ausnahmefällen (Risikomanagement). |
| SOLLTE NICHT / SOLLTEN NICHT | Normalerweise zu unterlassen; Ausnahmen begründen und dokumentieren. |
| KANN / KÖNNEN | Optionale Empfehlung ohne Verbindlichkeit. |

## Zuordnung Modalverb ↔ Anforderungsklasse (Klasse bestimmt das Leitverb)

- **3.1 Basis (B):** vorrangig und uneingeschränkt → überwiegend **MUSS / MÜSSEN**; wo ein Verbot die natürliche Form ist, **DARF NICHT**. Das volle Spektrum nutzen — nicht reflexhaft nur MUSS. SOLLTE ist hier untypisch.
- **3.2 Standard (S):** Stand der Technik bei normalem Schutzbedarf → überwiegend **SOLLTE / SOLLTE NICHT**. Eine S-Anforderung enthält **keinen MUSS-Kern**. (Häufiger Fehler: „Es MUSS jederzeit nachvollziehbar sein …" in einer (S)-Anforderung — das ist ein Verbindlichkeitskonflikt. Korrekt: „Es SOLLTE nachvollziehbar dokumentiert sein …".)
- **3.3 Erhöht (H):** Beispielcharakter, ersetzbar → überwiegend **SOLLTE**. **Pflicht:** am Ende jeder H-Anforderung den Schutzziel-Bezug in Klammern ausweisen: `(C)`, `(I)`, `(A)` bzw. Kombination (C = Vertraulichkeit, I = Integrität, A = Verfügbarkeit). Kein MUSS in einer H-Anforderung.

## Stilregeln für Anforderungstexte (BSI-Duktus)

1. **Atomar & prüfbar.** Eine Anforderung = eine eindeutig prüfbare Aussage („umgesetzt / teilweise / nicht umgesetzt / entbehrlich" muss eindeutig beantwortbar sein).
2. **Genau ein Verbindlichkeitsgrad pro Aussage.** Nicht MUSS und SOLLTE in einem Satz mischen; mehrere Pflichten auf mehrere Anforderungen aufteilen.
3. **Lösungsoffen & herstellerneutral.** Das *Was* (Schutzziel/Ergebnis) fordern, nicht ein produktspezifisches *Wie*. Konfigurationen, Tools und Schritt-für-Schritt-Anleitungen gehören in separate Umsetzungshinweise.
4. **Nüchtern, administrativ, präzise, normlastig.** Sachlicher Verwaltungsduktus, passivische/normative Formulierung. **Keine werblichen Aussagen, keine Füllwörter, kein „Plaudern".** Im normativen Satz **keine Begründung**, *warum* die Maßnahme gut ist — die Maßnahme selbst steht im Fokus (Begründendes ggf. knapp in den erläuternden Abschnittsvorspann, nicht in die Anforderung).
5. **Aktiv-eindeutiges Pflichtsubjekt.** Wer die Pflicht trägt, muss erkennbar sein; vage „und/oder"-Ketten und Schachtelsätze vermeiden.
6. **Rolle aus dem Katalog.** Abweichende Zuständigkeit in eckigen Klammern in der Anforderungsüberschrift, ausschließlich Rollen aus `rollenkatalog.md`.

## Beispiele

**Gut (Basis, MUSS, atomar, lösungsoffen):**
```
### SYS.1.6.A4 Verwendung sicherer Images (B)
Es MÜSSEN ausschließlich Images verwendet werden, deren Herkunft und
Integrität nachprüfbar sind.
```

**Gut (erhöht, SOLLTE, mit Pflicht-Schutzziel-Tag):**
```
### APP.4.10.A13 Nutzung von Privacy-Enhancing Technologies (H) [Entwickler]
Beim Training mit personenbezogenen Daten oder Geschäftsgeheimnissen SOLLTEN
PETs (z. B. Differential Privacy, Federated Learning) eingesetzt werden. (C)
```

**Schlecht (vermischt zwei Verbindlichkeiten und nennt ein konkretes Produkt):**
```
Es MUSS Docker Content Trust aktiviert und es SOLLTE zusätzlich ein
Scanner eingesetzt werden.
```
→ aufteilen: eine MUSS-Anforderung „Integrität der Images sicherstellen" (lösungsoffen) und eine SOLLTE-Anforderung „regelmäßiges Schwachstellen-Scanning".

**Schlecht (werblicher/erklärender Duktus):**
```
Mit einem modernen, leistungsstarken SIEM lassen sich Angriffe bequem und
zuverlässig erkennen, was die Sicherheit deutlich erhöht.
```
→ nüchtern und normativ: „Sicherheitsrelevante Ereignisse SOLLTEN zentral protokolliert und auf Angriffsmuster ausgewertet werden."
