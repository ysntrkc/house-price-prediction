import streamlit as st

st.set_page_config(page_title="About Us", page_icon="🔥")

with open("images/github.txt", "r") as f:
    github = f.read()
with open("images/linkedin.txt", "r") as f:
    linkedin = f.read()


st.title("About Us")
st.markdown("---")

col1, col2, col3 = st.columns([1.05, 1, 0.8])
with col1:
    st.subheader("Yasin Tarakçı")
with col2:
    st.subheader("Ömer Topçu")
with col3:
    st.subheader("Kumru Orkun")

col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 3, 2, 2])
with col1:
    st.markdown(f"[![Foo]({github})](https://github.com/ysntrkc)")
with col2:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/yasintarakci)")
with col3:
    st.markdown(f"[![Foo]({github})](https://github.com/dromertopcu)")
with col4:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/drot)")
with col5:
    st.markdown(f"[![Foo]({github})](https://github.com/kumruo)")
with col6:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/kumruorkun)")

st.markdown("---")

col1, col2, col3 = st.columns([1.05, 1, 1])
with col1:
    st.subheader("Enes Bol")
with col2:
    st.subheader("M. Yavuz Gökmen")
with col3:
    st.subheader("Tunahan Demirkol")

col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 3, 2, 2])
with col1:
    st.markdown(f"[![Foo]({github})](https://github.com/enesbol)")
with col2:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/enesbol)")
with col3:
    st.markdown(f"[![Foo]({github})](https://github.com/AbyssWatcher-17)")
with col4:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/myavuzgokmen)")
with col5:
    st.markdown(f"[![Foo]({github})](https://github.com/TunahanDemirkol)")
with col6:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/tunahandemirkol)")

st.markdown("---")

col1, col2, col3 = st.columns([1.05, 1, 0.9])
with col1:
    st.subheader("Furkan Güneştaş")
with col2:
    st.subheader("Eren Güneştaş")
with col3:
    st.subheader("Baranalp Özkan")

col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 3, 2, 2])
with col1:
    st.markdown(f"[![Foo]({github})](https://github.com/fgunestas)")
with col2:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/fgunestas)")
with col3:
    st.markdown(f"[![Foo]({github})](https://github.com/shuharii)")
with col4:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/erengunestas)")
with col5:
    st.markdown(f"[![Foo]({github})](https://github.com/baranalpozkan)")
with col6:
    st.markdown(f"[![Foo]({linkedin})](https://www.linkedin.com/in/baranalpozkan)")

st.markdown("---")
