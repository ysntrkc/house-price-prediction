import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.base import TransformerMixin
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import r2_score
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

df = pd.read_csv("data/house_price.csv")

df["MSSubClass"] = df["MSSubClass"].astype("object")

drop_cols = [
    "MiscFeature",
    "PoolQC",
    "Id",
    "GarageYrBlt",
    "TotRmsAbvGrd",
    "1stFlrSF",
    "ScreenPorch",
    "PoolArea",
]
fill_miss_cols = [
    "MasVnrArea",
    "Fence",
    "GarageCond",
    "GarageQual",
    "GarageFinish",
    "GarageYrBlt",
    "GarageType",
    "FireplaceQu",
    "Electrical",
    "BsmtFinType2",
    "BsmtFinType1",
    "BsmtExposure",
    "BsmtCond",
    "BsmtQual",
    "MasVnrType",
    "Alley",
    "LotFrontage",
]

for i in fill_miss_cols:
    if df[i].dtypes in ["int64", "float64"]:
        df[i].fillna(-999.0, inplace=True)
    elif df[i].dtypes in ["object"]:
        df[i].fillna("unknown", inplace=True)

df = df.drop(drop_cols, axis=1)

qual_cols = [
    "ExterQual",
    "ExterCond",
    "BsmtQual",
    "BsmtCond",
    "HeatingQC",
    "KitchenQual",
    "FireplaceQu",
    "GarageQual",
    "GarageCond",
]

qual_dict = {"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "NA": 0}

df[qual_cols] = df[qual_cols].replace(qual_dict)
df["BsmtExposure"] = df["BsmtExposure"].replace(
    {"Gd": 4, "Av": 3, "Mn": 2, "No": 1, "NA": 0}
)
df["CentralAir"] = df["CentralAir"].replace({"Y": 1, "N": 0})

for i in df:
    if (df[i].dtypes in ["int64", "float64"]) and (
        abs(df.corr()["SalePrice"][i]) < 0.03
    ):
        df = df.drop(i, axis=1)

categorical_cols = df.columns[df.dtypes == "object"].tolist()

single_row = df.mode(axis=0)
single_row = single_row.iloc[:, :-1]
single_row.to_csv("data/single_row.csv")

plus = df[:25]
plus = plus.iloc[:, :-1]
plus.to_csv("data/plus.csv")

ohe = OneHotEncoder()
hot = ohe.fit_transform(df[categorical_cols].astype(str))
col_names = list(df[categorical_cols].columns)

joblib.dump(ohe, "dump/ohe.pkl")

df[df["MSSubClass"] == 120]

cold_df = df.select_dtypes(exclude=["object"])
cold = csr_matrix(cold_df)

final_sparse_matrix = hstack([hot, cold])

final_df = pd.DataFrame(final_sparse_matrix.toarray())


class NullValueImputer(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for column in X.columns.tolist():
            if column in X.columns[X.dtypes == "object"].tolist():
                X[column].fillna(X[column].mode(), inplace=True)
            else:
                X[column].fillna(-999.0, inplace=True)
        return X


class SparseMatrix(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        categorical_cols = X.columns[X.dtypes == "object"].tolist()
        ohe = OneHotEncoder()
        hot = ohe.fit_transform(X[categorical_cols])
        cold_df = X.select_dtypes(exclude=["object"])
        cold = csr_matrix(cold_df)
        final_sparse_matrix = hstack([hot, cold])
        final_sparse_matrix = final_sparse_matrix.tocsr()
        return final_sparse_matrix


data_pipeline = Pipeline(
    [("null_imputer", NullValueImputer()), ("sparse", SparseMatrix())]
)

X = final_df.iloc[:, :-1]
y = final_df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

X_train_transformed = data_pipeline.fit_transform(X_train)
final_csr_matrix = final_sparse_matrix.tocsr()
kfold = KFold(n_splits=5, shuffle=True, random_state=2)


def cross_val(model):
    scores = cross_val_score(
        model,
        X_train_transformed,
        y_train,
        scoring="neg_root_mean_squared_error",
        cv=kfold,
    )
    rmse = -scores.mean()
    return rmse


X_train_transformed = X_train
cross_val(XGBRegressor(missing=-999.0))

X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(
    X_train_transformed, y_train, random_state=2
)


def n_estimators(model):
    eval_set = [(X_test_2, y_test_2)]
    eval_metric = "rmse"
    model.fit(
        X_train_2,
        y_train_2,
        eval_metric=eval_metric,
        eval_set=eval_set,
        early_stopping_rounds=100,
    )
    y_pred = model.predict(X_test_2)
    rmse = MSE(y_test_2, y_pred) ** 0.5
    return rmse


n_estimators(XGBRegressor(n_estimators=5000, missing=-999.0))


def grid_search(params, reg=XGBRegressor(missing=-999.0)):
    grid_reg = GridSearchCV(reg, params, scoring="neg_mean_squared_error", cv=kfold)
    grid_reg.fit(X_train_transformed, y_train)
    best_params = grid_reg.best_params_
    print("Best params:", best_params)
    best_score = np.sqrt(-grid_reg.best_score_)
    print("Best score:", best_score)


xgbr = XGBRegressor(
    max_depth=7,
    min_child_weight=4,
    subsample=0.8,
    colsample_bytree=0.8,
    colsample_bylevel=0.8,
    colsample_bynode=0.6,
    n_estimators=100,
    missing=-999.0,
    learning_rate=0.1,
)

xgbr.fit(X_train.values, y_train.values)
pred = xgbr.predict(X_test.values)

mse = MSE(y_test, pred)
r2 = r2_score(y_test, pred)

print("MSE: %.2f" % mse)
print("RMSE: %.2f" % (mse ** (1 / 2.0)))
print(f"R2: {r2}")

fe = xgbr.feature_importances_

ilk20 = [
    "ExterQual",
    "OverallQual",
    "GarageCars",
    "GrLivArea",
    "BsmtQual",
    "FireplaceQu",
    "FullBath",
    "KitchenQual",
    "CentralAir",
    "TotalBsmtSF",
    "BsmtFinSF1",
    "Alley",
    "LandContour",
    "2ndFlrSF",
    "KitchenAbvGr",
    "GarageArea",
    "Condition1",
    "Neighborhood",
    "GarageQual",
    "PavedDrive",
]

ilk20 = list(map(lambda x: x.replace("x33_N", "PavedDrive"), ilk20))

xgbr.save_model("model/houseprice.model")
