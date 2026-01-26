#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文到英文的翻译评估功能
"""

from novel_translation_evaluator import NovelTranslationEvaluator

def test_chinese_to_english_evaluation():
    """测试中文到英文的翻译评估"""
    evaluator = NovelTranslationEvaluator()

    # 测试单个句子
    reference_chinese = "在一个遥远的星球上，有一个叫做“梦幻森林”的地方。"
    translation_english = "On a distant planet, there is a place called the 'Dream Forest'."

    print("=== 中文到英文翻译评估测试 ===")
    print("中文参考句子:", reference_chinese)
    print("英文翻译句子:", translation_english)
    print("=" * 50)

    # 评估单个句子
    results = evaluator.evaluate_sentence(reference_chinese, translation_english)
    print("句子级评估结果:")
    for metric, value in results.items():
        print(f"{metric}: {value:.4f}")
    print()

    # 测试多个句子
    reference_text = """在一个遥远的星球上，有一个叫做“梦幻森林”的地方。那里生长着各种奇花异草，住着许多神奇的生物。森林的中心有一棵巨大的生命之树，它是整个森林的心脏。

有一天，森林里来了一位年轻的冒险者。他听说生命之树的果实可以实现任何愿望，所以决定前往森林中心寻找它。在路上，他遇到了许多困难和挑战，但他始终没有放弃。

最终，他成功找到了生命之树。当他伸手去摘果实时，树精出现了。树精告诉他，生命之树的果实并不是随意可以摘取的，只有那些真正需要它的人才能获得。冒险者说出了自己的愿望——他希望能够治愈自己重病的母亲。"""

    translation_text = """On a distant planet, there is a place called the 'Dream Forest'. There grow all kinds of exotic flowers and plants, and there live many magical creatures. At the center of the forest stands a huge Tree of Life, which is the heart of the entire forest.

One day, a young adventurer came to the forest. He heard that the fruit of the Tree of Life could fulfill any wish, so he decided to go to the center of the forest to find it. On the way, he encountered many difficulties and challenges, but he never gave up.

Finally, he successfully found the Tree of Life. When he reached out to pick the fruit, the tree spirit appeared. The tree spirit told him that the fruit of the Tree of Life could not be picked at will; only those who truly needed it could obtain it. The adventurer said his wish - he hoped to cure his seriously ill mother."""

    print("=== 多个句子翻译评估测试 ===")
    results = evaluator.evaluate_texts(reference_text, translation_text)
    print(f"句子数量: {results['total_sentences']}")
    print("整体评估结果:")
    for metric, value in results.items():
        if metric != "sentence_level_results" and metric != "total_sentences":
            print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    test_chinese_to_english_evaluation()