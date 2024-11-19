from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
import pandas as pd
import numpy as np
import bottleneck as bn

class ClusterGeneration:
    
    def flatten_singleton_clusters(cluster_dict):
        """
        Combine les clusters qui ne contiennent que des sous-clusters avec un seul actif ou n'ont pas besoin de niveau supplémentaire.

        Args:
            cluster_dict (dict): Dictionnaire contenant la hiérarchie des clusters.

        Returns:
            dict: Dictionnaire où les sous-clusters avec un seul actif ou inutiles ont été regroupés.
        """
        new_cluster_dict = {}
        
        for key, value in cluster_dict.items():
            if isinstance(value, dict):
                # Aplatir la structure récursivement
                flattened_value = ClusterGeneration.flatten_singleton_clusters(value)
                
                # Si le cluster contient uniquement un autre niveau ou que tout peut être regroupé
                if len(flattened_value) == 1 and all(isinstance(sub_value, list) for sub_value in flattened_value.values()):
                    # Fusionner les sous-clusters au niveau actuel
                    new_cluster_dict[key] = [item for sublist in flattened_value.values() for item in sublist]
                elif all(isinstance(sub_value, list) and len(sub_value) == 1 for sub_value in flattened_value.values()):
                    # Si tous les sous-clusters contiennent un seul actif, on les remonte au niveau du dessus
                    new_cluster_dict[key] = [item for sublist in flattened_value.values() for item in sublist]
                else:
                    # Si certains sous-clusters peuvent être fusionnés, on le fait, sinon on les garde
                    new_cluster_dict[key] = flattened_value
            else:
                new_cluster_dict[key] = value
        return new_cluster_dict


    def generate_static_clusters(returns_df, max_clusters=3, max_subclusters=None, max_subsubclusters=None):
        """
        Génére des clusters de corrélation à différents niveaux.

        Args:
            returns_df (pd.DataFrame): DataFrame des rendements journaliers, où chaque colonne représente un actif.
            max_clusters (int): Nombre maximal de clusters principaux souhaité.
            max_subclusters (int, optional): Nombre maximal de sous-clusters par cluster (ou None pour ne pas subdiviser).
            max_subsubclusters (int, optional): Nombre maximal de sous-sous-clusters par sous-cluster (ou None pour ne pas subdiviser).

        Returns:
            dict: Dictionnaire hiérarchisé des clusters avec possibilité de ne pas sous-diviser.
        """
        # Calculer la matrice de corrélation
        correlation_matrix = returns_df.corr()

        # Convertir la matrice de corrélation en une matrice de distance (1 - corrélation)
        distance_matrix = 1 - correlation_matrix

        # Appliquer le clustering hiérarchique pour les clusters principaux
        linkage_matrix = linkage(squareform(distance_matrix), method='complete')
        clusters = fcluster(linkage_matrix, max_clusters, criterion='maxclust')

        # Construire le dictionnaire des clusters principaux
        cluster_dict = {}
        for asset, cluster in zip(correlation_matrix.columns, clusters):
            if cluster not in cluster_dict:
                cluster_dict[cluster] = []
            cluster_dict[cluster].append(asset)

        # Ordonner le dictionnaire par numéro de cluster
        ordered_cluster_dict = {k: cluster_dict[k] for k in sorted(cluster_dict)}

        # Création des sous-clusters (si demandé)
        if max_subclusters is not None:
            for main_cluster, assets in ordered_cluster_dict.items():
                if len(assets) > 1:  # Si le cluster a plus d'un actif
                    # Calculer la matrice de distance pour les actifs dans ce cluster principal
                    sub_distance_matrix = 1 - returns_df[assets].corr()
                    sub_linkage_matrix = linkage(squareform(sub_distance_matrix), method='ward')

                    # Créer des sous-clusters
                    sub_clusters = fcluster(sub_linkage_matrix, max_subclusters, criterion='maxclust')

                    # Diviser les actifs en sous-clusters
                    subcluster_dict = {}
                    for asset, sub_cluster in zip(assets, sub_clusters):
                        if sub_cluster not in subcluster_dict:
                            subcluster_dict[sub_cluster] = []
                        subcluster_dict[sub_cluster].append(asset)

                    # Remplacer les actifs dans le cluster par les sous-clusters
                    ordered_cluster_dict[main_cluster] = subcluster_dict

        # Création des sous-sous-clusters (si demandé)
        if max_subsubclusters is not None:
            for main_cluster, subclusters in ordered_cluster_dict.items():
                if isinstance(subclusters, dict):  # Seulement si le cluster a déjà des sous-clusters
                    for sub_cluster, assets in subclusters.items():
                        if len(assets) > 1:  # Si le sous-cluster a plus d'un actif
                            # Calculer la matrice de distance pour les actifs dans ce sous-cluster
                            subsub_distance_matrix = 1 - returns_df[assets].corr()
                            subsub_linkage_matrix = linkage(squareform(subsub_distance_matrix), method='average')

                            # Créer des sous-sous-clusters
                            subsub_clusters = fcluster(subsub_linkage_matrix, max_subsubclusters, criterion='maxclust')

                            # Diviser les actifs en sous-sous-clusters
                            subsubcluster_dict = {}
                            for asset, subsub_cluster in zip(assets, subsub_clusters):
                                if subsub_cluster not in subsubcluster_dict:
                                    subsubcluster_dict[subsub_cluster] = []
                                subsubcluster_dict[subsub_cluster].append(asset)

                            # Remplacer les actifs dans le sous-cluster par les sous-sous-clusters
                            ordered_cluster_dict[main_cluster][sub_cluster] = subsubcluster_dict

        # Aplatir les clusters avec des enfants contenant un seul actif ou inutiles
        flattened_clusters = ClusterGeneration.flatten_singleton_clusters(ordered_cluster_dict)

        return flattened_clusters
    
    @staticmethod
    def generate_recursive_cluster_means(returns_df, cluster_tree, by_cluster=False):
        """
        Génère les moyennes des rendements de manière récursive pour chaque cluster en descendant dans l'arbre des clusters
        puis en remontant pour calculer les moyennes à chaque niveau. Si by_cluster est True, la fonction s'arrête au niveau
        des plus hauts clusters et renvoie une colonne par cluster.

        Args:
            returns_df (pd.DataFrame): DataFrame des rendements par actif.
            cluster_tree (dict): Dictionnaire imbriqué représentant la structure des clusters.
            by_cluster (bool): Si True, calcule les moyennes uniquement au niveau des plus hauts clusters.

        Returns:
            pd.DataFrame: DataFrame contenant les moyennes des rendements à chaque niveau ou par cluster.
        """
        
        group_means = {}  # Dictionnaire pour stocker les moyennes calculées à chaque niveau

        # Parcours récursif de l'arbre des clusters
        for cluster_key, cluster_value in cluster_tree.items():
            if isinstance(cluster_value, dict):
                # Si c'est un sous-cluster, appliquer la récursion pour obtenir les moyennes des sous-groupes
                if not by_cluster:
                    sub_group_mean = ClusterGeneration.generate_recursive_cluster_means(returns_df, cluster_value, by_cluster)
                    group_means[cluster_key] = sub_group_mean
                else:
                    # Si by_cluster est True, on ne descend pas plus bas, et on passe directement à ce niveau
                    matching_columns = []
                    for sub_key, sub_items in cluster_value.items():
                        # Filtrer les colonnes qui correspondent aux items du sous-cluster
                        matching_columns += [col for col in returns_df.columns if any(str(item) in col for item in sub_items)]
                    
                    if matching_columns:
                        # Calculer la moyenne des colonnes correspondantes pour ce cluster spécifique
                        cluster_mean = pd.Series(bn.nanmean(returns_df[matching_columns], axis=1), index=returns_df.index, name=f'Cluster_{cluster_key}')
                        group_means[cluster_key] = cluster_mean
            
            elif isinstance(cluster_value, list):
                # Si c'est une liste d'actifs (ou de stratégies), calculer la moyenne des rendements pour ces actifs
                matching_columns = [col for col in returns_df.columns if any(item in col for item in cluster_value)]
                if matching_columns:
                    sub_group_mean = pd.Series(bn.nanmean(returns_df[matching_columns], axis=1), index=returns_df.index, name=f'Cluster_{cluster_key}')
                    group_means[cluster_key] = sub_group_mean

        # Si by_cluster est True, on retourne directement les moyennes des plus hauts clusters
        if by_cluster and group_means:
            return pd.DataFrame(group_means, dtype=np.float32)
        
        # Si on n'a pas encore remonté, on calcule la moyenne finale en remontant à tous les niveaux
        if group_means:
            final_mean = pd.concat(group_means.values(), axis=1).mean(axis=1)
            return pd.DataFrame(final_mean, columns=['Cluster_Mean'], dtype=np.float32)
        
        # Si aucune donnée n'est disponible, retourner un DataFrame vide avec des NaN
        return pd.DataFrame(np.nan, index=returns_df.index, columns=['Cluster_Mean'], dtype=np.float32)
