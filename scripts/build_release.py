#!/usr/bin/env python3
"""Build exactly three archives from canonical sources; never publish anything."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

from release_lib import ROOT, PLATFORMS, archive_name, digest, metadata, payload, stage_path


def write_zip(path, entries):
    # Fixed metadata + sorted paths make repeated builds byte-identical in the same toolchain.
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries.items()):
            item = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, data, compresslevel=9)


def build(root=ROOT):
    from validate_release import validate_source, validate_dist

    root = root.resolve()
    validate_source(root)
    dist = root / "dist"
    if dist.is_symlink() or (dist.exists() and not dist.is_dir()):
        raise ValueError("dist must be a real directory, not a symlink or file")
    config = metadata(root)
    # Build and validate in isolation before touching the previous release.
    with tempfile.TemporaryDirectory(prefix="atr-build-") as temporary:
        staging = Path(temporary)
        sums = []
        for platform in PLATFORMS:
            entries = payload(root, platform)
            destination = stage_path(staging, config, platform)
            for name, data in entries.items():
                target = destination / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            archive = staging / archive_name(config, platform)
            write_zip(archive, entries)
            sums.append(f"{digest(archive.read_bytes())}  {archive.name}\n")
        (staging / "SHA256SUMS").write_text("".join(sums), encoding="utf-8")
        validate_dist(root, staging)
        if dist.exists():
            backups = root / ".release-backups"
            if backups.is_symlink():
                raise ValueError("Backup directory must not be a symlink")
            backups.mkdir(exist_ok=True)
            backup = Path(tempfile.mkdtemp(prefix="dist-", dir=backups)) / "dist"
            os.replace(dist, backup)
            print(f"Previous dist preserved at {backup}")
        shutil.copytree(staging, dist)
    print(f'Built {len(PLATFORMS)} releases at {dist} (version {config["version"]})')
    return dist


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
