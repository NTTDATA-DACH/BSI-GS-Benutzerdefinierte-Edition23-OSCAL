---
name: bsi-grundschutz-baustein
description: Erstellt und überarbeitet IT-Grundschutz-Bausteine im Format des BSI-IT-Grundschutz-Kompendiums (Edition 2023) sowie für IT-Grundschutz++. Nutze diesen Skill IMMER, wenn ein neuer Baustein, eine Gefährdungslage, Basis-/Standard-Anforderungen oder Anforderungen bei erhöhtem Schutzbedarf, eine Kreuzreferenztabelle, eine Bausteinüberarbeitung für eine neue Edition oder die korrekte BSI-Verbindlichkeitssprache (MUSS/SOLLTE/DARF NICHT) gefragt ist — auch wenn der Begriff "Baustein" nicht ausdrücklich fällt, etwa bei "Grundschutz-Anforderungen formulieren", "Modul fürs Kompendium", "Schicht APP/SYS/NET", "elementare Gefährdungen zuordnen" oder "Sicherheitsanforderungen nach BSI-Systematik". Deckt Struktur, Schicht-/ID-Systematik, Verbindlichkeits-Modalverben, Rollenkatalog, Zuständigkeitsmodell, Schutzziel-Kennzeichnung, Kreuzreferenztabelle und Qualitätssicherung ab.
---

# IT-Grundschutz-Baustein erstellen

**Version 2.0** — Änderungen ggü. 1.0 am Dateiende.

Dieser Skill erzeugt Bausteine, die exakt der Redaktionssystematik des BSI-IT-Grundschutz-Kompendiums (Edition 2023) folgen, damit sie ohne Nacharbeit in das Kompendium, ein Grundschutz-Profil oder ein IT-Grundschutz++-Repository übernommen werden können.

## Zielformat und Pipeline

Primärer Output ist **Markdown** (die übliche Bearbeitungsstufe vor der DOCX-Konvertierung). Für eine formatierte Word-Fassung danach den `docx`-Skill nutzen (Fließtext in Aptos, sonst Calibri). Tabellen als Markdown-Tabellen; die Kreuzreferenztabelle ggf. zusätzlich als separate Datei, falls sie sehr breit wird.

Vor dem Schreiben klären, sofern nicht aus dem Kontext ableitbar: **Schicht und ID** des Bausteins, **abgegrenztes Zielobjekt** und ob es ein **neuer Baustein** oder eine **Editionsüberarbeitung** ist. Wenn der Nutzer das Thema klar benennt, nicht mit Rückfragen aufhalten — eine begründete Annahme treffen und inline kenntlich machen.

## Markdown-Form: Überschriftenebenen (verbindlich)

Damit der Baustein in der DOCX-/OSCAL-Pipeline sauber navigierbar ist, gilt eine feste Ebenenzuordnung:

| Ebene | Inhalt |
|-------|--------|
| `#` (H1) | `<ID> <Name des Bausteins>` |
| `##` (H2) | Kapitel `1 Beschreibung`, `2 Gefährdungslage`, `3 Anforderungen`, `4 Weiterführende Informationen` |
| `###` (H3) | Unterkapitel (`1.1`, `1.2`, `1.3`, `3.1`, `3.2`, `3.3`, `4.1`), jede **Gefährdung** (Titel) und **jede Anforderung** |

**Jede Anforderung ist eine eigene, nicht nummerierte H3-Überschrift** — kein Fettdruck-Absatz, keine Aufzählungs-/Listennummerierung (`1.`, `-`). Die Anforderungs-ID (`.A<Nr>`) steht in der Überschrift, ist aber Teil der ID, keine Listennummer:

```
### APP.4.10.A1 Richtlinie für den sicheren Einsatz von KI (B) [Fachverantwortliche]
Es MUSS eine Richtlinie existieren, die …
```

Die Klassenabschnitte `3.1/3.2/3.3` sind ebenfalls H3; die Anforderungen folgen als H3-Geschwister unmittelbar darunter.

## Vorgehen: erst recherchieren, dann strukturieren

**Schritt 1 — Recherche (verpflichtend, vor dem Schreiben).** Zuerst recherchieren, wie das Zielobjekt nach aktuellem Stand der Technik abzusichern ist — **nicht** aus dem Gedächtnis formulieren. Quellen: Hersteller-Härtungsleitfäden und Security-Baselines, CIS Benchmarks, einschlägige BSI-Dokumente und benachbarte Kompendium-Bausteine, NIST-/ISO-Vorgaben, bekannte Schwachstellen- und Angriffsmuster (CVE/MITRE ATT&CK, bei KI zusätzlich MITRE ATLAS, OWASP-Listen). Websuche nutzen und aktuelle Versionen prüfen. Ergebnis ist eine ungeordnete Sammlung sinnvoller Schutzmaßnahmen samt Quellen — die Rohbasis für Gefährdungslage und Anforderungen. Quellen für 4.1 Wissenswertes festhalten.

**Schritt 2 — Gefährdungslage ableiten.** Aus den recherchierten Bedrohungen die spezifische Gefährdungslage (Kapitel 2) formulieren und die einschlägigen elementaren Gefährdungen (G 0.x) identifizieren — Nummer **und** Titel verbatim aus `references/elementare-gefaehrdungen.md` übernehmen.

**Schritt 3 — Anforderungen klassifizieren und sortieren.** Jede recherchierte Schutzmaßnahme in eine prüfbare Anforderung überführen und einer Klasse zuordnen — **Basis (B)** = unverzichtbares Fundament, **Standard (S)** = Stand der Technik bei normalem Schutzbedarf, **Erhöht (H)** = zusätzliche Beispielmaßnahmen bei erhöhtem Schutzbedarf. Einsortierung in der Reihenfolge 3.1 → 3.2 → 3.3.

**Schritt 4 — Reihenfolge innerhalb jeder Klasse.** In jeder Stufe (B, S, H) stehen **Planungs-Anforderungen am Anfang**, danach entlang des Lebenszyklus: Planung & Konzeption → Beschaffung → Umsetzung/Konfiguration → Betrieb → Notfallvorsorge/Aussonderung.

## Pflichtstruktur eines Bausteins

Diese Reihenfolge ist verbindlich und vollständig zu liefern:

```
[ID] [Name des Bausteins]

1   Beschreibung
1.1 Einleitung
1.2 Zielsetzung
1.3 Abgrenzung und Modellierung
2   Gefährdungslage
3   Anforderungen
    (Einleitung mit Zuständigkeiten)
3.1 Basis-Anforderungen
3.2 Standard-Anforderungen
3.3 Anforderungen bei erhöhtem Schutzbedarf
4   Weiterführende Informationen
4.1 Wissenswertes
    Kreuzreferenztabelle zu elementaren Gefährdungen
```

Befüllbare Vorlage: `references/baustein-vorlage.md` — als Gerüst verwenden.

### 1 Beschreibung
- **1.1 Einleitung**: Zielobjekt, Funktion/Technologie, Sicherheitsrelevanz. Sachlich, herstellerneutral, keine Werbung.
- **1.2 Zielsetzung**: Welches Sicherheitsziel der Baustein verfolgt (Aspekte von Vertraulichkeit, Integrität, Verfügbarkeit für dieses Zielobjekt).
- **1.3 Abgrenzung und Modellierung**: Worauf der Baustein anzuwenden ist, was **nicht** behandelt wird und auf welche anderen Bausteine verwiesen wird. **Querverweise mit korrekter ID UND korrektem Titel** angeben und gegen die Schicht-/ID-Referenz prüfen (`references/schichten-und-ids.md`) — z. B. „sichere Softwareentwicklung → CON.8", nicht CON.1. Falsche Querverweise sind ein häufiger und peinlicher Auditbefund.

### 2 Gefährdungslage
Spezifische Gefährdungen für genau dieses Zielobjekt — **keine** generischen Aussagen, **keine** Maßnahmen (nur Bedrohung, nicht Abhilfe). Jede Gefährdung als kurzer, konkreter Absatz mit eigener H3-Überschrift. Typisch 5–12 Gefährdungen. Jede muss sich später mindestens einer elementaren Gefährdung (G 0.x) zuordnen lassen und in eine Anforderung münden (Traceability in beide Richtungen, siehe Kreuzreferenztabelle).

### 3 Anforderungen
Einleitungsabsatz nennt die **grundsätzlich zuständige Rolle** und listet die Zuständigkeiten in einer kleinen Tabelle:

```
| Zuständigkeiten         | Rollen                                  |
| Grundsätzlich zuständig | <eine Rolle aus dem Rollenkatalog>      |
| Weitere Zuständigkeiten | <weitere Rollen aus dem Rollenkatalog>  |
```

**Rollen ausschließlich aus dem normierten Rollenkatalog** (`references/rollenkatalog.md`). Keine Rollen frei erfinden, keine eigenen Bezeichnungen bilden — das bricht die Mapping-Logik im Grundschutz-Check. Genau **eine** Rolle ist grundsätzlich zuständig. Weicht eine einzelne Anforderung davon ab, wird die abweichende Rolle direkt in der Anforderungs-Überschrift in eckigen Klammern genannt, z. B. `… (B) [Entwickler]`.

**Anforderungsklassen** (Modalverb-Logik und Stil in `references/modalverben-und-stil.md`):
- **3.1 Basis-Anforderungen (B)** — vorrangig zu erfüllen; überwiegend **MUSS / MÜSSEN** und, wo ein Verbot die natürliche Form ist, **DARF NICHT**. Das volle Verbindlichkeitsspektrum nutzen, nicht nur MUSS.
- **3.2 Standard-Anforderungen (S)** — Stand der Technik bei normalem Schutzbedarf; überwiegend **SOLLTE / SOLLTE NICHT**. Eine S-Anforderung enthält **keinen MUSS-Kern** — die Klasse bestimmt das Leitverb.
- **3.3 Anforderungen bei erhöhtem Schutzbedarf (H)** — Beispielcharakter, durch gleichwertige Maßnahmen ersetzbar; überwiegend **SOLLTE**. **Pflicht:** Am Ende **jeder** H-Anforderung den Schutzziel-Bezug in Klammern ausweisen — `(C)`, `(I)`, `(A)` bzw. die zutreffende Kombination (C = Vertraulichkeit, I = Integrität, A = Verfügbarkeit). Diese Kennzeichnung ist verbindlich (Hausregel/++-Attribut für Maschinenlesbarkeit). *Hinweis:* Die Basis-Edition transportiert den Schutzziel-Bezug primär über die Kreuzreferenztabelle; bei strenger Basis-Kompendium-Einreichung die Platzierung gegen die Zieledition prüfen.

### 4 Weiterführende Informationen
- **4.1 Wissenswertes**: Verweise auf einschlägige Normen, BSI-Dokumente (Standards 200-x, andere Bausteine, themenspezifische Leitfäden) und Gremien-/Hersteller-Literatur. Belastbare Quellen, keine Pflicht zur Vollständigkeit. Verwendete Quellen müssen zum gewählten Geltungsbereich passen (z. B. OWASP ML Security Top 10 bei klassischem ML, OWASP Top 10 for LLM Applications bei GenAI).

### Kreuzreferenztabelle
Matrix **Anforderungen × elementare Gefährdungen**: Zeilen = Anforderungen (A1 … An mit Klasse B/S/H), Spalten = die einschlägigen G 0.x; „X" markiert, welche Anforderung welche Gefährdung adressiert. Pflichtregeln:
1. **G-Nummer und -Titel verbatim** aus `references/elementare-gefaehrdungen.md` — niemals Titel umformulieren, niemals Nummern aus dem Gedächtnis vergeben. (Typische Fehler: G 0.18 ist *Fehlplanung oder fehlende Anpassung*, nicht „Diebstahl …" — das ist G 0.16; G 0.20 ist *Informationen oder Produkte aus unzuverlässiger Quelle*.)
2. **Jede Zuordnung muss einzeln begründbar sein.** Eine Anforderung, die in (fast) allen Spalten ein „X" trägt, ist ein Qualitätswarnsignal (Über-Mapping) und wird ausgedünnt.
3. **Lückenlos in beide Richtungen:** Jede Gefährdungs-Spalte hat ≥ 1 „X"; jede Anforderungs-Zeile hat ≥ 1 „X".

## Anforderungen schreiben — die zentralen Regeln

**Verbindlichkeit über Großbuchstaben-Modalverben.** Vollständige Tabelle in `references/modalverben-und-stil.md`; Kurzform:

| Verb | Bedeutung |
|------|-----------|
| MUSS / MÜSSEN, IST/SIND … ZU | uneingeschränkt zu erfüllen |
| DARF NICHT / DÜRFEN NICHT | in keinem Fall zulässig |
| SOLLTE / SOLLTEN | normalerweise zu erfüllen; Abweichung nur begründet |
| SOLLTE NICHT / SOLLTEN NICHT | normalerweise zu unterlassen; Ausnahmen begründen |
| KANN / KÖNNEN | optional |

**Klasse bestimmt das Leitverb.** B → MUSS/DARF NICHT, S → SOLLTE/SOLLTE NICHT, H → SOLLTE (+ Schutzziel-Tag). Verbindlichkeitsgrade nicht in einem Satz mischen; insbesondere kein MUSS in einer S- oder H-Anforderung.

**Eine Anforderung = eine prüfbare Aussage.** Atomar formulieren, sodass im IT-Grundschutz-Check eindeutig „umgesetzt / teilweise / nicht umgesetzt / entbehrlich" beantwortbar ist. Herstellerneutral, technologie- und lösungsoffen (das *Was*, nicht das produktspezifische *Wie*).

**Sprachstil/Duktus.** Nüchtern, administrativ, präzise, passiv-/normlastig. Keine werblichen Aussagen, keine Begründungen oder Erklärungen, *warum* eine Maßnahme gut ist, im normativen Satz — die Maßnahme selbst steht im Fokus. Keine Füllwörter, kein „Plaudern". Details und Negativbeispiel in `references/modalverben-und-stil.md`.

**Reihenfolge je Stufe: Planung zuerst**, danach Beschaffung → Umsetzung → Betrieb → Notfall/Aussonderung.

## ID- und Nummern-Systematik

Schema: `SCHICHT.Gruppe[.Teilbaustein].A<Nr>` — z. B. `APP.4.4.A1`, `SYS.1.6.A12`. Schichten, Vergaberegeln und häufig verwechselte Baustein-IDs (für korrekte Querverweise) in `references/schichten-und-ids.md`.

**Durchlaufende Nummerierung:** Anforderungen werden über alle drei Klassen hinweg fortlaufend nummeriert (A1, A2, A3 …); kein Neustart je Abschnitt. Die Klasse zeigt sich an `(B)/(S)/(H)` und der Abschnittszuordnung.

**Nummernstabilität bei Editionsüberarbeitung:** Gestrichene Anforderungen behalten ihre Nummer als Platzhalter und werden mit **„ENTFALLEN"** markiert. Neue Anforderungen erhalten die nächste freie Nummer am Ende — bestehende werden nicht umnummeriert.

## Überarbeitungsmodus (Editionspflege)

Eine Überarbeitung ist **nicht** bloßes Umformatieren. Wird ein bestehender Baustein überarbeitet, gilt:
1. **Recherche neu durchführen** (Schritt 1) — aktueller Stand der Technik, neue Angriffsmuster, neue Werkzeuge/Normen.
2. **Substantiell erweitern:** zusätzliche **Gefährdungen** und **Anforderungen** aufnehmen, die seit der Vorfassung relevant geworden sind. Neue Anforderungen mit nächster freier Nummer am Ende der jeweiligen Klasse; neue Gefährdungen in Kapitel 2 und in die Kreuzreferenztabelle einarbeiten.
3. **Stabilität wahren:** bestehende IDs nicht umnummerieren; entfallene als ENTFALLEN; Kreuzreferenztabelle vollständig nachziehen.
4. Standarderwartung an eine Überarbeitung ist ein **inhaltlicher Zuwachs**, nicht Parität mit der Vorfassung.

## Qualitätssicherung vor Abgabe

Checkliste in `references/qualitaetscheck.md` vollständig durchgehen. Kernpunkte:
1. Alle Pflichtkapitel (1–4 inkl. Unterkapitel, Zuständigkeiten, Kreuzreferenztabelle) vorhanden.
2. Jede Anforderung als nicht nummerierte H3-Überschrift, atomar, prüfbar, mit klassenkonformem Leitverb (kein MUSS in S/H).
3. Jede H-Anforderung trägt den Schutzziel-Tag (C/I/A).
4. Alle Rollen aus dem Rollenkatalog, korrekt bezeichnet (z. B. Beschaffungsstelle).
5. Gefährdungslage enthält nur Bedrohungen, keine Maßnahmen.
6. Querverweise mit korrekter ID + Titel; keine Doppelregelung.
7. Kreuzreferenztabelle: G-Titel verbatim, Mapping selektiv/begründet, in beide Richtungen lückenlos.
8. ID-Systematik korrekt, Nummern fortlaufend, ENTFALLEN-Platzhalter bei Überarbeitung; bei Überarbeitung Inhalt erweitert.
9. Herstellerneutral, sachlich, BSI-Duktus.

## IT-Grundschutz++ / Maschinenlesbarkeit (optional)

Soll der Baustein zusätzlich maschinenlesbar (OSCAL/Grundschutz++) vorliegen: stabile ID je Anforderung als Schlüssel, Klasse (B/S/H) und Schutzziel-Bezug (C/I/A) als Attribute (der H-Schutzziel-Tag ist hierfür direkt verwertbar), Kreuzreferenz als explizite Relation zu G 0.x. Zielschema projektspezifisch — beim Nutzer erfragen.

## Hinweis zur Edition

Struktur und Systematik folgen der Edition 2023. Da das Kompendium fortlaufend gepflegt wird, redaktionelle Detailkonventionen (Rollenbezeichnungen, Schutzziel-Kennzeichnung, neue Schichtbausteine, Kreuzreferenz-Konventionen) gegen die jeweils aktuelle Edition gegenprüfen, bevor ein Baustein final eingereicht wird.

---

## Änderungshistorie

- **2.0** — Rollen nur noch aus normiertem Katalog (`references/rollenkatalog.md`; korrekte Bezeichnung „Beschaffungsstelle"). Schutzziel-Tag (C/I/A) bei **jeder** H-Anforderung verpflichtend. Jede Anforderung als nicht nummerierte H3-Überschrift. Verbindliche Überschriften-Ebenen ergänzt. Kreuzreferenztabelle: G-Titel/-Nummern verbatim aus Referenz, Über-Mapping verboten. Querverweis-Korrektheit (ID + Titel) erzwungen, häufig verwechselte IDs ergänzt. Cross-Class-Verbindlichkeit (kein MUSS in S/H) geschärft. BSI-Duktus als explizite Stilregel. Überarbeitungsmodus: inhaltliche Erweiterung (zusätzliche Gefährdungen/Anforderungen) verpflichtend.
- **1.0** — Erstfassung.
