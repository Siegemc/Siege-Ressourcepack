#!/usr/bin/env python3
"""Build and validate v1.4.1 from the unchanged v1.3 ZIP (Python 3, stdlib only)."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'Siege-Yom-Kippur-1.21.11-v1.3-optimized.zip'
PREVIOUS = ROOT / 'Siege-Yom-Kippur-1.21.11-v1.4-resources.zip'
TARGET = ROOT / 'Siege-Yom-Kippur-1.21.11-v1.4.1-resources.zip'
OVERLAY = ROOT / 'resource-overrides'
BASE_SHA1 = 'e69367cd7d3e2767d279d9d30f0ec3b9a97e8b33'
ITEMS = {
    'dragon_breath': ('fuel', 'Fuel'),
    'blaze_powder': ('oil', 'Oil'),
    'ghast_tear': ('rubber', 'Rubber'),
    'redstone': ('aluminium', 'Aluminium'),
    'netherite_ingot': ('steel', 'Steel'),
}
LOCALES = ('de_de', 'en_us', 'en_gb')


def sha1(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def overlay_files():
    return {p.relative_to(OVERLAY).as_posix(): p.read_bytes()
            for p in sorted(OVERLAY.rglob('*')) if p.is_file()}


def validate():
    require(sha1(BASE) == BASE_SHA1, 'The v1.3 base archive has changed.')
    overlay = overlay_files()
    expected = {'pack.mcmeta'}
    for item, (resource, _) in ITEMS.items():
        expected.update({f'assets/minecraft/items/{item}.json',
                         f'assets/siege/models/item/resources/{resource}.json',
                         f'assets/siege/textures/item/resources/{resource}.png'})
    expected.update(f'assets/minecraft/lang/{locale}.json' for locale in LOCALES)
    require(set(overlay) == expected, 'Unexpected or missing override file.')
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(TARGET) as pack:
        require(pack.testzip() is None, 'ZIP CRC validation failed.')
        names = pack.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP paths.')
        require(set(names) == set(base.namelist()) | expected, 'Unexpected ZIP entries.')
        preserved = 0
        for name in base.namelist():
            if name not in overlay:
                require(pack.read(name) == base.read(name), f'Base asset changed: {name}')
                preserved += 1
        for name, data in overlay.items():
            require(pack.read(name) == data, f'ZIP differs from source: {name}')
        json_count = 0
        for name in names:
            require('\\' not in name and not name.startswith('/')
                    and '..' not in name.split('/'), f'Unsafe ZIP path: {name}')
            if name.endswith(('.json', '.mcmeta')):
                json.loads(pack.read(name))
                json_count += 1
        meta = json.loads(pack.read('pack.mcmeta'))['pack']
        require(all(meta[key] == 75 for key in ('pack_format', 'min_format', 'max_format')),
                'Expected Minecraft Java 1.21.11 resource format 75.')
        for item, (resource, _) in ITEMS.items():
            model_id = f'siege:item/resources/{resource}'
            definition = json.loads(pack.read(f'assets/minecraft/items/{item}.json'))
            require(definition == {'model': {'type': 'minecraft:model', 'model': model_id}},
                    f'Incorrect default item mapping: {item}')
            model = json.loads(pack.read(f'assets/siege/models/item/resources/{resource}.json'))
            require(model == {'parent': 'minecraft:item/generated',
                              'textures': {'layer0': model_id}}, f'Incorrect model: {resource}')
            png = pack.read(f'assets/siege/textures/item/resources/{resource}.png')
            require(png[:8] == b'\x89PNG\r\n\x1a\n' and png[12:16] == b'IHDR',
                    f'Invalid PNG: {resource}')
            require(struct.unpack('>IIBB', png[16:26]) == (32, 32, 8, 6),
                    f'Expected 32x32 8-bit RGBA texture: {resource}')
        labels = {f'item.minecraft.{item}': label for item, (_, label) in ITEMS.items()}
        for locale in LOCALES:
            require(json.loads(pack.read(f'assets/minecraft/lang/{locale}.json')) == labels,
                    f'Incorrect resource names: {locale}')
    checksum = sha1(TARGET)
    sums = (ROOT / 'SHA1SUMS').read_text(encoding='utf-8')
    for path in (BASE, PREVIOUS, TARGET):
        require(f'{sha1(path)}  {path.name}\n' in sums, f'Missing checksum: {path.name}')
    print(f'OK: {len(names)} ZIP entries; {json_count} JSON documents; '
          f'{preserved} original entries preserved byte-for-byte.')
    print('OK: 5 default item mappings, 5 models, 5 RGBA textures, 3 locales, format 75.')
    print(f'SHA-1: {checksum}\nSize: {TARGET.stat().st_size:,} bytes\nPack: {TARGET}')


def build():
    require(sha1(BASE) == BASE_SHA1, 'The v1.3 base archive has changed.')
    overlay = overlay_files()
    staging = TARGET.with_suffix('.zip.tmp')
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(staging, 'w',
            compression=zipfile.ZIP_DEFLATED, compresslevel=9) as pack:
        for info in base.infolist():
            if info.filename not in overlay:
                pack.writestr(info, base.read(info.filename))
        for name, data in sorted(overlay.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            pack.writestr(info, data, compresslevel=9)
    staging.replace(TARGET)
    # Later releases (v1.5 animated) are built in Siege-xc-xv; keep their checksums and server settings.
    own = {p.name: f'{sha1(p)}  {p.name}\n' for p in (BASE, PREVIOUS, TARGET)}
    other = [line + '\n' for line in (ROOT / 'SHA1SUMS').read_text(encoding='utf-8').splitlines()
             if line.split('  ', 1)[-1] not in own]
    (ROOT / 'SHA1SUMS').write_text(''.join(own.values()) + ''.join(other), encoding='utf-8', newline='\n')
    validate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate the existing release without writing.')
    args = parser.parse_args()
    validate() if args.check else build()
