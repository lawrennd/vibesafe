"""
Ensure VibeSafe's installed runtime copies (when present) match templates.

VibeSafe dogfoods its installer: the canonical source lives under `templates/`,
and installation copies those files into runtime locations (which are typically
gitignored in downstream projects).

In this repo, those runtime copies may or may not exist depending on whether
the installer has been run. These checks are therefore *conditional*.
"""

from pathlib import Path


def _read_text_normalized(path: Path) -> str:
    # Normalize newlines so the check is stable across platforms/editors.
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def _assert_files_identical(runtime_rel: str, template_rel: str) -> None:
    runtime_path = Path(runtime_rel)
    template_path = Path(template_rel)

    assert template_path.exists(), f"Missing template file: {template_rel}"
    if not runtime_path.exists():
        # Runtime file not installed in this checkout; that's fine.
        return

    runtime_text = _read_text_normalized(runtime_path)
    template_text = _read_text_normalized(template_path)

    assert runtime_text == template_text, (
        "Template/runtime drift detected.\n\n"
        f"- Runtime:   {runtime_rel}\n"
        f"- Template:  {template_rel}\n\n"
        "Fix by syncing templates to the updated runtime file (or vice versa)."
    )


def test_templates_scripts_whats_next_matches_runtime():
    _assert_files_identical(
        "scripts/whats_next.py",
        "templates/scripts/whats_next.py",
    )


def test_templates_scripts_validator_matches_runtime():
    _assert_files_identical(
        "scripts/validate_vibesafe_structure.py",
        "templates/scripts/validate_vibesafe_structure.py",
    )


def test_templates_backlog_update_index_matches_runtime():
    _assert_files_identical(
        "backlog/update_index.py",
        "templates/backlog/update_index.py",
    )


def test_templates_tenets_combine_tenets_matches_runtime():
    # Note: there is also a root-level `combine_tenets.py` which is not the
    # runtime copy for the tenets component. The tenets component uses the one
    # under `tenets/`.
    _assert_files_identical(
        "tenets/combine_tenets.py",
        "templates/tenets/combine_tenets.py",
    )

