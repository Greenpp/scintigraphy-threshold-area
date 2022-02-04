import logging

import streamlit as st

from scintigraphy_threshold_area.image import ScintigraphyImage

logging.basicConfig(level=logging.INFO)


@st.cache(show_spinner=False)
def load_image(file):
    return ScintigraphyImage(file)


st.set_page_config(page_title='Scyntygrafia')

st.title('Scyntygrafia - pole powierzchni')
image_file = st.file_uploader('Plik IMA')

if image_file is not None:
    img = load_image(image_file)

    col1, col2, col3 = st.columns(3)
    img_num = col1.slider('Obraz', 1, img.imgs_num, step=1)
    invert = col1.checkbox('Odwróć')
    use_threshold = col1.checkbox('Progowanie')
    threshold = None
    if use_threshold:
        threshold = col1.slider('Próg', 0.0, 1.0)
        col1.metric('Pole powierzchni [cm^2]', img.get_area(img_num - 1, threshold))
        col3.image(img.get_image(img_num - 1, invert, threshold))
    else:
        col3.empty()

    col2.image(img.get_image(img_num - 1, invert))
