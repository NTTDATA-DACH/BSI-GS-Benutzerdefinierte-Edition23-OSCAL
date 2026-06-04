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
