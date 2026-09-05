# Chrome Auto Scroll

Apre una pagina in Google Chrome e la fa scorrere da sola, a velocità costante. Utile per leggere a mani libere, per registrare uno scroll fluido o per tenere viva una pagina lunga senza toccare il mouse.

L'interfaccia è un pannello Tkinter: si incolla l'URL, si regolano i due cursori, si preme avvio.

## Requisiti

- Python 3.9+
- macOS — l'apertura e l'attivazione di Chrome usano `open -a` e `osascript`, quindi lo script funziona solo su macOS
- [PyAutoGUI](https://pyautogui.readthedocs.io/) per l'evento di scroll; Tkinter è incluso in Python

```bash
pip install -r Requirement.txt
```

Alla prima esecuzione macOS chiede il permesso di Accessibilità per il terminale: senza quello PyAutoGUI non può inviare lo scroll.

## Uso

```bash
python3 Autoscroll.py
```

1. Incolla l'URL nel campo in alto
2. **Scroll Amount** — pixel per singolo evento di scroll (1-50). Valori bassi = movimento più fluido
3. **Speed** — intervallo tra un evento e il successivo, in centesimi di secondo (0,01-0,50 s)
4. **Open & Start Scrolling** apre Chrome, lo porta in primo piano e avvia lo scorrimento
5. **Stop Scrolling** lo ferma

Lo scorrimento gira su un thread separato, così la finestra resta reattiva mentre la pagina scende.

## Interruzione di emergenza

`pyautogui.FAILSAFE` è attivo: portando il puntatore nell'angolo in alto a sinistra dello schermo lo script si interrompe subito, anche se la finestra non è raggiungibile.

## Licenza

GPL-3.0 — vedi [LICENSE](LICENSE).
