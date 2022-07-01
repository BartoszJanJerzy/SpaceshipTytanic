import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class KComparison:
    
    def __init__(self, df, cols, max_k):
        self.df = df
        self.cols = cols
        self.max_k = max_k
        self.wcss, self.silhs = self.get_scores()
    
    def get_scores(self):
        X = self.df[self.cols]
        wcss = []
        silhs = []

        for i in range(2, self.max_k+1):
            kmeans = KMeans(n_clusters=i, random_state=0)
            kmeans.fit(X)
            y = kmeans.predict(X)
            silh = silhouette_score(X, y)

            silhs.append(silh)
            wcss.append(kmeans.inertia_)
        
        return wcss, silhs
    
    def get_silh_colors(self):
        max_silh = max(self.silhs)
        max_id = 0
        colors = []
        
        for i in range(len(self.silhs)):
            if self.silhs[i] == max_silh:
                colors.append('green')
            else:
                colors.append('silver')
        
        return colors
    
    def make_graph(self):
        colors = self.get_silh_colors()
        x = [i for i in range(2, self.max_k+1)]
        
        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(
            name = 'Inertia',
            x = x,
            y = self.wcss,
        ), secondary_y=False)

        fig.add_trace(go.Bar(
            name = 'Silhouette',
            x = x,
            y = self.silhs,
            marker_color = colors,
            opacity = 0.5
        ), secondary_y=True)

        fig.update_layout(
            title='K number comparison',
            xaxis_title = 'k',
            width = 1000,
            height = 500
        )
        fig.show(renderer='notebook')