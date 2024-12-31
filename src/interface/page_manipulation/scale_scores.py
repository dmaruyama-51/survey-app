import streamlit as st
import pandas as pd
from typing import List, Dict
from src.core.manipulation import calculate_scale_scores


def render_scale_score_section(df: pd.DataFrame) -> pd.DataFrame:
    """因子得点計算のUIセクションを表示"""
    st.markdown("#### Scale Score Calculation")
    st.write(
        "Create scale scores by selecting items that belong to each scale. "
        "Both total scores and mean scores will be calculated."
    )

    # 因子の数を選択
    num_scales = st.number_input(
        "Number of scales to create",
        min_value=1,
        max_value=10,
        value=1,
        help="Enter the number of different scales you want to calculate",
    )

    scales_config: Dict[str, List[str]] = {}
    df_with_scores = df.copy()

    # 各因子の設定
    for i in range(num_scales):
        st.markdown(f"##### Scale {i + 1}")

        # 因子名の入力
        scale_name = st.text_input(
            f"Scale {i + 1} name",
            value=f"scale_{i + 1}",
            key=f"scale_name_{i}",
            help="Enter a name for this scale (e.g., 'anxiety', 'satisfaction')",
        )

        # 項目の選択（すでに逆転済みの項目も含める）
        scale_items: List[str] = st.multiselect(
            f"Select items for {scale_name}",
            options=df.columns,
            key=f"scale_items_{i}",
            help="Select all items that belong to this scale",
        )

        if scale_items:
            scales_config[scale_name] = scale_items
            # 因子得点を計算
            df_with_scores = calculate_scale_scores(
                df_with_scores, scale_items, scale_name
            )

            # プレビューを表示
            with st.expander(f"Preview {scale_name} scores"):
                preview_cols = scale_items + [
                    f"{scale_name}_total",
                    f"{scale_name}_mean",
                ]
                st.dataframe(
                    df_with_scores[preview_cols].head(),
                    use_container_width=True,
                )

    return df_with_scores
