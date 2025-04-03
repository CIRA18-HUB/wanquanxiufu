with col2:
    st.markdown('<div class="feishu-chart-container">', unsafe_allow_html=True)

    if len(filtered_distributor) > 0:
        try:
            # 深度复制数据框以防止修改原始数据
            temp_df = filtered_distributor.copy()
            
            # 如果销售规模列不存在，创建一个简单的二分组
            if '销售规模' not in temp_df.columns:
                median = temp_df['销售总额'].median()
                temp_df['销售规模'] = np.where(temp_df['销售总额'] > median, '大规模', '小规模')
            
            # 安全地计算物料多样性差异
            temp_df['物料多样性差异'] = temp_df.apply(
                lambda row: get_optimal_diversity(row) - row['物料多样性'] 
                if '销售规模' in row and pd.notna(row['物料多样性']) and row['物料多样性'] > 0 
                else 0,
                axis=1
            )
            
            # 筛选物料多样性差异较大的经销商
            diversity_gap = temp_df[temp_df['物料多样性差异'] > 1].sort_values(
                '物料多样性差异', ascending=False
            ).head(10)
            
            # 创建物料多样性差异图
            if len(diversity_gap) > 0:
                fig = px.bar(
                    diversity_gap,
                    y='经销商名称',
                    x='物料多样性差异',
                    color='销售规模',
                    text='物料多样性差异',
                    orientation='h',
                    title="物料多样性提升空间TOP10"
                )
                
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E0E4EA',
                        title='差距数量'
                    ),
                    yaxis=dict(
                        showgrid=False,
                        autorange="reversed",
                        title=''
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("没有物料多样性差异明显的经销商。")
        except Exception as e:
            st.error(f"创建物料多样性差异图表时出错: {str(e)}")
            st.info("无法创建物料多样性差异图表")
    else:
        st.info("暂无经销商数据。")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 解读部分保持不变
    st.markdown('''
    <div class="chart-explanation">
        <div class="chart-explanation-title">图表解读：</div>
        <p>此图显示了物料多样性提升空间最大的经销商。柱长代表当前物料多样性与推荐多样性的差距。建议优先为这些经销商增加物料品种，特别是大规模和中大规模的经销商，他们的物料品种丰富度直接影响销售效果。</p>
    </div>
    ''', unsafe_allow_html=True)