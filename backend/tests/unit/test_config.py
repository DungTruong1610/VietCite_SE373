from __future__ import annotations

import pytest

from geo.config import DEFAULT_PRICES, load_settings


def test_offline_disables_every_feature_and_uses_mock(settings):
    assert settings.offline is True
    assert settings.features == {"deepseek": False, "jina": False, "gemini": False}
    assert settings.model_for("writer") == "mock"


def test_roles_map_to_models_when_key_present(monkeypatch, tmp_path):
    monkeypatch.setenv("GEO_OFFLINE", "false")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "x" * 10)
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-chat")
    monkeypatch.setenv("DEEPSEEK_REASONING_MODEL", "deepseek-reasoner")
    s = load_settings(env_file=tmp_path / "none.env")
    assert s.features["deepseek"] is True
    assert s.model_for("writer") == "deepseek-chat"
    assert s.model_for("judge") == "deepseek-reasoner"
    with pytest.raises(ValueError):
        s.model_for("unknown-role")


def test_price_override_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("GEO_PRICE_DEEPSEEK_CHAT", "1,2,0.5")
    s = load_settings(env_file=tmp_path / "none.env")
    assert s.price_for("deepseek-chat").output == 2
    assert s.price_for("mock") == DEFAULT_PRICES["mock"]


def test_secrets_never_appear_in_repr(monkeypatch, tmp_path):
    from geo.providers.jina import JinaClient

    secret = "sk-" + "s" * 32
    monkeypatch.setenv("DEEPSEEK_API_KEY", secret)
    monkeypatch.setenv("JWT_SECRET", "jwt-" + "j" * 32)
    s = load_settings(env_file=tmp_path / "none.env")
    assert secret not in repr(s) and "jwt-jjj" not in repr(s)
    client = JinaClient(api_key="jina_" + "k" * 40)
    try:
        assert "jina_kkk" not in repr(client)
    finally:
        client.close()
