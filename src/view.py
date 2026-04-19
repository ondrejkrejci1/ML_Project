import streamlit as st
import json
from src.data_loader import DataLoader
from src.ml_engine import ModelManager


class DecathlonView:

    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.all_disciplines = self.config.get('features', [])
        self.default_values = {
            '100m': 11.50, 'Long_Jump': 7.00, 'Shot_Put': 13.50, 'High_Jump': 1.95, '400m': 50.00,
            '110m_Hurdles': 15.00, 'Discus': 40.00, 'Pole_Vault': 4.50, 'Javelin': 55.00, '1500m': 280.00
        }

        self.data_loader = DataLoader()
        self.model_manager = ModelManager()

    def initialize_state(self):
        if 'active_disciplines' not in st.session_state:
            st.session_state.active_disciplines = ['100m', 'Long_Jump', 'Shot_Put', 'High_Jump', '400m']

    def render_discipline_manager(self):
        st.subheader("Discipline Management")
        col1, col2 = st.columns(2)

        with col1:
            available_to_add = [d for d in self.all_disciplines if d not in st.session_state.active_disciplines]
            if available_to_add:
                add_choice = st.selectbox("Select a discipline to add:", available_to_add)
                if st.button("Add a discipline"):
                    if len(st.session_state.active_disciplines) >= 8:
                        st.warning("You cannot add any more! The maximum is 8 events.")
                    else:
                        st.session_state.active_disciplines.append(add_choice)
                        st.rerun()

        with col2:
            remove_choice = st.selectbox("Select the discipline to remove:", st.session_state.active_disciplines)
            if st.button("Remove discipline"):
                if len(st.session_state.active_disciplines) <= 5:
                    st.warning("Cannot be removed! A minimum of 5 events is required. First, add an event, and then remove this one.")
                else:
                    st.session_state.active_disciplines.remove(remove_choice)
                    st.rerun()

    def render_input_fields(self):
        st.subheader("Enter your results")
        user_inputs = {}

        for disc in st.session_state.active_disciplines:

            if disc == '1500m':
                time_str = st.text_input(
                    f"Result for {disc} (format MM:SS.tenths):",
                    value="4:40.00"
                )

                parsed_seconds = self.parse_time_to_seconds(time_str)

                if parsed_seconds is None:
                    st.error("Invalid time format! Please enter the time in a format such as 4:40.50")
                    user_inputs[disc] = 280.0
                else:
                    user_inputs[disc] = parsed_seconds

            else:
                val = st.number_input(
                    f"Result for {disc}:",
                    value=float(self.default_values.get(disc, 0.0)),
                    step=0.1
                )
                user_inputs[disc] = val

        sorted_order = ['100m', 'Long_Jump', 'Shot_Put', 'High_Jump', '400m', '110m_Hurdles', 'Discus', 'Pole_Vault', 'Javelin', '1500m']

        sorted_inputs = {}

        for disc in sorted_order:
            if disc in user_inputs:
                sorted_inputs[disc] = user_inputs[disc]

        return sorted_inputs

    def render_prediction_action(self, user_inputs):
        if st.button("Create a model and predict points", use_container_width=True, type="primary"):
            with st.spinner('Analyzing the data and train AI models'):
                try:
                    data = self.data_loader.get_data()
                    predicted_points = self.model_manager.predict_score(data, user_inputs)
                    st.success(f"Estimated score: {predicted_points} points!")
                except Exception as e:
                    st.error(f"An error occurred during the calculation: {e}")

    def parse_time_to_seconds(self, time_str):
        try:
            time_str = str(time_str).strip()

            time_str = time_str.replace(',', '.')

            if ":" in time_str:
                minutes, seconds = time_str.split(":")
                total_seconds = (int(minutes) * 60) + float(seconds)
            else:
                total_seconds = float(time_str)

            return total_seconds
        except ValueError:
            return None

    def render(self):
        st.set_page_config(page_title="AI Decathlon", layout="centered")
        st.markdown("""
                    <style>
                        .block-container {
                            padding-top: 0rem !important; 
                            padding-bottom: 1rem !important;
                        }
                        header {
                            visibility: hidden !important;
                            height: 0px !important;
                        }
                        h1 { 
                            padding-top: -0.2rem !important; 
                            margin-top: -0.2rem !important; 
                            padding-bottom: 0.5rem !important; 
                        }

                        h3 {
                            padding-top: 0.2rem !important;
                            margin-top: 0rem !important;
                        }

                        div[data-testid="stVerticalBlock"] > div {
                            gap: 0.5rem !important;
                        }

                        hr {
                            margin-top: -1rem !important;
                            margin-bottom: 0.3rem !important;
                            padding-bottom: 0px !important;
                            padding-top: 0px !important;
                        }
                    </style>
                """, unsafe_allow_html=True)
        self.initialize_state()

        st.title("AI Decathlon Predictor")
        st.write("Enter at least 5 and no more than 8 events. The AI will estimate your total score!")
        st.divider()

        self.render_discipline_manager()

        inputs = self.render_input_fields()

        self.render_prediction_action(inputs)