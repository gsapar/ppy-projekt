# Menedżer haseł

## Przegląd

Prosty menedżer haseł, który pozwala użytkownikom przechowywać, generować, edytować i zarządzać ich danymi uwierzytelniającymi. Aplikacja zapewnia szyfrowanie danych wrażliwych, sprawdzenie naruszeń haseł za pomocą API Have I Been Pwned (HIBP) oraz interaktywną nawigację terminalową dla łatwości użytkowania.

---

## Funkcje

### Zarządzanie kontami
- Dodawanie kont
- Usuwanie kont
- Edycja danych kont
- Wyświetlanie listy wszystkich kont

### Bezpieczeństwo
- Szyfrowanie danych przy użyciu algorytmu AES
- Sprawdzanie naruszeń haseł za pomocą API HIBP
- Ostrzeżenia przed użyciem naruszonych haseł

### Wygoda
- Interaktywne menu terminalowe
- Dowolność ścieżki zapisu pliku

---

## Instalacja

### Wymagania
- Python w wersji 3.7 lub wyższej
- Biblioteki Python:
  - `cryptography`
  - `requests`

### Kroki instalacji
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/username/password-manager.git
   ```

2. Przejdź do katalogu projektu:
   ```bash
   cd ppy-projekt
   ```

3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

---

## Użycie

Uruchom aplikację za pomocą następującego polecenia:
```bash
python main.py
```

### Opcje interaktywnego menu
- **Add account**: Dodaj nowe konto z opcjonalnym generowaniem hasła.
- **Get account**: Wyświetl wszystkie dane dotyczące wybranego konta.
- **Edit account**: Zmień szczegóły istniejącego konta.
- **Delete account**: Usuń konto na stałe.
- **List all accounts**: Wyświetl wszystkie przechowywane konta.
- **Save to file**: Zaszyfruj i zapisz konta do pliku. Wymagane jest podanie relatywnej ścieżki do pliku (np. jeśli ma być zapisany w obecnym katalogu to jest to ./plik).
- **Load file**: Odszyfruj i wczytaj konta z pliku. Wymagane jest podanie relatywnej ścieżki do pliku (np. jeśli plik jest w obecnym katalogu to jest to ./plik). 
- **Exit**: Zamknij menedżer haseł.

---

## Dokumentacja API

### Sprawdzanie naruszenia haseł
Aplikacja wykorzystuje API **Have I Been Pwned** do sprawdzania, czy dane hasło pojawiło się w naruszeniach danych.

1. Hasło jest haszowane za pomocą algorytmu SHA-1.
2. Pierwsze 5 znaków hasza jest wysyłane do API.
3. API zwraca listę haszy, które pasują do podanego prefiksu.
4. Sprawdzane jest, czy pozostała część hasza pasuje do któregoś wyniku.

### Szyfrowanie danych
1. Dane konta są konwertowane do formatu JSON.
2. Aplikacja generuje klucz szyfrujący na podstawie hasła głównego użytkownika.
3. Dane są szyfrowane za pomocą szyfrowania AES i zapisywane do pliku.

---

## Przykłady

### Dodanie konta z generowaniem hasła
1. Wybierz "Dodaj konto" w menu.
2. Wprowadź nazwę konta i nazwę użytkownika.
3. Wybierz opcję generowania hasła.
4. Określ długość i parametry hasła (wielkie litery, cyfry, znaki specjalne).
5. Zapisz szczegóły konta.

### Edytowanie konta
1. Wybierz "Edytuj konto" w menu.
2. Wprowadź nazwę konta do edycji.
3. Zaktualizuj nazwę, nazwę użytkownika lub hasło w razie potrzeby.

### Sprawdzanie naruszeń haseł
1. Jeśli hasło zostało naruszone, aplikacja ostrzega użytkownika.
2. Użytkownik może zdecydować, czy kontynuować, czy anulować operację.

