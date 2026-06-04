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
- Neue Anforderungen erhalten die nächste freie Nummer am Ende; bestehende werden **nicht** umnummeriert. Bei einer Überarbeitung sind neue Anforderungen ausdrücklich erwünscht (siehe Überarbeitungsmodus in SKILL.md).

## Modellierungslogik (für Kapitel 1.3)

- Prozessbausteine werden meist einmal auf den gesamten Informationsverbund angewendet, Systembausteine je Zielobjekt.
- In 1.3 explizit benennen, welche angrenzenden Bausteine ergänzend gelten (z. B. „Betriebssystem-Härtung → SYS.1.1", „Netzseparierung → NET.1.1", „Allgemeiner IT-Betrieb → OPS.1.1.1"), um Doppelregelungen zu vermeiden.
