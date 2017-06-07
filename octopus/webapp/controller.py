from flask import Flask, render_template, abort
from octopus.sns import get_articles, get_user_likes_map
from octopus.ml.clustering import KMeansClustering

app = Flask(__name__)
app.debug = True


@app.route('/favicon.ico')
def favicon():
    abort(404)


@app.route('/')
@app.route("/<username>")
def visualize_ml(username='huntrax11'):
    articles = get_articles(username)
    if not articles:
        abort(404)
    user_likes_map = get_user_likes_map(username)
    k = KMeansClustering(user_likes_map)
    nodes = []
    for i, cluster in enumerate(k.cluster()):
        min_distance = min(cluster['distances'])
        for user, distance in zip(cluster.get('users'), cluster['distances']):
            nodes.append({
                "cluster": i,
                "radius": (min_distance+1)/(distance+1)*30,
                "icon": user.profile_pic_url,
                "name": user.username
            })

    return render_template('cluster_visualize.htm',
                           user=articles[0].user,
                           nodes=nodes, m=k.num_of_clusters,
                           articles=articles)


if __name__ == "__main__":
    app.run()
