# Siege Resourcepack

Siege Yom Kippur v1.3 (optimized) fuer Minecraft Java Edition 1.21.11.

## Download

[Texturepack herunterladen](https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.3-optimized.zip)

Der Direktdownload funktioniert ohne Anmeldung, sobald dieses Repository oeffentlich ist.
Die ZIP wurde unveraendert hochgeladen; lediglich der lokale Namenszusatz ` (1)` wurde entfernt.

## Auf einem Minecraft-Server eintragen

Diese beiden Werte in der bestehenden `server.properties` setzen und den Server neu starten:

```properties
resource-pack=https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.3-optimized.zip
resource-pack-sha1=e69367cd7d3e2767d279d9d30f0ec3b9a97e8b33
```

Die gleichen Werte stehen in `server.properties.example`. Bei einem Hosting-Panel die URL unter Resource Pack und die Pruefsumme unter Resource Pack SHA-1 eintragen.
Wenn das Pack verpflichtend sein soll, zusaetzlich `require-resource-pack=true` setzen.
Bei jeder Aenderung der ZIP muss auch die SHA-1-Pruefsumme aktualisiert werden.

## Lokal installieren

ZIP herunterladen, in Minecraft unter Optionen > Ressourcenpakete > Paketordner oeffnen ablegen und aktivieren. Die ZIP nicht entpacken.

## Paketdaten

- Datei: `Siege-Yom-Kippur-1.21.11-v1.3-optimized.zip`
- Groesse: 5.883.063 Bytes
- SHA-1: `e69367cd7d3e2767d279d9d30f0ec3b9a97e8b33`
- Ressourcenpaket-Format laut `pack.mcmeta`: 75
- `pack.mcmeta` und `assets/` liegen direkt im ZIP-Hauptverzeichnis.

Format-Referenz: [Minecraft Java Edition 1.21.11](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-11).
Server-Einstellungen: [PaperMC server.properties](https://docs.papermc.io/paper/reference/server-properties/).
