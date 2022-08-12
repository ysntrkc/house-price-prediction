import streamlit as st

st.set_page_config(page_title="House Price Project", page_icon=":house_with_garden")


lang = ["TR", "EN"]
col1, _, col2 = st.columns([3, 7, 3])

with col1:
    lang_choice = st.radio("Language", lang)
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )

if lang_choice == "TR":
    with col2:
        button = st.button("Beğen 👍")
        if button:
            st.write("Teşekkür ederiz 💗")
            try:
                with open("log/counter.txt", "r") as f:
                    counter = int(f.read())
                    counter += 1
                    with open("log/counter.txt", "w") as f:
                        f.write(str(counter))
            except FileNotFoundError:
                with open("log/counter.txt", "w") as f:
                    f.write("1")

    st.title("HOŞGELDİNİZ!")

    st.markdown(
        """
        ---
        <span style="font-size:1.5em;"><b>Ev fiyatı tahminleme aracı:</b> Ev satın almak isteyen tüketicilerin kendileri için uygun bulduğu özelliklerdeki evin yaklaşık fiyatını gösteren bir Python projesidir.
        </span>
        <p></p>
        <span style="font-size:1.5em;">Ev satın almak isteyen tüketicilerin kendileri için uygun bulduğu özelliklerdeki evin yaklaşık fiyatını gösteren bir Python projesidir.
        </span>
        <p></p>
        <span style=font-size:1.5em;">Siz de hayallerinizde evin fiyatını görmek için Price Calculator sayfasından özellikleri seçin!
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.title("DESTEKÇİLERİMİZ")

elif lang_choice == "EN":
    with col2:
        button = st.button("Like 👍")
        if button:
            st.write("Appreciated 💗")
            try:
                with open("log/counter.txt", "r") as f:
                    counter = int(f.read())
                    counter += 1
                    with open("log/counter.txt", "w") as f:
                        f.write(str(counter))
            except FileNotFoundError:
                with open("log/counter.txt", "w") as f:
                    f.write("1")

    st.title("WELCOME!")
    st.markdown(
        """
        ---
        <span style="font-size:1.5em;"><b>House price estimation tool:</b> This is a Python project that shows the approximate price of a house with features that consumers who want to buy a house find suitable for them.
        </span>
        <p></p>
        <span style="font-size:1.5em;">This tool allows consumers to make a prediction about the price in terms of the features they want. At the same time, it is helpful to see giving up which features will get a more suitable price. The selected features are the features that affect the house price the most, respectively.
        </span>
        <p></p>
        <span style=font-size:1.5em;">Select the features from the Price Calculator page to see the price of your dream house!
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.title("OUR SUPPORTERS")

col1, _, col2 = st.columns([2, 1, 2])
with col1:
    st.image("images/1.png")
    st.image("images/3.png")
with col2:
    st.image("images/2.png")
    st.image("images/4.png")

_, col1, _ = st.columns([1.5, 2, 1.5])
with col1:
    st.image("images/5.png")
