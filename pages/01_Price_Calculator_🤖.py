from tkinter import Button
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb
from PIL import Image
from scipy.sparse import csr_matrix, hstack
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Price Calculator", page_icon="🤖")
