import streamlit as st
import json
import random

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Linear Affine Encryption Tool",
    page_icon="🔐",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

/* Main background and text */
.stApp {
    background-color: #101214;
    color: #eeeeee;
}

/* Headings and labels */
h1, h2, h3, p, label {
    color: #eeeeee !important;
}

/* Text input area */
.stTextArea textarea {
    background-color: #191d20 !important;
    color: #eeeeee !important;
    border: 1px solid #41494f;
    border-radius: 8px;
}

/* Placeholder text */
.stTextArea textarea::placeholder {
    color: #a0a7ad !important;
    opacity: 1;
}

/* Buttons */
.stButton > button {
    background-color: #20272b;
    color: #ffffff;
    border: 1px solid #41494f;
    border-radius: 7px;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #20c997;
    color: #20c997;
}

/* Download button */
.stDownloadButton > button {
    background-color: #20272b;
    color: #ffffff;
    border: 1px solid #41494f;
    border-radius: 7px;
}

/* Encrypted message */
.ciphertext {
    background-color: #191d20;
    border: 1px solid #343a40;
    border-radius: 8px;
    padding: 16px;
    color: #55d6e8;
    overflow-wrap: anywhere;
    font-size: 16px;
}

/* Statistics */
div[data-testid="stMetricValue"] {
    color: #eeeeee;
}

/* Expandable sections */
div[data-testid="stExpander"] {
    background-color: #101214;
    border-color: #343a40;
}

/* Dividers */
hr {
    border-color: #343a40;
}

/* App toolbar */
header[data-testid="stHeader"] {
    background-color: #101214;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "encrypted" not in st.session_state:
    st.session_state["encrypted"] = False
    st.session_state["ciphertext"] = ""
    st.session_state["keys"] = []
    st.session_state["original"] = ""
    st.session_state["decrypted"] = None

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Linear Affine Encryption Tool")

st.caption(
    "A mathematical model for text encryption and decryption."
)

st.markdown("---")

# --------------------------------------------------
# MESSAGE INPUT
# --------------------------------------------------

st.subheader("Enter your message")

message = st.text_area(
    "Message",
    placeholder="Type your message here...",
    height=120,
    label_visibility="collapsed",
    key="message_input"
)

if st.button("Encrypt Message", type="primary"):

    if not message:
        st.warning("Please enter a message first.")

    else:
        encrypted_values = []
        encryption_keys = []

        for character in message:
            # Generate numerical parameters
            a = random.randint(2, 9)
            b = random.randint(1, 9)

            # Convert character to its Unicode code point
            x = ord(character)

            # Encryption equation: y = ax + b
            y = a * x + b

            encrypted_values.append(y)

            encryption_keys.append({
                "a": a,
                "b": b
            })

        # Save results
        st.session_state["original"] = message

        st.session_state["ciphertext"] = " ".join(
            str(value) for value in encrypted_values
        )

        st.session_state["keys"] = encryption_keys
        st.session_state["encrypted"] = True
        st.session_state["decrypted"] = None

# --------------------------------------------------
# ENCRYPTION RESULT
# --------------------------------------------------

if st.session_state["encrypted"]:

    st.markdown("### Encrypted Message")

    st.markdown(
        f'<div class="ciphertext">'
        f'{st.session_state["ciphertext"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Three horizontal statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Characters",
            len(st.session_state["original"])
        )

    with col2:
        st.metric(
            "Cipher Values",
            len(st.session_state["keys"])
        )

    with col3:
        st.metric(
            "Ciphertext Length",
            len(st.session_state["ciphertext"])
        )

    st.markdown("---")

    # --------------------------------------------------
    # DECRYPTION
    # --------------------------------------------------

    st.subheader("Decryption")

    if st.button("Decrypt Message"):

        decrypted_characters = []

        encrypted_numbers = [
            int(value)
            for value in st.session_state["ciphertext"].split()
        ]

        for value, key in zip(
            encrypted_numbers,
            st.session_state["keys"]
        ):
            a = key["a"]
            b = key["b"]

            # Decryption equation: x = (y - b) / a
            x = (value - b) // a

            decrypted_characters.append(chr(x))

        st.session_state["decrypted"] = "".join(
            decrypted_characters
        )

    if st.session_state["decrypted"] is not None:

        st.success("Message decrypted successfully!")

        st.text_area(
            "Decrypted message",
            value=st.session_state["decrypted"],
            height=100,
            disabled=True,
            key="decrypted_output"
        )

    # --------------------------------------------------
    # ENCRYPTION KEYS
    # --------------------------------------------------

        # ENCRYPTION KEYS

    with st.expander("View Encryption Keys"):

        st.caption(
            "Each character has its own values of a and b."
        )

        key_table = []

        for index, key in enumerate(st.session_state["keys"]):
            key_table.append({
                "Character Position": index + 1,
                "Parameter a": key["a"],
                "Parameter b": key["b"]
            })

        st.dataframe(
            key_table,
            hide_index=True,
            use_container_width=True
        )

    key_table = []

    for index, key in enumerate(st.session_state["keys"]):
        key_table.append({
            "Character Position": index + 1,
            "Parameter a": key["a"],
            "Parameter b": key["b"]
        })

    
    

    # --------------------------------------------------
    # DOWNLOAD DATA
    # --------------------------------------------------

    download_data = {
        "original_message": st.session_state["original"],
        "encrypted_message": st.session_state["ciphertext"],
        "encryption_keys": st.session_state["keys"],
        "decrypted_message": st.session_state["decrypted"]
    }

    st.download_button(
        label="Download Project Data",
        data=json.dumps(download_data, indent=4),
        file_name="encryption_data.json",
        mime="application/json"
    )

    # --------------------------------------------------
    # MATHEMATICAL MODEL
    # --------------------------------------------------

    st.markdown("---")

    st.subheader("Mathematical Model")

    st.write("Encryption equation:")

    st.latex(r"y = ax + b")

    st.write("Decryption equation:")

    st.latex(r"x = \frac{y-b}{a}")

    st.write(
        """
        **Where:**

        - **x** = numerical code of the original character
        - **a, b** = numerical encryption parameters
        - **y** = encrypted numerical value
        """
    )

    st.caption(
        "Educational demonstration only. This custom method "
        "is not suitable for protecting confidential information."
    )
