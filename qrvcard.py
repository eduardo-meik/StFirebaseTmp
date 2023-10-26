# qrvcard.py
import streamlit as st
import qrcode
import io
from PIL import Image

def generate_qr(vcard_data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vcard_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def display_qr():
    st.title('vCard QR Code Generator')
    
    full_name = st.text_input("Nombre Completo", "Juan Soto")
    last_name, first_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

    organization = st.text_input("Organización", "Ejemplo Ltda.")
    title = st.text_input("Puesto", "CEO")
    role = st.text_input("Rol", "Manager")
    phone_cell = st.text_input("Teléfono (Celular)", "(555) 555-5555")
    phone_work = st.text_input("Teléfono (Trabajo)", "(555) 555-5555")
    email = st.text_input("Email (Trabajo)", "john.smith@example.com")
    url = st.text_input("Website", "https://www.example.com")
    linkedin = st.text_input("LinkedIn", "https://www.linkedin.com/in/juansoto/")

    vCard = {
        "BEGIN": "VCARD",
        "VERSION": "4.0",
        "KIND": "INDIVIDUAL",
        "FN": full_name,
        "N": f"{last_name};{first_name};;;",
        "EMAIL;TYPE=WORK": email,
        "TITLE": title,
        "ROLE": role,
        "TEL;TYPE=CELL": phone_cell,
        "TEL;TYPE=WORK": phone_work,
        "URL": url,
        "ORG": organization,
        "X-SOCIALPROFILE": linkedin,
        "END": "VCARD",
    }

    vcard_data = "\n".join(f"{key}:{value}" for key, value in vCard.items())

    if st.button('Generate QR Code'):
        img_pil = generate_qr(vcard_data)
        buffered = io.BytesIO()
        img_pil.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        st.image(img_bytes, caption='Generated QR Code', use_column_width=True)
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name=f"{full_name}.png",
            mime="image/png"
        )

