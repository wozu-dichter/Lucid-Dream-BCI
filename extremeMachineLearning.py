# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:06:35 2020

@author: Cagatay Demirel
"""

from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from boruta import BorutaPy
import time
from sklearn.ensemble import RandomForestClassifier
import os
import pickle

class extremeMachineLearning:
    
    def __init__(self, dataset, num_of_class, dataset_name):
        self.dataset = dataset
        self.num_of_class = num_of_class
        self.dataset_name = dataset_name 
        
    def feature_selection_Boruta(self, X,y,max_depth = 7):
        #import lib
        tic = time.time()
        
        #instantiate an estimator for Boruta. 
        rf = RandomForestClassifier(n_jobs=-1, class_weight=None, max_depth=max_depth)
        # Initiate Boruta object
        feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=0)
        # fir the object
        feat_selector.fit(X=X, y=y)
        # Check selected features
        print(feat_selector.support_)
        # Select the chosen features from our dataframe.
        Feat_selected = X[:, feat_selector.support_]
        print(f'Selected Feature Matrix Shape {Feat_selected.shape}')
        toc = time.time()
        print(f'Feature selection using Boruta took {toc-tic}')
        ranks = feat_selector.ranking_
        
        return ranks, Feat_selected
        
    def unsupervised_PCA(self, dimension=3):
        pca = PCA(n_components=3)
        dataset_dimreduced = pca.fit(self.dataset).transform(self.dataset) 
        return dataset_dimreduced
    
    def KMeans(self, dataset, n_clusters = 2, visualization=True, saveFigure=False):
        
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        y_pred = clusterer.fit_predict(dataset)
        
        silhouette_avg = silhouette_score(dataset, y_pred)
        print("For n_clusters = ", n_clusters, "The average silhouette_score is :", silhouette_avg)
        
        if(visualization==True and np.shape(dataset)[1]==2):
            
            #==== Defining Colors ======
            color_chunk = ("red", "green", "yellow", "darkorchid", "cyan")
            cluster_chunk = ('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5')
            
            colors = color_chunk[0:n_clusters]
            legends = cluster_chunk[0:n_clusters]
            #==== Defining Colors ======
            
            #=== Dataset Labelled from Clusters ===
            x,y = list(), list()
            for i in range(n_clusters):
                x.append(dataset[y_pred==i,0])
                y.append(dataset[y_pred==i,1])    
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
            
            for x_t, y_t,color,legend in zip(x,y,colors, legends):
                ax.scatter(x_t, y_t, alpha=0.8, c=color, edgecolors='none', s=50, label=legend)  
            
            plt.title('Scatter Plot of ' + self.dataset_name +  ' K-means clustered 2d')
            plt.legend(loc=2)
            plt.show()            
            
            #==== Save Figure =====
            if(visualization==True and saveFigure==True):
                plt.savefig('Scatter Plot of ' + self.dataset_name +  ' K-means clustered 2d', pad_inches=0, dpi=800)                
            #==== Save Figure =====
            
        elif(visualization==True and np.shape(dataset)[1]==3):
            
            #==== Defining Colors ======
            color_chunk = ("red", "green", "yellow", "darkorchid", "cyan")
            cluster_chunk = ('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5')
            
            colors = color_chunk[0:n_clusters]
            legends = cluster_chunk[0:n_clusters]
            #==== Defining Colors ======
            
            #=== Dataset Labelled from Clusters ===
            x,y,z = list(), list(), list()
            for i in range(n_clusters):
                x.append(dataset[y_pred==i,0])
                y.append(dataset[y_pred==i,1])    
                z.append(dataset[y_pred==i,2])
            
            ax = fig.gca(projection='3d')
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
            
            for x_t, y_t,z_t,color,legend in zip(x,y,z,colors, legends):
                ax.scatter(x_t, y_t,z_t, alpha=0.8, c=color, edgecolors='none', s=50, label=legend)  
            
            plt.title('Scatter Plot of ' + self.dataset_name +  ' K-means clustered 3d')
            plt.legend(loc=2)
            plt.show()
        
            #==== Save Figure =====
            if(visualization==True and saveFigure==True):
                plt.savefig('Scatter Plot of ' + self.dataset_name +  ' K-means clustered 3d', pad_inches=0, dpi=800)                
            #==== Save Figure =====
    
    def scatter2D(self, dataset_dimreduced, labels, n_cluster, if_labeled_scatter=False):
        
        #==== Defining Colors ======
        color_chunk = ("red", "green", "yellow", "darkorchid", "cyan")
        class_chunk = ('Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5')
        
        colors = color_chunk[0:self.num_of_class]
        legends = class_chunk[0:self.num_of_class]
        #==== Defining Colors ======
        
        #======= 2D =============
        x,y = list(), list()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
        
        if(if_labeled_scatter):
            for i in range(n_cluster):
                x.append(dataset_dimreduced[labels==i,0])
                y.append(dataset_dimreduced[labels==i,1])    
            
            for x_t, y_t,color,legend in zip(x,y,colors,legends):
                ax.scatter(x_t, y_t, alpha=0.8, c=color, edgecolors='none', s=50, label=legend)
        else:
             ax.scatter(dataset_dimreduced[:,0], dataset_dimreduced[:,1], alpha=0.8, edgecolors='none', s=50)
        #======= 2D =============
        
        #===== Save Figure ======
        plt.title('Scatter Plot of ' + self.dataset_name + ' feature set (2D)')
        plt.legend(loc=2)
        plt.show()
        plt.savefig('scatter Plot of ' + self.dataset_name +  ' feature set 2d', pad_inches=0, dpi=800)
        #===== Save Figure ======
            

    def scatter3D(self, dataset_dimreduced, labels, n_cluster, if_labeled_scatter=False):
        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
        
        #==== Defining Colors ======
        color_chunk = ("red", "green", "yellow", "darkorchid", "cyan")
        class_chunk = ('Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5')
        
        colors = color_chunk[0:self.num_of_class]
        legends = class_chunk[0:self.num_of_class]
        #==== Defining Colors ======
        
        # ======= 3D =============
        ax = fig.gca(projection='3d')
        x,y,z = list(), list(), list()
        
        if(if_labeled_scatter):
            for i in range(n_cluster):
                x.append(dataset_dimreduced[labels==i,0])
                y.append(dataset_dimreduced[labels==i,1])
                z.append(dataset_dimreduced[labels==i,2])     
            
            for x_t, y_t, z_t,color,legend in zip(x,y,z,colors,legends):
                ax.scatter(x_t, y_t, z_t, alpha=0.8, c=color, edgecolors='none', s=50, label=legend)
        else:
            ax.scatter(dataset_dimreduced[:,0], dataset_dimreduced[:,1], dataset_dimreduced[2,:], \
                       alpha=0.8, edgecolors='none', s=50)
        #======= 3D =============
        
        #===== Save Figure ======
        plt.title('Scatter Plot of ' + self.dataset_name + ' feature set (3D)')
        plt.legend(loc=2)
        plt.show()
        plt.savefig('scatter Plot of ' + self.dataset_name +  ' feature set 3d', pad_inches=0, dpi=800)
        #===== Save Figure ======
        
    def pickleLoader(self, directory):
        files = list()
        pickleList = list()
        for file in os.listdir(directory):
                 pickleList.append(pickle.load(open(file), 'r'))
                 
        return pickleList
        
        
