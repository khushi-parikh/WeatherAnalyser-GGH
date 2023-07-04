import streamlit as st

def data_footer(df):
    st.subheader("Data used :")
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df.csv',
        mime='text/csv',
    )
    st.write(df)

def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#9AD8E1",
    box_shadow: bool = True,
    color: str = "#000"
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
                color: {color}
            }}
            p{{
                color: {color}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )