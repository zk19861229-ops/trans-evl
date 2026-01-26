#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分词和BLEU分数计算过程
"""

from novel_translation_evaluator import NovelTranslationEvaluator

def test_tokenization():
    """测试分词方法"""
    evaluator = NovelTranslationEvaluator()

    # 测试中文分词
    chinese_text = "在一个遥远的星球上，有一个叫做“梦幻森林”的地方。"
    chinese_tokens = evaluator._tokenize_text(chinese_text, "zh")
    print("中文分词结果:")
    print(chinese_tokens)

    # 测试英文分词
    english_text = "On a distant planet, there is a place called the 'Dream Forest'."
    english_tokens = evaluator._tokenize_text(english_text, "en")
    print("\n英文分词结果:")
    print(english_tokens)

def test_bleu_score():
    """测试BLEU分数计算"""
    evaluator = NovelTranslationEvaluator()

    # 测试简单句子的BLEU分数
    reference = "在一个遥远的星球上，有一个叫做梦幻森林的地方。"
    translation = "On a distant planet, there is a place called Dream Forest."

    # 预处理文本
    preprocessed_ref = evaluator._preprocess_text(reference, "en")
    preprocessed_trans = evaluator._preprocess_text(translation, "en")

    print("预处理后的参考文本:")
    print(preprocessed_ref)

    print("\n预处理后的翻译文本:")
    print(preprocessed_trans)

    # 分词
    ref_tokens = evaluator._tokenize_text(preprocessed_ref, "en")
    trans_tokens = evaluator._tokenize_text(preprocessed_trans, "en")

    print("\n参考文本分词结果:")
    print(ref_tokens)

    print("\n翻译文本分词结果:")
    print(trans_tokens)

    # 计算BLEU分数
    bleu_score = evaluator.calculate_bleu(preprocessed_ref, preprocessed_trans)
    print(f"\nBLEU分数: {bleu_score:.4f}")

def test_cosine_similarity():
    """测试余弦相似度计算"""
    evaluator = NovelTranslationEvaluator()

    reference = "在一个遥远的星球上，有一个叫做梦幻森林的地方。"
    translation = "On a distant planet, there is a place called Dream Forest."

    # 预处理文本
    preprocessed_ref = evaluator._preprocess_text(reference, "en")
    preprocessed_trans = evaluator._preprocess_text(translation, "en")

    print("预处理后的参考文本:")
    print(preprocessed_ref)

    print("\n预处理后的翻译文本:")
    print(preprocessed_trans)

    # 计算余弦相似度
    cosine_sim = evaluator.calculate_cosine_similarity(preprocessed_ref, preprocessed_trans)
    print(f"\n余弦相似度: {cosine_sim:.4f}")

if __name__ == "__main__":
    print("=== 测试分词和BLEU分数计算过程 ===")
    print("=" * 50)

    try:
        test_tokenization()
        print("\n" + "=" * 50)
        test_bleu_score()
        print("\n" + "=" * 50)
        test_cosine_similarity()
    except Exception as e:
        print(f"测试过程中出现错误: {e}")