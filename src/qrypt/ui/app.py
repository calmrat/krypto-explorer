# -*- coding: utf-8 -*-

"""

Qrypto - Token API - Streamlit App UI

"""

import os
from pathlib import Path
from time import sleep
from urllib.parse import urljoin
from uuid import uuid4

import streamlit as st
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from qrypt.core.db import get_db
from qrypt.tokens.models import BlockchainPlatform, Token
from qrypt.tokens.services.coingecko.ops.admin import pull_tokens

st.set_page_config(page_title="🪙 Qrypt Coin Explorer", layout="centered")

BASE_URL = "http://127.0.0.1:8000"
STATIC_DIR = "./staticserve"
LOGO_UPLOAD_DIR = f"{STATIC_DIR}/logos"  # ensure this folder exists and is served
LOGO_STATIC_DIR = "/static/logos"


if not Path(STATIC_DIR).exists():
    os.makedirs(STATIC_DIR, exist_ok=True)
    st.warning(f"ℹ️ STATIC_DIR '{STATIC_DIR}' created.")


def delayed_rerun(delay: float = 0.3) -> None:
    sleep(delay)  # Just delay the rerun so you can see the success
    st.rerun()


def list_tokens(db: Session):
    """List all tokens in the database."""
    return db.query(Token).order_by(Token.symbol.desc()).all()


def add_token(db: Session, symbol, name, logo_url):
    """Add a new token to the database."""
    token = Token(symbol=symbol, name=name, logo_url=logo_url)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def update_token(db: Session, token_id, symbol, name, logo_url):
    """Update an existing token in the database."""
    token = db.query(Token).filter(Token.id == token_id).first()
    if token:
        token.symbol = symbol
        token.name = name
        token.logo_url = logo_url
        db.commit()
        db.refresh(token)
    return token


def delete_token(db: Session, token_id):
    """Delete a token from the database."""
    token = db.query(Token).filter(Token.id == token_id).first()
    if token:
        db.delete(token)
        db.commit()


def get_token(db: Session, token_id):
    """Get a token by ID."""
    return db.query(Token).filter(Token.id == token_id).first()


# Build the UI
st.title("🪙 Crypto Token Explorer")

session = next(get_db())


def sync_tokens() -> None:
    try:
        added, skipped = pull_tokens()
        st.success(f"Successfully pulled {len(added)} tokens from CoinGecko.")
        if skipped:
            st.warning(f"Skipped {len(skipped)} tokens that already exist.")
    except Exception as e:
        st.error(f"Error pulling tokens: {e}")


tabs = ["📋 View All", "➕ Add Token", "✏️ Update/Delete", "🔍 Search", "🛠️ Admin Panel"]

if "next_active_tab" in st.session_state:
    st.session_state["active_tab"] = st.session_state["next_active_tab"]
    del st.session_state["next_active_tab"]
# Set default active tab
elif "active_tab" not in st.session_state:
    st.session_state.active_tab = "📋 View All"

# Create tab selector with default value
# Create the selectbox tied directly to session state
st.selectbox(
    "☰ Menu",
    options=tabs,
    key="active_tab",  # This makes it persistent + reactive
    index=tabs.index(st.session_state.get("active_tab", tabs[0])),
)

tab_selector = st.session_state.active_tab
# Use conditional blocks to show tab content
if tab_selector == "📋 View All":
    st.subheader("💰 All Tokens")

    PER_PAGE = 3
    tokens = list_tokens(session)

    if not tokens:
        st.info("No tokens found in the database. Attempting to sync...")
        sync_tokens()
        st.success("Tokens pulled successfully.")
        delayed_rerun()

    total_tokens = len(tokens)

    total_pages = (total_tokens - 1) // PER_PAGE + 1

    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_tokens = tokens[start:end]

    st.write(
        f"Showing tokens {start + 1} to {min(end, total_tokens)} of {total_tokens}"
    )

    st.divider()
    st.header("ℹ️ **Token Details** ")

    if st.session_state.get("detail_token_id"):
        token = get_token(session, st.session_state["detail_token_id"])
        if token:
            if st.session_state.get("detail_token_id") == token.id:
                with st.expander(f"🔍 View Details for {token.symbol}"):
                    st.write(f"**Name:** {token.name}")
                    st.write(f"**Symbol:** {token.symbol}")
                    st.write(f"**logo**: {token.logo_url}")
                    if token.logo_url:
                        st.image(urljoin(BASE_URL, token.logo_url), width=80)
                    st.write(f"**Platforms:**")
                    for platform in token.platforms:
                        st.write(f"- {platform.name} ({platform.address})")
                    st.write(f"**Last Updated:** {token.last_updated}")
        else:
            st.error("Token not found.")
            st.session_state["detail_token_id"] = None
    else:
        st.write("Select a token to view details.")

    st.divider()

    for t in paginated_tokens:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # token info, update, delete

        with col1:
            st.markdown(f"**{t.symbol}** – {t.name}")
            if t.logo_url:
                st.image(urljoin(BASE_URL, t.logo_url), width=50)

        with col2:
            if st.button("📝 Update", key=f"view_update_{t.id}"):
                st.session_state["update_selected_token"] = t.id
                st.session_state["next_active_tab"] = "✏️ Update/Delete"
                delayed_rerun()

        with col3:
            if st.button("🗑️ Delete", key=f"view_delete_{t.id}", type="primary"):
                session.delete(t)
                session.commit()
                st.success(f"Deleted {t.symbol}")
                delayed_rerun()

        with col4:
            if st.button(f"🔍 Detail", key=f"view_btn_{t.id}"):
                st.session_state["detail_token_id"] = t.id
                delayed_rerun()
        st.divider()

elif tab_selector == "➕ Add Token":
    st.subheader("Add New Token")

    tokens = list_tokens(session)
    total_tokens = len(tokens)
    st.markdown(f"""
    ℹ️ **Total Tokens:** {total_tokens}
    """)

    with st.form("add_token_form"):
        symbol = st.text_input("Symbol")
        name = st.text_input("Name")
        logo_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])

        # Platform input (single for now)
        platform_name = st.text_input("Platform Name (e.g., Ethereum)")
        platform_address = st.text_input("Platform Address (e.g., 0x123...)")

        submitted = st.form_submit_button("Add Token")

        if submitted:
            # Save logo file if uploaded
            logo_url = None
            if logo_file:
                ext = os.path.splitext(logo_file.name)[1]
                logo_filename = f"{uuid4().hex}{ext}"
                logo_path = os.path.join(LOGO_UPLOAD_DIR, logo_filename)
                with open(logo_path, "wb") as f:
                    f.write(logo_file.read())
                logo_url = urljoin(BASE_URL, f"{LOGO_STATIC_DIR}/{logo_filename}")

            # Create platform and token objects
            platform = BlockchainPlatform(name=platform_name, address=platform_address)
            token = Token(
                symbol=symbol, name=name, logo_url=logo_url, platforms=[platform]
            )

            session.add(token)
            try:
                session.commit()
                session.refresh(token)
                st.session_state["detail_token_id"] = token.id
            except IntegrityError as e:
                st.error(f"Token with symbol '{symbol}' already exists!")
                st.error(e)
                session.rollback()
            else:
                st.success(f"Token '{symbol}' added!")
                delayed_rerun()

    token = get_token(session, st.session_state.get("detail_token_id"))
    if token:
        if st.session_state.get("detail_token_id") == token.id:
            with st.expander(f"🔍 ** {token.symbol} **"):
                st.write(f"**Name:** {token.name}")
                st.write(f"**Symbol:** {token.symbol}")
                st.write(f"**logo**: {token.logo_url}")
                if token.logo_url:
                    st.image(urljoin(BASE_URL, token.logo_url), width=80)
                st.write(f"**Platforms:**")
                for platform in token.platforms:
                    st.write(f"- {platform.name} ({platform.address})")
                st.write(f"**Last Updated:** {token.last_updated}")


elif tab_selector == "✏️ Update/Delete":
    # Preload token if redirected from another tab
    token = None
    selected_id = st.session_state.pop("update_selected_token", None)
    if selected_id is not None:
        token = session.query(Token).filter(Token.id == selected_id).first()

    st.subheader("Update or Delete Token")

    tokens = list_tokens(session)
    total_tokens = len(tokens)
    st.markdown(f"""
    ℹ️ **Total Tokens:** {total_tokens}
    """)

    tokens = list_tokens(session)
    token_names = [f"{t.id} - {t.symbol}" for t in tokens]

    if tokens:
        selected = st.selectbox("Select token to update/delete", token_names)
        selected_id = int(selected.split(" - ")[0])
        token = session.query(Token).filter(Token.id == selected_id).first()

        if token:
            st.subheader(f"Editing: {token.symbol}")
            new_symbol = st.text_input("Symbol", token.symbol)
            new_name = st.text_input("Name", token.name)
            new_logo_url = token.logo_url or ""

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**Current Logo**")
            if token.logo_url:
                st.image(urljoin(BASE_URL, token.logo_url), width=100)
            else:
                st.info("No logo uploaded.")

        with col2:
            st.markdown("**Upload New Logo (optional)**")
            logo_file = st.file_uploader(
                label="", type=["png", "jpg", "jpeg"], key=f"upload_{token.id}"
            )

        if st.button(
            "Update",
            type="secondary",
            use_container_width=True,
            key="update_button",
            disabled=False,
        ):
            if logo_file:
                ext = os.path.splitext(logo_file.name)[1]
                filename = f"{uuid4().hex}{ext}"
                logo_path = os.path.join(LOGO_UPLOAD_DIR, filename)
                with open(logo_path, "wb") as f:
                    f.write(logo_file.read())
                token.logo_url = f"{LOGO_STATIC_DIR}/{filename}"

            token.symbol = new_symbol
            token.name = new_name
            session.commit()
            st.success("Success")
            delayed_rerun()

        if st.button(
            "Delete",
            type="primary",
            use_container_width=True,
            key="delete_button",
            help="Danger action",
            disabled=False,
        ):
            session.delete(token)
            session.commit()
            st.warning("Token deleted.")
            delayed_rerun()

    else:
        st.info("No tokens found.")

elif tab_selector == "🔍 Search":
    st.subheader("Search Tokens by Name")

    tokens = list_tokens(session)
    total_tokens = len(tokens)
    st.markdown(f"""
    ℹ️ **Total Tokens:** {total_tokens}
    """)

    query = st.text_input("Enter name to search for")

    if query:
        like_pattern = f"%{query}%"
        results = (
            session.query(Token)
            .filter(Token.name.ilike(like_pattern))
            .order_by(Token.name.desc())
            .all()
        )

        st.write(f"Found {len(results)} result(s):")

        for t in results:
            col1, col2, col3 = st.columns([3, 1, 1])  # info, update, delete

            with col1:
                st.markdown(f"**{t.symbol}** – {t.name}")
                if t.logo_url:
                    st.image(urljoin(BASE_URL, t.logo_url), width=50)

            with col2:
                if st.button("📝 Update", key=f"update_{t.id}"):
                    st.session_state["update_selected_token"] = t.id
                    st.session_state["next_active_tab"] = "✏️ Update/Delete"
                    delayed_rerun()  # redirect to Update tab

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{t.id}", type="primary"):
                    session.delete(t)
                    session.commit()
                    st.success(f"Deleted token: {t.symbol}")
                    delayed_rerun()

            st.divider()
    else:
        st.info("Type in the box above to search by name.")

elif tab_selector == "🛠️ Admin Panel":
    st.subheader("🛠️ Admin Panel")

    tokens = list_tokens(session)
    total_tokens = len(tokens)
    st.markdown(f"""
    ℹ️ **Total Tokens:** {total_tokens}
    """)

    st.markdown("Perform administrative actions below:")

    if st.button("🔄 Pull Tokens from CoinGecko", use_container_width=True):
        sync_tokens()
        st.success("Tokens pulled successfully.")
        delayed_rerun(15)

    st.divider()

    st.subheader("Danger Zone")
    st.warning("This will permanently delete all tokens in the database.")

    confirm_delete = st.checkbox("Yes, I really want to delete all tokens")

    if confirm_delete:
        st.markdown("COMING SOON")

    if st.button(
        "🗑️ Delete All Tokens",
        use_container_width=True,
        type="primary",
        disabled=True,
    ):
        session.query(Token).delete()
        session.commit()
        st.success("All tokens deleted.")
        delayed_rerun()
    st.divider()

    st.markdown("### Other Admin Actions")
    # Add more admin actions here if needed
    st.markdown("*More actions coming soon...*")
