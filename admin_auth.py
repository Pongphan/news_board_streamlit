"""Small server-side password gate for the administrative page."""

from __future__ import annotations

import hashlib
import hmac

import streamlit as st


# SHA-256 digest of the requested default password. Keeping the digest instead
# of the plaintext avoids exposing the default directly in application code.
DEFAULT_ADMIN_PASSWORD_HASH = (
    "1b8828f30a7f0a42eb332649b6440c2ccddc0edd84024465ca6e15929140f080"
)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def configured_password_hash() -> str:
    """Use a Streamlit secret when configured, otherwise use the requested default."""

    try:
        configured = str(st.secrets["admin"]["password"]).strip()
    except (KeyError, FileNotFoundError, TypeError):
        configured = ""
    except Exception:
        configured = ""
    return _sha256(configured) if configured else DEFAULT_ADMIN_PASSWORD_HASH


def verify_admin_password(candidate: str, expected_hash: str | None = None) -> bool:
    """Compare password digests in constant time."""

    return hmac.compare_digest(_sha256(candidate), expected_hash or configured_password_hash())


def is_admin_authenticated() -> bool:
    return bool(st.session_state.get("admin_authenticated", False))


def sign_in_admin() -> None:
    st.session_state["admin_authenticated"] = True


def sign_out_admin() -> None:
    for key in ("admin_authenticated", "admin_password", "confirm_delete_id"):
        st.session_state.pop(key, None)
