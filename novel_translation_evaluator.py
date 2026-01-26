#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说翻译效果评估工具
核心功能实现模块
"""

import os
import re
import yaml
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from tqdm import tqdm
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import spacy
from deep_translator import GoogleTranslator

# 下载必要的NLTK数据
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class NovelTranslationEvaluator:
    """小说翻译效果评估器"""

    def __init__(self, config_file: str = "config.yaml"):
        """初始化评估器"""
        self.config = self._load_config(config_file)
        self._initialize_nlp_models()
        self.translator = GoogleTranslator(source=self.config["language"]["source"], target=self.config["language"]["target"])

    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "language": {
                "source": "zh",
                "target": "en"
            },
            "metrics": {
                "bleu": True,
                "meteor": True,
                "cosine_similarity": True,
                "length_ratio": True
            },
            "preprocessing": {
                "remove_punctuation": True,
                "lowercase": False,
                "remove_stopwords": False
            }
        }

        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
            default_config.update(user_config)

        return default_config

    def _initialize_nlp_models(self):
        """初始化NLP模型"""
        self.nlp_models = {}
        if self.config["language"]["target"] == "en":
            try:
                self.nlp_models["en"] = spacy.load("en_core_web_sm")
            except Exception as e:
                print(f"无法加载spaCy英文模型，使用简单分词方法替代: {e}")
                self.nlp_models["en"] = None

        if self.config["language"]["source"] == "zh":
            self.nlp_models["zh"] = jieba

    def _preprocess_text(self, text: str, language: str) -> str:
        """文本预处理"""
        if self.config["preprocessing"]["remove_punctuation"]:
            if language == "zh":
                # 中文标点符号
                text = re.sub(r'[。，！？；：“”‘’（）【】{}《》<>.,!?;:"\'()\[\]{}<>]', '', text)
            else:
                # 英文标点符号
                text = re.sub(r'[.,!?;:"\'()\[\]{}<>]', '', text)

        if self.config["preprocessing"]["lowercase"]:
            text = text.lower()

        return text.strip()

    def _tokenize_text(self, text: str, language: str) -> List[str]:
        """文本分词"""
        if language == "en":
            if self.nlp_models["en"]:
                doc = self.nlp_models["en"](text)
                return [token.text for token in doc if not token.is_punct and not token.is_space]
            else:
                # 如果无法加载spaCy模型，使用简单的分词方法
                return text.split()
        elif language == "zh":
            return list(self.nlp_models["zh"].cut(text))
        else:
            return text.split()

    def calculate_bleu(self, reference: str, translation: str) -> float:
        """计算BLEU分数"""
        ref_tokens = self._tokenize_text(reference, self.config["language"]["target"])
        trans_tokens = self._tokenize_text(translation, self.config["language"]["target"])

        smooth_fn = SmoothingFunction().method1
        try:
            score = sentence_bleu([ref_tokens], trans_tokens, smoothing_function=smooth_fn)
        except Exception as e:
            print(f"BLEU分数计算错误: {e}")
            score = 0.0

        return score

    def calculate_meteor(self, reference: str, translation: str) -> float:
        """计算METEOR分数"""
        ref_tokens = self._tokenize_text(reference, self.config["language"]["target"])
        trans_tokens = self._tokenize_text(translation, self.config["language"]["target"])

        try:
            score = meteor_score([ref_tokens], trans_tokens)
        except Exception as e:
            print(f"METEOR分数计算错误: {e}")
            score = 0.0

        return score

    def calculate_cosine_similarity(self, reference: str, translation: str) -> float:
        """计算余弦相似度"""
        vectorizer = TfidfVectorizer(tokenizer=lambda x: self._tokenize_text(x, self.config["language"]["target"]))
        try:
            tfidf_matrix = vectorizer.fit_transform([reference, translation])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except Exception as e:
            print(f"余弦相似度计算错误: {e}")
            cosine_sim = 0.0

        return cosine_sim

    def calculate_length_ratio(self, reference: str, translation: str) -> float:
        """计算长度比率"""
        ref_length = len(reference.strip())
        trans_length = len(translation.strip())

        if ref_length == 0 or trans_length == 0:
            return 0.0

        return min(trans_length / ref_length, ref_length / trans_length)

    def evaluate_sentence(self, reference: str, translation: str) -> Dict[str, float]:
        """评估单个句子的翻译质量"""
        results = {}

        # 如果源语言和目标语言不同，先将参考文本翻译成目标语言
        if self.config["language"]["source"] != self.config["language"]["target"]:
            try:
                reference = self.translator.translate(reference)
                print(f"翻译后的参考文本: {reference}")
            except Exception as e:
                print(f"翻译参考文本时出错: {e}")
                return {"bleu": 0.0, "meteor": 0.0, "cosine_similarity": 0.0, "length_ratio": 0.0, "overall_score": 0.0}

        # 预处理文本，使用目标语言的预处理方法
        processed_reference = self._preprocess_text(reference, self.config["language"]["target"])
        processed_translation = self._preprocess_text(translation, self.config["language"]["target"])

        if self.config["metrics"]["bleu"]:
            results["bleu"] = self.calculate_bleu(processed_reference, processed_translation)

        if self.config["metrics"]["meteor"]:
            results["meteor"] = self.calculate_meteor(processed_reference, processed_translation)

        if self.config["metrics"]["cosine_similarity"]:
            results["cosine_similarity"] = self.calculate_cosine_similarity(processed_reference, processed_translation)

        if self.config["metrics"]["length_ratio"]:
            results["length_ratio"] = self.calculate_length_ratio(processed_reference, processed_translation)

        # 计算综合评分
        results["overall_score"] = np.mean(list(results.values()))

        return results

    def evaluate_texts(self, reference_text: str, translation_text: str) -> Dict[str, Any]:
        """评估整个文本的翻译质量"""
        # 句子分割
        try:
            if self.config["language"]["source"] == "zh-CN" or self.config["language"]["source"] == "zh":
                # 中文句子分割
                reference_sentences = re.split(r'[。！？；]', reference_text)
                reference_sentences = [s.strip() for s in reference_sentences if s.strip()]
            else:
                reference_sentences = nltk.sent_tokenize(reference_text)

            if self.config["language"]["target"] == "en":
                translation_sentences = nltk.sent_tokenize(translation_text)
            else:
                # 其他语言句子分割
                translation_sentences = []
                temp = []
                for char in translation_text:
                    temp.append(char)
                    if char in ['.', '!', '?', ';']:
                        translation_sentences.append(''.join(temp).strip())
                        temp = []
                if temp:
                    translation_sentences.append(''.join(temp).strip())

        except Exception as e:
            print(f"无法使用NLTK进行句子分割，使用简单方法替代: {e}")
            # 使用简单的句子分割方法
            if self.config["language"]["source"] == "zh":
                reference_sentences = reference_text.split('。')
                reference_sentences = [s.strip() for s in reference_sentences if s.strip()]
            else:
                reference_sentences = reference_text.split('.')
                reference_sentences = [s.strip() for s in reference_sentences if s.strip()]

            if self.config["language"]["target"] == "zh":
                translation_sentences = translation_text.split('。')
                translation_sentences = [s.strip() for s in translation_sentences if s.strip()]
            else:
                translation_sentences = translation_text.split('.')
                translation_sentences = [s.strip() for s in translation_sentences if s.strip()]

        # 确保句子数量一致
        min_len = min(len(reference_sentences), len(translation_sentences))
        reference_sentences = reference_sentences[:min_len]
        translation_sentences = translation_sentences[:min_len]

        # 评估每个句子
        sentence_results = []
        for ref_sent, trans_sent in tqdm(zip(reference_sentences, translation_sentences),
                                         total=min_len, desc="评估进度"):
            result = self.evaluate_sentence(ref_sent, trans_sent)
            result["reference"] = ref_sent
            result["translation"] = trans_sent
            sentence_results.append(result)

        # 计算整体统计
        df = pd.DataFrame(sentence_results)
        overall_stats = df.mean(numeric_only=True).to_dict()
        overall_stats["total_sentences"] = min_len
        overall_stats["sentence_level_results"] = sentence_results

        return overall_stats

    def evaluate_file(self, reference_file: str, translation_file: str, output_file: str = None) -> Dict[str, Any]:
        """评估文件的翻译质量"""
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_text = f.read()

        with open(translation_file, 'r', encoding='utf-8') as f:
            translation_text = f.read()

        results = self.evaluate_texts(reference_text, translation_text)

        if output_file:
            self._save_results(results, output_file)

        return results

    def _save_results(self, results: Dict[str, Any], output_file: str):
        """保存评估结果"""
        df = pd.DataFrame(results["sentence_level_results"])
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        # 保存统计信息
        stats_file = output_file.replace('.csv', '_stats.txt')
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("翻译效果评估统计结果\n")
            f.write("=" * 30 + "\n")
            for key, value in results.items():
                if key != "sentence_level_results":
                    if isinstance(value, float):
                        f.write(f"{key}: {value:.4f}\n")
                    else:
                        f.write(f"{key}: {value}\n")

    def compare_translations(self, reference_file: str, translation_files: List[str],
                           output_dir: str = "comparison_results") -> Dict[str, Any]:
        """比较多个翻译版本"""
        os.makedirs(output_dir, exist_ok=True)

        # 读取参考文本
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_text = f.read()

        comparison_results = {
            "reference_file": reference_file,
            "translation_files": translation_files,
            "results": []
        }

        for trans_file in translation_files:
            result = self.evaluate_file(reference_file, trans_file)
            comparison_results["results"].append({
                "translation_file": trans_file,
                "scores": result
            })

            # 保存单个文件的结果
            filename = os.path.basename(trans_file).split('.')[0]
            output_file = os.path.join(output_dir, f"{filename}_results.csv")
            self._save_results(result, output_file)

        # 保存比较摘要
        self._save_comparison_summary(comparison_results, output_dir)

        return comparison_results

    def _save_comparison_summary(self, comparison_results: Dict[str, Any], output_dir: str):
        """保存比较摘要"""
        summary_file = os.path.join(output_dir, "comparison_summary.csv")

        summary_data = []
        for result in comparison_results["results"]:
            row = {
                "translation_file": result["translation_file"],
                "overall_score": result["scores"]["overall_score"],
                "bleu": result["scores"]["bleu"],
                "meteor": result["scores"]["meteor"],
                "cosine_similarity": result["scores"]["cosine_similarity"],
                "length_ratio": result["scores"]["length_ratio"],
                "total_sentences": result["scores"]["total_sentences"]
            }
            summary_data.append(row)

        pd.DataFrame(summary_data).to_csv(summary_file, index=False, encoding='utf-8-sig')

        # 保存详细统计
        detailed_file = os.path.join(output_dir, "detailed_comparison.txt")
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write("翻译版本比较结果\n")
            f.write("=" * 40 + "\n")
            f.write(f"参考文件: {comparison_results['reference_file']}\n\n")

            for i, result in enumerate(comparison_results['results'], 1):
                f.write(f"翻译版本 {i}: {result['translation_file']}\n")
                f.write("-" * 30 + "\n")
                for key, value in result['scores'].items():
                    if key != "sentence_level_results":
                        if isinstance(value, float):
                            f.write(f"{key}: {value:.4f}\n")
                        else:
                            f.write(f"{key}: {value}\n")
                f.write("\n")

    def analyze_sentence_length_effect(self, reference_file: str, translation_file: str,
                                     output_file: str = "sentence_length_analysis.csv"):
        """分析句子长度对翻译质量的影响"""
        results = self.evaluate_file(reference_file, translation_file)

        analysis_data = []
        for sent_result in results['sentence_level_results']:
            ref_length = len(sent_result['reference'])
            trans_length = len(sent_result['translation'])

            analysis_data.append({
                'reference_length': ref_length,
                'translation_length': trans_length,
                'length_ratio': sent_result['length_ratio'],
                'bleu': sent_result['bleu'],
                'meteor': sent_result['meteor'],
                'cosine_similarity': sent_result['cosine_similarity'],
                'overall_score': sent_result['overall_score']
            })

        pd.DataFrame(analysis_data).to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"句子长度分析结果已保存到: {output_file}")

    def generate_report(self, results: Dict[str, Any], report_file: str = "translation_report.txt"):
        """生成详细的评估报告"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("小说翻译效果评估报告\n")
            f.write("=" * 40 + "\n\n")

            # 基本信息
            f.write("1. 评估基本信息\n")
            f.write("-" * 30 + "\n")
            f.write(f"源语言: {self.config['language']['source']}\n")
            f.write(f"目标语言: {self.config['language']['target']}\n")
            f.write(f"评估指标: {', '.join([k for k, v in self.config['metrics'].items() if v])}\n")
            f.write(f"句子数量: {results['total_sentences']}\n\n")

            # 整体评分
            f.write("2. 整体翻译质量评分\n")
            f.write("-" * 30 + "\n")
            for metric, value in results.items():
                if isinstance(value, float) and metric != 'total_sentences':
                    f.write(f"{metric:20} | {value:.4f}\n")
            f.write("\n")

            # 最佳/最差句子
            df = pd.DataFrame(results['sentence_level_results'])
            best_sent = df.loc[df['overall_score'].idxmax()]
            worst_sent = df.loc[df['overall_score'].idxmin()]

            f.write("3. 最佳翻译示例\n")
            f.write("-" * 30 + "\n")
            f.write(f"原始句子: {best_sent['reference']}\n")
            f.write(f"翻译句子: {best_sent['translation']}\n")
            f.write(f"综合评分: {best_sent['overall_score']:.4f}\n")
            for metric in self.config['metrics']:
                if metric in best_sent and self.config['metrics'][metric]:
                    f.write(f"{metric}: {best_sent[metric]:.4f}\n")
            f.write("\n")

            f.write("4. 最差翻译示例\n")
            f.write("-" * 30 + "\n")
            f.write(f"原始句子: {worst_sent['reference']}\n")
            f.write(f"翻译句子: {worst_sent['translation']}\n")
            f.write(f"综合评分: {worst_sent['overall_score']:.4f}\n")
            for metric in self.config['metrics']:
                if metric in worst_sent and self.config['metrics'][metric]:
                    f.write(f"{metric}: {worst_sent[metric]:.4f}\n")
            f.write("\n")

            # 统计信息
            f.write("5. 统计信息\n")
            f.write("-" * 30 + "\n")
            for metric in self.config['metrics']:
                if self.config['metrics'][metric]:
                    metric_values = df[metric].values
                    f.write(f"{metric}:\n")
                    f.write(f"  平均值: {np.mean(metric_values):.4f}\n")
                    f.write(f"  标准差: {np.std(metric_values):.4f}\n")
                    f.write(f"  最小值: {np.min(metric_values):.4f}\n")
                    f.write(f"  最大值: {np.max(metric_values):.4f}\n")
                    f.write("\n")

        print(f"评估报告已保存到: {report_file}")