import streamlit as st
import json
import random

st.set_page_config(
    page_title="Linear Affine Encryption Tool",
    page_icon="🔐",
    layout="centered"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background-color: #101214;
    color: #eeeeee;
}
h1, h2, h3, p, label {
    color: #eeeeee !important;
}
.stTextArea textarea {
    background-color: #191d20;
    color: #eeeeee;
    border: 1px solid #343a40;
    border-radius: 8px;
}
.stButton > button {
    background-color: #20272b;
    color: #ffffff;
    border: 1px solid #41494f;
    border-radius: 7px;
    width: 100%;
}
.stButton > button:hover {
    border-color: #20c997;
    color: #20c997;
}
.ciphertext {
    background: #191d20;
    border: 1px solid #343a40;
    border-radius: 8px;
    padding: 15px;
    color: #55d6e8;
    overflow-wrap: anywhere;
}
.success {
    color: #20c997;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION DATA ----------
if "encrypted" not in st.session_state:
    st.session_state.encrypted = False
    st.session_state.ciphertext = ""
    st.session_state.keys = []
    st.session_state.original = ""
    st.session_state.decrypted = None

# ---------- TITLE ----------
st.title("Linear Affine Encryption Tool")
st.caption("A mathematical model for text encryption and decryption.")

st.markdown("---")

# ---------- INPUT ----------
st.subheader("Enter your message")

message = st.text_area(
    "Message",
    placeholder="Type your message here...",
    height=120,
    label_visibility="collapsed"
)

if st.button("Encrypt Message", type="primary"):
    if not message:
        st.warning("Please enter a message first.")
    else:
        encrypted_values = []
        keys = []

        for char in message:
            a = random.randint(2, 9)
            b = random.randint(1, 9)

            value = a * ord(char) + b
            encrypted_values.append(value)
            keys.append({"a": a, "b": b})

        st.session_state.original = message
        st.session_state.ciphertext = " ".join(map(str, encrypted_values))
        st.session_state.keys = keys
        st.session_state.encrypted = True
        st.session_state.decrypted = None

# ---------- ENCRYPTION RESULT ----------
if st.session_state.encrypted:
    st.markdown("### Encrypted Message")
    st.markdown(
        f'<div class="ciphertext">{st.session_state.ciphertext}</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Characters", len(st.session_state.original))
    with col2:
        st.metric("Cipher Values", len(st.session_state.keys))
    with col3:
        st.metric("Ciphertext Length", len(st.session_state.ciphertext))

    st.markdown("---")

    # ---------- DECRYPTION ----------
    st.subheader("Decryption")

    if st.button("Decrypt Message"):
        decrypted_chars = []

        for value, key in zip(
            map(int, st.session_state.ciphertext.split()),
            st.session_state.keys
        ):
            char_code = (value - key["b"]) // key["a"]
            decrypted_chars.append(chr(char_code))

        st.session_state.decrypted = "".join(decrypted_chars)

    if st.session_state.decrypted is not None:
        st.success("Message decrypted successfully!")
        st.text_area(
            "Decrypted message",
            value=st.session_state.decrypted,
            height=100,
            disabled=True
        )

    # ---------- KEYS ----------
    with st.expander("View Encryption Keys"):
        st.caption("Each character has its own values of a and b.")
        st.json(st.session_state.keys)

    # ---------- DOWNLOAD ----------
    download_data = {
        "original_message": st.session_state.original,
        "encrypted_message": st.session_state.ciphertext,
        "keys": st.session_state.keys,
        "decrypted_message": st.session_state.decrypted
    }

    st.download_button(
        label="Download Project Data",
        data=json.dumps(download_data, indent=4),
        file_name="encryption_data.json",
        mime="application/json"
    )

    # ---------- MATHEMATICAL MODEL ----------
    st.markdown("---")
    st.subheader("Mathematical Model")

    st.latex(r"E(x) = ax + b")
    st.latex(r"D(y) = \frac{y-b}{a}")

    st.write(
        "Here, x is the character's ASCII/Unicode code point, "
        "a and b are numerical parameters, and y is the encrypted value."
    )

    st.caption(
        "Educational demonstration only. This custom method is not "
        "secure enough for protecting real confidential information."
    )
