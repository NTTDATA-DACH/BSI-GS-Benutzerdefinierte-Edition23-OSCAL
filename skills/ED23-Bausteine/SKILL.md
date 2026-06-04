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

**Schritt 2 — Gefährdungslage ableiten.** Aus den recherchierten Bedrohungen die spezifische Gefährdungslage (Kapitel 2) formulieren und die einschlägigen elementaren Gefährdungen (G 0.x) identifizieren — Nummer **und** Titel verbatim aus `references/elementare-gefaehrdungen` übernehmen.

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

Befüllbare Vorlage: `references/baustein-vorlage` — als Gerüst verwenden.

### 1 Beschreibung
- **1.1 Einleitung**: Zielobjekt, Funktion/Technologie, Sicherheitsrelevanz. Sachlich, herstellerneutral, keine Werbung.
- **1.2 Zielsetzung**: Welches Sicherheitsziel der Baustein verfolgt (Aspekte von Vertraulichkeit, Integrität, Verfügbarkeit für dieses Zielobjekt).
- **1.3 Abgrenzung und Modellierung**: Worauf der Baustein anzuwenden ist, was **nicht** behandelt wird und auf welche anderen Bausteine verwiesen wird. **Querverweise mit korrekter ID UND korrektem Titel** angeben und gegen die Schicht-/ID-Referenz prüfen (`references/schichten-und-ids`) — z. B. „sichere Softwareentwicklung → CON.8", nicht CON.1. Falsche Querverweise sind ein häufiger und peinlicher Auditbefund.

### 2 Gefährdungslage
Spezifische Gefährdungen für genau dieses Zielobjekt — **keine** generischen Aussagen, **keine** Maßnahmen (nur Bedrohung, nicht Abhilfe). Jede Gefährdung als kurzer, konkreter Absatz mit eigener H3-Überschrift. Typisch 5–12 Gefährdungen. Jede muss sich später mindestens einer elementaren Gefährdung (G 0.x) zuordnen lassen und in eine Anforderung münden (Traceability in beide Richtungen, siehe Kreuzreferenztabelle).

### 3 Anforderungen
Einleitungsabsatz nennt die **grundsätzlich zuständige Rolle** und listet die Zuständigkeiten in einer kleinen Tabelle:

```
| Zuständigkeiten         | Rollen                                  |
| Grundsätzlich zuständig | <eine Rolle aus dem Rollenkatalog>      |
| Weitere Zuständigkeiten | <weitere Rollen aus dem Rollenkatalog>  |
```

**Rollen ausschließlich aus dem normierten Rollenkatalog** (`references/rollenkatalog`). Keine Rollen frei erfinden, keine eigenen Bezeichnungen bilden — das bricht die Mapping-Logik im Grundschutz-Check. Genau **eine** Rolle ist grundsätzlich zuständig. Weicht eine einzelne Anforderung davon ab, wird die abweichende Rolle direkt in der Anforderungs-Überschrift in eckigen Klammern genannt, z. B. `… (B) [Entwickler]`.

**Anforderungsklassen** (Modalverb-Logik und Stil in `references/modalverben-und-stil`):
- **3.1 Basis-Anforderungen (B)** — vorrangig zu erfüllen; überwiegend **MUSS / MÜSSEN** und, wo ein Verbot die natürliche Form ist, **DARF NICHT**. Das volle Verbindlichkeitsspektrum nutzen, nicht nur MUSS.
- **3.2 Standard-Anforderungen (S)** — Stand der Technik bei normalem Schutzbedarf; überwiegend **SOLLTE / SOLLTE NICHT**. Eine S-Anforderung enthält **keinen MUSS-Kern** — die Klasse bestimmt das Leitverb.
- **3.3 Anforderungen bei erhöhtem Schutzbedarf (H)** — Beispielcharakter, durch gleichwertige Maßnahmen ersetzbar; überwiegend **SOLLTE**. **Pflicht:** Am Ende **jeder** H-Anforderung den Schutzziel-Bezug in Klammern ausweisen — `(C)`, `(I)`, `(A)` bzw. die zutreffende Kombination (C = Vertraulichkeit, I = Integrität, A = Verfügbarkeit). Diese Kennzeichnung ist verbindlich (Hausregel/++-Attribut für Maschinenlesbarkeit). *Hinweis:* Die Basis-Edition transportiert den Schutzziel-Bezug primär über die Kreuzreferenztabelle; bei strenger Basis-Kompendium-Einreichung die Platzierung gegen die Zieledition prüfen.

### 4 Weiterführende Informationen
- **4.1 Wissenswertes**: Verweise auf einschlägige Normen, BSI-Dokumente (Standards 200-x, andere Bausteine, themenspezifische Leitfäden) und Gremien-/Hersteller-Literatur. Belastbare Quellen, keine Pflicht zur Vollständigkeit. Verwendete Quellen müssen zum gewählten Geltungsbereich passen (z. B. OWASP ML Security Top 10 bei klassischem ML, OWASP Top 10 for LLM Applications bei GenAI).

### Kreuzreferenztabelle
Matrix **Anforderungen × elementare Gefährdungen**: Zeilen = Anforderungen (A1 … An mit Klasse B/S/H), Spalten = die einschlägigen G 0.x; „X" markiert, welche Anforderung welche Gefährdung adressiert. Pflichtregeln:
1. **G-Nummer und -Titel verbatim** aus `references/elementare-gefaehrdungen` — niemals Titel umformulieren, niemals Nummern aus dem Gedächtnis vergeben. (Typische Fehler: G 0.18 ist *Fehlplanung oder fehlende Anpassung*, nicht „Diebstahl …" — das ist G 0.16; G 0.20 ist *Informationen oder Produkte aus unzuverlässiger Quelle*.)
2. **Jede Zuordnung muss einzeln begründbar sein.** Eine Anforderung, die in (fast) allen Spalten ein „X" trägt, ist ein Qualitätswarnsignal (Über-Mapping) und wird ausgedünnt.
3. **Lückenlos in beide Richtungen:** Jede Gefährdungs-Spalte hat ≥ 1 „X"; jede Anforderungs-Zeile hat ≥ 1 „X".

## Anforderungen schreiben — die zentralen Regeln

**Verbindlichkeit über Großbuchstaben-Modalverben.** Vollständige Tabelle in `references/modalverben-und-stil`; Kurzform:

| Verb | Bedeutung |
|------|-----------|
| MUSS / MÜSSEN, IST/SIND … ZU | uneingeschränkt zu erfüllen |
| DARF NICHT / DÜRFEN NICHT | in keinem Fall zulässig |
| SOLLTE / SOLLTEN | normalerweise zu erfüllen; Abweichung nur begründet |
| SOLLTE NICHT / SOLLTEN NICHT | normalerweise zu unterlassen; Ausnahmen begründen |
| KANN / KÖNNEN | optional |

**Klasse bestimmt das Leitverb.** B → MUSS/DARF NICHT, S → SOLLTE/SOLLTE NICHT, H → SOLLTE (+ Schutzziel-Tag). Verbindlichkeitsgrade nicht in einem Satz mischen; insbesondere kein MUSS in einer S- oder H-Anforderung.

**Eine Anforderung = eine prüfbare Aussage.** Atomar formulieren, sodass im IT-Grundschutz-Check eindeutig „umgesetzt / teilweise / nicht umgesetzt / entbehrlich" beantwortbar ist. Herstellerneutral, technologie- und lösungsoffen (das *Was*, nicht das produktspezifische *Wie*).

**Sprachstil/Duktus.** Nüchtern, administrativ, präzise, passiv-/normlastig. Keine werblichen Aussagen, keine Begründungen oder Erklärungen, *warum* eine Maßnahme gut ist, im normativen Satz — die Maßnahme selbst steht im Fokus. Keine Füllwörter, kein „Plaudern". Details und Negativbeispiel in `references/modalverben-und-stil`.

**Reihenfolge je Stufe: Planung zuerst**, danach Beschaffung → Umsetzung → Betrieb → Notfall/Aussonderung.

## ID- und Nummern-Systematik

Schema: `SCHICHT.Gruppe[.Teilbaustein].A<Nr>` — z. B. `APP.4.4.A1`, `SYS.1.6.A12`. Schichten, Vergaberegeln und häufig verwechselte Baustein-IDs (für korrekte Querverweise) in `references/schichten-und-ids`.

**Durchlaufende Nummerierung:** Anforderungen werden über alle drei Klassen hinweg fortlaufend nummeriert (A1, A2, A3 …); kein Neustart je Abschnitt. Die Klasse zeigt sich an `(B)/(S)/(H)` und der Abschnittszuordnung.

**Nummernstabilität bei Editionsüberarbeitung:** Gestrichene Anforderungen behalten ihre Nummer als Platzhalter und werden mit **„ENTFALLEN"** markiert. Neue Anforderungen erhalten die nächste freie Nummer am Ende — bestehende werden nicht umnummeriert.

## Überarbeitungsmodus (Editionspflege)

Eine Überarbeitung ist **nicht** bloßes Umformatieren. Wird ein bestehender Baustein überarbeitet, gilt:
1. **Recherche neu durchführen** (Schritt 1) — aktueller Stand der Technik, neue Angriffsmuster, neue Werkzeuge/Normen.
2. **Substantiell erweitern:** zusätzliche **Gefährdungen** und **Anforderungen** aufnehmen, die seit der Vorfassung relevant geworden sind. Neue Anforderungen mit nächster freier Nummer am Ende der jeweiligen Klasse; neue Gefährdungen in Kapitel 2 und in die Kreuzreferenztabelle einarbeiten.
3. **Stabilität wahren:** bestehende IDs nicht umnummerieren; entfallene als ENTFALLEN; Kreuzreferenztabelle vollständig nachziehen.
4. Standarderwartung an eine Überarbeitung ist ein **inhaltlicher Zuwachs**, nicht Parität mit der Vorfassung.

## Qualitätssicherung vor Abgabe

Checkliste in `references/qualitaetscheck` vollständig durchgehen. Kernpunkte:
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

- **2.0** — Rollen nur noch aus normiertem Katalog (`references/rollenkatalog`; korrekte Bezeichnung „Beschaffungsstelle"). Schutzziel-Tag (C/I/A) bei **jeder** H-Anforderung verpflichtend. Jede Anforderung als nicht nummerierte H3-Überschrift. Verbindliche Überschriften-Ebenen ergänzt. Kreuzreferenztabelle: G-Titel/-Nummern verbatim aus Referenz, Über-Mapping verboten. Querverweis-Korrektheit (ID + Titel) erzwungen, häufig verwechselte IDs ergänzt. Cross-Class-Verbindlichkeit (kein MUSS in S/H) geschärft. BSI-Duktus als explizite Stilregel. Überarbeitungsmodus: inhaltliche Erweiterung (zusätzliche Gefährdungen/Anforderungen) verpflichtend.
- **1.0** — Erstfassung.

# references/baustein-vorlage

# references/baustein-vorlage
# Baustein-Vorlage (Gerüst zum Befüllen)

Platzhalter in `<…>` ersetzen. Struktur 1:1 als Markdown-Gerüst übernehmen. **Überschriften-Ebenen beachten:** Kapitel = `##`, Unterkapitel/Gefährdungen/**Anforderungen** = `###` (Anforderungen sind nicht nummerierte H3-Überschriften, keine Listenpunkte).

---

# <ID> <Name des Bausteins>

## 1 Beschreibung

### 1.1 Einleitung
<Zielobjekt, Technologie/Funktion, Sicherheitsrelevanz. Herstellerneutral.>

### 1.2 Zielsetzung
<Sicherheitsziel des Bausteins; welche Aspekte von Vertraulichkeit, Integrität, Verfügbarkeit im Vordergrund stehen.>

### 1.3 Abgrenzung und Modellierung
<Worauf der Baustein anzuwenden ist; was NICHT behandelt wird; Querverweise auf angrenzende Bausteine mit korrekter ID UND korrektem Titel, z. B. „sichere Softwareentwicklung → CON.8 Software-Entwicklung", „Cloud-Bezug → OPS.2.2 Cloud-Nutzung", „Betriebssystem-Härtung → SYS.1.1 Allgemeiner Server". IDs gegen references/schichten-und-ids prüfen.>

## 2 Gefährdungslage
<Einleitungssatz: für dieses Zielobjekt sind folgende spezifische Gefährdungen von besonderer Bedeutung.>

### <Gefährdung 1 – Titel>
<Konkrete Bedrohung, keine Maßnahme.>

### <Gefährdung 2 – Titel>
<…>

<… 5–12 Gefährdungen; jede muss in mind. eine Anforderung münden und sich einer G 0.x zuordnen lassen …>

## 3 Anforderungen
Im Folgenden sind die spezifischen Anforderungen des Bausteins <ID> aufgeführt. Grundsätzlich ist <Rolle aus rollenkatalog> für die Erfüllung der Anforderungen zuständig. Abweichungen werden in den entsprechenden Anforderungen gesondert genannt.

| Zuständigkeiten | Rollen |
|-----------------|--------|
| Grundsätzlich zuständig | <z. B. IT-Betrieb> |
| Weitere Zuständigkeiten | <z. B. Fachverantwortliche, Entwickler, Beschaffungsstelle> |

### 3.1 Basis-Anforderungen
Die folgenden Anforderungen MÜSSEN vorrangig erfüllt werden.

### <ID>.A1 Planung <des Einsatzes / der Separierung / …> (B) [optional: abweichende Rolle]
<Planungs-/Konzeptionsanforderung – steht am Anfang der Stufe. Text mit MUSS.>

### <ID>.A2 <Titel> (B)
<Weitere Basis-Anforderung entlang des Lebenszyklus (Beschaffung → Umsetzung → Betrieb → Notfall). MUSS / DARF NICHT.>

### 3.2 Standard-Anforderungen
Gemeinsam mit den Basis-Anforderungen entsprechen die folgenden Anforderungen dem Stand der Technik bei normalem Schutzbedarf. Sie SOLLTEN grundsätzlich erfüllt werden.

### <ID>.A<n> Planung / Konzeption <…> (S)
<Sofern auf Standard-Niveau einschlägig: Planung zuerst. Text mit SOLLTE — kein MUSS-Kern.>

### <ID>.A<n> <Titel> (S) [optional: abweichende Rolle]
<Text mit SOLLTE / SOLLTE NICHT, Lebenszyklus-Reihenfolge.>

### 3.3 Anforderungen bei erhöhtem Schutzbedarf
Die folgenden Anforderungen sind exemplarisch und bei erhöhtem Schutzbedarf zu berücksichtigen; die konkrete Festlegung erfolgt im Rahmen einer Risikoanalyse. Der Schutzziel-Bezug ist am Ende jeder Anforderung in Klammern angegeben (C = Vertraulichkeit, I = Integrität, A = Verfügbarkeit).

### <ID>.A<n> Planung / Konzeption <…> bei erhöhtem Schutzbedarf (H)
<Sofern einschlägig: Planung zuerst. Text SOLLTE … (C, I, A)>

### <ID>.A<n> <Titel> (H) [optional: abweichende Rolle]
<Text, überwiegend SOLLTE; am Satzende Schutzziel-Tag, z. B. (C, I)>

## 4 Weiterführende Informationen

### 4.1 Wissenswertes
<Verweise auf Normen, BSI-Standards 200-x, themenspezifische BSI-Leitfäden, einschlägige Literatur und angrenzende Bausteine. Quellen passend zum Geltungsbereich.>

## Kreuzreferenztabelle zu elementaren Gefährdungen
<Einleitungssatz + Liste der relevanten elementaren Gefährdungen mit Nummer UND Titel, verbatim aus elementare-gefaehrdungen.>

Spalten = relevante elementare Gefährdungen (nur die einschlägigen, in der Praxis meist 8–20); Zeilen = Anforderungen mit Klasse. „X" markiert die Zuordnung — jede Zuordnung einzeln begründbar (keine „X-überall"-Zeile).

| Anforderung | G 0.<a> | G 0.<b> | G 0.<c> | … |
|-------------|:------:|:------:|:------:|:--:|
| <ID>.A1 (B) | X |  | X | |
| <ID>.A2 (B) |  | X |  | |
| <ID>.A<n> (S) | | X | X | |
| <ID>.A<n> (H) | X | | | |

Prüfen: Jede Spalte (Gefährdung) hat mindestens ein „X"; jede Zeile (Anforderung) hat mindestens ein „X".

# references/elementare-gefaehrdungen
# Elementare Gefährdungen (G 0.1 – G 0.47)

Das BSI definiert 47 elementare Gefährdungen. Sie sind herstellerneutral, produkt- und technikunabhängig formuliert und bilden die Bezugsbasis für die Kreuzreferenztabelle jedes Bausteins. In der Gefährdungslage (Kapitel 2) werden die *spezifischen* Bedrohungen des Zielobjekts beschrieben; in der Kreuzreferenztabelle werden die Anforderungen den hier gelisteten elementaren Gefährdungen zugeordnet.

Stand: Edition 2023. Vor dem finalen Mapping gegen die aktuelle Edition gegenprüfen.

> **Verbindliche Nutzung (Pflicht).** Für die Kreuzreferenztabelle Nummer **und** Titel jeder elementaren Gefährdung **verbatim** aus dieser Tabelle übernehmen. Titel niemals umformulieren oder paraphrasieren; Nummern niemals aus dem Gedächtnis vergeben. Typische Fehlerquellen: G 0.16 (Diebstahl …) vs. G 0.18 (Fehlplanung oder fehlende Anpassung); G 0.19 (Offenlegung schützenswerter Informationen) vs. G 0.20 (Informationen oder Produkte aus unzuverlässiger Quelle); für KI/ML häufig einschlägig: G 0.14, G 0.19, G 0.20, G 0.22, G 0.28, G 0.39, G 0.40, G 0.45, G 0.46.


| ID | Elementare Gefährdung |
|------|-----------------------|
| G 0.1 | Feuer |
| G 0.2 | Ungünstige klimatische Bedingungen |
| G 0.3 | Wasser |
| G 0.4 | Verschmutzung, Staub, Korrosion |
| G 0.5 | Naturkatastrophen |
| G 0.6 | Katastrophen im Umfeld |
| G 0.7 | Großereignisse im Umfeld |
| G 0.8 | Ausfall oder Störung der Stromversorgung |
| G 0.9 | Ausfall oder Störung von Kommunikationsnetzen |
| G 0.10 | Ausfall oder Störung von Versorgungsnetzen |
| G 0.11 | Ausfall oder Störung von Dienstleistern |
| G 0.12 | Elektromagnetische Störstrahlung |
| G 0.13 | Abfangen kompromittierender Strahlung |
| G 0.14 | Ausspähen von Informationen (Spionage) |
| G 0.15 | Abhören |
| G 0.16 | Diebstahl von Geräten, Datenträgern oder Dokumenten |
| G 0.17 | Verlust von Geräten, Datenträgern oder Dokumenten |
| G 0.18 | Fehlplanung oder fehlende Anpassung |
| G 0.19 | Offenlegung schützenswerter Informationen |
| G 0.20 | Informationen oder Produkte aus unzuverlässiger Quelle |
| G 0.21 | Manipulation von Hard- oder Software |
| G 0.22 | Manipulation von Informationen |
| G 0.23 | Unbefugtes Eindringen in IT-Systeme |
| G 0.24 | Zerstörung von Geräten oder Datenträgern |
| G 0.25 | Ausfall von Geräten oder Systemen |
| G 0.26 | Fehlfunktion von Geräten oder Systemen |
| G 0.27 | Ressourcenmangel |
| G 0.28 | Software-Schwachstellen oder -Fehler |
| G 0.29 | Verstoß gegen Gesetze oder Regelungen |
| G 0.30 | Unberechtigte Nutzung oder Administration von Geräten und Systemen |
| G 0.31 | Fehlerhafte Nutzung oder Administration von Geräten und Systemen |
| G 0.32 | Missbrauch von Berechtigungen |
| G 0.33 | Personalausfall |
| G 0.34 | Anschlag |
| G 0.35 | Nötigung, Erpressung oder Korruption |
| G 0.36 | Identitätsdiebstahl |
| G 0.37 | Abstreiten von Handlungen |
| G 0.38 | Missbrauch personenbezogener Daten |
| G 0.39 | Schadprogramme |
| G 0.40 | Verhinderung von Diensten (Denial of Service) |
| G 0.41 | Sabotage |
| G 0.42 | Social Engineering |
| G 0.43 | Einspielen von Nachrichten |
| G 0.44 | Unbefugtes Eindringen in Räumlichkeiten |
| G 0.45 | Datenverlust |
| G 0.46 | Integritätsverlust schützenswerter Informationen |
| G 0.47 | Schädliche Seiteneffekte IT-gestützter Angriffe |

## Auswahl für einen Baustein

- Nur die elementaren Gefährdungen aufnehmen, die für das Zielobjekt **tatsächlich** relevant sind (in der Praxis meist 8–20).
- Infrastruktur-/Umweltgefährdungen (G 0.1–G 0.12) sind für reine Anwendungs-/Prozessbausteine oft nicht einschlägig und werden dann an die zuständigen INF-/Prozessbausteine abgegrenzt.
- Jede in Kapitel 2 beschriebene spezifische Gefährdung sollte sich genau einer oder mehreren elementaren Gefährdungen zuordnen lassen; passt nichts, ist die Bedrohung evtl. außerhalb des Geltungsbereichs.

# references/modalverben-und-stil
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
6. **Rolle aus dem Katalog.** Abweichende Zuständigkeit in eckigen Klammern in der Anforderungsüberschrift, ausschließlich Rollen aus `rollenkatalog`.

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

# references/qualitaetscheck
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
- [ ] Alle Rollen stammen aus dem normierten **Rollenkatalog** (references/rollenkatalog); keine erfundenen Rollen.
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
- [ ] **Querverweise mit korrekter ID UND korrektem Titel** (gegen references/schichten-und-ids geprüft) — z. B. CON.8 ≠ CON.1, APP.1.1 = Office-Produkte.

## Kreuzreferenztabelle
- [ ] Nur einschlägige elementare Gefährdungen als Spalten.
- [ ] **G-Nummern und -Titel verbatim** aus references/elementare-gefaehrdungen (nicht umformuliert, nicht aus dem Gedächtnis vergeben).
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

# references/rollenkatalog
# Rollenkatalog (verbindliche Allowlist)

Das BSI-IT-Grundschutz-Kompendium arbeitet mit einem **normierten Rollenkatalog**. In Bausteinen (Zuständigkeitstabelle und abweichende Rollen in eckigen Klammern) dürfen **ausschließlich** diese standardisierten Rollen verwendet werden. **Keine eigenen Rollen erfinden** und keine freien Bezeichnungen bilden — sonst bricht die Mapping-/Zuständigkeitslogik im IT-Grundschutz-Check und in nachgelagerten Mappings.

Genau **eine** Rolle ist je Baustein „Grundsätzlich zuständig"; alles andere sind „Weitere Zuständigkeiten" bzw. anforderungsspezifische Abweichungen.

## Häufig in APP-/SYS-/NET-Bausteinen verwendete Rollen

| Rolle | Kurzbeschreibung |
|-------|------------------|
| Institutionsleitung | Oberste Leitungsebene; trägt Gesamtverantwortung für Informationssicherheit. |
| Informationssicherheitsbeauftragter (ISB) | Steuert das ISMS, erstellt/fortschreibt Richtlinien, sensibilisiert. |
| Fachverantwortliche | Inhaltlich für einen oder mehrere Geschäftsprozesse/Fachverfahren zuständig (fasst weitere Rollen wie Änderungs-/Archivverwaltung zusammen). |
| IT-Betrieb | Plant, konfiguriert, betreibt und wartet IT-Systeme/-Dienste. |
| Entwickler | Konzipiert und implementiert Software/Konfigurationen. |
| Planer | Plant Architektur/Einführung von Systemen und Diensten. |
| Benutzer | Nutzende der Systeme/Anwendungen. |
| Beschaffungsstelle | Initiiert und überwacht Beschaffungen (öffentliche Vergabe inkl.); schließt die zuständige Leitung mit ein. **Korrekte Bezeichnung — nicht „Beschaffer".** |

## Weitere normierte Rollen (je nach Schicht/Thema)

| Rolle | Kurzbeschreibung |
|-------|------------------|
| Vorgesetzte | Disziplinarische/fachliche Führungsverantwortung. |
| Personalabteilung | Personelle Maßnahmen (Ein-/Austritt, Verpflichtungen). |
| Datenschutzbeauftragte | Wirken auf datenschutzkonformen Umgang mit personenbezogenen Daten hin. |
| Bereichssicherheitsbeauftragte | ISB-Aufgaben für einen abgegrenzten Bereich. |
| Notfallbeauftragte | Verantwortlich für Notfallmanagement/BCM. |
| Auditteam | Führt interne Audits/Revisionen durch. |
| Haustechnik | Infrastruktur eines Gebäudes/Liegenschaft (inkl. zuständiger Leitung). |
| Brandschutzbeauftragte | Alle Fragen des Brandschutzes. |
| Wartungspersonal | Wartung/Instandhaltung von Geräten und Anlagen. |
| ICS-Informationssicherheitsbeauftragte | Informationssicherheit in industriellen Steuerungsumgebungen (IND-Schicht). |

## Regeln

- Bezeichnungen **exakt** wie im Rollenkapitel der Zieledition schreiben (das Kompendium hat in Edition 2023 mehrere Rollenbezeichnungen angepasst und teils geschlechtsneutral formuliert, z. B. „Benutzende", „Entwickelnde", „Planende"). Im Zweifel die Schreibweise/Geschlechtsform gegen das Rollenkapitel der Zieledition prüfen — aber **immer aus diesem Katalog** wählen.
- Ist keine passende Standardrolle vorhanden, ist meist „Fachverantwortliche" oder „IT-Betrieb" die richtige Sammelrolle — **keine** Neuschöpfung.
- Abweichende Zuständigkeit einzelner Anforderungen in eckigen Klammern in der H3-Anforderungsüberschrift, z. B. `### …A6 … (B) [ISB]`.

> Maßgebliche Quelle ist das Kapitel „Rollen" des IT-Grundschutz-Kompendiums (Edition 2023). Diese Allowlist ist eine Arbeitsauswahl der gebräuchlichsten Rollen; bei selteneren Rollen dort gegenprüfen.

# references/schichten-und-ids
# Schichten und ID-Systematik

## Die zehn Schichten des IT-Grundschutz-Kompendiums

Prozessbausteine (organisations-/managementnah):

| Präfix | Schicht |
|--------|---------|
| ISMS | Sicherheitsmanagement |
| ORP | Organisation und Personal |
| CON | Konzeption und Vorgehensweise |
| OPS | Betrieb |
| DER | Detektion und Reaktion |

Systembausteine (technik-/objektnah):

| Präfix | Schicht |
|--------|---------|
| APP | Anwendungen |
| SYS | IT-Systeme |
| IND | Industrielle IT |
| NET | Netze und Kommunikation |
| INF | Infrastruktur |

## Aufbau der Baustein-ID

`SCHICHT.Gruppe[.Teilbaustein]` und je Anforderung `.A<Nr>`:

- `SYS.1.6` → Schicht SYS, Gruppe 1 (Server allgemein), Teilbaustein 6 (Containerisierung)
- `APP.4.4` → Schicht APP, Gruppe 4 (Business-Anwendungen), Teilbaustein 4 (Kubernetes)
- `NET.1.1` → Schicht NET, Gruppe 1 (Netzarchitektur), Teilbaustein 1 (Netzarchitektur und -design)

Bei einem **neuen** Baustein die freie, thematisch passende Position in der Schichtgliederung wählen und mit der BSI-Redaktion bzw. dem Grundschutz++-Vorgehen abstimmen — nicht willkürlich vergeben.

## Häufig verwechselte Baustein-IDs (Querverweis-Referenz)

Querverweise in 1.3/4.1 mit **korrekter ID UND korrektem Titel** angeben. Diese IDs werden besonders oft falsch zitiert (Edition 2023):

| ID | Korrekter Titel | Nicht verwechseln mit |
|----|-----------------|-----------------------|
| CON.1 | Kryptokonzept | **nicht** Software-Entwicklung |
| CON.8 | Software-Entwicklung (auftragnehmende Seite) | ≠ CON.1 |
| CON.10 | Entwicklung von Webanwendungen | ≠ APP.1.1, ≠ APP.3.1 |
| APP.1.1 | Office-Produkte | **nicht** „Webanwendungen"/„Individualsoftware" |
| APP.1.4 | Mobile Anwendung (Apps) | **nicht** „Individualsoftware" |
| APP.7 | Entwicklung von Individualsoftware (auftraggebende Seite) | ≠ APP.1.4 |
| APP.3.1 | Webanwendungen und Webservices (Betrieb) | ≠ CON.10 (Entwicklung) |
| APP.4.3 | Relationale Datenbanksysteme | — |
| APP.4.4 | Kubernetes | — |
| OPS.2.2 | Cloud-Nutzung | ≠ OPS.2.3 |
| OPS.2.3 | Nutzung von Outsourcing (ersetzt OPS.2.1) | ≠ OPS.2.2 |
| OPS.3.2 | Anbieten von Outsourcing (ersetzt OPS.3.1) | — |
| SYS.1.1 | Allgemeiner Server | — |
| SYS.1.6 | Containerisierung | — |
| NET.1.1 | Netzarchitektur und -design | — |

> Im Zweifel die offizielle Baustein-Liste der Zieledition prüfen (BSI: „IT-Grundschutz-Bausteine (Edition 20xx)"). Die APP.4-Untergruppe endet in Edition 2023 bei APP.4.6 — ein „APP.4.10" o. ä. ist dort (noch) nicht vergeben und nur als Entwurf/++-Kandidat zu verstehen.

## Anforderungsnummern

- Fortlaufend über alle drei Klassen hinweg: `A1, A2, A3, …` (kein Neustart je Abschnitt).
- Die Klasse wird über `(B)`, `(S)`, `(H)` in der Anforderungsüberschrift und die Abschnittszuordnung (3.1/3.2/3.3) ausgedrückt, **nicht** über die Nummer.
- **ENTFALLEN:** Bei Streichung in einer neuen Edition bleibt die Nummer als Platzhalter erhalten:
  ```
  ### APP.4.4.A7 ENTFALLEN
  Diese Anforderung ist entfallen.
  ```
  So bleiben IDs über Editionen hinweg stabil (Audit-Nachweise, Verweise, Mappings).
- Neue Anforderungen erhalten die nächste freie Nummer am Ende; bestehende werden **nicht** umnummeriert. Bei einer Überarbeitung sind neue Anforderungen ausdrücklich erwünscht (siehe Überarbeitungsmodus in SKILL).

## Modellierungslogik (für Kapitel 1.3)

- Prozessbausteine werden meist einmal auf den gesamten Informationsverbund angewendet, Systembausteine je Zielobjekt.
- In 1.3 explizit benennen, welche angrenzenden Bausteine ergänzend gelten (z. B. „Betriebssystem-Härtung → SYS.1.1", „Netzseparierung → NET.1.1", „Allgemeiner IT-Betrieb → OPS.1.1.1"), um Doppelregelungen zu vermeiden.
