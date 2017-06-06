from flask import Flask
from flask import render_template

from octopus.ml.clustering import KMeansClustering
from octopus.sns import get_user_likes_map, api

app = Flask(__name__)
app.debug = True

MAX_DISTANCE = 12


@app.route('/')
@app.route("/<username>")
def visualize_ml(username=api.username):
    user_likes_map = get_user_likes_map(username)
    k = KMeansClustering(user_likes_map)
    nodes = []
    for i, cluster in enumerate(k.cluster()):
        for j, user in enumerate(cluster.get('users')):
            nodes.append({"cluster": i, "radius": (MAX_DISTANCE - cluster['distances'][j])*3,
                          "icon": user.profile_pic_url, "name": user.username})

    return render_template('cluster_visualize.htm',
                           username=username, user_pic_url=api.user_pic_url,
                           nodes=nodes, m=k.num_of_clusters,
                           pic="https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/18645325_1800731410256118_4283465158832947200_n.jpg",
                           text="역대급 맑은 날 오늘은 무조건 나가요🙌")


if __name__ == "__main__":
    app.run()
