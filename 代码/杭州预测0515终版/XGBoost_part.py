import numpy as np
import pandas as pd
import xgboost as xgb
from gensim.parsing import preprocessing
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn import preprocessing
from category_encoders import TargetEncoder


# 1. 特征工程函数
def engineer_features(X, y=None, is_training=True):
    # 复制数据避免修改原始数据
    X_new = X.copy()

    # 1.1 创建交互特征

    # 添加交互特征
    X_new['面积x区域'] = X_new['建筑面积'] * X_new['所在区域'].cat.codes
    X_new['面积x位置'] = X_new['建筑面积'] * X_new['所在位置'].cat.codes
    X_new['面积x装修'] = X_new['建筑面积'] * X_new['装修情况'].cat.codes
    X_new['层数x电梯'] = X_new['总层数'] * X_new['是否电梯']

    # 1.2 非线性变换
    X_new['建筑面积_sqrt'] = np.sqrt(X_new['建筑面积'])
    X_new['建筑面积_log'] = np.log1p(X_new['建筑面积'])
    X_new['总层数_sqrt'] = np.sqrt(X_new['总层数'])

    # 1.3 合并房间特征
    X_new['总房间数'] = X_new['卧室数'] + X_new['卫生间数'] + X_new['客厅数']
    X_new['房间密度'] = X_new['总房间数'] / X_new['建筑面积']

    # 1.4 适用目标编码(仅对高重要性类别特征)
    # 重要类别特征的目标编码
    if is_training and y is not None:
        # 初始化全局编码器用于保存
        global encoders
        encoders = {}

        for col in ['所在区域', '所在位置', '小区名称']:
            encoders[col] = TargetEncoder(cols=[col])
            transformed = encoders[col].fit_transform(X_new[col], y)
            X_new[f'{col}_encoded'] = transformed
    else:
        # 测试集应用已训练的编码器
        for col in ['所在区域', '所在位置', '小区名称']:
            if col in encoders:
                X_new[f'{col}_encoded'] = encoders[col].transform(X_new[col])

    # 1.5 去除低重要性特征
    '''low_importance = ['产权类型', '是否有抵押', '得房率']
    X_new = X_new.drop(low_importance, axis=1, errors='ignore')'''

    # 1.6 处理类别变量(XGBoost需要)
    for col in X_new.select_dtypes(include=['category']).columns:
        X_new[col] = X_new[col].cat.codes

    return X_new


# 2. XGBoost模型训练与调参
def train_xgboost_model(X_train, y_train, X_test, y_test):
    """
    训练优化的XGBoost模型

    参数:
    X_train, y_train: 训练数据
    X_test, y_test: 测试数据

    返回:
    最佳模型和评估结果
    """
    # 2.1 应用特征工程
    X_train_fe = engineer_features(X_train, y_train, is_training=True)
    X_test_fe = engineer_features(X_test, None, is_training=False)

    # 2.2 定义参数网格
    param_grid = {
        'n_estimators': [100, 200, 300, 500],
        'max_depth': [3, 5, 7, 9],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'min_child_weight': [1, 3, 5],
        'gamma': [0, 0.1, 0.2],
        'reg_alpha': [0, 0.1, 0.5],
        'reg_lambda': [0.5, 1, 1.5]
    }

    # 2.3 初始化模型
    xgb_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_jobs=-1,
        random_state=42
    )

    # 2.4 随机搜索最佳参数
    search = RandomizedSearchCV(
        estimator=xgb_model,
        param_distributions=param_grid,
        n_iter=20,  # 随机尝试的参数组合数
        cv=5,
        verbose=1,
        random_state=42,
        n_jobs=-1,
        scoring='r2'
    )

    # 2.5 训练并找到最佳参数
    search.fit(X_train_fe, y_train)

    print("最佳参数:", search.best_params_)
    print("最佳交叉验证得分:", search.best_score_)

    # 2.6 使用最佳参数训练最终模型
    best_model = xgb.XGBRegressor(**search.best_params_, random_state=42)
    best_model.fit(X_train_fe, y_train)

    # 2.7 评估模型
    y_pred = best_model.predict(X_test_fe)
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
    feature_importance = pd.DataFrame({
        'feature': X_train_fe.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n变量重要性:")
    print(feature_importance)

    return best_model, feature_importance, X_train_fe, X_test_fe


# 3. 实现学习曲线分析以理解模型性能
def learning_curve_analysis(X_train_fe, y_train):
    """分析不同训练集大小下模型的表现"""
    from sklearn.model_selection import learning_curve

    # 使用较简单的XGBoost配置
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    # 计算学习曲线
    train_sizes, train_scores, test_scores = learning_curve(
        model, X_train_fe, y_train,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5, scoring='r2', n_jobs=-1
    )

    # 计算均值和标准差
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    print("\n学习曲线分析:")
    print("训练集大小比例: ", train_sizes / len(X_train_fe))
    print("训练集R²均值: ", train_mean)
    print("验证集R²均值: ", test_mean)

    # 如果需要可视化，可以使用matplotlib绘制图形
    # 这里仅返回数据供后续处理
    return train_sizes, train_mean, test_mean


# 4. 模型解释
def explain_model(model, X_train_fe, X_test_fe, y_test):
    """使用SHAP值解释模型预测"""
    try:
        import shap

        # 创建SHAP解释器
        explainer = shap.TreeExplainer(model)

        # 计算测试集的SHAP值
        # 为了速度，可以只使用部分样本
        shap_values = explainer.shap_values(X_test_fe.iloc[:100])

        print("\nSHAP分析完成 - 可用于理解每个特征对预测的贡献")

        # 返回解释器和SHAP值供后续处理
        return explainer, shap_values
    except ImportError:
        print("\n需要安装SHAP库以进行模型解释")
        return None, None


# 5. 完整预测流程
def full_prediction_pipeline(X_train, y_train, X_test, y_test):
    """完整的XGBoost预测流程，包括所有优化策略"""

    # 5.1 训练优化的XGBoost模型
    model, importance, X_train_fe, X_test_fe = train_xgboost_model(X_train, y_train, X_test, y_test)

    # 5.2 学习曲线分析
    train_sizes, train_mean, test_mean = learning_curve_analysis(X_train_fe, y_train)

    # 5.3 模型解释(可选)
    explainer, shap_values = explain_model(model, X_train_fe, X_test_fe, y_test)

    # 5.4 对比随机森林
    print("\n与随机森林模型对比:")
    print("随机森林 R²: 0.8477")
    print("XGBoost R²: {:.4f}".format(r2_score(y_test, model.predict(X_test_fe))))

    return model


# 主函数 - 调用整个流程
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

    categorical_columns = [
        '交通情况', '挂牌时间', '交易权属', '上次交易', '房屋年限',
        '产权所属', '抵押信息', '房本备件', '房屋户型', '所在楼层',
        '户型结构', '房屋朝向', '建筑结构', '梯户比例', '配备电梯',
        '用水类型', '用电类型', '燃气价格', '临近地铁站', '所在区域',
        '所在位置', '装修情况', '小区名称', '建筑类型', '房屋用途',
    ]

    for col in categorical_columns:
        if col in data.columns:
            data[col] = data[col].astype('category')

    X = data.drop(
        ['单价', '总价', '楼层高度', '套内面积', '产权类型', '房本备件', '燃气价格', '产权所属', '抵押信息', 'id'],
        axis=1)
    Y = data['总价']

    print(np.array(X).shape)

    # 划分训练集和验证集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    # 运行完整预测流程
    model = full_prediction_pipeline(X_train, Y_train, X_test, Y_test)
    model.save_model('xgboost_model_part0.1.json')

    print("\n优化完成! 最终模型已保存。")
    return model


# 如果作为独立脚本运行
if __name__ == "__main__":
    main()
