# 小说翻译效果评估工具

一个专业的小说翻译效果评估工具，支持多种评估指标，帮助您客观评估翻译质量。

## 功能特点

### 核心功能
- **翻译质量评估**：支持单个翻译文件的质量评估
- **翻译版本比较**：支持多个翻译版本的对比分析
- **详细报告生成**：自动生成包含详细评估结果的报告
- **句子级分析**：对每个句子进行单独评估
- **统计分析**：提供翻译质量的统计分析
- **Web界面**：提供直观的Web界面，便于使用

### 评估指标
- **BLEU**：机器翻译常用的评估指标，基于n元语法匹配
- **METEOR**：考虑词相似度的评估指标
- **余弦相似度**：基于TF-IDF的文本相似度
- **长度比率**：评估翻译文本与原文长度的一致性

## 安装

### 依赖库安装
```bash
pip install -r requirements.txt
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple deep-translator
```

### 下载语言模型
```bash
python -m spacy download en_core_web_sm
```

## 使用方法

### 1. 命令行使用

#### 评估翻译文件
```bash
python app.py evaluate examples/reference.txt examples/translation1.txt -o results.csv
```

#### 比较多个翻译版本
```bash
python app.py compare examples/reference.txt examples/translation1.txt examples/translation2.txt -o comparison_results
```

#### 分析句子长度对翻译质量的影响
```bash
python app.py analyze-length examples/reference.txt examples/translation1.txt -o length_analysis.csv
```

#### 启动Web界面
```bash
python app.py web
```

### 2. 配置文件

工具使用 `config.yaml` 文件进行配置：

```yaml
language:
  source: "zh-CN"       # 源语言 (zh-CN 中文, en 英文, ja 日文, etc.)
  target: "en"          # 目标语言 (zh-CN 中文, en 英文, ja 日文, etc.)
metrics:
  bleu: true            # BLEU分数
  meteor: true          # METEOR分数
  cosine_similarity: true  # 余弦相似度
  length_ratio: true    # 长度比率
preprocessing:
  remove_punctuation: true  # 是否去除标点符号
  lowercase: false         # 是否转为小写
  remove_stopwords: false  # 是否去除停用词
```

### 3. Web界面使用

1. 启动Web服务：
   ```bash
   python app.py web
   ```

2. 在浏览器中访问显示的地址（通常是 `http://localhost:8501`）

3. 上传参考原文和翻译文件，点击"开始评估"

4. 查看评估结果和详细报告

## 项目结构

```
trans-evl/
├── app.py                    # 主程序入口
├── novel_translation_evaluator.py  # 核心功能实现
├── config.yaml               # 配置文件
├── requirements.txt          # 依赖库列表
├── README.md                 # 使用说明
└── examples/                 # 示例文件
    ├── reference.txt         # 中文原文示例
    ├── translation1.txt      # 英文翻译示例1
    └── translation2.txt      # 英文翻译示例2
```

## 评估结果说明

### 整体评分
- **综合评分**：所有评估指标的平均值
- **BLEU分数**：范围0-1，分数越高表示翻译质量越好
- **METEOR分数**：范围0-1，考虑词相似度的指标
- **余弦相似度**：范围0-1，基于TF-IDF的文本相似度
- **长度比率**：范围0-1，评估翻译文本与原文长度的一致性

### 句子级结果
- 每个句子的单独评估结果
- 最佳/最差翻译示例
- 详细的评估指标值

## 示例文件

项目包含了几个示例文件，您可以使用这些文件测试工具的功能：

### 中文到英文翻译评估示例
```bash
python app.py evaluate examples/reference.txt examples/translation1.txt
```

### 英文到英文翻译评估示例
```bash
python app.py evaluate examples/reference_en.txt examples/translation1.txt
```

## 高级功能

### 自定义评估指标
您可以通过修改 `novel_translation_evaluator.py` 文件添加新的评估指标。

### 批量处理
可以通过编写脚本来实现批量处理多个翻译文件的功能。

## 技术说明

- **NLP库**：使用spaCy进行英文分词，jieba进行中文分词
- **评估指标**：使用nltk库提供的BLEU和METEOR算法
- **相似度计算**：使用scikit-learn库的TF-IDF和余弦相似度
- **Web界面**：使用Streamlit构建直观的用户界面
- **翻译支持**：使用deep-translator库的GoogleTranslator实现自动翻译

## 注意事项

1. 工具支持多种语言，但主要针对中英文翻译进行了优化
2. 评估结果仅供参考，最终质量判断需要结合人工评估
3. 对于长文本，评估过程可能会需要一些时间
4. 确保安装了所需的语言模型（如spaCy的英文模型）

## 许可证

本项目采用MIT许可证，详情请参考LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进工具的功能。