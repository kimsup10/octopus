import numpy as np


class KMeansClustering:
    def __init__(self, user_likes_map, K=None):
        self.user_likes_map = user_likes_map
        if K is None:
            K = np.sqrt(len(user_likes_map)).astype('int')
        self.num_of_clusters = K
        self.num_of_users = len(user_likes_map)
        self.num_of_attr = len(list(user_likes_map.values())[0])
        self.init_clusters()

    def init_clusters(self):
        self.clusters = [{
            'centroid': np.random.choice([True, False], self.num_of_attr),
            'users': [],
        } for i in range(self.num_of_clusters)]

    def compute_centroid(self, users):
        return np.round(np.mean([self.user_likes_map[user]
                                 for user in users], axis=0))

    @staticmethod
    def _distance(a, b):
        return np.count_nonzero(np.not_equal(a, b))

    def get_nearest_cluster(self, user):
        user_likes_map = self.user_likes_map[user]
        return min(self.clusters,
                   key=lambda c: self._distance(user_likes_map, c['centroid']))

    def cluster(self):
        is_centroid_changed = False

        while is_centroid_changed is False:
            for cluster in self.clusters:
                cluster['users'] = []

            for user in self.user_likes_map:
                nearest_cluster = self.get_nearest_cluster(user)
                nearest_cluster['users'].append(user)

            for cluster in self.clusters:
                new_centroid = self.compute_centroid(cluster['users'])
                if not np.array_equal(new_centroid, cluster['centroid']):
                    is_centroid_changed = True
                    cluster['centroid'] = new_centroid

        return self.clusters
