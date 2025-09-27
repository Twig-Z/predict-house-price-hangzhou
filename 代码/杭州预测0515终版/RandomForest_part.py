import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from gensim.parsing import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn import preprocessing
from category_encoders import TargetEncoder
from sklearn.preprocessing import LabelEncoder


def full_prediction_pipeline(X_train, y_train, X_test, y_test):
    """完整的XGBoost预测流程，包括所有优化策略"""
    # 定义参数网格
    criterion = ['squared_error']  # 仅使用默认和最常用的选项
    n_estimators = [50, 100, 200, 400]  # 大幅减少数量并使用更小的值
    max_features = [1.0, 'sqrt']  # 保持不变
    max_depth = [30, 40, 50, None]  # 减少深度选项
    min_samples_split = [2, 5]  # 减少选项
    min_samples_leaf = [1, 2]  # 减少选项
    bootstrap = [True]  # 通常True性能更好

    param_grid = {
        'criterion': criterion,
        'n_estimators': n_estimators,
        'max_features': max_features,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'bootstrap': bootstrap
    }


    # 2.3 初始化模型
    rf_model = RandomForestRegressor(
        criterion='squared_error',
        n_jobs=-1,
        random_state=42
    )

    # 2.4 随机搜索最佳参数
    search = RandomizedSearchCV(
        estimator=rf_model,
        param_distributions=param_grid,
        n_iter=10,  # 保持不变
        cv=3,       # 保持不变
        verbose=1,  # 减少输出详细程度
        random_state=42,
        n_jobs=-1   # 使用所有可用CPU核心
    )

    # 2.5 训练并找到最佳参数
    search.fit(X_train, y_train)

    print("最佳参数:", search.best_params_)
    print("最佳交叉验证得分:", search.best_score_)

    # 2.6 使用最佳参数训练最终模型
    best_model = RandomForestRegressor(**search.best_params_, random_state=42)
    best_model.fit(X_train, y_train)

    # 2.7 评估模型
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    average_price = np.mean(y_test)
    rmse_percentage = (rmse / average_price) * 100
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\nXGBoost模型性能:")
    print(f"RMSE: {rmse:.2f}万元")
    print(mae)
    print(average_price)
    print(f"RMSE百分比表示: {rmse_percentage:.2f}%")
    print(f"R² Score: {r2:.4f}")

    # 2.8 特征重要性
    features = [
        '所在区域', '建筑类型', '建筑面积', '建筑结构',
        '装修情况', '小区名称', '所在位置', '房屋用途',
        '卧室数', '客厅数', '卫生间数', '楼层位置', '总层数', '得房率', '是否有抵押', '抵押金额', '是否地铁',
        '是否电梯', '产权类型',
    ]
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n变量重要性:")
    print(feature_importance.head(20))

    return best_model

def main():
    name = "hangzhou"
    chengshi = "杭州"

    """数据加载"""
    file_path = 'E:\\data\\{}\\data_processing\\{}_clean.csv'.format(name, name)

    # miss_value = ["null", "暂无数据"]
    # data = pd.read_csv(file_path, na_values=miss_value, encoding="utf-8")
    df = pd.read_csv(file_path, encoding="utf-8")
    print(df.info())

    data = df.sample(n=len(df))

    # 初始化LabelEncoder
    le = LabelEncoder()
    # 处理分类特征
    categorical_features = ['所在区域', '建筑类型', '建筑结构', '装修情况', '小区名称', '所在位置', '房屋用途']
    encoded_features = []
    for col in categorical_features:
        le.fit(data[col].unique())
        encoded_features.append(le.transform(data[col]))
    # 处理数值特征
    numerical_features = ['建筑面积', '卧室数', '客厅数', '卫生间数', '楼层位置', '总层数', '得房率', '是否有抵押',
                          '抵押金额', '是否地铁', '是否电梯', '产权类型']
    numerical_features_transformed = [data[col].astype('int').values for col in numerical_features]
    # 构建特征矩阵
    X = np.column_stack(encoded_features + numerical_features_transformed)
    Y = data['总价']

    print(np.array(X).shape)

    # 划分训练集和验证集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # 运行完整预测流程
    model = full_prediction_pipeline(X_train, Y_train, X_test, Y_test)
    joblib.dump(model, 'random_forest_model_part0.2.pkl')

    print("\n优化完成! 最终模型已保存。")
    return model


# 如果作为独立脚本运行
if __name__ == "__main__":
    main()