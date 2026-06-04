# Qualitätssicherung – Checkliste vor Abgabe

## Struktur & Form
- [ ] Kopfzeile (H1) mit korrekter ID und Name.
- [ ] Kapitel 1 mit 1.1 Einleitung, 1.2 Zielsetzung, 1.3 Abgrenzung und Modellierung.
- [ ] Kapitel 2 Gefährdungslage vorhanden (5–12 spezifische Gefährdungen).
- [ ] Kapitel 3 mit Zuständigkeits-Einleitung, Zuständigkeitstabelle, 3.1/3.2/3.3.
- [ ] Kapitel 4 mit 4.1 Wissenswertes.
- [ ] Kreuzreferenztabelle vorhanden.
- [ ] **Überschriften-Ebenen korrekt:** Kapitel = `##`; Unterkapitel, Gefährdungen und jede Anforderung = `###`.
- [ ] **Jede Anforderung ist eine nicht nummerierte H3-Überschrift** (kein Fettdruck-Absatz, keine Listennummerierung).

## Anforderungen
- [ ] Jede Anforderung ist atomar und prüfbar (eindeutige Soll-Ist-Bewertung möglich).
- [ ] Klassenkonformes Leitverb: B → MUSS/DARF NICHT; S → SOLLTE/SOLLTE NICHT; H → SOLLTE.
- [ ] **Kein MUSS-Kern in einer S- oder H-Anforderung**; kein Mischen von Verbindlichkeitsgraden in einem Satz.
- [ ] Basis-Anforderungen nutzen das volle Spektrum inkl. **DARF NICHT**, wo ein Verbot die natürliche Form ist.
- [ ] **Jede H-Anforderung trägt am Ende den Schutzziel-Tag** (C / I / A bzw. Kombination).
- [ ] Lösungsoffen/herstellerneutral; keine produktspezifischen Pflicht-Konfigurationen.
- [ ] In jeder Klasse (B/S/H) steht eine Planungs-/Konzeptionsanforderung am Anfang; danach Lebenszyklus-Reihenfolge.
- [ ] Recherche vor dem Schreiben durchgeführt; Anforderungen leiten sich aus belegten Schutzmaßnahmen ab (Quellen in 4.1).

## Rollen
- [ ] Alle Rollen stammen aus dem normierten **Rollenkatalog** (references/rollenkatalog.md); keine erfundenen Rollen.
- [ ] Korrekte Bezeichnungen (z. B. **Beschaffungsstelle**, nicht „Beschaffer").
- [ ] Genau eine Rolle „Grundsätzlich zuständig"; abweichende Zuständigkeit in eckigen Klammern in der Anforderungsüberschrift.

## Nummerierung & ID
- [ ] ID-Systematik korrekt (Schicht/Gruppe/Teilbaustein).
- [ ] Anforderungsnummern fortlaufend über alle Klassen (kein Neustart je Abschnitt).
- [ ] Bei Editionsüberarbeitung: gestrichene Anforderungen als „ENTFALLEN" mit erhaltener Nummer; keine Umnummerierung bestehender.
- [ ] **Bei Überarbeitung:** zusätzliche Gefährdungen/Anforderungen nach aktuellem Stand der Technik aufgenommen (inhaltlicher Zuwachs, nicht nur Reformatierung).

## Gefährdungslage
- [ ] Nur Bedrohungen beschrieben, keine Maßnahmen/Abhilfen.
- [ ] Spezifisch für das Zielobjekt, nicht generisch.
- [ ] Jede Gefährdung mindestens einer elementaren Gefährdung (G 0.x) zuordenbar UND in mindestens einer Anforderung adressiert (Traceability beidseitig).

## Abgrenzung & Querverweise
- [ ] 1.3 verweist auf angrenzende Bausteine; keine Doppelregelung.
- [ ] **Querverweise mit korrekter ID UND korrektem Titel** (gegen references/schichten-und-ids.md geprüft) — z. B. CON.8 ≠ CON.1, APP.1.1 = Office-Produkte.

## Kreuzreferenztabelle
- [ ] Nur einschlägige elementare Gefährdungen als Spalten.
- [ ] **G-Nummern und -Titel verbatim** aus references/elementare-gefaehrdungen.md (nicht umformuliert, nicht aus dem Gedächtnis vergeben).
- [ ] **Keine „X-überall"-Zeile**; jede Zuordnung einzeln begründbar (kein Über-Mapping).
- [ ] Jede Gefährdungs-Spalte von mindestens einer Anforderung abgedeckt.
- [ ] Jede Anforderungs-Zeile adressiert mindestens eine Gefährdung.

## Sprache & Form
- [ ] Nüchterner, administrativer BSI-Duktus; keine Werbung, keine Füllwörter, keine Begründung im normativen Satz.
- [ ] Konsistente Terminologie über den ganzen Baustein.
- [ ] Edition-Konventionen (Rollen, Schutzziel-Kennzeichnung) gegen die aktuelle Kompendium-Edition gegengeprüft.

## Mapping/Interoperabilität (falls gefordert)
- [ ] ISO-27001-Bezug bzw. weiteres Framework-Mapping geprüft.
- [ ] Bei IT-Grundschutz++: stabile IDs als Schlüssel, Klasse + Schutzziel (C/I/A aus H-Tag) als Attribute, G-0.x-Relationen explizit.
