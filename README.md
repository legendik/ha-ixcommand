# ha-ixcommand

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant komponenta pro iXcommand EV nabíječky. Ovládejte svou EV nabíječku a sledujte procesy nabíjení s plnou integrací do Energy Dashboardu Home Assistant.

## Funkce

- **Kompletní ovládání**: Zapnutí/vypnutí nabíjení, nastavení proudových limitů, konfigurace boost režimu
- **Sledování v reálném čase**: Sledování nabíjecího výkonu, proudu, spotřeby energie a stavu
- **Integrace s Energy Dashboardem**: Automatické začlenění dat o spotřebě energie
- **Podpora více nabíječek**: Přidejte libovolný počet nabíječek (každá jako samostatná integrace)
- **WiFi diagnostika**: Sledování síly signálu, SSID a stavu připojení

## Instalace

### Možnost 1: HACS (Doporučeno)

1. Ujistěte se, že je [HACS](https://hacs.xyz/) nainstalován
2. Přidejte tuto repository jako custom repository v HACS:
   - Jděte do HACS → Integrace
   - Klikněte na tři tečky (⋮) → Vlastní repository
   - Přidejte `https://github.com/legendik/ha-ixcommand` jako URL repository
   - Vyberte kategorii "Integrace"
3. Vyhledejte "iXcommand EV Charger" a nainstalujte
4. Restartujte Home Assistant

### Možnost 2: Manuální instalace

1. Stáhněte složku `custom_components/ixcommand/` z této repository
2. Zkopírujte ji do složky `custom_components/` vašeho Home Assistant
3. Restartujte Home Assistant

## Konfigurace

1. Jděte do **Nastavení** → **Zařízení a služby** → **Přidat integraci**
2. Vyhledejte "iXcommand EV Charger" a vyberte ji
3. Zadejte:
   - **API klíč**: Váš iXcommand API klíč
   - **Sériové číslo**: Sériové číslo vaší nabíječky (formát: XXX-XXX-XXX)
4. Klikněte na **Odeslat**

### Získání API klíče a sériového čísla

1. Přihlaste se na https://www.ixfield.com/app/account
2. V sekci API vygenerujte nový API klíč
3. Sériové číslo najdete na štítku na zadní straně nabíječky (označení S/N)
   - Formát: XXX-XXX-XXX (např. ABC-123-DEF)

### Přidání více nabíječek

Pro přidání další nabíječky:
1. Jděte do **Nastavení** → **Zařízení a služby** → **Přidat integraci**
2. Vyhledejte "iXcommand EV Charger" znovu
3. Zadejte API klíč a sériové číslo pro druhou nabíječku
4. Každá nabíječka se zobrazí jako samostatné zařízení v Home Assistant

## Entity

Každá nabíječka vytváří následující entity:

### Senzory
- **Current Charging Power** (`sensor`): Aktuální nabíjecí výkon ve wattech
- **Total Energy** (`sensor`): Celková spotřeba energie ve watthodinách (dostupné v Energy Dashboardu)
- **Charging Current L1/L2/L3** (`sensor`): Proud na fázi v ampérech
- **Boost Remaining** (`sensor`): Zbývající čas boostu v sekundách
- **WiFi Signal** (`sensor`): Síla WiFi signálu v procentech
- **Charging Status** (`sensor`): Aktuální stav nabíjení (INIT/IDLE/CONNECTED/CHARGING/atd.)
- **WiFi SSID** (`sensor`): Název připojené WiFi sítě
- **WiFi BSSID** (`sensor`): MAC adresa WiFi přístupového bodu

### Přepínače
- **Charging Enable** (`switch`): Zapnutí/vypnutí nabíjení
- **Single Phase Mode** (`switch`): Přepínání mezi 1-fázovým a 3-fázovým nabíjením
- **Boost Mode** (`switch`): Stav boost režimu (pouze čtení)

### Číselné ovladače
- **Target Current** (`number`): Nastavení normálního nabíjecího proudu (6-16A, podle max. proudu)
- **Boost Current** (`number`): Nastavení boost nabíjecího proudu (6-16A, podle max. proudu)
- **Maximum Current** (`number`): Nastavení maximálního povoleného proudu (6-16A)
- **Boost Time** (`number`): Nastavení doby trvání boostu (0-86400 sekund)

## Energy Dashboard

Senzor **Total Energy** je automaticky nakonfigurován pro Energy Dashboard Home Assistant:
- Device Class: `energy`
- State Class: `total_increasing`
- Jednotka: `Wh`

Pro přidání do Energy Dashboardu:
1. Jděte do **Nastavení** → **Dashboards** → **Energy**
2. V sekci "Individual Devices" klikněte na **Přidat zařízení**
3. Vyberte vaše iXcommand zařízení
4. Spotřeba energie bude sledována automaticky

## Informace o API

Tato integrace používá iXcommand API na `https://evcharger.ixcommand.com/api/v1/`. API vyžaduje:
- **Autentifikace**: X-API-KEY header
- **Endpoints**: `/thing/{serial}/properties` pro čtení/zápis vlastností nabíječky
- **Dotazování**: 30-sekundové intervaly pro minimalizaci zátěže API

## Řešení problémů

### Problémy s připojením
- Ověřte, že váš API klíč je správný
- Zkontrolujte, že vaše sériové číslo je ve formátu XXX-XXX-XXX
- Ujistěte se, že je vaše nabíječka online a připojena k internetu

### Chyby autentifikace
- Váš API klíč může být neplatný nebo expirovaný
- Použijte proces re-autentifikace v Home Assistant pro aktualizaci údajů

### Chybějící entity
- Restartujte Home Assistant po instalaci
- Zkontrolujte logy Home Assistant pro případné chybové zprávy

## Podpora

Pro problémy nebo žádosti o funkce vytvořte prosím issue na této GitHub repository.

## Licence

Tento projekt je licencován pod MIT License - viz LICENSE soubor.
