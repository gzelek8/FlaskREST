Grzegorz Zelek
Tycjan Woronko

WPROWADZENIE:
Stworzyliśmy część serwerową aplikacji internetowej, zgodnej z architekturą REST. Aplikacja ma za zadanie stworzenie imitacji StackOverflow pozwalającej użytkownikom na dzielenie się swoimi błędami podczas programowania gier w programie Unity Engine. Została napisana w języku Python, wykorzystując framework Flask.

FUNKCJONALNOŚĆ:
•	Wyświetlanie wszystkich opublikowanych błędów – strona domyślna, dostępna dla wszystkich. Wyświetla wszystkie rekordy z tabeli błędów bazy danych, zwracając odpowiedź w postaci jsona. Wykorzystuje polecenie http GET.
•	Publikacja nowych oraz usuwanie, edytowanie starych błędów – pobierając z żądania parametry, tworzy nowy obiekt błędu I dodaje go do bazy danych. Funkcjonalność dostępna tylko dla zalogowanych użytkowników, uprzednio sprawdzając obecność access-tokena w plikach cookies. Zwraca odpowiedź w postaci jsona i wykorzystuje polecenie http GET oraz POST.
•	Rejestracja nowego konta użytkownika - pobierając z żądania parametry, tworzy nowy obiekt użytkownika I dodaje go do bazy danych. Przesłane hasło jest uprzednio szyfrowane korzystając z Python Werkzeug, które umożliwia jednostronne hashowanie hasła. Uniemożliwia to odczytanie go z bazy danych jako tekst oraz szyfrując. Zwraca odpowiedź w postaci jsona i wykorzystuje polecenie http POST.
•	Logowanie na istniejące już konto użytkownika –  na początku sprawdza w plikach cookies, czy użytkownik jest już zalogowany, by uniemożliwić wielokrotne logowanie. Następniei korzystając z autoryzacji przesyłamy nasze parametry (nazwę użytkownika oraz hasło), a na końcu szukamy pasującego w rejestrze użytowników w bazie danych. Zwraca odpowiedź z kodem 200 oraz ustawia access-token w ciasteczkach. Logowanie jest wyjątkiem w architekturze REST i wykorzystuje polecenie http POST z powodów bezpieczeństwa.
•	Wyświetlanie informacji o wszystkich bądź wybranym użytkowniku –  funkcjonalność tylko dostępna dla administratora, uprzednio sprawdzając w access-tokenie czy zalogowany użytkownik ma uprawnienia admina. Wyświetla wszystkie rekordy z tabeli użytkowników bazy danych, zwracając odpowiedź w postaci jsona. Wykorzystuje polecenie http GET.
