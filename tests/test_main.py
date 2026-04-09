"""Test basic project functionality."""


def test_game_import() -> None:
    """Check project imports successfully."""
    import monorail  # noqa: F401


def test_main_exists():
    """Check main function exists."""
    from monorail.main import main

    assert callable(main)
