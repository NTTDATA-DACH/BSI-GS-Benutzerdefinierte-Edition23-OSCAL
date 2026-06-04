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
<Worauf der Baustein anzuwenden ist; was NICHT behandelt wird; Querverweise auf angrenzende Bausteine mit korrekter ID UND korrektem Titel, z. B. „sichere Softwareentwicklung → CON.8 Software-Entwicklung", „Cloud-Bezug → OPS.2.2 Cloud-Nutzung", „Betriebssystem-Härtung → SYS.1.1 Allgemeiner Server". IDs gegen references/schichten-und-ids.md prüfen.>

## 2 Gefährdungslage
<Einleitungssatz: für dieses Zielobjekt sind folgende spezifische Gefährdungen von besonderer Bedeutung.>

### <Gefährdung 1 – Titel>
<Konkrete Bedrohung, keine Maßnahme.>

### <Gefährdung 2 – Titel>
<…>

<… 5–12 Gefährdungen; jede muss in mind. eine Anforderung münden und sich einer G 0.x zuordnen lassen …>

## 3 Anforderungen
Im Folgenden sind die spezifischen Anforderungen des Bausteins <ID> aufgeführt. Grundsätzlich ist <Rolle aus rollenkatalog.md> für die Erfüllung der Anforderungen zuständig. Abweichungen werden in den entsprechenden Anforderungen gesondert genannt.

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
<Einleitungssatz + Liste der relevanten elementaren Gefährdungen mit Nummer UND Titel, verbatim aus elementare-gefaehrdungen.md.>

Spalten = relevante elementare Gefährdungen (nur die einschlägigen, in der Praxis meist 8–20); Zeilen = Anforderungen mit Klasse. „X" markiert die Zuordnung — jede Zuordnung einzeln begründbar (keine „X-überall"-Zeile).

| Anforderung | G 0.<a> | G 0.<b> | G 0.<c> | … |
|-------------|:------:|:------:|:------:|:--:|
| <ID>.A1 (B) | X |  | X | |
| <ID>.A2 (B) |  | X |  | |
| <ID>.A<n> (S) | | X | X | |
| <ID>.A<n> (H) | X | | | |

Prüfen: Jede Spalte (Gefährdung) hat mindestens ein „X"; jede Zeile (Anforderung) hat mindestens ein „X".
