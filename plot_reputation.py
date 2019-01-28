import json
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors

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
        self.line.set_label(self.user_id[:2] + "..." + self.user_id[-2:])
        plotter.legend(loc='best')

    def get_line(self):
        return self.line

    def get_annotation(self,index):
        return self.annotate[index]

    def __eq__(self, other):
        l = len (self.reputation_data)
        lo = len(other.reputation_data)
        return self.reputation_data[l-1]["score"] == other.reputation_data[lo-1]["score"]

    def __lt__(self, other):
        l = len(self.reputation_data)
        lo = len(other.reputation_data)
        return self.reputation_data[l-1]["score"] < other.reputation_data[lo-1]["score"]

    def get_last_reputation_params(self):
        l = len (self.reputation_data);
        params = self.reputation_data[l-1]["params"]
        u = params["totalUpVotes"];
        d = params["totalDownVotes"]
        h = params["totalHides"]
        t = params["totalVotes"]
        v = self.reputation_data[l-1]["score_params"]["vote_score"]
        return t,u,d,h,v
        
validatorList = []

with open("indorse-prod.validatorsv6.json") as f:
    data = json.loads(f.read())
    for idx,validators in enumerate(data):
        validator = Validator(data[idx])
        validatorList.append(validator)
 
fig, ax = plt.subplots()
ax.set_xlabel("Data point")
ax.set_ylabel("Validator Reputation")

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


#validatorList.sort(reverse=True)
for validator in validatorList:
    validator.plot_validator(plt)




    
def plot_validator_metrics(validatorList,plotter):
    total_vote_count = 0
    total_votes_dict = {"0-10": 0, "10-20": 0, "20-30": 0, "30-40": 0, "40-INF": 0}
    total_upvote_count = 0
    total_upvotes_dict = {"0-2": 0, "2-4": 0, "4-8": 0, "8-INF": 0}
    total_downvote_count = 0
    total_downvotes_dict = {"0-2": 0, "2-4": 0, "4-8": 0, "8-INF": 0}
    total_hide_count = 0
    total_hide_dict = {"0-2": 0, "2-4": 0, "4-8": 0, "8-INF": 0}
    total_consensus_perc = 0
    total_consesnsus_perc_dict = {"0-20": 0, "20-40": 0, "40-60": 0,"60-80":0,  "80-100": 0}


    for validator in validatorList:
        t, u, d, h, v = validator.get_last_reputation_params()
        print("T="+str(t) + " U="+str(u) + " D="+str(d) + " H="+str(h) +" V="+str(v));

        #Total Votes
        total_vote_count += t
        if(t < 10):
            total_votes_dict["0-10"] += 1
        elif(t < 20):
            total_votes_dict["10-20"] += 1
        elif(t < 30):
            total_votes_dict["30-40"] += 1
        elif(t < 40):
            total_votes_dict["30-40"] += 1
        elif(t > 40):
            total_votes_dict["40-INF"] += 1

        #Total Upvotes
        total_upvote_count += u
        if(u < 2):
            total_upvotes_dict["0-2"] += 1
        elif(u < 4):
            total_upvotes_dict["2-4"] += 1
        elif(u < 8):
            total_upvotes_dict["4-8"] += 1
        elif(u > 8):
            total_upvotes_dict["8-INF"] += 1

        #Total Downvotes
        total_downvote_count += d
        if(d < 2):
            total_downvotes_dict["0-2"] += 1
        elif(d < 4):
            total_downvotes_dict["2-4"] += 1
        elif(d < 8):
            total_downvotes_dict["4-8"] += 1
        elif(d > 8):
            total_downvotes_dict["8-INF"] += 1

        #Total Hides
        total_hide_count += h
        if(h < 2):
            total_hide_dict["0-2"] += 1
        elif(h < 4):
            total_hide_dict["2-4"] += 1
        elif(h < 8):
            total_hide_dict["4-8"] += 1
        elif(h > 8):
            total_hide_dict["8-INF"] += 1

        #Total Consensus percentage
        total_consensus_perc += v
        if(v < 20):
            total_consesnsus_perc_dict["0-20"] += 1
        elif(v < 40):
            total_consesnsus_perc_dict["20-40"] += 1
        elif(v < 60):
            total_consesnsus_perc_dict["40-60"] += 1
        elif(v<80):
            total_consesnsus_perc_dict["60-80"] += 1
        elif(v > 80):
            total_consesnsus_perc_dict["80-100"] += 1

    #print(total_consesnsus_perc_dict)


    fig2 = plotter.figure(2, figsize=(22, 5))
    ax1 = fig2.add_subplot(231)
    ax2 = fig2.add_subplot(232)
    ax3 = fig2.add_subplot(233)
    ax4 = fig2.add_subplot(234)
    ax5 = fig2.add_subplot(235)

    plt.subplot(231)
    plotter.bar(total_consesnsus_perc_dict.keys(),total_consesnsus_perc_dict.values())
    ax1.set_title("Consensus %")
    plt.subplot(232)
    plotter.bar(total_hide_dict.keys(),total_hide_dict.values())
    ax2.set_title("Hidden Votes (T=" + str(total_hide_count) +")")
    plt.subplot(233)
    plotter.bar(total_downvotes_dict.keys(), total_downvotes_dict.values())
    ax3.set_title("Downvotes")
    plt.subplot(234)
    plotter.bar(total_upvotes_dict.keys(), total_upvotes_dict.values())
    ax4.set_title("Upvotes")
    plt.subplot(235)
    plotter.bar(total_votes_dict.keys(), total_votes_dict.values())
    ax5.set_title("Total Votes cast")


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

plot_validator_metrics(validatorList,plt)




plt.show()
