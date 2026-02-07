# Poznań Public Transport - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integracja Home Assistant dla transportu publicznego w Poznaniu (ZTM Poznań / PEKA).

## Funkcje

- 🚌 Wyświetlanie rozkładu jazdy w czasie rzeczywistym
- 📍 Obsługa wielu przystanków
- 🔍 Filtrowanie po liniach autobusowych/tramwajowych
- ♿ Informacje o udogodnieniach (klimatyzacja, niskie podłogi, stojaki na rowery)
- 🎨 Ładna karta Lovelace z ikonami
- ⚡ Automatyczne odświeżanie co 30 sekund

## Instalacja

### Metoda 1: HACS (rekomendowana)

1. Otwórz HACS w Home Assistant
2. Kliknij "Integrations"
3. Kliknij menu (3 kropki) i wybierz "Custom repositories"
4. Dodaj URL: `https://github.com/pbromber/ztm-hass`
5. Wybierz kategorię: "Integration"
6. Kliknij "Add"
7. Znajdź "Poznań Public Transport" i kliknij "Download"
8. Zrestartuj Home Assistant

### Metoda 2: Manualna

1. Skopiuj folder `custom_components/poznan_transport` do `config/custom_components/poznan_transport`
2. **Ważne:** Skopiuj plik `www/poznan-transport-card.js` z tego repozytorium do katalogu `config/www/` w Home Assistant:
   - Pobierz plik: [poznan-transport-card.js](www/poznan-transport-card.js)
   - Skopiuj go do katalogu `www` w Home Assistant (jeśli folder nie istnieje, utwórz go)
   - Pełna ścieżka w Home Assistant: `config/www/poznan-transport-card.js`
3. Zrestartuj Home Assistant

## Konfiguracja

### Dodawanie przystanku

1. Przejdź do **Settings** → **Devices & Services**
2. Kliknij **Add Integration**
3. Wyszukaj **Poznań Public Transport**
4. Podaj:
   - **Stop Symbol** - kod przystanku (np. `NIED01`)
   - **Lines** (opcjonalnie) - linie do filtrowania, oddzielone przecinkami (np. `171, 172, 173`)

### Jak znaleźć kod przystanku?

1. Wejdź na https://www.peka.poznan.pl/
2. Znajdź swój przystanek na mapie
3. Kod przystanku to zazwyczaj kilka pierwszych liter nazwy + numer słupka
4. Przykłady:
   - `NIED01` - Niedziałkowskiego
   - `RONDO01` - Rondo Kaponiera
   - `DWOR01` - Dworzec Główny

## Sensory

Po dodaniu przystanku, utworzone zostaną 2 sensory:

### 1. Next Departure
- **Entity ID**: `sensor.{przystanek}_next_departure`
- **Stan**: Najbliższy odjazd (np. "Line 171 - 5 min")
- **Atrybuty**:
  - `line` - numer linii
  - `direction` - kierunek jazdy
  - `minutes` - czas do odjazdu w minutach
  - `departure` - dokładna godzina odjazdu
  - `real_time` - czy to dane real-time (true/false)
  - `vehicle` - numer pojazdu
  - `bike` - stojak na rowery
  - `air_conditioning` - klimatyzacja
  - `low_floor` - niska podłoga

### 2. All Departures
- **Entity ID**: `sensor.{przystanek}_all_departures`
- **Stan**: Liczba najbliższych odjazdów
- **Atrybuty**:
  - `departures` - lista wszystkich odjazdów (max 10)

## Lovelace Card

### Dodawanie karty

1. Dodaj zasób w **Settings** → **Dashboards** → **Resources**:
   ```
   URL: /local/poznan-transport-card.js
   Type: JavaScript Module
   ```

2. Dodaj kartę do dashboardu:
   - Otwórz swój dashboard w Home Assistant
   - Kliknij **Edit Dashboard** (ikona ołówka w prawym górnym rogu)
   - Kliknij **Add Card** (niebieski przycisk na dole)
   - Przewiń w dół i wybierz **Manual** (ręczna konfiguracja)
   - Wklej poniższy YAML:
   ```yaml
   type: custom:poznan-transport-card
   entity: sensor.niedziałkowskiego_all_departures
   max_departures: 5
   ```
   - Kliknij **Save**, a następnie **Done**

### Opcje karty

| Opcja | Typ | Wymagane | Opis |
|-------|-----|----------|------|
| `entity` | string | Tak | Entity ID sensora "All Departures" |
| `max_departures` | number | Nie | Maksymalna liczba odjazdów do wyświetlenia (domyślnie: 5) |

### Przykładowa konfiguracja

```yaml
type: custom:poznan-transport-card
entity: sensor.niedziałkowskiego_all_departures
max_departures: 8
```

## Przykłady użycia

### Prosty sensor w dashboard

```yaml
type: entities
entities:
  - entity: sensor.niedziałkowskiego_next_departure
    name: Najbliższy autobus
```

### Karta z wieloma przystankami

```yaml
type: vertical-stack
cards:
  - type: custom:poznan-transport-card
    entity: sensor.niedziałkowskiego_all_departures
    max_departures: 5
  - type: custom:poznan-transport-card
    entity: sensor.rondo_kaponiera_all_departures
    max_departures: 3
```

### Automatyzacja - powiadomienie o autobusie

```yaml
automation:
  - alias: "Powiadom o autobusie"
    trigger:
      - platform: state
        entity_id: sensor.niedziałkowskiego_next_departure
    condition:
      - condition: template
        value_template: "{{ state_attr('sensor.niedziałkowskiego_next_departure', 'minutes') == 5 }}"
      - condition: template
        value_template: "{{ state_attr('sensor.niedziałkowskiego_next_departure', 'line') == '171' }}"
    action:
      - service: notify.mobile_app
        data:
          title: "Autobus 171"
          message: "Odjeżdża za 5 minut!"
```

### Conditional card - pokaż tylko gdy autobus jedzie

```yaml
type: conditional
conditions:
  - entity: sensor.niedziałkowskiego_next_departure
    state_not: "No departures"
card:
  type: custom:poznan-transport-card
  entity: sensor.niedziałkowskiego_all_departures
  max_departures: 3
```

## Troubleshooting

### Nie widać integracji w "Add Integration"

1. Zrestartuj Home Assistant
2. Wyczyść cache przeglądarki (Ctrl+Shift+R)
3. Sprawdź logi: **Settings** → **System** → **Logs**

### Karta nie wyświetla się / "Custom element doesn't exist: poznan-transport-card"

1. **Sprawdź czy plik karty istnieje w Home Assistant:**
   - Plik musi być w katalogu `config/www/poznan-transport-card.js`
   - Jeśli nie ma, skopiuj go z repozytorium (folder `www/poznan-transport-card.js`)
2. **Dodaj zasób:** **Settings** → **Dashboards** → **Resources**
   - URL: `/local/poznan-transport-card.js`
   - Type: JavaScript Module
3. **Wyczyść cache przeglądarki:** Ctrl+Shift+R (lub Cmd+Shift+R na Mac)
4. **Zrestartuj Home Assistant**
5. Sprawdź konsolę deweloperską (F12) w przeglądarce - czy są błędy ładowania pliku

### "Invalid stop symbol"

1. Sprawdź czy kod przystanku jest prawidłowy
2. Upewnij się, że jest napisany WIELKIMI LITERAMI
3. Spróbuj innego przystanku (np. `NIED01`)

### Dane nie odświeżają się

1. Sprawdź połączenie internetowe Home Assistant
2. API ZTM Poznań może być chwilowo niedostępne
3. Sprawdź logi integracji

## Techniczne

- **API**: https://www.peka.poznan.pl/vm/method.vm
- **Aktualizacja**: Co 30 sekund
- **Timeout**: 10 sekund
- **Platforma**: Sensor
- **Wymagania**: Home Assistant 2023.1+

## Licencja

MIT License

## Autor

Created by [@pbromber](https://github.com/pbromber)

## Wsparcie

Jeśli podoba Ci się ta integracja, zostaw ⭐ na GitHub!

Znalazłeś bug? [Zgłoś issue](https://github.com/pbromber/ztm-hass/issues)

