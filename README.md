# Siege Resourcepack

Siege Yom Kippur **v1.5 Animated** für Minecraft Java Edition **1.21.11**.
Enthält alle Inhalte von v1.4.1 (inklusive der fünf Rohstoffe) und zusätzlich
die First-Person-Animationen aller zwölf Yom-Kippur-Waffen sowie den AT-4.

## Download

[Aktuelles Resourcepack herunterladen](https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.5-animated.zip)

Die ZIP ist das vollständige Pack und kann direkt installiert werden.
Die statische [Version v1.4.1](https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.4.1-resources.zip)
(ohne Waffenanimationen, 5,95 MB) und [v1.4](https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.4-resources.zip)
bleiben als unveränderte Vorgängerversionen verfügbar.

## Waffenanimationen (v1.5)

v1.5 enthält die gebackenen Animations-Posen für AK-47, AT-4, Barrett M82,
Beretta M1951, FN FAL, Galil, Ithaca 37, M16A1, M4A1, Mossberg 500, RPG-7 und Uzi.
Die Posen werden im Repository Siege-xc-xv aus den Blockbench-Modellen kompiliert
(`scripts/build_siegemc_yom_kippur_pack.py`, danach `tools/optimize_gun_pack.py`)
und mit `resource-overrides/` dieses Repositories zusammengeführt.

Die Animationen spielen nur, wenn der Server das Pack mit der Pack-ID
`975cfc35-75b4-4190-a934-d02a54c94378` sendet und die passenden XC-Manifeste in
`plugins/xc/animations/` installiert sind. Pack und Manifeste stammen immer aus
demselben Build. Ohne passende ID zeigt XC die statischen Waffen.

## Neue Rohstoffe

| Minecraft-Gegenstand | Anzeigename | Aussehen |
| --- | --- | --- |
| `minecraft:dragon_breath` | Fuel | Olivgrüner Treibstoffkanister mit X-Verstärkung |
| `minecraft:blaze_powder` | Oil | Dunkles Ölfass mit Rippen und Tropfensymbol |
| `minecraft:ghast_tear` | Rubber | Schwarzer Gummireifen mit grobem Profil |
| `minecraft:redstone` | Aluminium | Sauberer, heller silberblauer Minecraft-Barren |
| `minecraft:netherite_ingot` | Steel | Sauberer, dunkelgrauer Minecraft-Barren mit heller Metallkante |

![Vorschau der fünf fertigen 32×32-Texturen](docs/resources-preview.png)

Die Texturen sind 32×32-Pixel-PNGs mit transparentem Hintergrund. Die normalen
Gegenstände erhalten die neuen Modelle ohne `CustomModelData` oder zusätzliche Mods.
Aluminium und Steel orientieren sich an der klassischen Minecraft-Ingot-Form:
große, ruhige Farbflächen ohne Flecken oder Rost. Die Barren verwenden ein
16×16-Pixelraster, das ohne Glättung auf 32×32 Pixel vergrößert wurde.
Seit v1.4.1 bleibt das vollständige Raster erhalten, statt die Kontur auf 14 Pixel
zu stauchen. Beide Barren haben dadurch die pixelgenaue Kontur des Vanilla-Eisenbarrens.
Die Anzeigenamen gelten in Deutsch, Englisch (US) und Englisch (UK).
Minecraft-IDs, Rezepte und Spielmechaniken bleiben bestehen; platziertes Redstone bleibt Redstone.
Serverseitig gesetzte eigene Namen oder `item_model`-Komponenten haben weiterhin Vorrang.

Alle bestehenden Waffen-, Fahrzeug- und übrigen Asset-Dateien bleiben bytegleich erhalten.
Nur die Pack-Beschreibung wird aktualisiert; die Rohstoffdateien kommen neu hinzu.

## Auf einem Minecraft-Server eintragen

Diese drei Werte in der bestehenden `server.properties` setzen und den Server neu starten:

```properties
resource-pack=https://raw.githubusercontent.com/Siegemc/Siege-Ressourcepack/main/Siege-Yom-Kippur-1.21.11-v1.5-animated.zip
resource-pack-id=975cfc35-75b4-4190-a934-d02a54c94378
resource-pack-sha1=837def4784f800c6b48b86d36f5a769408c8f9ac
```

Die gleichen Werte stehen in `server.properties.example`. Bei einem Hosting-Panel
die URL unter Resource Pack, die ID unter Resource Pack ID und die Prüfsumme unter
Resource Pack SHA-1 eintragen.
Wenn das Pack verpflichtend sein soll, zusätzlich `require-resource-pack=true` setzen.
Bei jeder Änderung der ZIP muss auch die SHA-1-Prüfsumme aktualisiert werden.

## Lokal installieren und prüfen

ZIP herunterladen, in Minecraft unter **Optionen > Ressourcenpakete > Paketordner öffnen**
ablegen und aktivieren. Die ZIP nicht entpacken. Bei mehreren aktiven Packs Siege nach oben setzen.

Für einen Test in einer Welt mit Befehlsrechten:

```mcfunction
/give @s minecraft:dragon_breath
/give @s minecraft:blaze_powder
/give @s minecraft:ghast_tear
/give @s minecraft:redstone
/give @s minecraft:netherite_ingot
```

Inventaransicht, Namen beim Darüberfahren und die Gegenstände in der Hand prüfen.
Bei einem bereits laufenden Client lädt `F3+T` die Ressourcen neu.

## Quelldateien und Neubau

`resource-overrides/` enthält die neuen Item-Definitionen, Modelle, Texturen,
Sprachdateien und `pack.mcmeta`. Die ursprüngliche v1.3-ZIP ist die Basis.
Die Motive wurden mit dem integrierten Imagegen-Werkzeug erstellt und für Minecraft
auf 32×32 Pixel mit harten Alphakanten exportiert.
[Prompts und Exportparameter](docs/texture-prompts.json) liegen im Repository.

Zum Bauen genügt Python 3, ohne zusätzliche Pakete:

```sh
python scripts/build_pack.py
python scripts/build_pack.py --check
```

Der Neubau erzeugt die statische v1.4.1-ZIP. Die animierte v1.5-ZIP wird in
Siege-xc-xv gebaut (siehe oben); `server.properties.example` zeigt auf v1.5. Nach späteren Texturänderungen die Prüfsumme und Größe
in dieser README ebenfalls anpassen.
Die Prüfung kontrolliert ZIP-CRC, alle JSON-Dateien, Item-/Modell-/Texturzuordnungen,
Sprachschlüssel, PNG-Abmessungen, Pack-Format, Server-Prüfsumme und den bytegleichen
Erhalt sämtlicher nicht überschriebener Originaldateien.

## Paketdaten

- Datei: `Siege-Yom-Kippur-1.21.11-v1.5-animated.zip`
- Größe: 17.351.422 Bytes
- SHA-1: `837def4784f800c6b48b86d36f5a769408c8f9ac`
- Pack-ID: `975cfc35-75b4-4190-a934-d02a54c94378`
- Ressourcenpaket-Format: 75 (Minecraft Java 1.21.11)
- `pack.mcmeta` und `assets/` liegen direkt im ZIP-Hauptverzeichnis.

Format-Referenzen: [Minecraft Java 1.21.11](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-11)
und [Item-Definitionen ab Java 1.21.4](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-4).
Server-Einstellungen: [PaperMC server.properties](https://docs.papermc.io/paper/reference/server-properties/).
