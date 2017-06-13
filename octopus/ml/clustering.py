import random
import numpy as np


class KMeansClustering:
    def __init__(self, user_likes_map, K=None):
        self.user_likes_map = {
            user: likes_map
            for user, likes_map in user_likes_map.items()
            if np.count_nonzero(likes_map) > len(likes_map)*0.05
        }

        if K is None:
            K = np.sqrt(len(self.user_likes_map)).astype('int')
        self.num_of_clusters = K
        self.num_of_users = len(user_likes_map)
        self.num_of_attr = len(list(user_likes_map.values())[0])
        self.init_clusters()

    def init_clusters(self):
        self.clusters = [{
            'centroid': random.choice(list(self.user_likes_map.values())),
            'users': [],
        }]
        for i in range(1, self.num_of_clusters):
            d_square = np.array(
                [self._distance(self.user_likes_map[user],
                                self.get_nearest_cluster(user)['centroid'])
                 for user in self.user_likes_map]) ** 2
            ds_proportion = d_square / d_square.sum()
            choice = np.random.choice(d_square, 1, p=ds_proportion)
            i = np.where(d_square == choice)[0][0]
            self.clusters.append({
                'centroid': list(self.user_likes_map.values())[i],
                'users': [],
            })

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

        max_iter = 10

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
            max_iter -= 1
            if max_iter <= 0:
                break

        for cluster in self.clusters:
            cluster['distances'] = [
                self._distance(self.user_likes_map[user], cluster['centroid'])
                for user in cluster['users']
            ]

        return self.clusters
