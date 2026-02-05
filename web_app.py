#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说翻译效果评估工具 - Web应用
"""

import streamlit as st
import os
import pandas as pd
from novel_translation_evaluator import NovelTranslationEvaluator

# 设置Streamlit配置，跳过邮箱验证
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# 设置页面配置
st.set_page_config(page_title="小说翻译效果评估工具", layout="wide")

# 标题
st.title("📚 小说翻译效果评估工具")

st.markdown("""
这是一个专业的小说翻译效果评估工具，支持多种评估指标，帮助您客观评估翻译质量。
""")

# 配置区域
st.sidebar.header("⚙️ 配置")
config_file = st.sidebar.file_uploader("选择配置文件", type=["yaml", "yml"])

if config_file:
    evaluator = NovelTranslationEvaluator(config_file)
else:
    evaluator = NovelTranslationEvaluator()

# 阈值配置区域
st.sidebar.header("🎯 阈值配置")
st.sidebar.markdown("设置各个评估指标的阈值，低于阈值的句子将被标记为需要改进")

# 获取当前配置的阈值
default_thresholds = evaluator.config['metrics']['thresholds']

# 创建阈值滑块
thresholds = {}
thresholds['bleu'] = st.sidebar.slider("BLEU分数阈值", 0.0, 1.0, default_thresholds.get('bleu', 0.4), 0.05)
thresholds['meteor'] = st.sidebar.slider("METEOR分数阈值", 0.0, 1.0, default_thresholds.get('meteor', 0.6), 0.05)
thresholds['cosine_similarity'] = st.sidebar.slider("余弦相似度阈值", 0.0, 1.0, default_thresholds.get('cosine_similarity', 0.6), 0.05)
thresholds['length_ratio'] = st.sidebar.slider("长度比率阈值", 0.0, 1.0, default_thresholds.get('length_ratio', 0.7), 0.05)
thresholds['comet'] = st.sidebar.slider("COMET分数阈值", 0.0, 1.0, default_thresholds.get('comet', 0.7), 0.05)
thresholds['overall'] = st.sidebar.slider("综合评分阈值", 0.0, 1.0, default_thresholds.get('overall', 0.6), 0.05)

# 打分标准说明区域
st.sidebar.header("📊 打分标准说明")
st.sidebar.markdown("""
### BLEU分数
- **0.0 - 0.2**: 非常差，翻译与参考文本几乎不匹配
- **0.2 - 0.4**: 较差，匹配度低，存在大量错误
- **0.4 - 0.6**: 一般，基本匹配，但有一些错误
- **0.6 - 0.8**: 良好，匹配度高，翻译质量较好
- **0.8 - 1.0**: 优秀，翻译与参考文本高度匹配

### METEOR分数
- **0.0 - 0.4**: 非常差，词汇和语义匹配度低
- **0.4 - 0.6**: 较差，有一些匹配，但整体质量不高
- **0.6 - 0.7**: 一般，词汇和语义匹配度中等
- **0.7 - 0.8**: 良好，词汇和语义匹配度高
- **0.8 - 1.0**: 优秀，词汇和语义高度匹配

### 余弦相似度
- **0.0 - 0.5**: 非常差，语义相似度极低
- **0.5 - 0.6**: 较差，语义相似度较低
- **0.6 - 0.7**: 一般，语义相似度中等
- **0.7 - 0.8**: 良好，语义相似度高
- **0.8 - 1.0**: 优秀，语义高度相似

### 长度比率
- **0.0 - 0.6**: 非常差，翻译长度与参考文本差异过大
- **0.6 - 0.7**: 较差，长度差异较大
- **0.7 - 0.8**: 一般，长度差异适中
- **0.8 - 0.9**: 良好，长度差异较小
- **0.9 - 1.0**: 优秀，翻译长度与参考文本高度一致

### COMET分数
- **0.0 - 0.5**: 非常差，翻译质量严重不符合要求
- **0.5 - 0.6**: 较差，翻译质量较低
- **0.6 - 0.7**: 一般，翻译质量中等
- **0.7 - 0.8**: 良好，翻译质量较高
- **0.8 - 1.0**: 优秀，翻译质量非常高

### 综合评分
- **0.0 - 0.5**: 非常差，整体翻译质量严重不符合要求
- **0.5 - 0.6**: 较差，整体翻译质量较低
- **0.6 - 0.7**: 一般，整体翻译质量中等
- **0.7 - 0.8**: 良好，整体翻译质量较高
- **0.8 - 1.0**: 优秀，整体翻译质量非常高
""")

# 评估区域
st.header("📝 评估翻译质量")

col1, col2 = st.columns(2)

with col1:
    reference_file = st.file_uploader("上传参考原文文件", type=["txt", "md"])
    reference_text = st.text_area("或直接输入参考原文", height=300)

with col2:
    translation_file = st.file_uploader("上传翻译文件", type=["txt", "md"])
    translation_text = st.text_area("或直接输入翻译文本", height=300)

if st.button("开始评估", key="evaluate_btn"):
    # 读取文件内容
    if reference_file:
        reference_text = reference_file.getvalue().decode("utf-8")

    if translation_file:
        translation_text = translation_file.getvalue().decode("utf-8")

    if reference_text.strip() and translation_text.strip():
        with st.spinner("正在评估中..."):
            results = evaluator.evaluate_texts(reference_text, translation_text)

            # 显示结果
            st.success("评估完成！")

            # 整体评分
            st.subheader("📊 整体翻译质量评分")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("综合评分", f"{results['overall_score']:.4f}")
            col2.metric("BLEU分数", f"{results['bleu']:.4f}")
            col3.metric("METEOR分数", f"{results['meteor']:.4f}")
            col4.metric("余弦相似度", f"{results['cosine_similarity']:.4f}")
            col5.metric("长度比率", f"{results['length_ratio']:.4f}")
            col6.metric("COMET分数", f"{results['comet']:.4f}")

            # 句子级结果
            st.subheader("📄 句子级评估结果")
            df = st.dataframe(
                [
                    {
                        "原始句子": r["reference"],
                        "翻译句子": r["translation"],
                        "综合评分": f"{r['overall_score']:.4f}",
                        "BLEU": f"{r['bleu']:.4f}",
                        "METEOR": f"{r['meteor']:.4f}",
                        "余弦相似度": f"{r['cosine_similarity']:.4f}",
                        "长度比率": f"{r['length_ratio']:.4f}",
                        "COMET": f"{r['comet']:.4f}"
                    }
                    for r in results['sentence_level_results']
                ]
            )

            # 最佳/最差句子
            st.subheader("🏆 最佳/最差翻译示例")
            df_data = results['sentence_level_results']
            best_sent = max(df_data, key=lambda x: x['overall_score'])
            worst_sent = min(df_data, key=lambda x: x['overall_score'])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 最佳翻译")
                st.write(f"**原始句子:** {best_sent['reference']}")
                st.write(f"**翻译句子:** {best_sent['translation']}")
                st.write(f"**综合评分:** {best_sent['overall_score']:.4f}")

            with col2:
                st.markdown("### 最差翻译")
                st.write(f"**原始句子:** {worst_sent['reference']}")
                st.write(f"**翻译句子:** {worst_sent['translation']}")
                st.write(f"**综合评分:** {worst_sent['overall_score']:.4f}")

            # 翻译修改建议
            st.subheader("📝 翻译修改建议")
            suggestions = evaluator.generate_translation_suggestions(reference_text, translation_text, thresholds)
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    with st.expander(f"句子 {i}: 综合评分 {suggestion['overall_score']:.4f}"):
                        st.write(f"**原始句子:** {suggestion['reference']}")
                        st.write(f"**当前翻译:** {suggestion['translation']}")
                        st.write(f"**建议翻译:** {suggestion['suggestion']}")

                        # 显示问题原因
                        if suggestion['reasons']:
                            st.write("**问题原因:**")
                            for reason in suggestion['reasons']:
                                st.write(f"- {reason}")

                        # 显示详细指标
                        st.markdown("**详细评分:**")
                        for metric, value in suggestion['metrics'].items():
                            st.write(f"- {metric}: {value:.4f}")
            else:
                st.success("所有句子的翻译质量都符合要求")

            # 保存结果
            csv_data = evaluator._save_results(results, "temp_results.csv")
            with open("temp_results.csv", 'r', encoding='utf-8') as f:
                csv_content = f.read()

            st.download_button(
                "下载结果CSV",
                csv_content,
                file_name="evaluation_results.csv",
                mime="text/csv"
            )

            # 删除临时文件
            os.remove("temp_results.csv")
            os.remove("temp_results_stats.txt")
    else:
        st.error("请输入或上传参考原文和翻译文本")

# 文件对比区域
st.header("🔍 比较多个翻译版本")

reference_file_compare = st.file_uploader("上传参考原文文件", type=["txt", "md"], key="ref_compare")
translation_files = st.file_uploader("上传翻译文件", type=["txt", "md"], accept_multiple_files=True, key="trans_compare")

if st.button("开始比较", key="compare_btn"):
    if reference_file_compare and translation_files:
        with st.spinner("正在比较中..."):
            # 保存临时文件
            with open("temp_reference.txt", 'w', encoding='utf-8') as f:
                f.write(reference_file_compare.getvalue().decode("utf-8"))

            temp_trans_files = []
            for i, file in enumerate(translation_files):
                temp_path = f"temp_translation_{i}.txt"
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(file.getvalue().decode("utf-8"))
                temp_trans_files.append(temp_path)

            comparison_results = evaluator.compare_translations("temp_reference.txt", temp_trans_files, "temp_comparison")

            st.success("比较完成！")

            # 显示比较结果
            st.subheader("📈 翻译版本比较结果")

            # 读取比较摘要
            with open("temp_comparison/comparison_summary.csv", 'r', encoding='utf-8') as f:
                comparison_df = pd.read_csv(f)

            st.dataframe(comparison_df)

            # 下载结果
            with open("temp_comparison/comparison_summary.csv", 'r', encoding='utf-8') as f:
                st.download_button(
                    "下载比较结果",
                    f.read(),
                    file_name="comparison_results.csv",
                    mime="text/csv"
                )

            # 清理临时文件
            os.remove("temp_reference.txt")
            for file in temp_trans_files:
                os.remove(file)
            import shutil
            shutil.rmtree("temp_comparison")
    else:
        st.error("请上传参考原文和至少一个翻译文件")

# 文档区域
st.sidebar.header("📖 使用说明")
st.sidebar.markdown("""
## 工具功能

### 1. 评估翻译质量
- 支持多种评估指标（BLEU, METEOR, 余弦相似度, 长度比率）
- 句子级和整体级别的评估
- 详细的评估报告

### 2. 比较翻译版本
- 同时比较多个翻译版本
- 生成比较报告
- 可视化分析结果

### 3. 分析功能
- 句子长度对翻译质量的影响
- 评估指标的相关性分析
- 翻译质量的分布分析

## 使用方法

### 评估单个翻译

1. 准备参考原文文件（.txt或.md格式）
2. 准备翻译文件（.txt或.md格式）
3. 使用命令 `python app.py evaluate reference.txt translation.txt`

### 比较多个翻译

1. 准备参考原文文件
2. 准备多个翻译文件
3. 使用命令 `python app.py compare reference.txt translation1.txt translation2.txt`

### Web界面

使用命令 `streamlit run web_app.py` 启动Web界面，然后在浏览器中访问显示的地址。
""")
