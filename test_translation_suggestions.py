#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试翻译修改建议功能
"""

from novel_translation_evaluator import NovelTranslationEvaluator

def test_translation_suggestions():
    """测试翻译修改建议功能"""
    evaluator = NovelTranslationEvaluator()

    # 测试文本（包含一些翻译质量较低的句子）
    reference_text = """在一个遥远的星球上，有一个叫做“梦幻森林”的地方。那里生长着各种奇花异草，住着许多神奇的生物。森林的中心有一棵巨大的生命之树，它是整个森林的心脏。

有一天，森林里来了一位年轻的冒险者。他听说生命之树的果实可以实现任何愿望，所以决定前往森林中心寻找它。在路上，他遇到了许多困难和挑战，但他始终没有放弃。

最终，他成功找到了生命之树。当他伸手去摘果实时，树精出现了。树精告诉他，生命之树的果实并不是随意可以摘取的，只有那些真正需要它的人才能获得。冒险者说出了自己的愿望——他希望能够治愈自己重病的母亲。"""

    # 包含一些低质量翻译的文本
    translation_text = """On a faraway planet, there is a place called "Dream Forest". There are various strange flowers and plants growing, and many magical creatures living there. At the center of the forest is a huge Tree of Life, which is the heart of the entire forest.

One day, a young adventurer came to the forest. He heard that the fruit of the Tree of Life can fulfill any wish, so he decided to go to the forest center to find it. On the way, he encountered many difficulties and challenges, but he never gave up.

Finally, he succeeded in finding the Tree of Life. When he reached out to pick the fruit, the tree spirit appeared. The tree spirit told him that the fruit of the Tree of Life is not something that can be picked at will. Only those who truly need it can obtain it. The adventurer said his wish - he hopes to cure his seriously ill mother.

This is a very bad translation. It doesn't make sense at all. Please improve it.

Another very poor translation. The quality is extremely low. Please fix this.

This is just a placeholder. It doesn't mean anything. Please replace this with a real translation.

"""

    print("=== 翻译修改建议功能测试 ===\n")

    # 生成翻译建议（使用默认阈值）
    suggestions = evaluator.generate_translation_suggestions(reference_text, translation_text)

    if suggestions:
        print(f"发现 {len(suggestions)} 个需要改进的句子：\n")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"句子 {i}:")
            print(f"原始句子: {suggestion['reference']}")
            print(f"当前翻译: {suggestion['translation']}")
            print(f"建议翻译: {suggestion['suggestion']}")
            print(f"综合评分: {suggestion['overall_score']:.4f}")
            print("问题原因:")
            for reason in suggestion['reasons']:
                print(f"- {reason}")
            print()
    else:
        print("所有句子的翻译质量都符合要求！")

    print("=" * 50)
    print("测试完成")

if __name__ == "__main__":
    test_translation_suggestions()
