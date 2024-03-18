import numpy as np
import tensorflow as tf
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

model = load_model('tanh_model.h5')

# 加载Scaler和PCA转换器
scaler = joblib.load('scaler_0306.pkl')
pca = joblib.load('pca_0306.pkl')


def predict(input_data):
    # 将输入数据转换为numpy数组
    data = np.array(input_data).reshape(1, -1)

    # 数据标准化和PCA转换
    data_scaled = scaler.transform(data)
    data_pca = pca.transform(data_scaled)[:, :12]

    # 使用模型进行预测
    prediction = model.predict(data_pca)
    print(prediction[0])
    return prediction[0]


