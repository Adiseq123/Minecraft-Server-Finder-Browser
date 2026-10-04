# 🔍 Minecraft Server Finder & Browser

<img width="1917" height="1038" alt="image" src="https://github.com/user-attachments/assets/ba8be0b6-37bc-498d-8ca0-b11ca554e060" />

Aplikacja okienkowa **GUI napisana w Pythonie**, służąca do skanowania zakresów adresów IP oraz wyszukiwania aktywnych serwerów **Minecraft Java Edition**.

Program umożliwia szybkie wykrywanie dostępnych usług Minecraft, a następnie szczegółową weryfikację znalezionych serwerów za pomocą biblioteki `mcstatus`.

---

## ✨ Funkcje

- **⚡ Szybkie skanowanie portów:** Obsługa ultraszybkiego skanera `Masscan` oraz wbudowanego, bezpieczniejszego trybu **Czysty Python**.
- **🎮 Pełna weryfikacja Minecraft:** Pobieranie wersji serwera, liczby graczy online, pingu oraz MOTD.
- **🧹 Czyszczenie MOTD:** Automatyczne usuwanie kodów kolorów `§` z opisu serwera.
- **📂 Wczytywanie gotowych wyników:** Import wyników z zewnętrznych skanów w formacie **Masscan JSON**.
- **🔎 Wyszukiwarka i filtry:** Filtrowanie wyników po IP, wersji Minecraft oraz MOTD.
- **👥 Tylko serwery z graczami:** Możliwość pokazania wyłącznie serwerów, na których są aktualnie gracze.
- **↕️ Sortowanie:** Sortowanie wyników bezpośrednio w tabeli.
- **📋 Kopiowanie IP:** Dwukrotne kliknięcie wiersza pozwala szybko skopiować adres serwera do schowka.
- **🖥️ GUI:** Wszystkie wyniki prezentowane są w wygodnej tabeli bez konieczności korzystania wyłącznie z terminala.

---

## 📋 Wymagania

1. **Python 3.8+**
2. **Npcap — Windows**
3. **Masscan** — jeżeli korzystasz z trybu Masscan
4. Biblioteka Python `mcstatus`

### Npcap

Npcap jest wymagany przez Masscan na systemie Windows.

Podczas instalacji należy włączyć:

`Install Npcap in WinPcap API-compatible Mode`

---

## 📦 Instalacja

Zainstaluj wymagane biblioteki Pythona:

```bash
pip install mcstatus
```

Następnie umieść skompilowany:

`masscan.exe`

w głównym folderze projektu.

---

## 🚀 Uruchomienie

Uruchom **PowerShell lub Wiersz poleceń jako Administrator** w systemie Windows.

W systemie Linux uruchom terminal z odpowiednimi uprawnieniami wymaganymi przez używany tryb skanowania.

Następnie:

```bash
python serverfinder.py
```

Po uruchomieniu aplikacji możesz wybrać odpowiedni tryb skanowania i przeglądać znalezione serwery w interfejsie GUI.

---

## ⚙️ Tryby skanowania

### Masscan

Tryb wykorzystujący zewnętrzny skaner `Masscan` do szybkiego sprawdzania wskazanych zakresów.

Wymaga poprawnie skonfigurowanego `masscan.exe` oraz odpowiednich uprawnień systemowych.

### Czysty Python

Wbudowany tryb wykorzystujący Pythona bez konieczności korzystania z Masscan.

Jest prostszy w konfiguracji, ale może być znacznie wolniejszy przy większych zakresach adresów.

---

## 📊 Wyniki

Po zakończeniu skanowania aplikacja może zweryfikować znalezione adresy pod kątem usługi Minecraft Java Edition.

Dla znalezionych serwerów prezentowane są m.in.:

| Informacja | Opis |
| :--- | :--- |
| **IP** | Adres serwera Minecraft |
| **Port** | Port usługi |
| **Wersja** | Wykryta wersja Minecraft |
| **Gracze** | Aktualna liczba graczy online |
| **Ping** | Czas odpowiedzi serwera |
| **MOTD** | Opis serwera bez kodów kolorów `§` |

---

## 📂 Import Masscan JSON

Aplikacja umożliwia również wczytanie wcześniej przygotowanych wyników skanowania w formacie **Masscan JSON**.

Pozwala to oddzielić etap skanowania od późniejszej weryfikacji serwerów Minecraft.

---

## 💡 Porady eksploatacyjne

### Rate

Prędkość skanowania określana jest w pakietach na sekundę.

Dla zwykłych łączy domowych należy stosować ostrożne wartości, ponieważ zbyt wysoki rate może powodować przeciążenie własnego routera, utratę pakietów lub problemy z połączeniem.

**Zalecane jest rozpoczęcie od niskiej wartości i zwiększanie jej tylko wtedy, gdy infrastruktura na to pozwala.**

---

## ⚠️ Ważne ostrzeżenie

**Korzystasz z programu na własne ryzyko.**

Skanowanie zakresów adresów IP może być wykrywane przez administratorów sieci i systemy bezpieczeństwa.

Używaj aplikacji wyłącznie do **własnej infrastruktury, środowisk testowych lub zakresów, dla których posiadasz odpowiednie uprawnienia do przeprowadzania testów**.

Autor projektu nie ponosi odpowiedzialności za skutki niewłaściwego wykorzystania programu, w tym za problemy z siecią, usługami lub systemami należącymi do osób trzecich.

---

## 📜 Licencja

Projekt jest udostępniany na licencji **GNU General Public License v3.0 (GPL-3.0)**.

**Korzystasz z projektu na własne ryzyko.**
