import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import timedelta
import random

def add_loyalty_predictor():
    st.markdown("<h2 style='text-align: center;'>Quick Loyalty Score Predictor</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchases = st.slider("Number of Purchases (last 12 months)", 0, 30, 5)
        activity_days = st.slider("Days Since Last Activity", 0, 60, 10)
    
    with col2:
        feedback = st.slider("Customer Feedback (1-5)", 1.0, 5.0, 3.5, 0.1)
        engagement = st.slider("Engagement Level (0-1)", 0.0, 1.0, 0.5, 0.01)
    
    # Calculate predicted score based on simple weighted formula
    if st.button("Calculate Loyalty Score", use_container_width=True):
        with st.spinner("Analyzing..."):
            # Simple weighted formula for loyalty prediction
            predicted_score = (
                (purchases / 30) * 25 +                    # 25% weight
                ((60 - activity_days) / 60) * 25 +         # 25% weight
                (feedback / 5) * 25 +                      # 25% weight
                engagement * 25                            # 25% weight
            )
            
            # Determine category
            if predicted_score >= 70:
                category = "🏆 Loyal"
                color = "#00d2ff"
            elif predicted_score >= 40:
                category = "⚠️ At Risk"
                color = "#ffd166"
            else:
                category = "🚨 Churned"
                color = "#ef476f"
            
            # Display result with custom styling
            st.markdown(f"""
            <div style='background: rgba(0,0,0,0.2); padding: 20px; border-radius: 10px; border: 1px solid {color}; text-align: center;'>
                <h3 style='color: {color}!important; margin-bottom: 10px;'>Predicted Score: {predicted_score:.1f}</h3>
                <h4>Customer Category: {category}</h4>
            </div>
            """, unsafe_allow_html=True)

# Configure page layout and theme
st.set_page_config(
    page_title="Customer Loyalty Analytics",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic blue theme
st.markdown("""
<style>
    .stApp {background: linear-gradient(to bottom right, #051937, #004d7a); color: white;}
    header {background-color: rgba(0, 123, 255, 0.2) !important; backdrop-filter: blur(10px);}
    .metric-card {background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; 
                border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;}
    .stButton button {background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important; 
                    color: white !important; border: none !important; border-radius: 25px !important;}
    h1, h2, h3 {color: #00d2ff !important; text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);}
    .chart-container {background: rgba(0, 20, 40, 0.3); border-radius: 15px; padding: 15px; 
                    border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# Generate mock data for visualizations
def generate_mock_data(num_records=100):
    categories = ['Loyal', 'At Risk', 'Churned']
    industries = ['Retail', 'Technology', 'Healthcare', 'Finance', 'Education']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    data = []
    for i in range(num_records):
        loyalty_score = random.randint(0, 100)
        if loyalty_score >= 70:
            category = 'Loyal'
        elif loyalty_score >= 40:
            category = 'At Risk'
        else:
            category = 'Churned'
            
        data.append({
            'user_id': 10000 + i,
            'loyalty_score': loyalty_score,
            'category': category,
            'purchases': random.randint(0, 20),
            'last_activity_days': random.randint(0, 60),
            'feedback_score': round(random.uniform(1.0, 5.0), 1),
            'engagement_score': round(random.uniform(0.0, 1.0), 2),
            'industry': random.choice(industries),
            'month': random.choice(months)
        })
    return pd.DataFrame(data)

# Create sidebar with tabs
with st.sidebar:
    st.markdown("### 🔮 Loyalty Analytics")
    
    # Sidebar navigation
    page = st.radio("", ["Dashboard", "Predictor", "Customer Insights"], 
                   format_func=lambda x: f"📊 {x}" if x == "Dashboard" else 
                                        f"🔍 {x}" if x == "Predictor" else f"👥 {x}")
    
    st.markdown("---")
    st.markdown("### 📊 Loyalty Categories")
    st.markdown("- 🏆 **Loyal**: 70-100")
    st.markdown("- ⚠️ **At Risk**: 40-69")
    st.markdown("- 🚨 **Churned**: 0-39")

# Generate mock data
mock_df = generate_mock_data()

# DASHBOARD PAGE
if page == "Dashboard":
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📊 Customer Loyalty Dashboard</h1>", unsafe_allow_html=True)
    
    # Key metrics row
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.markdown("<div class='metric-card' style='text-align:center'>", unsafe_allow_html=True)
        st.metric("Avg. Loyalty Score", f"{mock_df['loyalty_score'].mean():.1f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("<div class='metric-card' style='text-align:center'>", unsafe_allow_html=True)
        st.metric("Loyal Customers", f"{len(mock_df[mock_df['category'] == 'Loyal'])} ({len(mock_df[mock_df['category'] == 'Loyal'])/len(mock_df)*100:.1f}%)")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with metric_col3:
        st.markdown("<div class='metric-card' style='text-align:center'>", unsafe_allow_html=True)
        st.metric("At Risk Customers", f"{len(mock_df[mock_df['category'] == 'At Risk'])} ({len(mock_df[mock_df['category'] == 'At Risk'])/len(mock_df)*100:.1f}%)")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with metric_col4:
        st.markdown("<div class='metric-card' style='text-align:center'>", unsafe_allow_html=True)
        st.metric("Churned Customers", f"{len(mock_df[mock_df['category'] == 'Churned'])} ({len(mock_df[mock_df['category'] == 'Churned'])/len(mock_df)*100:.1f}%)")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts row 1
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Customer Loyalty Distribution")
        
        # Pie chart of customer categories
        category_counts = mock_df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        
        fig = px.pie(
            category_counts, 
            values='count', 
            names='category',
            color='category',
            color_discrete_map={'Loyal': '#00d2ff', 'At Risk': '#ffd166', 'Churned': '#ef476f'},
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Loyalty Score by Industry")
        
        # Bar chart for loyalty score by industry
        industry_scores = mock_df.groupby('industry')['loyalty_score'].mean().reset_index()
        
        fig = px.bar(
            industry_scores,
            x='industry',
            y='loyalty_score',
            color='loyalty_score',
            color_continuous_scale=['#ef476f', '#ffd166', '#00d2ff'],
            text_auto=True
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts row 2
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Monthly Trends")
        
        # Line chart for monthly trends
        monthly_data = mock_df.groupby('month')['loyalty_score'].mean().reset_index()
        monthly_data['month_num'] = pd.Categorical(monthly_data['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
        monthly_data = monthly_data.sort_values('month_num')
        
        fig = px.line(
            monthly_data,
            x='month',
            y='loyalty_score',
            markers=True,
            line_shape='spline'
        )
        fig.update_traces(line_color='#00d2ff', line_width=3)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col4:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Engagement vs. Loyalty")
        
        # Scatter plot
        fig = px.scatter(
            mock_df,
            x='engagement_score',
            y='loyalty_score',
            color='category',
            color_discrete_map={'Loyal': '#00d2ff', 'At Risk': '#ffd166', 'Churned': '#ef476f'},
            size='purchases',
            hover_data=['user_id', 'feedback_score']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Data table with filter
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("Customer Data Explorer")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        category_filter = st.multiselect("Filter by Category", options=mock_df['category'].unique(), default=mock_df['category'].unique())
    
    filtered_df = mock_df[mock_df['category'].isin(category_filter)]
    st.dataframe(filtered_df[['user_id', 'loyalty_score', 'category', 'purchases', 'engagement_score', 'feedback_score']], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# PREDICTOR PAGE (original functionality)
elif page == "Predictor":
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🔮 Customer Loyalty Predictor</h1>", unsafe_allow_html=True)
    
    # Create two columns for input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Customer Information")
        user_id = st.number_input("User ID", min_value=1, step=1, value=12345)
        
        # Use date input for last activity
        today = datetime.date.today()
        last_activity = st.date_input(
            "Last Activity Date", 
            value=today - timedelta(days=7),
            max_value=today
        )
        last_activity_days = (today - last_activity).days
        
        purchases = st.number_input("Number of Purchases", min_value=0, step=1, value=5)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Customer Engagement")
        feedback_score = st.slider(
            "Feedback Score", 
            1.0, 5.0, 
            value=4.2,
            step=0.1
        )
        
        engagement_score = st.slider(
            "Engagement Score", 
            0.0, 1.0, 
            value=0.75,
            step=0.01
        )
        
        industry = st.selectbox("Industry", ["Retail", "Technology", "Healthcare", "Finance", "Education"])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔍 PREDICT LOYALTY SCORE", use_container_width=True)
    
    # Results container
    if predict_button:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Prediction Results")
    
        with st.spinner("Calculating loyalty score..."):
            # Calculate mock loyalty score based on input
            mock_loyalty_score = min(100, int(
                (purchases * 5) + 
                (max(0, 30 - last_activity_days)) + 
                (feedback_score * 10) + 
                (engagement_score * 30)
            ))
            
            # Determine category
            if mock_loyalty_score >= 70:
                category = "🏆 Loyal"
                color = "#00d2ff"
                reward = "Exclusive VIP access + 20% discount on next purchase"
            elif mock_loyalty_score >= 40:
                category = "⚠️ At Risk"
                color = "#ffd166"
                reward = "Limited-time 10% discount to encourage re-engagement"
            else:
                category = "🚨 Churned"
                color = "#ef476f"
                reward = "Welcome back offer: 25% off your next purchase + free item"
            
            # Create columns for results
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <h2 style='color: {color}!important; font-size: 40px; margin-bottom: 0;'>{mock_loyalty_score}</h2>
                    <p>Loyalty Score</p>
                </div>
                """, unsafe_allow_html=True)
                
            with res_col2:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <h2 style='color: {color}!important; font-size: 40px; margin-bottom: 0;'>{category}</h2>
                    <p>Category</p>
                </div>
                """, unsafe_allow_html=True)
                
            with res_col3:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <h2 style='color: {color}!important; font-size: 40px; margin-bottom: 0;'>🎁</h2>
                    <p>Recommended Reward</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Reward recommendation
            st.markdown(f"""
            <div style='background: rgba(0, 40, 80, 0.3); padding: 15px; border-radius: 10px; border: 1px solid {color}; margin-top: 20px;'>
                <p style='font-size: 18px; margin-bottom: 0;'>{reward}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a visual gauge for the loyalty score
            st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
            
            # Use plotly for gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = mock_loyalty_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(239, 71, 111, 0.7)'},
                        {'range': [40, 70], 'color': 'rgba(255, 209, 102, 0.7)'},
                        {'range': [70, 100], 'color': 'rgba(0, 210, 255, 0.7)'}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': mock_loyalty_score
                    }
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Arial"},
                height=200,
                margin=dict(l=20, r=20, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# CUSTOMER INSIGHTS PAGE
else:  # Customer Insights page
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>👥 Customer Insights</h1>", unsafe_allow_html=True)
    
    # Create heatmap visualization
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Correlation Matrix")
    
    # Calculate correlation
    corr_data = mock_df[['loyalty_score', 'purchases', 'last_activity_days', 'feedback_score', 'engagement_score']]
    corr = corr_data.corr()
    
    # Create heatmap
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale=["#ef476f", "#ffd166", "#00d2ff"],
        aspect="equal"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=30, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Customer segment analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Customer Segments Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average metrics by category
        category_metrics = mock_df.groupby('category')[['purchases', 'feedback_score', 'engagement_score']].mean().reset_index()
        
        fig = px.bar(
            category_metrics,
            x='category',
            y=['purchases', 'feedback_score', 'engagement_score'],
            barmode='group',
            color_discrete_sequence=['#00d2ff', '#ffd166', '#ef476f']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend_title_text='Metric',
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Radar chart for segment comparison
        categories = ['Purchases', 'Feedback', 'Engagement', 'Activity']
        
        loyal_values = [
            mock_df[mock_df['category'] == 'Loyal']['purchases'].mean() / 20,
            mock_df[mock_df['category'] == 'Loyal']['feedback_score'].mean() / 5,
            mock_df[mock_df['category'] == 'Loyal']['engagement_score'].mean(),
            1 - (mock_df[mock_df['category'] == 'Loyal']['last_activity_days'].mean() / 60)
        ]
        
        at_risk_values = [
            mock_df[mock_df['category'] == 'At Risk']['purchases'].mean() / 20,
            mock_df[mock_df['category'] == 'At Risk']['feedback_score'].mean() / 5,
            mock_df[mock_df['category'] == 'At Risk']['engagement_score'].mean(),
            1 - (mock_df[mock_df['category'] == 'At Risk']['last_activity_days'].mean() / 60)
        ]
        
        churned_values = [
            mock_df[mock_df['category'] == 'Churned']['purchases'].mean() / 20,
            mock_df[mock_df['category'] == 'Churned']['feedback_score'].mean() / 5,
            mock_df[mock_df['category'] == 'Churned']['engagement_score'].mean(),
            1 - (mock_df[mock_df['category'] == 'Churned']['last_activity_days'].mean() / 60)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=loyal_values,
            theta=categories,
            fill='toself',
            name='Loyal',
            line_color='#00d2ff'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=at_risk_values,
            theta=categories,
            fill='toself',
            name='At Risk',
            line_color='#ffd166'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=churned_values,
            theta=categories,
            fill='toself',
            name='Churned',
            line_color='#ef476f'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=30, l=30, r=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Customer recommendations
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("Recommended Actions")
    
    tab1, tab2, tab3 = st.tabs(["🏆 For Loyal", "⚠️ For At Risk", "🚨 For Churned"])
    
    with tab1:
        st.markdown("""
        - **VIP Program**: Launch exclusive benefits for top customers
        - **Referral Incentives**: Offer rewards for bringing new customers
        - **Preview Access**: Give early access to new products/features
        - **Personalized Communication**: Send tailored content based on preferences
        """)
    
    with tab2:
        st.markdown("""
        - **Re-engagement Campaign**: Send targeted offers to spark interest
        - **Feedback Collection**: Understand pain points and areas for improvement
        - **Product Education**: Help customers get more value from products
        - **Limited-Time Offers**: Create urgency with time-sensitive deals
        """)
    
    with tab3:
        st.markdown("""
        - **Win-back Campaign**: Significant offers to return
        - **Exit Survey**: Understand reasons for churning
        - **Alternative Products**: Suggest different offerings that might fit better
        - **Reduced Friction**: Simplify the return process
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; opacity: 0.7;'>
    <p>© 2025 Loyalty Analytics Dashboard | Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)
