import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# 设置页面配置
st.set_page_config(
    page_title="IP数据分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px 15px;
        margin: 5px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        text-align: center;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-title {
        font-size: 13px;
        font-weight: 600;
        color: white;
        margin-bottom: 6px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 22px;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-subtitle {
        font-size: 11px;
        color: rgba(255,255,255,0.9);
        margin-top: 3px;
    }
    .main-title {
        margin-bottom: 0.5rem !important;
        padding-top: 0.2rem !important;
    }
    .chart-title {
        margin-bottom: 0.2rem !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    /* 商品配置区域样式 */
    .config-scroll-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    .product-config-item {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .config-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    .config-buttons {
        display: flex;
        gap: 5px;
    }
    .store-count-info {
        font-size: 12px;
        color: #666;
        margin-top: 5px;
    }
    .info-box {
        background-color: #f0f2f6;
        border-left: 4px solid #4CAF50;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        font-size: 14px;
    }
    /* 图表区域背景 */
    .chart-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# 页面导航
def create_navigation():
    st.sidebar.markdown("## 🧭 页面导航")
    if st.sidebar.button("📊 IP社媒/电商数据大屏", use_container_width=True, key="nav_dashboard"):
        st.session_state.current_page = "dashboard"
    if st.sidebar.button("🎯 IP商品销量预测模拟器", use_container_width=True, key="nav_predictor"):
        st.session_state.current_page = "predictor"
    st.sidebar.markdown("---")
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"

# 创建指标卡片
def create_metric_card(title, value, subtitle=""):
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# 第一页：社媒/电商数据大屏 - 保持完全不变
def dashboard_page():
    try:
        # 读取数据
        @st.cache_data
        def load_data():
            df = pd.read_excel('demo_data.xlsx', sheet_name='社媒_电商原始数据表')
            df['日期'] = pd.to_datetime(df['日期'])
            return df
        
        df = load_data()
        
        # 左侧标题 - 减小上方间距
        st.markdown("<h2 style='text-align: left; margin-bottom: 0.5rem; padding-top: 0.2rem;'>📊 IP社媒/电商数据大屏</h2>", unsafe_allow_html=True)
        
        # 侧边栏
        st.sidebar.markdown("**指标筛选**")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            show_engagement = st.checkbox("互动量", value=True, key="engagement")
            show_posts = st.checkbox("发帖数", value=True, key="posts")
        with col2:
            show_sales = st.checkbox("销量", value=True, key="sales")
            show_secondhand = st.checkbox("二手销量", value=False, key="secondhand_sales")
        
        st.sidebar.markdown("**社媒平台**")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            tiktok_social = st.checkbox("TikTok", value=True, key="tiktok")
            ins = st.checkbox("Instagram", value=True, key="ins")
            facebook = st.checkbox("Facebook", value=True, key="facebook")
        with col2:
            twitter = st.checkbox("Twitter", value=True, key="twitter")
            news = st.checkbox("News", value=True, key="news")
            fan_heat = st.checkbox("同人热度", value=True, key="fan_heat")
        
        st.sidebar.markdown("**电商平台**")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            amazon = st.checkbox("Amazon", value=True, key="amazon")
        with col2:
            tiktok_sale = st.checkbox("TikTok Shop", value=True, key="tiktok_sale")
        secondhand = st.sidebar.checkbox("二手市场", value=False, key="secondhand")
        
        st.sidebar.markdown("**IP选择**")
        unique_ips = df['IP名称'].unique()
        selected_ips = st.sidebar.multiselect(
            "选择IP名称",
            options=unique_ips,
            default=list(unique_ips)[:2] if len(unique_ips) > 0 else [],
            key="ip_selector",
            label_visibility="collapsed"
        )
        
        st.sidebar.markdown("**时间范围**")
        min_date = df['日期'].min().date()
        max_date = df['日期'].max().date()
        start_date = st.sidebar.date_input("起始日期", value=min_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
        end_date = st.sidebar.date_input("结束日期", value=max_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
        
        if start_date > end_date:
            st.sidebar.error("错误：起始日期不能晚于结束日期")
            start_date, end_date = end_date, start_date
        
        # 数据过滤
        filtered_df = df[
            (df['IP名称'].isin(selected_ips)) & 
            (df['日期'] >= pd.to_datetime(start_date)) & 
            (df['日期'] <= pd.to_datetime(end_date))
        ].sort_values('日期')
        
        if filtered_df.empty:
            st.warning("没有找到符合条件的数据，请调整筛选条件")
            return
        
        # 计算仪表盘指标
        st.markdown('<div class="compact-section">', unsafe_allow_html=True)
        st.subheader("📈 关键指标仪表盘")
        
        # 创建指标列
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # 1. 日均发帖数
        with col1:
            social_platforms = []
            if tiktok_social: social_platforms.append('tiktok_social')
            if ins: social_platforms.append('ins')
            if facebook: social_platforms.append('facebook')
            if twitter: social_platforms.append('twitter')
            if news: social_platforms.append('news')
            
            if social_platforms:
                post_columns = []
                for platform in social_platforms:
                    col_name = f'社媒热度_发帖数_{platform}'
                    if col_name in filtered_df.columns:
                        post_columns.append(col_name)
                
                if post_columns:
                    daily_posts = filtered_df[filtered_df['数据状态'] == '实际'][post_columns].sum(axis=1).mean()
                    create_metric_card("📤 日均发帖数", f"{daily_posts:,.0f}", f"共{len(post_columns)}个平台")
                else:
                    create_metric_card("📤 日均发帖数", "0", "列不存在")
            else:
                create_metric_card("📤 日均发帖数", "0", "未选择平台")
        
        # 2. 日均互动量
        with col2:
            if social_platforms:
                engagement_columns = []
                for platform in social_platforms:
                    col_name = f'社媒热度_互动量_{platform}'
                    if col_name in filtered_df.columns:
                        engagement_columns.append(col_name)
                
                if engagement_columns:
                    daily_engagement = filtered_df[filtered_df['数据状态'] == '实际'][engagement_columns].sum(axis=1).mean()
                    create_metric_card("💬 日均互动量", f"{daily_engagement:,.0f}", f"共{len(engagement_columns)}个平台")
                else:
                    create_metric_card("💬 日均互动量", "0", "列不存在")
            else:
                create_metric_card("💬 日均互动量", "0", "未选择平台")
        
        # 3. 日均同人热度
        with col3:
            if '社媒热度_同人热度' in filtered_df.columns:
                daily_fan_heat = filtered_df[filtered_df['数据状态'] == '实际']['社媒热度_同人热度'].mean()
                create_metric_card("🔥 日均同人热度", f"{daily_fan_heat:.1f}", "热度指数")
            else:
                create_metric_card("🔥 日均同人热度", "0", "数据不可用")
        
        # 4. 日均电商销量
        with col4:
            ecommerce_platforms = []
            if amazon: ecommerce_platforms.append('amazon')
            if tiktok_sale: ecommerce_platforms.append('tiktok_sale')
            
            if ecommerce_platforms:
                sales_columns = []
                for platform in ecommerce_platforms:
                    col_name = f'电商热度_销量_{platform}'
                    if col_name in filtered_df.columns:
                        sales_columns.append(col_name)
                
                if sales_columns:
                    daily_sales = filtered_df[filtered_df['数据状态'] == '实际'][sales_columns].sum(axis=1).mean()
                    create_metric_card("🛒 日均电商销量", f"{daily_sales:,.0f}", f"共{len(sales_columns)}个平台")
                else:
                    create_metric_card("🛒 日均电商销量", "0", "列不存在")
            else:
                create_metric_card("🛒 日均电商销量", "0", "未选择平台")
        
        # 5. 日均二手销量
        with col5:
            if '电商热度_二手销量' in filtered_df.columns:
                daily_secondhand = filtered_df[filtered_df['数据状态'] == '实际']['电商热度_二手销量'].mean()
                create_metric_card("🔄 日均二手销量", f"{daily_secondhand:,.0f}", "二手市场")
            else:
                create_metric_card("🔄 日均二手销量", "0", "数据不可用")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 趋势图表 - 使用Streamlit container实现浅灰色背景
        st.markdown('<div class="compact-section">', unsafe_allow_html=True)
        st.subheader("📊 趋势分析")

        # 使用Streamlit容器包装整个趋势分析区域，添加浅灰色背景
        with st.container():
            # 为容器添加浅灰色背景样式
            st.markdown(
                """
                <style>
                div[data-testid="stContainer"] {
                    background-color: #f8f9fa !important;
                    border-radius: 15px !important;
                    padding: 25px !important;
                    margin: 15px 0 !important;
                    border: 1px solid #e9ecef !important;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # 创建带分割线的布局
            col1, divider, col2 = st.columns([48, 2, 48])
            
            with col1:
                # 紧凑标题间距
                st.markdown('<p class="chart-title">📱 社媒热度趋势</p>', unsafe_allow_html=True)
                
                if social_platforms and selected_ips:
                    fig_social = make_subplots(specs=[[{"secondary_y": True}]])
                    
                    # 现代配色方案
                    colors = ['#4361ee', '#3a0ca3', '#4cc9f0', '#f72585', '#7209b7', '#4895ef', '#560bad', '#b5179e']
                    color_idx = 0
                    
                    # 互动量数据（主纵轴）
                    if show_engagement:
                        for platform in social_platforms:
                            engagement_col = f'社媒热度_互动量_{platform}'
                            if engagement_col in filtered_df.columns:
                                for ip in selected_ips:
                                    color = colors[color_idx % len(colors)]
                                    color_idx += 1
                                    ip_data = filtered_df[filtered_df['IP名称'] == ip]
                                    # 实际数据
                                    actual_data = ip_data[ip_data['数据状态'] == '实际']
                                    if not actual_data.empty:
                                        # 获取最后一天的数据点用于标签
                                        last_date = actual_data['日期'].iloc[-1]
                                        last_value = actual_data[engagement_col].iloc[-1]
                                        
                                        fig_social.add_trace(
                                            go.Scatter(
                                                x=actual_data['日期'],
                                                y=actual_data[engagement_col],
                                                name=f"{ip} {platform}互动量",
                                                line=dict(width=3, shape='spline', color=color),
                                                mode='lines'
                                            ),
                                            secondary_y=False
                                        )
                                        # 在最后点添加标签
                                        fig_social.add_annotation(
                                            x=last_date,
                                            y=last_value,
                                            text=f"{ip} {platform}互动量",
                                            showarrow=False,
                                            xshift=40,
                                            yshift=0,
                                            bgcolor="white",
                                            bordercolor=color,
                                            borderwidth=1,
                                            borderpad=2,
                                            font=dict(size=10, color=color)
                                        )
                                    # 预测数据
                                    forecast_data = ip_data[ip_data['数据状态'] == '预测']
                                    if not forecast_data.empty:
                                        fig_social.add_trace(
                                            go.Scatter(
                                                x=forecast_data['日期'],
                                                y=forecast_data[engagement_col],
                                                name=f"{ip} {platform}互动量(预测)",
                                                line=dict(width=2, dash='dash', shape='spline', color=color),
                                                mode='lines',
                                                showlegend=False
                                            ),
                                            secondary_y=False
                                        )
                    
                    # 发帖数数据（副纵轴）
                    if show_posts:
                        for platform in social_platforms:
                            posts_col = f'社媒热度_发帖数_{platform}'
                            if posts_col in filtered_df.columns:
                                for ip in selected_ips:
                                    color = colors[color_idx % len(colors)]
                                    color_idx += 1
                                    ip_data = filtered_df[filtered_df['IP名称'] == ip]
                                    # 实际数据
                                    actual_data = ip_data[ip_data['数据状态'] == '实际']
                                    if not actual_data.empty:
                                        # 获取最后一天的数据点用于标签
                                        last_date = actual_data['日期'].iloc[-1]
                                        last_value = actual_data[posts_col].iloc[-1]
                                        
                                        fig_social.add_trace(
                                            go.Scatter(
                                                x=actual_data['日期'],
                                                y=actual_data[posts_col],
                                                name=f"{ip} {platform}发帖数",
                                                line=dict(width=2, dash='dot', shape='spline', color=color),
                                                mode='lines'
                                            ),
                                            secondary_y=True
                                        )
                                        # 在最后点添加标签
                                        fig_social.add_annotation(
                                            x=last_date,
                                            y=last_value,
                                            text=f"{ip} {platform}发帖数",
                                            showarrow=False,
                                            xshift=40,
                                            yshift=0,
                                            bgcolor="white",
                                            bordercolor=color,
                                            borderwidth=1,
                                            borderpad=2,
                                            font=dict(size=10, color=color)
                                        )
                                    # 预测数据
                                    forecast_data = ip_data[ip_data['数据状态'] == '预测']
                                    if not forecast_data.empty:
                                        fig_social.add_trace(
                                            go.Scatter(
                                                x=forecast_data['日期'],
                                                y=forecast_data[posts_col],
                                                name=f"{ip} {platform}发帖数(预测)",
                                                line=dict(width=1.5, dash='dot', shape='spline', color=color),
                                                mode='lines',
                                                showlegend=False
                                            ),
                                            secondary_y=True
                                        )
                    
                    # 优化布局 - 深灰色坐标轴，紧凑间距
                    fig_social.update_layout(
                        height=450,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(size=11),
                        margin=dict(t=30, l=50, r=30, b=50),
                        showlegend=False,
                    )
                    # 深灰色坐标轴
                    fig_social.update_yaxes(
                        title_text="互动量", 
                        secondary_y=False, 
                        showgrid=True,
                        gridwidth=0.5,
                        gridcolor='rgba(128,128,128,0.1)',
                        zeroline=True,
                        zerolinewidth=1,
                        zerolinecolor='rgba(80,80,80,0.5)',
                        linecolor='rgba(80,80,80,0.8)',
                        linewidth=1
                    )
                    if show_posts:
                        fig_social.update_yaxes(
                            title_text="发帖数", 
                            secondary_y=True, 
                            showgrid=False,
                            zeroline=True,
                            zerolinewidth=1,
                            zerolinecolor='rgba(80,80,80,0.5)',
                            linecolor='rgba(80,80,80,0.8)',
                            linewidth=1
                        )
                    # 深灰色X轴，中文日期格式
                    fig_social.update_xaxes(
                        showgrid=True,
                        gridwidth=0.5,
                        gridcolor='rgba(128,128,128,0.1)',
                        zeroline=True,
                        zerolinewidth=1,
                        zerolinecolor='rgba(80,80,80,0.5)',
                        linecolor='rgba(80,80,80,0.8)',
                        linewidth=1,
                        tickformat='%Y-%m',
                        dtick="M1"
                    )
                    
                    st.plotly_chart(fig_social, use_container_width=True)
                else:
                    st.info("请选择至少一个社媒平台和IP来显示图表")
            
            # 竖线分割
            with divider:
                st.markdown('<div class="chart-divider"></div>', unsafe_allow_html=True)
            
            with col2:
                # 紧凑标题间距
                st.markdown('<p class="chart-title">🛍️ 电商热度趋势</p>', unsafe_allow_html=True)
                
                if ecommerce_platforms and selected_ips:
                    fig_ecommerce = make_subplots(specs=[[{"secondary_y": True}]])
                    
                    # 现代配色方案
                    colors = ['#ff6b6b', '#ff9e00', '#06d6a0', '#118ab2', '#ef476f', '#ffd166', '#073b4c', '#7209b7']
                    color_idx = 0
                    
                    # 电商销量数据（主纵轴）
                    if show_sales:
                        for platform in ecommerce_platforms:
                            sales_col = f'电商热度_销量_{platform}'
                            if sales_col in filtered_df.columns:
                                for ip in selected_ips:
                                    color = colors[color_idx % len(colors)]
                                    color_idx += 1
                                    ip_data = filtered_df[filtered_df['IP名称'] == ip]
                                    # 实际数据
                                    actual_data = ip_data[ip_data['数据状态'] == '实际']
                                    if not actual_data.empty:
                                        # 获取最后一天的数据点用于标签
                                        last_date = actual_data['日期'].iloc[-1]
                                        last_value = actual_data[sales_col].iloc[-1]
                                        
                                        fig_ecommerce.add_trace(
                                            go.Scatter(
                                                x=actual_data['日期'],
                                                y=actual_data[sales_col],
                                                name=f"{ip} {platform}销量",
                                                line=dict(width=3, shape='spline', color=color),
                                                mode='lines'
                                            ),
                                            secondary_y=False
                                        )
                                        # 在最后点添加标签
                                        fig_ecommerce.add_annotation(
                                            x=last_date,
                                            y=last_value,
                                            text=f"{ip} {platform}销量",
                                            showarrow=False,
                                            xshift=40,
                                            yshift=0,
                                            bgcolor="white",
                                            bordercolor=color,
                                            borderwidth=1,
                                            borderpad=2,
                                            font=dict(size=10, color=color)
                                        )
                                    # 预测数据
                                    forecast_data = ip_data[ip_data['数据状态'] == '预测']
                                    if not forecast_data.empty:
                                        fig_ecommerce.add_trace(
                                            go.Scatter(
                                                x=forecast_data['日期'],
                                                y=forecast_data[sales_col],
                                                name=f"{ip} {platform}销量(预测)",
                                                line=dict(width=2, dash='dash', shape='spline', color=color),
                                                mode='lines',
                                                showlegend=False
                                            ),
                                            secondary_y=False
                                        )
                    
                    # 二手销量数据（副纵轴）
                    if show_secondhand and '电商热度_二手销量' in filtered_df.columns:
                        for ip in selected_ips:
                            color = colors[color_idx % len(colors)]
                            color_idx += 1
                            ip_data = filtered_df[filtered_df['IP名称'] == ip]
                            # 实际数据
                            actual_data = ip_data[ip_data['数据状态'] == '实际']
                            if not actual_data.empty:
                                # 获取最后一天的数据点用于标签
                                last_date = actual_data['日期'].iloc[-1]
                                last_value = actual_data['电商热度_二手销量'].iloc[-1]
                                
                                fig_ecommerce.add_trace(
                                    go.Scatter(
                                        x=actual_data['日期'],
                                        y=actual_data['电商热度_二手销量'],
                                        name=f"{ip} 二手销量",
                                        line=dict(width=2, dash='dot', shape='spline', color=color),
                                        mode='lines'
                                    ),
                                    secondary_y=True
                                )
                                # 在最后点添加标签
                                fig_ecommerce.add_annotation(
                                    x=last_date,
                                    y=last_value,
                                    text=f"{ip} 二手销量",
                                    showarrow=False,
                                    xshift=40,
                                    yshift=0,
                                    bgcolor="white",
                                    bordercolor=color,
                                    borderwidth=1,
                                    borderpad=2,
                                    font=dict(size=10, color=color)
                                )
                            # 预测数据
                            forecast_data = ip_data[ip_data['数据状态'] == '预测']
                            if not forecast_data.empty:
                                fig_ecommerce.add_trace(
                                    go.Scatter(
                                        x=forecast_data['日期'],
                                        y=forecast_data['电商热度_二手销量'],
                                        name=f"{ip} 二手销量(预测)",
                                        line=dict(width=1.5, dash='dot', shape='spline', color=color),
                                        mode='lines',
                                        showlegend=False
                                    ),
                                    secondary_y=True
                                )
                    
                    # 优化布局 - 深灰色坐标轴，紧凑间距
                    fig_ecommerce.update_layout(
                        height=450,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(size=11),
                        margin=dict(t=30, l=50, r=30, b=50),
                        showlegend=False,
                    )

                    if show_sales:
                        fig_ecommerce.update_yaxes(
                            title_text="销量", 
                            secondary_y=False, 
                            showgrid=True,
                            gridwidth=0.5,
                            gridcolor='rgba(128,128,128,0.1)',
                            zeroline=True,
                            zerolinewidth=1,
                            zerolinecolor='rgba(80,80,80,0.5)',
                            linecolor='rgba(80,80,80,0.8)',
                            linewidth=1
                        )
                    if show_secondhand:
                        fig_ecommerce.update_yaxes(
                            title_text="二手销量", 
                            secondary_y=True, 
                            showgrid=False,
                            zeroline=True,
                            zerolinewidth=1,
                            zerolinecolor='rgba(80,80,80,0.5)',
                            linecolor='rgba(80,80,80,0.8)',
                            linewidth=1
                        )
                    # 深灰色X轴，中文日期格式
                    fig_ecommerce.update_xaxes(
                        showgrid=True,
                        gridwidth=0.5,
                        gridcolor='rgba(128,128,128,0.1)',
                        zeroline=True,
                        zerolinewidth=1,
                        zerolinecolor='rgba(80,80,80,0.5)',
                        linecolor='rgba(80,80,80,0.8)',
                        linewidth=1,
                        tickformat='%Y-%m',
                        dtick="M1"
                    )
                    
                    st.plotly_chart(fig_ecommerce, use_container_width=True)
                else:
                    st.info("请选择至少一个电商平台和IP来显示图表")

        st.markdown('</div>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("找不到数据文件")
    except Exception as e:
        st.error(f"加载数据时出现错误: {str(e)}")

# 第二页：IP商品销量预测模拟器 - 最终修正版
def predictor_page():
    try:
        # 读取数据
        @st.cache_data
        def load_data():
            df = pd.read_excel('demo_data.xlsx', sheet_name='预测结果底表')
            if '销售起始日期' in df.columns:
                df['销售起始日期'] = pd.to_datetime(df['销售起始日期']).dt.date
            return df
        
        df = load_data()
        
        st.markdown("<h2 style='text-align: left; margin-bottom: 1rem; margin-top: -1rem;'>🎯 IP商品销量预测模拟器</h2>", unsafe_allow_html=True)
        
        # 目标选择
        st.sidebar.markdown("**⭐ 目标选择**")

        # 目标周数选择
        target_week = st.sidebar.selectbox(
            "**目标周数**",
            options=[1, 2, 3, 4, 5, 6, 7, 8],
            index=7,  # 默认选择第8周
            help="选择预测的目标周数"
        )

        # 市场筛选 - 改为下拉多选
        markets = st.sidebar.multiselect(
            "**市场**",
            options=df['市场'].unique(),
            default=df['市场'].unique(),  # 默认全选
            help="选择目标市场"
        )

        # 销售渠道筛选 - 改为下拉多选
        channels = st.sidebar.multiselect(
            "**销售渠道**",
            options=df['销售渠道'].unique(),
            default=df['销售渠道'].unique(),  # 默认全选
            help="选择销售渠道"
        )

        # 商品选择
        st.sidebar.markdown("**🛍️ 商品选择**")

        # IP类别筛选
        ip_categories = st.sidebar.multiselect(
            "**IP类别**",
            options=df['IP类别'].unique(),
            default=["IP类别_古风独家IP"],  # 默认选择古风独家IP
            help="选择IP类别"
        )

        # 商品材质筛选
        materials = st.sidebar.multiselect(
            "**商品材质**",
            options=df['商品材质'].unique(),
            default=["木质"],  # 默认选择木质
            help="选择商品材质"
        )

        # 商品用途筛选
        purposes = st.sidebar.multiselect(
            "**商品用途**",
            options=df['商品用途'].unique(),
            default=["箱包配饰"],  # 默认选择箱包配饰
            help="选择商品用途"
        )

        # 商品选择
        st.sidebar.markdown("**🛍️ 商品选择**")
        # IP类别筛选
        ip_categories = st.sidebar.multiselect(
            "IP类别",
            options=df['IP类别'].unique(),
            default=["IP类别_古风独家IP"],  # 默认选择古风独家IP
            key="ip_category_select"
        )
        
        # 商品材质筛选
        materials = st.sidebar.multiselect(
            "商品材质",
            options=df['商品材质'].unique(),
            default=["木质"],  # 默认选择木质
            key="material_select"
        )
        
        # 商品用途筛选
        purposes = st.sidebar.multiselect(
            "商品用途",
            options=df['商品用途'].unique(),
            default=["箱包配饰"],  # 默认选择箱包配饰
            key="purpose_select"
        )
        
        # 数据过滤
        filtered_df = df.copy()
        
        if markets:
            filtered_df = filtered_df[filtered_df['市场'].isin(markets)]
        if channels:
            filtered_df = filtered_df[filtered_df['销售渠道'].isin(channels)]
        if ip_categories:
            filtered_df = filtered_df[filtered_df['IP类别'].isin(ip_categories)]
        if materials:
            filtered_df = filtered_df[filtered_df['商品材质'].isin(materials)]
        if purposes:
            filtered_df = filtered_df[filtered_df['商品用途'].isin(purposes)]
        
        if filtered_df.empty:
            st.warning("没有找到符合条件的数据，请调整筛选条件")
            return
        
        # 获取唯一组合
        unique_combinations = filtered_df[['IP名称', '商品编号', '销售渠道', '市场']].drop_duplicates()
        
        # 初始化session state
        if 'deleted_combinations' not in st.session_state:
            st.session_state.deleted_combinations = set()
        
        if 'store_counts' not in st.session_state:
            st.session_state.store_counts = {}
        
        if 'store_types' not in st.session_state:
            st.session_state.store_types = {}
        
        # 构建active_configs和表格数据
        active_configs = {}
        table_data = []
        
        # 收集所有可用的门店类型和最大门店数
        all_available_types = set()
        max_possible_stores = 0
        
        for idx, combo in unique_combinations.iterrows():
            combo_key = f"{combo['IP名称']}|{combo['商品编号']}|{combo['销售渠道']}|{combo['市场']}"
            
            if combo_key in st.session_state.deleted_combinations:
                continue
                
            # 获取该组合的数据
            combo_data = filtered_df[
                (filtered_df['IP名称'] == combo['IP名称']) &
                (filtered_df['商品编号'] == combo['商品编号']) &
                (filtered_df['销售渠道'] == combo['销售渠道']) &
                (filtered_df['市场'] == combo['市场'])
            ]
            
            # 获取销售起始日期
            start_date = combo_data['销售起始日期'].min() if '销售起始日期' in combo_data.columns else datetime.date.today()
            
            # 获取最大门店数和可用门店类型
            max_stores = len(combo_data['门店编号'].unique()) if '门店编号' in combo_data.columns else 0
            
            # 获取可用门店类型
            available_types = []
            if '门店信息_门店商圈类型' in combo_data.columns:
                available_types = combo_data['门店信息_门店商圈类型'].dropna().unique().tolist()
            elif '门店商圈类型' in combo_data.columns:
                available_types = combo_data['门店商圈类型'].dropna().unique().tolist()
            
            # 更新全局选项
            all_available_types.update(available_types)
            max_possible_stores = max(max_possible_stores, max_stores)
            
            # 初始化配置
            if combo_key not in st.session_state.store_counts:
                st.session_state.store_counts[combo_key] = max_stores
            
            if combo_key not in st.session_state.store_types:
                valid_default_types = [t for t in available_types if t in available_types]
                st.session_state.store_types[combo_key] = valid_default_types
            
            # 商品信息
            if not combo_data.empty:
                sample = combo_data.iloc[0]
                material = sample.get("商品材质", "N/A")
                purpose = sample.get("商品用途", "N/A")
                color = sample.get("商品颜色", "N/A")
                size = sample.get("商品尺寸", "N/A")
                price = str(sample.get("商品价格", "N/A"))
            else:
                material = purpose = color = size = price = "N/A"
            
            # 添加到表格数据
            table_data.append({
                'IP名称-商品编号': f"{combo['IP名称']}-{combo['商品编号']}",
                '渠道': combo['销售渠道'],
                '市场': combo['市场'],
                '首次销售日期': str(start_date),
                '覆盖门店种类': st.session_state.store_types[combo_key][0] if st.session_state.store_types[combo_key] else (available_types[0] if available_types else "N/A"),
                '覆盖门店数': st.session_state.store_counts[combo_key],
                '商品材质': material,
                '商品用途': purpose,
                '商品颜色': color,
                '商品尺寸': size,
                '商品价格': price,
                '删除': False,
                '确认': False,
                'combo_key': combo_key,
                'available_types': available_types,
                'max_stores': max_stores
            })
            
            # 添加到active_configs
            active_configs[combo_key] = {
                'ip_name': combo['IP名称'],
                'product_code': combo['商品编号'],
                'channel': combo['销售渠道'],
                'market': combo['市场'],
                'start_date': start_date,
                'store_count': st.session_state.store_counts[combo_key],
                'store_types': st.session_state.store_types[combo_key]
            }
        
        st.markdown("### 📋 商品配置选择")
        
        # 使用st.data_editor显示可编辑表格
        if table_data:
            # 创建DataFrame
            display_df = pd.DataFrame(table_data)
            display_columns = ['IP名称-商品编号', '渠道', '市场', '首次销售日期', 
                            '覆盖门店种类', '覆盖门店数', '商品材质', '商品用途', 
                            '商品颜色', '商品尺寸', '商品价格', '删除', '确认']
            display_df = display_df[display_columns]
            
            # 准备全局选项
            store_type_options = list(all_available_types)
            store_count_options = list(range(1, max_possible_stores + 1)) if max_possible_stores > 0 else [0]
            
            # 配置列属性
            column_config = {
                '删除': st.column_config.CheckboxColumn(
                    '🗑️',
                    help="选择要删除的配置",
                    default=False,
                    width="small"
                ),
                '确认': st.column_config.CheckboxColumn(
                    '✅',
                    help="确认删除",
                    default=False,
                    width="small"
                ),
                'IP名称-商品编号': st.column_config.TextColumn(
                    'IP商品',
                    help='IP名称和商品编号',
                    width="medium"
                ),
                '渠道': st.column_config.TextColumn(
                    '销售渠道',
                    help='线上或线下',
                    width="small"
                ),
                '市场': st.column_config.TextColumn(
                    '市场',
                    help='US或MX',
                    width="small"
                ),
                '首次销售日期': st.column_config.TextColumn(
                    '首发日期',
                    help='首次销售日期',
                    width="small"
                ),
                '覆盖门店种类': st.column_config.SelectboxColumn(
                    '门店类型',
                    help='选择门店类型',
                    options=store_type_options,
                    width="medium"
                ),
                '覆盖门店数': st.column_config.SelectboxColumn(
                    '门店数量',
                    help='选择门店数量',
                    options=store_count_options,
                    width="small"
                ),
                '商品材质': st.column_config.TextColumn(
                    '材质',
                    help='商品材质',
                    width="small"
                ),
                '商品用途': st.column_config.TextColumn(
                    '用途',
                    help='商品用途',
                    width="small"
                ),
                '商品颜色': st.column_config.TextColumn(
                    '颜色',
                    help='商品颜色',
                    width="small"
                ),
                '商品尺寸': st.column_config.NumberColumn(
                    '尺寸',
                    help='商品尺寸',
                    format="%d",
                    width="small"
                ),
                '商品价格': st.column_config.NumberColumn(
                    '价格',
                    help='商品价格',
                    format="%d",
                    width="small"
                )
            }

            # 改进的CSS样式 - 强制居中对齐
            st.markdown("""
            <style>
                /* 强制所有表格内容居中对齐 */
                div[data-testid="stDataFrame"] table {
                    text-align: center !important;
                }
                
                /* 表头单元格 */
                div[data-testid="stDataFrame"] th {
                    text-align: center !important;
                    background-color: #1f77b4 !important;
                    color: white !important;
                    font-weight: bold !important;
                    border: 1px solid #ddd !important;
                }
                
                /* 数据单元格 */
                div[data-testid="stDataFrame"] td {
                    text-align: center !important;
                    vertical-align: middle !important;
                    border: 1px solid #e0e0e0 !important;
                }
                
                /* 选择框和输入框居中 */
                div[data-testid="stDataFrame"] select,
                div[data-testid="stDataFrame"] input {
                    text-align: center !important;
                    margin: 0 auto !important;
                    display: block !important;
                }
                
                /* 复选框居中 */
                div[data-testid="stCheckbox"] > label > div:first-child {
                    margin: 0 auto !important;
                }
                
                /* 表格行交替颜色 */
                div[data-testid="stDataFrame"] tbody tr:nth-child(even) {
                    background-color: #f8f9fa !important;
                }
                
                div[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
                    background-color: #ffffff !important;
                }
                
                /* 鼠标悬停效果 */
                div[data-testid="stDataFrame"] tbody tr:hover {
                    background-color: #e3f2fd !important;
                }
                
                /* 表格整体样式 */
                div[data-testid="stDataFrame"] {
                    border-radius: 8px !important;
                    overflow: hidden !important;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
                    border: 1px solid #e0e0e0 !important;
                }
                
                /* 确保表格容器正确显示 */
                div[data-testid="stDataFrameResizable"] {
                    text-align: center !important;
                }
            </style>
            """, unsafe_allow_html=True)

            # 显示可编辑表格
            edited_df = st.data_editor(
                display_df,
                column_config=column_config,
                use_container_width=True,
                height=250,  # 固定高度250
                hide_index=True,
                key="config_editor"
            )
            
            # 更新session state中的配置
            for idx, row in edited_df.iterrows():
                combo_key = table_data[idx]['combo_key']
                st.session_state.store_types[combo_key] = [row['覆盖门店种类']]
                st.session_state.store_counts[combo_key] = row['覆盖门店数']
                
                # 更新active_configs
                active_configs[combo_key]['store_count'] = row['覆盖门店数']
                active_configs[combo_key]['store_types'] = [row['覆盖门店种类']]
                
                # 检查是否需要删除（同时勾选了删除和确认）
                if row['删除'] and row['确认']:
                    if combo_key not in st.session_state.deleted_combinations:
                        st.session_state.deleted_combinations.add(combo_key)
                        st.success(f"已删除配置: {row['IP名称-商品编号']}")
                        st.rerun()
            
        else:
            st.info("所有配置已被删除，调整左侧筛选条件可重新显示")
        
        # 销量分析部分
        if active_configs:
            with st.container():
                st.markdown("### 📊 销量分析")
                
                # 销量计算函数
                def calculate_sales_data(config):
                    # 筛选数据
                    market_channel_df = filtered_df[
                        (filtered_df['IP名称'] == config['ip_name']) &
                        (filtered_df['商品编号'] == config['product_code']) & 
                        (filtered_df['销售渠道'] == config['channel']) & 
                        (filtered_df['市场'] == config['market'])
                    ]
                    
                    # 按门店类型筛选
                    if config['store_types']:
                        if '门店信息_门店商圈类型' in market_channel_df.columns:
                            market_channel_df = market_channel_df[market_channel_df['门店信息_门店商圈类型'].isin(config['store_types'])]
                        elif '门店商圈类型' in market_channel_df.columns:
                            market_channel_df = market_channel_df[market_channel_df['门店商圈类型'].isin(config['store_types'])]
                    
                    if market_channel_df.empty:
                        return 0, []
                    
                    # 按销量_上市首周排序选择前N个门店
                    store_sales = []
                    for store in market_channel_df['门店编号'].unique():
                        store_data = market_channel_df[market_channel_df['门店编号'] == store]
                        # 获取该门店的销量_上市首周
                        if '销量_上市首周' in store_data.columns:
                            first_week_sales = store_data['销量_上市首周'].iloc[0]
                        else:
                            # 如果没有首周列，使用第一周数据
                            first_week_sales = store_data[f'销量_上市第1周'].iloc[0] if f'销量_上市第1周' in store_data.columns else 0
                        
                        store_sales.append({'门店编号': store, '首周销量': first_week_sales})
                    
                    # 按首周销量排序并选择前N个门店
                    store_sales.sort(key=lambda x: x['首周销量'], reverse=True)
                    top_store_ids = [store['门店编号'] for store in store_sales[:config['store_count']]]
                    
                    # 计算总销量（目标周数的总和）
                    total_sales = 0
                    for week in range(1, target_week + 1):
                        sales_col = f'销量_上市第{week}周'
                        if sales_col in market_channel_df.columns:
                            week_sales = market_channel_df[
                                market_channel_df['门店编号'].isin(top_store_ids)
                            ][sales_col].sum()
                            total_sales += week_sales
                    
                    return total_sales, top_store_ids
                
                # 准备环形图和趋势图数据
                pie_data = []
                trend_data = []
                
                for combo_key, config in active_configs.items():
                    total_sales, top_store_ids = calculate_sales_data(config)
                    label = f"{config['ip_name']}-{config['product_code']}"
                    
                    if total_sales > 0:  # 只添加有销量的数据
                        pie_data.append({'label': label, 'value': total_sales})
                        
                        # 趋势数据计算
                        market_channel_df = filtered_df[
                            (filtered_df['IP名称'] == config['ip_name']) &
                            (filtered_df['商品编号'] == config['product_code']) & 
                            (filtered_df['销售渠道'] == config['channel']) & 
                            (filtered_df['市场'] == config['market'])
                        ]
                        
                        # 按门店类型筛选
                        if config['store_types']:
                            if '门店信息_门店商圈类型' in market_channel_df.columns:
                                market_channel_df = market_channel_df[market_channel_df['门店信息_门店商圈类型'].isin(config['store_types'])]
                            elif '门店商圈类型' in market_channel_df.columns:
                                market_channel_df = market_channel_df[market_channel_df['门店商圈类型'].isin(config['store_types'])]
                        
                        if not market_channel_df.empty and top_store_ids:
                            # 计算每周销量
                            weekly_sales = []
                            dates = []
                            
                            for week in range(1, target_week + 1):
                                sales_col = f'销量_上市第{week}周'
                                if sales_col in market_channel_df.columns:
                                    week_sales = market_channel_df[
                                        market_channel_df['门店编号'].isin(top_store_ids)
                                    ][sales_col].sum()
                                    weekly_sales.append(week_sales)
                                else:
                                    weekly_sales.append(0)
                                
                                # 计算日期（从首次销售日期开始）
                                week_date = config['start_date'] + datetime.timedelta(weeks=week-1)
                                dates.append(week_date)
                            
                            trend_data.append({
                                'label': label,
                                'dates': dates,
                                'sales': weekly_sales
                            })
                
                # 显示图表
                if pie_data:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # 销量占比分析容器
                        with st.container():
                            st.markdown("#### 🥧 销量占比分析")
                            fig_pie = go.Figure(data=[go.Pie(
                                labels=[item['label'] for item in pie_data],
                                values=[item['value'] for item in pie_data],
                                hole=0.4,
                                textinfo='percent+label',
                                marker=dict(colors=['#4361ee', '#3a0ca3', '#4cc9f0', '#f72585', '#7209b7']),
                                showlegend=False
                            )])
                            fig_pie.update_layout(
                                height=275,
                                margin=dict(l=10, r=10, t=30, b=10)
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col2:
                        # 销量趋势分析容器
                        with st.container():
                            st.markdown("#### 📈 销量趋势分析")
                            if trend_data:
                                fig_trend = go.Figure()
                                
                                colors = ['#4361ee', '#3a0ca3', '#4cc9f0', '#f72585', '#7209b7']
                                
                                for i, data in enumerate(trend_data):
                                    if data['sales'] and any(sales > 0 for sales in data['sales']):
                                        color = colors[i % len(colors)]
                                        fig_trend.add_trace(go.Scatter(
                                            x=data['dates'],
                                            y=data['sales'],
                                            mode='lines',
                                            name=data['label'],
                                            line=dict(width=3, color=color, shape='spline'),
                                            showlegend=False
                                        ))
                                        
                                        # 在最后一个数据点添加标签
                                        if data['dates'] and data['sales']:
                                            last_date = data['dates'][-1]
                                            last_sales = data['sales'][-1]
                                            
                                            fig_trend.add_annotation(
                                                x=last_date,
                                                y=last_sales,
                                                text=data['label'],
                                                showarrow=True,
                                                arrowhead=2,
                                                arrowsize=1,
                                                arrowwidth=2,
                                                arrowcolor=color,
                                                bgcolor="white",
                                                bordercolor=color,
                                                borderwidth=1,
                                                borderpad=4,
                                                font=dict(size=10, color=color),
                                                yshift=20
                                            )
                                
                                fig_trend.update_layout(
                                    height=300,
                                    margin=dict(l=10, r=10, t=30, b=10),
                                    xaxis_title="日期",
                                    yaxis_title="销量",
                                    showlegend=False,
                                    xaxis=dict(
                                        tickformat='%Y-%m-%d',
                                        tickangle=45,
                                        linecolor='#666666',
                                        gridcolor='rgba(128,128,128,0.2)',
                                        zerolinecolor='rgba(128,128,128,0.5)'
                                    ),
                                    yaxis=dict(
                                        linecolor='#666666',
                                        gridcolor='rgba(128,128,128,0.2)',
                                        zerolinecolor='rgba(128,128,128,0.5)'
                                    )
                                )
                                st.plotly_chart(fig_trend, use_container_width=True)
                            else:
                                st.info("无法生成趋势图，请检查数据")
                else:
                    st.warning("没有找到销量数据，请检查筛选条件和配置")
        
        else:
            st.info("请选择商品配置进行分析")
            
    except FileNotFoundError:
        st.error("找不到数据文件")
    except Exception as e:
        st.error(f"加载数据时出现错误: {str(e)}")

# 主应用逻辑
def main():
    create_navigation()
    if st.session_state.current_page == "dashboard":
        dashboard_page()
    elif st.session_state.current_page == "predictor":
        predictor_page()

if __name__ == "__main__":
    main()