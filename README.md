# BudgetButlerWeb

[Webseite + Dokumentation](https://SebastianRzk.github.io/BudgetButlerWeb/)

## Umgebungsvariablen
| Wert | Default | Beschreibung |
|------| ------- | ------------ |
| DATABASE_PATH | /data (Docker) bzw. ".." (lokal) | Ordner an dem die Datenbanken gesucht werden sollen. |
| CONFIG_PATH | /data (Docker) bzw. ".." (lokal) | Ordner an dem die Configuration gesucht werden soll. |

## Beispiel Docker-Compose für Offline-App

```
budgetbutler_offline:
    environment:
      - 'DATABASE_PATH=/data'
      - 'CONFIG_PATH=/data'
      - 'TZ=${TZ}'
    image: 'dmkif/budgetbutler-offline:latest'
    ports: 
      - 5000:5000
    volumes:
      - '${USERDIR}/budgetbutler:/data'
```
