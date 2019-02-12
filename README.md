# Fetch_20newsgroups

利用sklearn自带的fetch_20newsgroups数据进行朴素贝叶斯分类实践

- 数据来源：from sklearn.datasets import fetch_20newsgroups

- 分析：

1. 载入数据
2. 进行训练集和测试集分割
3. 采用tf-idf分析对训练集进行特征抽取
4. 以训练集当中的词的列表进行每篇文章重要性统计
5. 利用朴素贝叶斯进行预估
