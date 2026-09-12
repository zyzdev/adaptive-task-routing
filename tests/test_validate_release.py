from __future__ import annotations

import contextlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_release_under_test", PROJECT_ROOT / "scripts/validate_release.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name) / "adaptive-task-routing"
        shutil.copytree(
            PROJECT_ROOT,
            self.root,
            ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc", ".git", ".venv", "build", ".release-backups"),
        )

    @contextlib.contextmanager
    def temporary_root(self):
        previous_root = VALIDATOR.ROOT
        previous_argv = sys.argv
        VALIDATOR.ROOT = self.root
        sys.argv = ["validate_release.py", "--source-only"]
        try:
            yield
        finally:
            VALIDATOR.ROOT = previous_root
            sys.argv = previous_argv

    def test_source_validation_accepts_current_release(self) -> None:
        with self.temporary_root():
            self.assertEqual(VALIDATOR.main(), 0)

    def test_source_validation_rejects_missing_shared_file(self) -> None:
        (self.root / "shared/defaults.yaml").unlink()
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Missing required file: shared/defaults.yaml"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_stale_fallback_registry(self) -> None:
        path = self.root / "shared/model-catalogs/openai-codex-cli.json"
        registry = json.loads(path.read_text())
        registry["expires_at"] = registry["observed_at"]
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Bundled fallback registry is stale"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_stale_gemini_fallback_registry(self) -> None:
        path = self.root / "shared/model-catalogs/gemini-cli.json"
        registry = json.loads(path.read_text())
        registry["expires_at"] = registry["observed_at"]
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Gemini fallback registry is stale"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_legacy_gemini_model(self) -> None:
        path = self.root / "shared/model-catalogs/gemini-cli.json"
        registry = json.loads(path.read_text())
        registry["models"][1]["model"] = "gemini-1.5-pro"
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Invalid Gemini fallback models"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_incomplete_fallback_model_metadata(self) -> None:
        path = self.root / "shared/model-catalogs/openai-codex-cli.json"
        registry = json.loads(path.read_text())
        del registry["models"][0]["selection_guidance"]
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Invalid fallback model"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_incomplete_fallback_inventory(self) -> None:
        path = self.root / "shared/model-catalogs/openai-codex-cli.json"
        registry = json.loads(path.read_text())
        registry["models"].pop()
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Incomplete bundled fallback registry"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_missing_fallback_reference_scope(self) -> None:
        path = self.root / "shared/model-catalogs/openai-codex-cli.json"
        registry = json.loads(path.read_text())
        del registry["reference_surfaces"]
        path.write_text(json.dumps(registry, indent=2) + "\n")
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Invalid fallback cross-surface reference scope"
        ):
            VALIDATOR.main()

    def test_source_validation_rejects_changed_permission_escalation_policy(self) -> None:
        path = self.root / "shared/defaults.yaml"
        defaults = VALIDATOR.yaml.load(path.read_text(), Loader=VALIDATOR.UniqueLoader)
        defaults["discovery"]["permission_escalation"]["recommendation_default"] = "prompt"
        path.write_text(VALIDATOR.yaml.safe_dump(defaults, sort_keys=False))
        with self.temporary_root(), self.assertRaisesRegex(
            ValueError, "Invalid permission escalation defaults"
        ):
            VALIDATOR.main()

    def test_package_rejects_broken_relative_link(self) -> None:
        archive = self.root / "broken-link.zip"
        expected = {"README.md": b"[missing](docs/not-there.md)\n"}
        self._write_archive(archive, expected)

        with self.assertRaisesRegex(ValueError, "broken packaged link"):
            VALIDATOR.validate_package(archive, expected)

    def test_package_rejects_stale_payload(self) -> None:
        archive = self.root / "stale.zip"
        self._write_archive(archive, {"README.md": b"old contents\n"})

        with self.assertRaisesRegex(ValueError, "stale or modified payload"):
            VALIDATOR.validate_package(archive, {"README.md": b"new contents\n"})

    def test_package_rejects_foreign_manifest(self) -> None:
        archive = self.root / "foreign-manifest.zip"
        expected = {
            ".codex-plugin/plugin.json": b"{}\n",
            "README.md": b"release\n",
        }
        self._write_archive(
            archive,
            {**expected, ".claude-plugin/plugin.json": b"{}\n"},
        )

        with self.assertRaisesRegex(ValueError, "unexpected=.*claude-plugin"):
            VALIDATOR.validate_package(archive, expected)

    def test_checksums_reject_wrong_digest(self) -> None:
        dist = self.root / "dist"
        dist.mkdir()
        archive = dist / "adaptive-task-routing-openai-0.3.1.zip"
        archive.write_bytes(b"archive payload")
        (dist / "SHA256SUMS").write_text(
            f"{'0' * 64}  {archive.name}\n", encoding="utf-8"
        )

        with self.assertRaisesRegex(ValueError, "does not match"):
            VALIDATOR.validate_checksums(dist, [archive])

    def test_rejects_changed_trigger(self):
        path = self.root / "skills/adaptive-task-routing/SKILL.md"
        path.write_text(path.read_text().replace("Primary routing entrypoint", "Changed routing entrypoint", 1))
        with self.assertRaisesRegex(ValueError, "Trigger definition changed"):
            VALIDATOR.validate_source(self.root)

    def test_rejects_duplicate_yaml_key(self):
        data = b"---\nname: sample\nname: sample\ndescription: example\n---\nInstructions\n"
        with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
            VALIDATOR.frontmatter(data, "sample")

    def test_rejects_missing_presentation_and_unshipped_asset(self):
        path = self.root / "release.json"
        config = json.loads(path.read_text())
        config["interface"]["logo"] = "./assets/not-shipped.png"
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "Asset not in release"):
            VALIDATOR.validate_source(self.root)
        del config["interface"]["logo"]
        config["interface"]["defaultPrompt"] = ["x" * 129]
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "Invalid starter prompts"):
            VALIDATOR.validate_source(self.root)

    def test_rejects_nested_foreign_manifest(self):
        folder = self.root / "skills/adaptive-task-routing/.claude-plugin"
        folder.mkdir()
        (folder / "plugin.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Foreign or misplaced manifest"):
            VALIDATOR.validate_source(self.root)

    def test_rejects_extra_empty_stage_directory(self):
        from build_release import build
        dist = build(self.root)
        (dist / "gemini/adaptive-task-routing/extra-empty").mkdir()
        with self.assertRaisesRegex(ValueError, "Extra staging directory"):
            VALIDATOR.validate_dist(self.root, dist)

    def test_rejects_empty_skill_body(self):
        with self.assertRaisesRegex(ValueError, "Empty Skill body"):
            VALIDATOR.frontmatter(b"---\nname: sample\ndescription: example\n---\n", "sample")

    def test_rejects_invalid_semver_and_missing_changelog(self):
        path = self.root / "release.json"
        config = json.loads(path.read_text())
        for version in ("01.2.3", "1.2", "1.2.3-01", "9.9.9"):
            with self.subTest(version=version):
                config["version"] = version
                path.write_text(json.dumps(config))
                with self.assertRaises(ValueError):
                    VALIDATOR.validate_source(self.root)

    def test_rejects_extra_skill(self):
        folder = self.root / "skills/extra"
        folder.mkdir()
        (folder / "SKILL.md").write_text("---\nname: extra\ndescription: test\n---\nTest\n")
        with self.assertRaisesRegex(ValueError, "exactly three Skills"):
            VALIDATOR.validate_source(self.root)

    def test_links_check_reference_style_anchors_and_escapes(self):
        good = {"README.md": b"[go][target]\n\n[target]: docs/guide.md#hello-world\n",
                "docs/guide.md": b"# Hello world\n"}
        VALIDATOR.validate_links(good)
        for link in ("docs/guide.md#missing", "../outside.md", "/absolute.md", "docs/%2e%2e/%2e%2e/out.md"):
            with self.subTest(link=link), self.assertRaises(ValueError):
                VALIDATOR.validate_links({**good, "README.md": f"[go]({link})\n".encode()})

    def test_rejects_undefined_reference(self):
        with self.assertRaisesRegex(ValueError, "Undefined reference"):
            VALIDATOR.validate_links({"README.md": b"[go][missing]\n"})

    def test_rejects_duplicate_zip_members(self):
        import warnings
        archive = self.root / "duplicate.zip"
        with warnings.catch_warnings(), zipfile.ZipFile(archive, "w") as package:
            warnings.simplefilter("ignore")
            package.writestr("README.md", b"a")
            package.writestr("README.md", b"b")
        with self.assertRaisesRegex(ValueError, "Duplicate ZIP entry"):
            VALIDATOR.validate_package(archive, {"README.md": b"b"})

    def test_rejects_unsafe_archive_paths_and_junk(self):
        for name in ("../escape", "/absolute", "a/../b", "a\\b", ".DS_Store", "__pycache__/x.pyc", "dist/old.zip"):
            with self.subTest(name=name):
                archive = self.root / "unsafe.zip"
                self._write_archive(archive, {name: b"x"})
                with self.assertRaisesRegex(ValueError, "Unsafe ZIP entry"):
                    VALIDATOR.validate_package(archive, {name: b"x"})

    def test_rejects_zip_symlink(self):
        archive = self.root / "symlink.zip"
        with zipfile.ZipFile(archive, "w") as package:
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = 0o120777 << 16
            package.writestr(info, "outside")
        with self.assertRaisesRegex(ValueError, "Unsafe ZIP entry"):
            VALIDATOR.validate_package(archive, {"link": b"outside"})

    def test_rejects_insufficient_submission_cases(self):
        path = self.root / "tests/behavioral-matrix.json"
        matrix = json.loads(path.read_text())
        matrix["cases"] = [c for c in matrix["cases"] if c["id"] != "N03"]
        path.write_text(json.dumps(matrix))
        with self.assertRaisesRegex(ValueError, "3 submission negative"):
            VALIDATOR.validate_matrix(self.root)

    def test_behavioral_pass_requires_evidence(self):
        path = self.root / "tests/behavioral-matrix.json"
        matrix = json.loads(path.read_text())
        matrix["cases"][0]["results"]["codex"]["status"] = "pass"
        path.write_text(json.dumps(matrix))
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            VALIDATOR.validate_matrix(self.root)

    def test_surface_matrix_requires_every_surface_and_case(self):
        path = self.root / "tests/surface-matrix.json"
        original = json.loads(path.read_text())
        for remove_surface in (True, False):
            matrix = json.loads(json.dumps(original))
            if remove_surface:
                del matrix["surfaces"]["codex-app"]
            else:
                del matrix["surfaces"]["codex-cli"]["R01"]
            path.write_text(json.dumps(matrix))
            with self.assertRaisesRegex(ValueError, "Missing"):
                VALIDATOR.validate_matrix(self.root)

    def test_surface_pass_requires_evidence(self):
        path = self.root / "tests/surface-matrix.json"
        matrix = json.loads(path.read_text())
        matrix["surfaces"]["chatgpt-web"]["R01"]["status"] = "pass"
        path.write_text(json.dumps(matrix))
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            VALIDATOR.validate_matrix(self.root)

    def test_only_reviewed_skill_helper_is_packaged(self):
        path = self.root / "skills/research-model-router/scripts/unreviewed.py"
        path.write_text("print('unexpected')")
        with self.assertRaisesRegex(ValueError, "Skill helper"):
            VALIDATOR.validate_source(self.root)

    def test_missing_discovery_guide_rejected(self):
        (self.root / "shared/hosts/gemini.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required"):
            VALIDATOR.validate_source(self.root)

    def test_build_reproducibility_cleanup_and_platform_isolation(self):
        from build_release import build
        from release_lib import PLATFORMS, MANIFESTS, metadata, archive_name, stage_path
        dist = build(self.root)
        config = metadata(self.root)
        first = {p.name: p.read_bytes() for p in dist.glob("*.zip")}
        self.assertEqual(len(first), 3)
        # Old output is preserved, but must never leak into the new release.
        (dist / "old-version.zip").write_bytes(b"old")
        (dist / ".DS_Store").write_bytes(b"junk")
        (self.root / "skills/.DS_Store").write_bytes(b"source junk")
        build(self.root)
        self.assertEqual(first, {p.name: p.read_bytes() for p in dist.glob("*.zip")})
        self.assertFalse((dist / "old-version.zip").exists())
        self.assertTrue(list((self.root / ".release-backups").glob("*/dist/old-version.zip")))
        all_manifests = set().union(*MANIFESTS.values())
        for platform in PLATFORMS:
            with zipfile.ZipFile(dist / archive_name(config, platform)) as package:
                self.assertEqual(set(package.namelist()) & all_manifests, MANIFESTS[platform])
                self.assertIn("shared/defaults.yaml", package.namelist())
                for name in ("adaptive-task-routing", "task-context-router", "research-model-router"):
                    packaged = package.read(f"skills/{name}/SKILL.md")
                    source = (self.root / f"skills/{name}/SKILL.md").read_bytes()
                    if platform == "gemini" and name == "adaptive-task-routing":
                        self.assertTrue(packaged.startswith(source.rstrip()))
                        self.assertIn(b"Generated Gemini dependency appendix", packaged)
                    else:
                        self.assertEqual(packaged, source)
            self.assertEqual(stage_path(dist, config, platform).name, "adaptive-task-routing")
        VALIDATOR.validate_dist(self.root, dist)

    def test_platform_packages_include_automatic_activation(self):
        from release_lib import AUTO_ACTIVATION, payload

        openai = payload(self.root, "openai")
        legacy = json.loads(openai[".codex-plugin/plugin.json"])
        codex_handlers = legacy["hooks"]["hooks"]["UserPromptSubmit"][0]["hooks"]
        self.assertEqual(codex_handlers[0]["type"], "command")
        self.assertIn(AUTO_ACTIVATION["openai"], codex_handlers[0]["command"])

        claude = payload(self.root, "claude")
        claude_hooks = json.loads(claude["hooks/hooks.json"])
        claude_handlers = claude_hooks["hooks"]["UserPromptSubmit"][0]["hooks"]
        self.assertIn(AUTO_ACTIVATION["claude"], claude_handlers[0]["command"])

        gemini = payload(self.root, "gemini")
        gemini_manifest = json.loads(gemini["gemini-extension.json"])
        self.assertEqual(gemini_manifest["contextFileName"], "GEMINI.md")
        self.assertIn(AUTO_ACTIVATION["gemini"], gemini["GEMINI.md"].decode())
        self.assertIn("Embedded automatic coordinator contract",
                      gemini["GEMINI.md"].decode())

    def test_rejects_modified_automatic_activation(self):
        from release_lib import payload

        entries = payload(self.root, "claude")
        hook = json.loads(entries["hooks/hooks.json"])
        hook["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"] = "echo bypass"
        entries["hooks/hooks.json"] = json.dumps(hook).encode()
        with self.assertRaisesRegex(ValueError, "Claude automatic routing hook mismatch"):
            VALIDATOR.validate_manifests(entries, "claude", VALIDATOR.metadata(self.root))

    def test_invalid_source_preserves_previous_dist(self):
        from build_release import build
        dist = build(self.root)
        sums = (dist / "SHA256SUMS").read_bytes()
        (self.root / "shared/defaults.yaml").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required"):
            build(self.root)
        self.assertEqual((dist / "SHA256SUMS").read_bytes(), sums)

    def test_rejects_extra_or_modified_staging_file(self):
        from build_release import build
        dist = build(self.root)
        path = dist / "claude/adaptive-task-routing/foreign.txt"
        path.write_text("foreign")
        with self.assertRaisesRegex(ValueError, "staging payload"):
            VALIDATOR.validate_dist(self.root, dist)

    def test_rejects_source_symlink_and_dist_symlink(self):
        from build_release import build
        path = self.root / "skills/link"
        path.symlink_to(self.root / "shared")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            VALIDATOR.validate_source(self.root)
        path.unlink()
        (self.root / "dist").symlink_to(self.root / "shared")
        with self.assertRaisesRegex(ValueError, "dist must be"):
            build(self.root)

    def test_checksum_rejects_duplicate_and_missing_entries(self):
        dist = self.root / "dist"
        dist.mkdir()
        archive = dist / "example.zip"
        archive.write_bytes(b"example")
        digest = VALIDATOR.digest(archive.read_bytes())
        for text in ("", f"{digest}  example.zip\n{digest}  example.zip\n"):
            (dist / "SHA256SUMS").write_text(text)
            with self.assertRaises(ValueError):
                VALIDATOR.validate_checksums(dist, [archive])

    @staticmethod
    def _write_archive(archive: Path, entries: dict[str, bytes]) -> None:
        with zipfile.ZipFile(archive, "w") as package:
            for name, data in entries.items():
                package.writestr(name, data)


if __name__ == "__main__":
    unittest.main()
