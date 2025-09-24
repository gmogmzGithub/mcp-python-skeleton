"""Tests for the CLI entrypoint in mcpskeleton.__main__.py.

This file follows the same style as other tests in this project and only
validates behavior observable at the boundary (arguments and env). The
server launch is stubbed so tests run instantly.
"""

from typing import Any, Dict

from click.testing import CliRunner


class TestMainEntrypoint:
    """Test suite for the click entrypoint."""

    def _invoke_main(self, monkeypatch, env: Dict[str, str], debug_flag: bool):
        # Import lazily so monkeypatches can target the module namespace
        import mcpskeleton.__main__ as entry

        calls: Dict[str, Any] = {}

        def fake_run(*args, **kwargs):  # mimic uvicorn.run
            calls["args"] = args
            calls["kwargs"] = kwargs
            return None

        # Patch uvicorn.run used inside entry module
        monkeypatch.setattr(entry.uvicorn, "run", fake_run)

        # Apply environment variables for this invocation
        for k, v in env.items():
            monkeypatch.setenv(k, v)

        runner = CliRunner()
        result = runner.invoke(entry.main, ["--debug"] if debug_flag else [])

        # Click should exit cleanly since fake_run returns quickly
        assert result.exit_code == 0, result.output

        return calls

    def test_entrypoint_runs_with_debug(self, monkeypatch):
        calls = self._invoke_main(
            monkeypatch,
            env={
                "PORT0": "8091",
                "HOST0": "127.0.0.1",
            },
            debug_flag=True,
        )

        # Validate uvicorn.run invocation
        args = calls["args"]
        kwargs = calls["kwargs"]

        # Since we changed to pass the app directly, args[0] is now the app instance
        assert kwargs["host"] == "127.0.0.1"
        assert kwargs["port"] == 8091
        # When --debug is set, code forces workers=1 and reload=True
        assert kwargs["workers"] == 1
        assert kwargs["reload"] is True

    def test_entrypoint_respects_workers_env(self, monkeypatch):
        calls = self._invoke_main(
            monkeypatch,
            env={
                "PORT0": "8092",
                "HOST0": "0.0.0.0",
                "WORKERS": "3",
            },
            debug_flag=False,
        )

        kwargs = calls["kwargs"]
        assert kwargs["port"] == 8092
        assert kwargs["host"] == "0.0.0.0"
        assert kwargs["workers"] == 3
        assert kwargs["reload"] is False
