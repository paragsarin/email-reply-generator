import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from app.words import Words


def make_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 EMail Reply Generator")
    data = st.text_area("Enter an email text:", value="...")
    submit_button = st.button("Submit")
    
    if submit_button:
        try:
            portfolio.load_portfolio()
            concerns = llm.extract_concerns(data)
            for concern in concerns:
                con = concern.get('concern', [])
                links = Words.query_links(con)
                email,tone,summary = llm.write_mail(concern, links)
                #print tone
                st.markdown("**Tone of email:**"+"<span style='color: red;'>**"+tone+"**</span>", unsafe_allow_html=True)
                #print summary
                st.markdown("**Summary of email:**"+"<span style='color: blue;'>**"+summary+"**</span>", unsafe_allow_html=True)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Reply Email Generator", page_icon="📧")
    make_streamlit_app(chain, portfolio, clean_text)

