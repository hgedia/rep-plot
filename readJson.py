import json
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)


class Validator():
    def __init__(self,data=None):
        self.user_id = data["user_id"]
        self.reputation_data = data["reputation_data"] 
        self.compute_score(); 
       
     
    def getUserId(self):
        return self.user_id

    def compute_score(self):
        for idx,reputation in enumerate(self.reputation_data):
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
            self.x.append(idx);
            #self.annotate.append(self.reputation_data["idx"]["annotation"][:]);

        self.line = plotter.plot(self.x,self.y,marker="o")


        
validatorList = []

with open("indorse-prod.validatorsv3.json") as f:
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
    print(validator.getUserId())
    print(validator.reputation_data)
    validator.plot_validator(plt)


plt.show()
