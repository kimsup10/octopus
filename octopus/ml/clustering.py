from functools import reduce
import random
import numpy as np


def get_dummy_user_likes_map(M, N):
    return {str(i): np.array([random.choice([1, 0]) for j in range(M)]) for i in range(N)}


class KMeansClustering:
    def __init__(self, user_likes_map, K=10):
        # TODO: Replace with real user_likes_map
        self.user_likes_map = user_likes_map
        self.num_of_clusters = K
        self.num_of_users = len(user_likes_map.keys())
        self.num_of_attr = len(list(user_likes_map.values())[0])

        self.clusters = self.set_initial_clusters()

    def set_initial_clusters(self):
        users = list(self.user_likes_map.keys())
        centroid_users = [users[random.randrange(self.num_of_users)]
                          for i in range(self.num_of_clusters)]

        while True:
            if len(set(centroid_users)) == self.num_of_clusters:
                clusters = list(map(lambda user: {"centroid": self.user_likes_map[user],
                                                   "users": [user]},
                                    centroid_users))
                return clusters
            centroid_users.append(random.randrange(self.num_of_users))

    def recompute_centroid(self, users):
        map_sum = np.array([0]*self.num_of_attr)
        for user in users:
            map_sum = np.add(map_sum, self.user_likes_map[user])

        return np.round(map_sum / len(users))

    def get_nearest_cluster(self, user):
        user_likes_map = self.user_likes_map[user]
        nearest_centroid = {"cluster": None, "distance": self.num_of_attr}
        for idx, cluster in enumerate(self.clusters):
            distance = np.count_nonzero(user_likes_map != cluster["centroid"])
            if distance < nearest_centroid["distance"]:
                nearest_centroid["cluster"] = idx
                nearest_centroid["distance"] = distance
        return nearest_centroid["cluster"]

    def cluster(self):
        users = self.user_likes_map.keys()
        is_any_centroid_changed = False

        while is_any_centroid_changed is False:
            for cluster in self.clusters:
                cluster["users"] = []

            for user in users:
                nearest_cluster = self.get_nearest_cluster(user)
                self.clusters[nearest_cluster]["users"].append(user)
                new_centroid = self.recompute_centroid(self.clusters[nearest_cluster]["users"])
                if not np.array_equal(new_centroid, self.clusters[nearest_cluster]["centroid"]):
                    is_any_centroid_changed = True
                    self.clusters[nearest_cluster]["centroid"] = new_centroid

        return self.clusters
