from flask import Flask
from flask import render_template

from octopus.ml.clustering import KMeansClustering
from octopus.sns import get_articles, get_user_likes_map

app = Flask(__name__)
app.debug = True


@app.route('/')
@app.route("/<username>")
def visualize_ml(username='huntrax11'):
    articles = get_articles(username)
    user_likes_map = get_user_likes_map(username)
    k = KMeansClustering(user_likes_map)
    nodes = []
    for i, cluster in enumerate(k.cluster()):
        min_distance = min(cluster['distances'])
        for user, distance in zip(cluster.get('users'), cluster['distances']):
            nodes.append({
                "cluster": i,
                "radius": (min_distance+1)/(distance+1)*25,
                "icon": user.profile_pic_url,
                "name": user.username
            })

    return render_template('cluster_visualize.htm',
                           user=articles[0].user,
                           nodes=nodes, m=k.num_of_clusters,
                           articles=articles)


if __name__ == "__main__":
    app.run()
