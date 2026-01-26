#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试句子分割方法
"""

import nltk
from novel_translation_evaluator import NovelTranslationEvaluator

def test_sentence_splitting():
    """测试句子分割方法"""
    evaluator = NovelTranslationEvaluator()

    # 读取英文参考文本
    with open("examples/reference_en.txt", 'r', encoding='utf-8') as f:
        reference_text = f.read()

    # 读取英文翻译文本
    with open("examples/translation1.txt", 'r', encoding='utf-8') as f:
        translation_text = f.read()

    print("=== 英文参考文本句子分割测试 ===")
    print("原始文本:")
    print(reference_text)
    print("\n" + "-" * 50 + "\n")

    # 使用NLTK分割句子
    try:
        reference_sentences = nltk.sent_tokenize(reference_text)
        print(f"句子数量: {len(reference_sentences)}")
        print("\n句子列表:")
        for i, sent in enumerate(reference_sentences, 1):
            print(f"{i}. {sent}")
    except Exception as e:
        print(f"句子分割错误: {e}")

    print("\n" + "=" * 50 + "\n")

    print("=== 英文翻译文本句子分割测试 ===")
    print("原始文本:")
    print(translation_text)
    print("\n" + "-" * 50 + "\n")

    try:
        translation_sentences = nltk.sent_tokenize(translation_text)
        print(f"句子数量: {len(translation_sentences)}")
        print("\n句子列表:")
        for i, sent in enumerate(translation_sentences, 1):
            print(f"{i}. {sent}")
    except Exception as e:
        print(f"句子分割错误: {e}")

    print("\n" + "=" * 50 + "\n")

    # 测试自定义句子分割方法
    print("=== 自定义英文句子分割方法测试 ===")
    custom_reference_sentences = []
    temp = []
    for char in reference_text:
        temp.append(char)
        if char in ['.', '!', '?', ';']:
            custom_reference_sentences.append(''.join(temp).strip())
            temp = []
    if temp:
        custom_reference_sentences.append(''.join(temp).strip())

    print(f"句子数量: {len(custom_reference_sentences)}")
    print("\n句子列表:")
    for i, sent in enumerate(custom_reference_sentences, 1):
        print(f"{i}. {sent}")

if __name__ == "__main__":
    test_sentence_splitting()