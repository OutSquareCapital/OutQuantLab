
# OutQuantLab

**OutQuantLab** is a comprehensive Python framework for financial research and systematic trading strategy development.  
Designed with modularity, performance, and scalability in mind, it provides tools for data processing, signal generation, backtesting, portfolio management, and visualization, empowering researchers and traders to build and test complex strategies efficiently.

List of available dashboards so far:  
- Equity  
- Rolling Volatility  
- Rolling Drawdown  
- Rolling Sharpe Ratio  
- Rolling Smoothed Skewness  
- Rolling Average Inverted Correlation  
- Overall Returns  
- Overall Sharpe Ratio  
- Overall Volatility  
- Overall Average Drawdown  
- Overall Average Inverted Correlation  
- Overall Monthly Skew  
- Returns Distribution Violin  
- Returns Distribution Histogram  
- Correlation Heatmap  
- Clusters Icicle  
- Sharpe Ratio Heatmap  
- Overall Sharpe Ratio 3D Scatter  

Use case:  
```python
dashboards = DashboardsCollection(length=1250)
dashboards.plot("Equity").show()
```
