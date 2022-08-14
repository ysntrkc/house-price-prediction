import joblib
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb
from scipy.sparse import csr_matrix, hstack
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Price Calculator", page_icon="🤖")

lang = ["TR", "EN"]
col1, _, col2 = st.columns([3, 7, 3])

with col1:
    lang_choice = st.radio("Language", lang)
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )


class SparseMatrix(TransformerMixin):
    def __init__(self):
        None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        categorical_columns = [
            "MSSubClass",
            "MSZoning",
            "Street",
            "Alley",
            "LotShape",
            "LandContour",
            "Utilities",
            "LotConfig",
            "LandSlope",
            "Neighborhood",
            "Condition1",
            "Condition2",
            "BldgType",
            "HouseStyle",
            "RoofStyle",
            "RoofMatl",
            "Exterior1st",
            "Exterior2nd",
            "MasVnrType",
            "Foundation",
            "BsmtQual",
            "BsmtCond",
            "BsmtExposure",
            "BsmtFinType1",
            "BsmtFinType2",
            "Heating",
            "Electrical",
            "Functional",
            "FireplaceQu",
            "GarageType",
            "GarageFinish",
            "GarageQual",
            "GarageCond",
            "PavedDrive",
            "Fence",
            "SaleType",
            "SaleCondition",
        ]
        X[categorical_columns] = X[categorical_columns].astype(str)
        ohe = joblib.load("dump/ohe.pkl")
        hot = ohe.transform(X[categorical_columns].astype(str))
        cold_df = X.select_dtypes(exclude=["object"])
        cold = csr_matrix(cold_df.values)
        final_sparse_matrix = hstack((hot, cold))
        final_csr_matrix = final_sparse_matrix.tocsr()
        return final_csr_matrix


data_pipeline = Pipeline([("sparse", SparseMatrix())])
bst = xgb.Booster()
bst.load_model("model/houseprice.model")
single_row = pd.read_csv("data/single_row.csv", index_col=0)

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

    st.title("Lütfen sol taraftaki pencereden istediğiniz evin özelliklerini seçiniz!")

    with st.sidebar:
        st.title("Özellikler")

        LandContour_dict = {
            "": "",
            "Daireye Yakın/Seviye": "Lvl",
            "Yatırılmış - Hızlı ve önemli artış": "Bnk",
            "Yamaç": "HLS",
            "Depresyon": "Low",
        }
        LandContour = st.sidebar.selectbox(
            "Mülkün düzlüğü",
            options=LandContour_dict.keys(),
        )

        PavedDrive_dict = {
            "": "",
            "Döşeli": "Y",
            "Kısmi Kaldırım": "P",
            "Kir/Çakıl": "N",
        }
        PavedDrive = st.sidebar.selectbox(
            "Döşeme yolu",
            options=PavedDrive_dict.keys(),
        )

        BsmtQual_dict = {
            "": "",
            "Mükemmel": "5",
            "İyi": "4",
            "Ortalama": "3",
            "İdare Eder": "2",
        }
        BsmtQual = st.sidebar.selectbox(
            "Bodrum Kalitesi Türü",
            options=BsmtQual_dict.keys(),
        )

        Condition1_dict = {
            "": "",
            "Ana caddeye bitişik": "Artery",
            "Besleyici caddeye bitişik": "Feedr",
            "Normal": "Norm",
            "Kuzey-Güney Demiryolunun 200'ü İçinde": "RRNn",
            "Kuzey-Güney Demiryoluna Bitişik": "RRAn",
            "Pozitif saha dışı özelliği-- park, yeşil kuşak, vb.": "PosN",
            "Pozitif tesis dışı özelliğe bitişik": "PosA",
            "Doğu-Batı Demiryolunun 200'ü içinde": "RRNe",
            "Doğu-Batı Demiryoluna Bitişik": "RRAe",
        }
        Condition1 = st.sidebar.selectbox(
            "Çeşitli koşullara yakınlık",
            options=Condition1_dict.keys(),
        )

        FireplaceQu_dict = {
            "": "",
            "Olağanüstü Duvar Şömine": "5",
            "Ana seviyede duvar şöminesi": "4",
            "Ana yaşam alanında Prefabrik Şömine veya bodrum katında Yığma Şömine": "3",
            "Bodrumda Prefabrik Şömine": "2",
            "Ben Franklin Soba": "1",
        }
        FireplaceQu = st.sidebar.selectbox(
            "Şömine Kalitesi",
            options=FireplaceQu_dict.keys(),
        )

        Alley_dict = {"": "", "Çakıl": "Grvl", "Döşeli": "Pave"}
        Alley = st.sidebar.selectbox(
            "Mülke geçit erişimi türü",
            options=Alley_dict.keys(),
        )

        Neighborhood_dict = {
            "": "",
            "Bloomington Heights": "Blmngtn",
            "Bluestem": "Blueste",
            "Briardale": "BrDale",
            "Brookside": "BrkSide",
            "Clear Creek": "ClearCr",
            "College Creek": "CollgCr",
            "Crawford": "Crawfor",
            "Edwards": "Edwards",
            "Gilbert": "Gilbert",
            "Iowa DOT and Rail Road": "IDOTRR",
            "Meadow Village": "MeadowV",
            "Mitchell": "Mitchel",
            "North Ames": "Names",
            "Northridge": "NoRidge",
            "Northpark Villa": "NPkVill",
            "Northridge Heights": "NridgHt",
            "Northwest Ames": "NWAmes",
            "Old Town": "OldTown",
            "South & West of Iowa State University": "SWISU",
            "Sawyer": "Sawyer",
            "Sawyer West": "SawyerW",
            "Somerset": "Somerst",
            "Stone Brook": "StoneBr",
            "Timberland": "Timber",
            "Veenker": "Veenker",
        }
        Neighborhood = st.sidebar.selectbox(
            "Ames şehir sınırları içindeki fiziksel konumlar",
            options=Neighborhood_dict.keys(),
        )

        GarageQual_dict = {
            "": "",
            "Çok iyi": "5",
            "İyi": "4",
            "Klasik": "3",
            "Ortalama": "2",
            "Kötü": "1",
        }
        GarageQual = st.sidebar.selectbox(
            "Garaj Kalitesi",
            options=GarageQual_dict.keys(),
        )

        BsmtFinSF1 = st.sidebar.select_slider(
            "Tamamlanmış bodrum alanı", options=[*range(0, 5645)]
        )

        FullBath = st.sidebar.select_slider(
            "Üst sınıf banyolar", options=[*range(0, 4)]
        )

        KitchenQual = st.sidebar.select_slider(
            "Mutfak kalitesi", options=[*range(2, 6)]
        )

        TotalBsmtSF = st.sidebar.select_slider(
            "Bodrum alanının toplam metrekaresi", options=[*range(0, 6111)]
        )

        ndFlrSF = st.sidebar.select_slider(
            "İkinci kat metrekare", options=[*range(1, 2066)]
        )

        GarageArea = st.sidebar.select_slider(
            "Garajın metrekare cinsinden büyüklüğü", options=[*range(0, 1419)]
        )

        KitchenAbvGr = st.sidebar.select_slider(
            "Sınıf Üstü Mutfaklar", options=[*range(0, 4)]
        )

        OverallQual = st.sidebar.select_slider(
            "Evin genel malzemesi ve bitişinin değerlendirmesi",
            options=[*range(1, 11)],
        )

        GrLivArea = st.sidebar.select_slider(
            "Zeminden yüksekteki yaşam alanı", options=[*range(334, 5643)]
        )

        GarageCars = st.sidebar.select_slider(
            "Garajın araç kapasitesi", options=[*range(0, 5)]
        )

        ExterQual = st.sidebar.select_slider(
            "Dış cephe  malzeme kalitesi", options=[*range(2, 6)]
        )

    feature_list_str = [
        "LandContour",
        "PavedDrive",
        "BsmtQual",
        "Condition1",
        "FireplaceQu",
        "Alley",
        "Neighborhood",
        "GarageQual",
        "BsmtFinSF1",
        "FullBath",
        "KitchenQual",
        "TotalBsmtSF",
        "2ndFlrSF",
        "GarageArea",
        "KitchenAbvGr",
        "OverallQual",
        "GrLivArea",
        "GarageCars",
        "ExterQual",
    ]

    feature_list = [
        LandContour,
        PavedDrive,
        BsmtQual,
        Condition1,
        FireplaceQu,
        Alley,
        Neighborhood,
        GarageQual,
    ]

    for idx, item in enumerate(feature_list):
        dict_name = f"{feature_list_str[idx]}_dict"
        feature_list[idx] = eval(dict_name)[item]

    feature_list += [
        BsmtFinSF1,
        FullBath,
        KitchenQual,
        TotalBsmtSF,
        ndFlrSF,
        GarageArea,
        KitchenAbvGr,
        OverallQual,
        GrLivArea,
        GarageCars,
        ExterQual,
    ]

    if st.sidebar.button("Evin Tahmini Fiyatını Göster"):
        for i in range(len(feature_list)):
            if feature_list[i] != "":
                single_row.loc[0, feature_list_str[i]] = feature_list[i]
        single_row_trans = data_pipeline.fit_transform(single_row)
        xgmat = xgb.DMatrix(single_row_trans, missing=999.0)
        ypred = bst.predict(xgmat)
        st.markdown("---")
        st.title("Seçtiğiniz evin tahmini fiyatı:")
        st.title(np.round(ypred[0]))
        if st.button("Baştan Başlayalım!"):
            # TODO: tekrar bak
            pass

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

    st.title("Please select the properties of the house you want from the sidebar!")

    with st.sidebar:
        st.title("Features")

        LandContour_dict = {
            "": "",
            "Near Flat/Level": "Lvl",
            "Banked - Quick and significant rise": "Bnk",
            "Hillside": "HLS",
            "Depression": "Low",
        }
        LandContour = st.sidebar.selectbox(
            "Flatness of the property", options=LandContour_dict.keys()
        )

        PavedDrive_dict = {
            "": "",
            "Paved": "Y",
            "Partial Pavement": "P",
            "Dirt/Gravel": "N",
        }
        PavedDrive = st.sidebar.selectbox(
            "Paved driveway", options=PavedDrive_dict.keys()
        )

        BsmtQual_dict = {
            "": "",
            "Excellent": "5",
            "Good": "4",
            "Typical": "3",
            "Fair": "2",
        }
        BsmtQual = st.sidebar.selectbox(
            "Type of Basement Quality", options=BsmtQual_dict.keys()
        )

        Condition1_dict = {
            "": "",
            "Adjacent to arterial street": "Artery",
            "Adjacent to feeder street": "Feedr",
            "Normal": "Norm",
            "Within 200' of North-South Railroad": "RRNn",
            "Adjacent to North-South Railroad": "RRAn",
            "Near positive off-site feature--park, greenbelt, etc.": "PosN",
            "Adjacent to postive off-site feature": "PosA",
            "Within 200' of East-West Railroad": "RRNe",
            "Adjacent to East-West Railroad": "RRAe",
        }
        Condition1 = st.sidebar.selectbox(
            "Proximity to various conditions", options=Condition1_dict.keys()
        )

        FireplaceQu_dict = {
            "": "",
            "Exceptional Masonry Fireplace": "5",
            "Masonry Fireplace in main level": "4",
            "Prefabricated Fireplace in main living area or Masonry Fireplace in basement": "3",
            "Prefabricated Fireplace in basement": "2",
            "Ben Franklin Stove": "1",
        }
        FireplaceQu = st.sidebar.selectbox(
            "Fireplace Quality", options=FireplaceQu_dict.keys()
        )

        Alley_dict = {"": "", "Gravel": "Grvl", "Paved": "Pave"}
        Alley = st.sidebar.selectbox(
            "Type of alley access to property", options=Alley_dict.keys()
        )

        Neighborhood_dict = {
            "": "",
            "Bloomington Heights": "Blmngtn",
            "Bluestem": "Blueste",
            "Briardale": "BrDale",
            "Brookside": "BrkSide",
            "Clear Creek": "ClearCr",
            "College Creek": "CollgCr",
            "Crawford": "Crawfor",
            "Edwards": "Edwards",
            "Gilbert": "Gilbert",
            "Iowa DOT and Rail Road": "IDOTRR",
            "Meadow Village": "MeadowV",
            "Mitchell": "Mitchel",
            "North Ames": "Names",
            "Northridge": "NoRidge",
            "Northpark Villa": "NPkVill",
            "Northridge Heights": "NridgHt",
            "Northwest Ames": "NWAmes",
            "Old Town": "OldTown",
            "South & West of Iowa State University": "SWISU",
            "Sawyer": "Sawyer",
            "Sawyer West": "SawyerW",
            "Somerset": "Somerst",
            "Stone Brook": "StoneBr",
            "Timberland": "Timber",
            "Veenker": "Veenker",
        }

        Neighborhood = st.sidebar.selectbox(
            "Physical locations within Ames city limits",
            options=Neighborhood_dict.keys(),
        )

        GarageQual_dict = {
            "": "",
            "Excellent": "5",
            "Good": "4",
            "Typical": "3",
            "Fair": "2",
            "Poor": "1",
        }
        GarageQual = st.sidebar.selectbox(
            "Garage Quality", options=GarageQual_dict.keys()
        )

        BsmtFinSF1 = st.sidebar.select_slider(
            "Finished Basement Area", options=[*range(0, 5645)]
        )

        FullBath = st.sidebar.select_slider(
            "Full bathrooms above grade", options=[*range(0, 4)]
        )

        KitchenQual = st.sidebar.select_slider(
            "Kitchen quality", options=[*range(2, 6)]
        )

        TotalBsmtSF = st.sidebar.select_slider(
            "Total square feet of basement area", options=[*range(0, 6111)]
        )

        ndFlrSF = st.sidebar.select_slider(
            "Second floor square feet", options=[*range(1, 2066)]
        )

        GarageArea = st.sidebar.select_slider(
            "Size of garage in square feet", options=[*range(0, 1419)]
        )

        KitchenAbvGr = st.sidebar.select_slider(
            "Kitchens above grade", options=[*range(0, 4)]
        )

        OverallQual = st.sidebar.select_slider(
            "Rates the overall material and finish of the house",
            options=[*range(1, 11)],
        )

        GrLivArea = st.sidebar.select_slider(
            "Above grade (ground) living area square feet",
            options=[*range(334, 5643)],
        )

        GarageCars = st.sidebar.select_slider(
            "The size of garage according to car capacity", options=[*range(0, 5)]
        )

        ExterQual = st.sidebar.select_slider(
            "Evaluates the quality of the material on the exterior",
            options=[*range(2, 6)],
        )

        feature_list_str = [
            "LandContour",
            "PavedDrive",
            "BsmtQual",
            "Condition1",
            "FireplaceQu",
            "Alley",
            "Neighborhood",
            "GarageQual",
            "BsmtFinSF1",
            "FullBath",
            "KitchenQual",
            "TotalBsmtSF",
            "2ndFlrSF",
            "GarageArea",
            "KitchenAbvGr",
            "OverallQual",
            "GrLivArea",
            "GarageCars",
            "ExterQual",
        ]

        feature_list = [
            LandContour,
            PavedDrive,
            BsmtQual,
            Condition1,
            FireplaceQu,
            Alley,
            Neighborhood,
            GarageQual,
        ]

        for idx, item in enumerate(feature_list):
            dict_name = f"{feature_list_str[idx]}_dict"
            feature_list[idx] = eval(dict_name)[item]

        feature_list += [
            BsmtFinSF1,
            FullBath,
            KitchenQual,
            TotalBsmtSF,
            ndFlrSF,
            GarageArea,
            KitchenAbvGr,
            OverallQual,
            GrLivArea,
            GarageCars,
            ExterQual,
        ]

    if st.sidebar.button("Show House Price"):
        for i in range(len(feature_list)):
            if feature_list[i] != "":
                single_row.loc[0, feature_list_str[i]] = feature_list[i]
        single_row_trans = data_pipeline.fit_transform(single_row)
        xgmat = xgb.DMatrix(single_row_trans, missing=999.0)
        ypred = bst.predict(xgmat)
        st.markdown("---")
        st.title("With selected properties, estimated Price of the House:")
        st.title(np.round(ypred[0]))
        if st.button("Start over!"):
            # TODO: tekrar bak
            pass
