# BSI-Grundschutz zu OSCAL: Die automatisierte Konvertierungspipeline

Dieses Projekt stellt eine leistungsstarke, automatisierte Pipeline zur Konvertierung von BSI-Grundschutz-„Baustein“-PDF-Dokumenten in ein reichhaltiges, strukturiertes und OSCAL-konformes JSON-Format bereit. Es nutzt die fortschrittlichen Fähigkeiten des `gemini-2.5-pro`-Modells von Google, um den Inhalt nicht nur zu übersetzen, sondern ihn auch mit einem mehrstufigen Reifegradmodell und kontextuellen Informationen anzureichern, sodass der endgültige Katalog sofort für Analysen und das Compliance-Management nützlich ist.

Das System ist als serverloser **Google Cloud Run Job** konzipiert und arbeitet **inkrementell**. Es liest intelligent einen bestehenden Master-OSCAL-Katalog ein, verarbeitet neue oder aktualisierte PDFs und führt die Ergebnisse nahtlos zusammen, indem es neue „Bausteine“ hinzufügt oder bestehende überschreibt.

### Hauptmerkmale

* **Vollautomatische Konvertierung:** Wandelt rohe PDF-Inhalte ohne manuellen Eingriff in strukturiertes OSCAL-JSON um.
* **Inkrementelle Updates:** Fügt intelligent neue Bausteine hinzu oder überschreibt bestehende in einer Master-Katalogdatei, was den Prozess wiederholbar und effizient macht.
* **Kontextuelle Anreicherung:** Extrahiert einleitende Kapitel (Einleitung, Zielsetzung, Modellierung) und die vollständige Gefährdungslage in strukturierte `parts` und liefert so wichtigen Kontext direkt im Katalog.
* **G++ konforme Praktiken:** Jedes Control wird in eine der definierten Praktiken einsortiert.
* **WiBA-konforme Checklisten:** Der [Viewer unterstützt Checklisten wie WiBA](https://github.com/NTTDATA-DACH/BSI-GS-Benutzerdefinierte-Edition23-OSCAL/blob/main/src/g2oscal/WiBa_Checklisten_bsi_oscal.html). Sie können als JSON-Dateien gespeichert und geladen werden. Filter funktionieren darauf, sodass ein Benutzer beispielsweise die Checkliste für alle Basis-Controls in der ISMS-Umsetzungsphase durchführen kann.
* **OSCAL-konforme Control-Klassen:** Jedem Control wird eine Klasse basierend auf der offiziellen OSCAL-Spezifikation zugewiesen.
* **BSI-Stufe:** Jedes Control erhält eine Stufe basierend auf den BSI-Grundschutz-Kategorien Basis, Standard und Erhöht in den neuen G++ konformen Stufen 1 bis 5.
* **5-stufiges Reifegradmodell:** Erzeugt fünf verschiedene Reifegradstufen für jede einzelne Anforderung und ermöglicht so eine granulare Bewertung über die einfache Einhaltung hinaus.
* **ISMS-Phasen-Zuordnung:** Ordnet jede Anforderung einer Phase des ISMS-Lebenszyklus zu (z. B. Umsetzung, Betrieb) zur besseren Prozessintegration.
* **Analyse der Schutzziele (CIA):** Stellt fest, ob ein Control die Vertraulichkeit, Integrität oder Verfügbarkeit beeinflusst.

# Bereitgestellte Werkzeuge

## OSCAL Catalog Pruner
**Zweck:** Gezielte Reduzierung großer OSCAL-Kataloge auf das Wesentliche. 

Oftmals werden für spezifische Aufgaben nicht alle, sondern nur ausgewählte Bausteine oder Praktiken aus einem umfassenden Katalog benötigt. Mit dem **OSCAL Catalog Pruner** lassen sich große JSON-Kataloge direkt im Browser filtern. Über eine intuitive Baumstruktur können exakt die benötigten Gruppen ausgewählt und als verkleinertes, bereinigtes JSON exportiert werden. Das minimiert den Daten-Overhead für Folgeprozesse massiv. 

**Eigenschaften:**
- **Datenschutz by Design:** 100% lokale Verarbeitung im Browser – keine API-Aufrufe, keine Uploads.
- **Flexibilität:** Optionales "Flattening" von verschachtelten Gruppenstrukturen.
- **Effizienz:** Schneller Export des passgenauen JSON-Auszugs für spezifische Teil-Audits oder Analysen.



## Automatische Erzeugung von OSCAL-Komponenten aus dem BSI-Katalog

Das `g2oscal`-Werkzeug ist als **einfacher Weg zur Konvertierung von BSI-Grundschutz-Bausteinen in einen deutschen OSCAL-Katalog** konzipiert. Es verwendet die originalen deutschen PDFs und erzeugt eine hochwertige, angereicherte deutsche JSON-Datei.

---

## Der Übersetzungs-Workflow: Erstellung mehrsprachiger Kataloge

Um übersetzte Versionen (z. B. auf Englisch) zu erstellen, kann `translate_oscal` in jede Sprache übersetzen, die die GenAI anbietet.

1.  Führen Sie zuerst das `g2oscal`-Projekt aus, um eine deutsche OSCAL `BSI_Catalog_....json`-Datei zu erzeugen.
2.  Navigieren Sie zum Geschwisterverzeichnis dieses Projekts: `../translate_oscal`.
3.  Die Skripte in diesem Verzeichnis sind speziell dafür ausgelegt, die deutsche OSCAL-JSON-Datei als **Eingabe** zu verwenden und deren Inhalt mit einem KI-Modell in andere Sprachen zu übersetzen, während die gesamte OSCAL-Struktur sorgfältig erhalten bleibt.

Diese Trennung der Aufgaben stellt sicher, dass die Kerndatenerzeugung robust ist und die Übersetzung als unabhängiger, nachfolgender Schritt verwaltet werden kann.

---

## Erstellung von Komponentendefinitionen

Das Projekt `oscal_components_from_grundschutz` enthält ein Skript, das darauf ausgelegt ist, automatisch angereicherte OSCAL-Komponentendefinitionen aus einem BSI-IT-Grundschutz-Katalog zu erstellen. Das Skript identifiziert einzelne „Bausteine“ aus dem Quellkatalog, erstellt für jeden eine Basis-Komponentendefinition und verwendet dann das Google Vertex AI Gemini Pro-Modell, um intelligent relevante Controls aus anderen Bausteinen zu entdecken und hinzuzufügen. Um die eher statische Komponente für die „Prozessbausteine“ zu erzeugen, existiert ebenfalls ein kleineres Skript: `create_prozessbausteine_component.py`. Dieses wird einmalig ausgeführt.

Die endgültige Ausgabe ist ein Satz OSCAL-konformer JSON-Dateien, eine für jeden technischen Baustein, die in einem Google Cloud Storage (GCS) Bucket gespeichert werden.
Die endgültige Ausgabe ist ein Satz OSCAL-konformer JSON-Dateien, eine für jeden technischen Baustein, die in einem Google Cloud Storage (GCS) Bucket gespeichert werden.

---

## Qualitätssicherung

Das Werkzeug `quality_control` nimmt OSCAL-Komponentendefinitionen und einen Katalog entgegen und führt einen anspruchsvollen, vielschichtigen Qualitätskontroll- und Anreicherungszyklus an einem OSCAL-basierten Sicherheitskatalog durch. Es geht über einfache Linting- oder Syntaxprüfungen hinaus, indem es ein großes Sprachmodell (Google Gemini 2.5 Pro) verwendet, um die semantische Bedeutung, den Kontext und die Vollständigkeit von Sicherheits-Controls zu analysieren.

Es fügt dem Katalog Kommentare in einem Teil namens „prose_qs“ hinzu und ergänzt neue Controls, wenn der aktuelle Satz nicht vollständig ist.

---

# Angereicherte Datenmodelle

## 1. Kontextinformationen (`parts`)

Um den Nutzen des Katalogs zu erhöhen, extrahiert die Pipeline nun wichtige einleitende und kontextbezogene Kapitel aus jedem Baustein-PDF. Diese Informationen werden im `parts`-Array jeder `bausteinGroup` gespeichert, sodass Benutzer den Zweck und die zugehörigen Risiken verstehen können, ohne auf das ursprüngliche PDF zurückgreifen zu müssen.

* **1. Einleitung:** Ein ausklappbarer Abschnitt, der den Prosatext aus den Kapiteln 1.1, 1.2 und 1.3 enthält.
* **2. Gefährdungslage:** Ein ausklappbarer Abschnitt, der jede relevante Gefährdung auflistet, wobei jede Gefährdung mit ihrem offiziellen Titel und ihrer vollständigen Beschreibung dargestellt wird.

## 2. Das 5-stufige Reifegradmodell

Ein Kernziel dieses Projekts ist es, die OSCAL-Daten um eine qualitative Bewertungsebene zu erweitern. Zu diesem Zweck wird jede aus dem BSI-Grundschutz extrahierte Anforderung einem 5-stufigen Reifegradmodell zugeordnet. Dieses Modell ermöglicht eine granulare und differenzierte Bewertung der Umsetzungsqualität von Sicherheitsmaßnahmen, die weit über eine rein binäre (erfüllt/nicht erfüllt) Konformitätsaussage hinausgeht.

* **Stufe 1: Partial (Teilweise umgesetzt)**
* **Stufe 2: Foundational (Grundlegend umgesetzt)**
* **Stufe 3: Defined (Definiert umgesetzt)** - **Baseline/Referenz**
* **Stufe 4: Enhanced (Erweitert umgesetzt)**
* **Stufe 5: Comprehensive (Umfassend umgesetzt)**

**Strategischer Wert des Modells:**
Das Modell dient als strategisches Instrument für Informationssicherheits-Managementsysteme (ISMS). Es ermöglicht Organisationen, ihre aktuelle Sicherheitsposition präzise zu bewerten (Ist-Analyse) und unterstützt die Definition von zielgerichteten, risikobasierten Soll-Zuständen (Soll-Architektur). Durch die Quantifizierung der Umsetzungsqualität können Ressourcen effizienter zugewiesen und Verbesserungsbereiche im Sinne eines kontinuierlichen Verbesserungsprozesses (KVP) systematisch identifiziert und priorisiert werden.
**Strategischer Wert des Modells:**
Das Modell dient als strategisches Instrument für Informationssicherheits-Managementsysteme (ISMS). Es ermöglicht Organisationen, ihre aktuelle Sicherheitsposition präzise zu bewerten (Ist-Analyse) und unterstützt die Definition von zielgerichteten, risikobasierten Soll-Zuständen (Soll-Architektur). Durch die Quantifizierung der Umsetzungsqualität können Ressourcen effizienter zugewiesen und Verbesserungsbereiche im Sinne eines kontinuierlichen Verbesserungsprozesses (KVP) systematisch identifiziert und priorisiert werden.

Das KI-Modell wurde darauf trainiert, fünf qualitative Variationen für jede Anforderung zu generieren. Der normative Text aus dem BSI-Kompendium für die jeweilige Anforderung dient als Referenz für die Reifegradstufe 3 („Definiert“). Die anderen Stufen werden durch logische Extrapolation abgeleitet, um ein konsistentes und verständliches Bewertungsframework zu schaffen.

### Stufe 1: Partial (Teilweise)
* **Beschreibung:** Das Control wird nur sporadisch, ad hoc oder in einem sehr begrenzten Teilbereich seines beabsichtigten Umfangs umgesetzt. Die Umsetzung ist inkonsistent, weist erhebliche Abdeckungslücken auf und adressiert nur einen Bruchteil des beabsichtigten Risikos. Es handelt sich oft um eine reaktive, isolierte Maßnahme statt um Teil einer geplanten Strategie.
* **Schlüsselmerkmale:** Ad-hoc-Reaktionen, inkonsistente Anwendung, hoher manueller Aufwand für Insellösungen, hohes verbleibendes Restrisiko.

---

### Stufe 2: Foundational (Grundlegend)
* **Beschreibung:** Das Control wird über seinen gesamten beabsichtigten Umfang umgesetzt, stützt sich jedoch hauptsächlich auf Standard-Konfigurationen (out-of-the-box) ohne tiefgehende Anpassung an spezifische organisatorische Richtlinien oder Risiken. Obwohl eine grundlegende Abdeckung besteht, wird ihre Wirksamkeit oft nur durch manuelle Überprüfung sichergestellt und ist noch nicht optimiert.
* **Schlüsselmerkmale:** Vollständige Basisabdeckung, Verwendung von Standardeinstellungen, Mangel an Anpassung und Härtung, konsistent, aber nicht maßgeschneidert.

---

### Stufe 3: Defined (Definiert)
* **Beschreibung:** Die Umsetzung des Controls folgt einem dokumentierten, standardisierten und wiederholbaren Prozess. Die Konfigurationen sind bewusst auf die unternehmensspezifischen Sicherheitsrichtlinien und Risikoanalysen zugeschnitten. Obwohl der Prozess zuverlässig ist, kann er noch weitgehend manuell sein und ist noch nicht tief in andere Sicherheitssysteme integriert. **Diese Stufe stellt die Baseline für eine ordnungsgemäß und nachweisbar betriebene Sicherheitsmaßnahme dar.**
* **Schlüsselmerkmale:** Dokumentierter und wiederholbarer Prozess, an Unternehmensrichtlinien angepasste Konfigurationen, Überprüfbarkeit der Umsetzung, Erfüllung der Kernanforderung („MUSS“-Anforderung).

---

### Stufe 4: Enhanced (Erweitert)
* **Beschreibung:** Aufbauend auf dem definierten Prozess werden zusätzliche Kontrollen und Optimierungen implementiert, die über die Grundanforderung hinausgehen. Dies umfasst typischerweise die Umsetzung wichtiger „SOLLTE“-Empfehlungen des BSI, die Verwendung gehärteter Konfigurationen, die Einführung von Automatisierungs- und Überwachungstechniken zur Steigerung der Wirksamkeit sowie die formale Integration mit angrenzenden Prozessen. Die Umsetzung ist nachweislich widerstandsfähiger als die Baseline.
* **Schlüsselmerkmale:** Umsetzung von „SOLLTE“-Empfehlungen, erhöhte Wirksamkeit und Widerstandsfähigkeit, erste Automatisierung und proaktive Überwachung, formalisierte Prozesse.

---

### Stufe 5: Comprehensive (Umfassend)
* **Beschreibung:** Das Control ist als Best-Practice-Lösung implementiert und tief in die Sicherheitsarchitektur (Defense-in-Depth) integriert. Es ist hochwirksam, oft weitgehend automatisiert und wird proaktiv überwacht und kontinuierlich optimiert. Diese Stufe spiegelt eine reife, vorausschauende Sicherheitsstrategie wider, die oft alle relevanten „SOLLTE“-Empfehlungen sinnvoll kombiniert und verfeinert.
* **Schlüsselmerkmale:** Best-Practice-Implementierung, hochgradig automatisiert und integriert, kontinuierliche Überwachung und Optimierung, proaktive Sicherheitsposition.

---

## 3. ISMS-Phasen-Zuordnung

Um den strategischen Wert des Katalogs zu erhöhen und die Lücke zwischen technischen Controls und Managementprozessen zu schließen, wird jede Sicherheitsanforderung einer spezifischen Phase des Lebenszyklus eines Informationssicherheits-Managementsystems (ISMS) zugeordnet. Diese Klassifizierung ist von etablierten Frameworks wie ISO/IEC 27001 und dem Plan-Do-Check-Act (PDCA)-Zyklus inspiriert und bietet einen prozessorientierten Kontext für jedes Control.

**Strategischer Wert der Phasen-Zuordnung:**
Diese Zuordnung ermöglicht es Stakeholdern – wie CISOs, Sicherheitsbeauftragten und Projektmanagern – Controls basierend auf ihrem aktuellen strategischen oder operativen Fokus zu filtern und zu priorisieren. Sie hilft, technische Sicherheitsmaßnahmen direkt in die übergeordneten Aktivitäten des Risikomanagements, der Projektplanung und der kontinuierlichen Verbesserung zu integrieren und stärkt so die Governance und die prozessuale Verankerung der Informationssicherheit.

Das KI-Modell ist darauf trainiert, jeder Anforderung die logisch am besten passende Phase zuzuordnen, wobei „Umsetzung“ für die meisten technischen Controls als Standard dient.

### Die ISMS-Phasen im Detail
### Die ISMS-Phasen im Detail

---
#### **Initiierung**
* **Beschreibung:** Diese Phase umfasst die strategische Vorbereitung und Zieldefinition für sicherheitsrelevante Initiativen. Sie beinhaltet die Etablierung von Governance-Strukturen, die Festlegung des ISMS-Geltungsbereichs und die Formulierung der zentralen Informationssicherheitsleitlinie. Controls in dieser Phase sind typischerweise grundlegend und richtlinienbasiert.

---
#### **Risikobewertung**
* **Beschreibung:** Dies beinhaltet die systematische Identifizierung, Analyse und Bewertung von Informationssicherheitsrisiken. Diese Phase ist fundamental für die Bestimmung des Schutzbedarfs und für die Ableitung angemessener Sicherheitsmaßnahmen. Controls zur Identifizierung von Assets und zur Bedrohungsanalyse gehören hierher.

---
#### **Risikobehandlung**
* **Beschreibung:** Dies ist der Prozess der Auswahl und Gestaltung von Maßnahmen zur Adressierung der in der Bewertungsphase identifizierten Risiken. Es umfasst strategische Entscheidungen darüber, ob ein gegebenes Risiko gemindert, vermieden, übertragen oder akzeptiert werden soll. Controls in dieser Phase sind oft konzeptionell und planungsbezogen.

---
#### **Umsetzung**
* **Beschreibung:** Diese Phase betrifft die technische und organisatorische Einführung der im Risikobehandlungsplan definierten Sicherheits-Controls. Es ist die „Build“-Phase, die konzeptionelle Anforderungen in einen operativen Zustand überführt. Die Mehrheit der technischen BSI-Grundschutz-Controls fällt in diese Kategorie.

---
#### **Betrieb**
* **Beschreibung:** Diese Phase deckt die laufende Ausführung und Wartung der implementierten Sicherheits-Controls ab. Sie umfasst Routineprozesse wie Überwachung, Patch-Management, Incident-Handling und die Durchführung regelmäßiger Sicherheitsaufgaben.

---
#### **Audit (Überprüfung)**
* **Beschreibung:** Dies beinhaltet die periodische und systematische Überprüfung der Wirksamkeit, Effizienz und Konformität des ISMS und seiner Controls. Audits liefern die notwendigen Daten zur Bewertung der Sicherheitsleistung und zur Überprüfung, ob die Controls wie beabsichtigt funktionieren.

---
#### **Verbesserung**
* **Beschreibung:** Diese Phase konzentriert sich auf die kontinuierliche Optimierung des ISMS auf der Grundlage der Ergebnisse von Audits, Leistungskennzahlen und der Analyse von Sicherheitsvorfällen. Sie schließt den PDCA-Zyklus und treibt die fortlaufende Entwicklung und Reifung der Sicherheitsposition der Organisation voran.
