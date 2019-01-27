import json
import matplotlib.pyplot as plt

class Validator():
    def __init__(self,data=None):
        self.user_id = data["user_id"]
        self.reputation_data = data["reputation_data"] 
        self.compute_score(); 
       
     
    def getUserId(self):
        return self.user_id

    def compute_score(self):
        for idx,_ in enumerate(self.reputation_data):
            params = self.reputation_data[idx]["params"];
            vote_score  =0;
            upvote_score =0;
            downvote_score = 0;
            hide_score = 0;

            vote_score = self.reputation_data[idx]["score_params"]["vote_score"];

            if(params["totalUpVotes"] > 0):
                upvote_score = round(params["totalUpVotes"]/params["totalVotes"]*100,2)
                downvote_score = round(params["totalDownVotes"]/params["totalVotes"]*100,2)
                hide_score = round(params["totalHides"]/params["totalVotes"]*100,2)
                self.reputation_data[idx]["score"] = round((vote_score + upvote_score - downvote_score - hide_score)/2,2)
                self.reputation_data[idx]["annotation"] = "U={},D={},V={},H={}".format(str(upvote_score),str(downvote_score),str(vote_score),str(hide_score))
            else :
                self.reputation_data[idx]["score"] = round(vote_score/2,2);
                self.reputation_data[idx]["annotation"] = "U={},D={},V={},H={}".format(str(0),str(0),str(vote_score),str(0))

    def plot_validator(self,plotter):
        self.x =[]
        self.y =[]
        self.annotate =[]
        for idx,_ in enumerate(self.reputation_data):
            self.y.append(self.reputation_data[idx]["score"])
            self.x.append(idx)
            self.annotate.append(self.reputation_data[idx]["annotation"])

        self.line, = plotter.plot(self.x,self.y,marker="o")

    def get_line(self):
        return self.line

    def get_annotation(self,index):
        return self.annotate[index]

        
validatorList = []

with open("indorse-prod.validatorsv4.json") as f:
    data = json.loads(f.read())
    for idx,validators in enumerate(data):
        validator = Validator(data[idx])
        validatorList.append(validator)
 
fig, ax = plt.subplots()

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


for validator in validatorList:
    validator.plot_validator(plt)


def search_and_generate_annotation(event):
    for validator in validatorList:
       line = validator.get_line()
       cont, indArr = line.contains(event)
       if cont:
           x, y = line.get_data()
           xy = (x[indArr["ind"][0]], y[indArr["ind"][0]])
           annotation = validator.get_annotation(indArr["ind"][0])
           return True,xy,annotation

    return False,"",""

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, xy, text = search_and_generate_annotation(event)
        if cont:
            annot.xy = xy
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.4)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()