"""
朴素贝叶斯

P(C|W) = P(W|C) / P(W)

NOTE:
W为给定文档的特征值(频数统计，由预测文档提供)，C为文档类别

P(C|F1,F2……) = P(F1,F2……|C) * P(C) / P(F1,F2……)

NOTE:
P(C):每个文档类别的概率 (某文档类别词数/总文档词数)
P(W|C):给定类别下特征(被预测文档中出现的词)的概率
𝑃(𝐹i│𝐶) = 𝑁𝑖 / 𝑁	（训练文档中去计算）
𝑁𝑖为该𝐹i词在C类别所有文档中出现的次数
N为所属类别C下的文档所有词出现的次数和
𝑃(𝐹1,𝐹2,…)     预测文档中每个词的概率

拉普拉斯平滑系数(防止概率计算为零)
P(Fi|C) = (Ni + a) / (N + a*m)
a为制定系数一般为1，m为训练文档中统计出的特征词个数

朴素贝叶斯分类优缺点
1、优点：
1)朴素贝叶斯模型发源于古典数学理论，有稳定的分类效率。
2)对缺失数据不太敏感，算法也比较简单，常用于文本分类。
3)分类准确度高，速度快
4)不需要调参
2、缺点：
1)需要知道先验概率P(F1,F2,…|C)，因此在某些时候会由于假设的先验模型的原因导致预测效果不佳。
2)假设文章中词语之间相互独立，可能会出现误差
3)从训练集中统计词语，可能会对结果造成干扰


案例：利用sklearn自带的20类新闻数据进行朴素贝叶斯分类实践
分析：
1、载入数据
2、进行训练集和测试集分割
3、采用tf-idf分析对训练集进行特征抽取
tf-idf：如果某个词或短语在一篇文章中出现的概率高，并且在其他文章中很少则出现，认为此词或者短语具有很好的类别区分能力，适合用来分类。用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。
tf: term frequency 词的频率
idf: inverse document frequency 逆文档频率 log(总文档数量/该词出现的文档数量)
tf * idf 表示一个词的重要性程度
4、以训练集当中的词的列表进行每篇文章重要性统计
5、利用朴素贝叶斯进行预估
"""
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


def naivebayes():
    """
    朴素贝叶斯进行文本分类
    :return: None
    """
    # 获取所有新闻类别
    news = fetch_20newsgroups(subset="all")

    # 分割训练集和测试集
    # x_train 训练集特征值
    # x_test 测试集特征值
    # y_train 训练集目标值
    # y_test 测试集目标值
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)

    # 采用tf-idf分析对训练集进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词的列表进行每篇文章重要性统计
    x_train = tf.fit_transform(x_train)
    print(tf.get_feature_names())
    # 测试集要使用训练集的分词进行统计
    x_test = tf.transform(x_test)

    # 进行朴素贝叶斯算法预测
    mlt = MultinomialNB(alpha=1.0)  # 拉普拉斯平滑系数为1
    # fit输入数据，predict预测目标值，score得到准确性
    mlt.fit(x_train, y_train)
    # 得出预测结果
    y_predict = mlt.predict(x_test)
    print("预测文章类别：", y_predict)
    # 得出准确率
    print("预测准确率：", mlt.score(x_test, y_test))
    
    """
    混淆矩阵：以二分类为例，在分类任务下，Predict Condition与True Condition之间存在四种不同组合，构成混淆矩阵
                   _______________________预测结果_______________________
             _____|__________正例____________|___________假例___________|
            |正例 | 真正例TP(true positive)  | 伪反例FN(false negative) |
    真实结果 ———————————————————————————————————————————————————————————
            |假例 | 伪正例FP(fasle positive)|  真反例TN(true negative) |

    精确率Precision：预测结果为正例的样本中真是为正例的比例
                    真正例 / (真正例+伪正例)     查得准

    召回率Recall：真实为正例的样本中预测结果为正例的比例
                    真正例 / (真正例+伪反例)     查得全

    F1-score，综合反映模型稳健性
    F1 = 2TP / (2TP+FN+FP) = 2*Precision*Recall / (Precision+Recall)
    """
    from sklearn.metrics import classification_report
    print("预测精确率和召回率：", classification_report(y_test, y_predict, target_names=news.target_names))

    return None


if __name__ == '__main__':
    naivebayes()
