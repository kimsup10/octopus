from .naive_bayes import naive


obj = naive()


def setting():
    return obj.set_naive_bayes()

def get_naive_bayes():
    return obj.cal_naive_bayes()



