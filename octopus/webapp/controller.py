from flask import Flask
from flask import render_template

from octopus.ml.clustering import KMeansClustering
from octopus.sns import get_user_likes_map, api

app = Flask(__name__)
app.debug = True


@app.route('/')
@app.route("/<username>")
def visualize_ml(username=api.username):
    user_likes_map = get_user_likes_map(username)
    k = KMeansClustering(user_likes_map)
    nodes = []
    for i, cluster in enumerate(k.cluster()):
        nodes.extend(list(
            map(lambda user: {"cluster": i, "radius": len(user)},
                cluster.get('users'))));
    return render_template('cluster_visualize.htm',
                           username=username, nodes=nodes,
                           m=k.num_of_clusters)


if __name__ == "__main__":
    app.run()