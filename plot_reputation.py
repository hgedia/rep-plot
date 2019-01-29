import json
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
import numpy as np

class Validator():    

    def __init__(self,data=None):
        self.user_id = data["user_id"]
        self.reputation_data = data["reputation_data"] 
        self.compute_score(); 
       
     
    def get_user_id(self):
        return self.user_id

    def compute_score(self):
        for idx,_ in enumerate(self.reputation_data):
            params = self.reputation_data[idx]["params"];
            vote_score  =0
            upvote_score =0
            downvote_score = 0
            hide_score = 0

            vote_score = self.reputation_data[idx]["score_params"]["vote_score"];
            
            if(params["totalVotes"] > 0 ):
                upvote_score = round(params["totalUpVotes"]/params["totalVotes"]*100,2)
                downvote_score = round(params["totalDownVotes"]/params["totalVotes"]*100,2)
                hide_score = round(params["totalHides"]/params["totalVotes"]*100,2)
                if(params["totalVotes"] > 15):
                    self.reputation_data[idx]["score"] = round(
                        ((0.9* vote_score) + (0.1 * upvote_score) - downvote_score - hide_score), 2)
                else:
                    self.reputation_data[idx]["score"]=0
                #if(params["totalVotes"] > 20):
                #    self.reputation_data[idx]["score"] = round((vote_score + upvote_score - downvote_score - hide_score)/2,2)
                #else:
                #   self.reputation_data[idx]["score"] = 0
                #print("Score = " + str(self.reputation_data[idx]["score"]))
                self.reputation_data[idx]["annotation"] = "U={},D={},V={},H={}".format(str(upvote_score),str(downvote_score),str(vote_score),str(hide_score))
            #else :                
            #    if(params["totalVotes"] > 15):
            #        self.reputation_data[idx]["score"] = round(vote_score *0.9,2);
            #    else:
            #        self.reputation_data[idx]["score"] =0
            #    self.reputation_data[idx]["annotation"] = "U={},D={},V={},H={}".format(str(0),str(0),str(vote_score),str(0))
            else:
                 self.reputation_data[idx]["annotation"] = "U={},D={},V={},H={}".format(
                     str(0), str(0), str(vote_score), str(0))

    def plot_validator(self,plotter,legend):
        self.x =[]
        self.y =[]
        self.annotate =[]
        print("PLOT")
        for idx,_ in enumerate(self.reputation_data):
            self.y.append(self.reputation_data[idx]["score"])
            self.x.append(idx)
            self.annotate.append(self.reputation_data[idx]["annotation"])

        self.line, = plotter.plot(self.x,self.y,marker="o")
        if(self.user_id in legend):
            l = len(self.reputation_data)
            self.line.set_label(self.user_id[:2] + "..." + self.user_id[-2:] + "(S=" + str(self.reputation_data[l-1]["score"]) +")")
            print(self.user_id[:2] + "..." + self.user_id[-2:]  + "A = " + self.reputation_data[l-1]["annotation"] +
                  "TV=" + str(self.reputation_data[l-1]["params"]["totalVotes"]))
            
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


    def get_last_reputation_score(self):
        l = len(self.reputation_data)
        s = self.reputation_data[l-1]["score"]
        return s
#Helpers    
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
    total_votes_cast =0
    total_upvotes_cast =0
    total_downvotes_cast =0
    total_hides_cast =0


    for validator in validatorList:
        t, u, d, h, v = validator.get_last_reputation_params()
        #Total Votes
        
        if(t>0):
            total_votes_cast +=t
            total_vote_count += 1
            if(t < 10):
                total_votes_dict["0-10"] += 1
            elif(t < 20):
                total_votes_dict["10-20"] += 1
            elif(t < 30):
                total_votes_dict["30-40"] += 1
            elif(t < 40):
                total_votes_dict["30-40"] += 1
            elif(t >= 40):
                total_votes_dict["40-INF"] += 1

        #Total Upvotes
        if(u>0):
            total_upvotes_cast+=u
            total_upvote_count += 1
            if(u < 2):
                total_upvotes_dict["0-2"] += 1
            elif(u < 4):
                total_upvotes_dict["2-4"] += 1
            elif(u < 8):
                total_upvotes_dict["4-8"] += 1
            elif(u >= 8):
                total_upvotes_dict["8-INF"] += 1

        #Total Downvotes
        if(d >0):
            total_downvotes_cast+=d
            total_downvote_count += 1
            if(d < 2):
                total_downvotes_dict["0-2"] += 1
            elif(d < 4):
                total_downvotes_dict["2-4"] += 1
            elif(d < 8):
                total_downvotes_dict["4-8"] += 1
            elif(d >= 8):
                total_downvotes_dict["8-INF"] += 1

        #Total Hides
        if(h > 0):
            total_hides_cast+=h
            total_hide_count +=1
            if(h < 2):            
                total_hide_dict["0-2"] += 1
            elif(h < 4):
                total_hide_dict["2-4"] += 1
            elif(h < 8):
                total_hide_dict["4-8"] += 1
            elif(h >= 8):
                total_hide_dict["8-INF"] += 1

        #Total Consensus percentage
        if(v > 0):
            total_consensus_perc += 1
            if(v < 20):
                total_consesnsus_perc_dict["0-20"] += 1
            elif(v < 40):
                total_consesnsus_perc_dict["20-40"] += 1
            elif(v < 60):
                total_consesnsus_perc_dict["40-60"] += 1
            elif(v<80):
                total_consesnsus_perc_dict["60-80"] += 1
            elif(v >= 80):
                total_consesnsus_perc_dict["80-100"] += 1

    #print(total_consesnsus_perc_dict)


    fig2 = plotter.figure(2, figsize=(22, 6))
    ax1 = fig2.add_subplot(231)
    ax2 = fig2.add_subplot(232)
    ax3 = fig2.add_subplot(233)
    ax4 = fig2.add_subplot(234)
    ax5 = fig2.add_subplot(235)
    ax6 = fig2.add_subplot(236)

    plt.subplot(231)
    plotter.bar(total_consesnsus_perc_dict.keys(),total_consesnsus_perc_dict.values())
    ax1.set_title("Consensus % (T=" + str(total_consensus_perc) + ")")
    plt.subplot(232)
    plotter.bar(total_hide_dict.keys(),total_hide_dict.values())
    ax2.set_title("Hidden Votes (T=" + str(total_hide_count) +")")
    plt.subplot(233)
    plotter.bar(total_downvotes_dict.keys(), total_downvotes_dict.values())
    ax3.set_title("Downvotes (T=" + str(total_downvote_count) + ")")
    plt.subplot(234)
    plotter.bar(total_upvotes_dict.keys(), total_upvotes_dict.values())
    ax4.set_title("Upvotes (T=" + str(total_upvote_count) + ")")
    plt.subplot(235)
    plotter.bar(total_votes_dict.keys(), total_votes_dict.values())
    ax5.set_title("Votes cast by validator  (T=" + str(total_vote_count) + ")")

    labels = 'Upvotes', 'Downvotes', 'Hidevotes', 'Votes'
    sizes =[total_upvotes_cast, total_downvotes_cast,total_hides_cast,total_votes_cast-total_upvotes_cast - total_downvotes_cast]


    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    wedges, texts, autotexts = ax6.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax6.axis('equal')

    legend_lables = 'Upvotes (T=' + str(total_upvotes_cast) + ')','Downvotes (T=' + str(total_downvotes_cast) + ')','Hidevotes (T=' + str(total_hides_cast) + ')','Votes (T=' + str(total_votes_cast - total_upvotes_cast - total_downvotes_cast) + ')'
                    
    ax6.legend(wedges, legend_lables,
               title="Votes (T=" + str(sum(sizes)) + ")",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))



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


def plot_validator_score_bar(validatorList,plotter):
    fig3 = plotter.figure()
    validator_score_dict = {"0-5":0 ,"5-10":0 ,"10-15":0, "15-20" :0 ,"20-25":0, "25-30":0, "30-35":0,"35-40":0,"40-45":0, "45-50" :0,"50-55":0 ,"55-60":0 ,"60-65":0, "65-70":0,"70-75":0 , "75-80":0,"80-85":0, "85-90":0,"90-95":0 , "95-100":0}
    total_validator_count = 0
    for validator in validatorList:
        s = validator.get_last_reputation_score()
        if(s>0):
            total_validator_count+=1
            if(s <5):
                validator_score_dict["0-5"] += 1
            elif(s < 10):
                validator_score_dict["5-10"] += 1
            elif(s < 15):
                validator_score_dict["10-15"] += 1
            elif(s<20):
                validator_score_dict["15-20"] += 1
            elif(s < 25):
                validator_score_dict["20-25"] += 1
            elif(s < 30):
                validator_score_dict["25-30"] += 1
            elif(s < 35):
                validator_score_dict["30-35"] += 1
            elif(s < 40):
                validator_score_dict["35-40"] += 1
            elif(s < 45):
                validator_score_dict["40-45"] += 1
            elif(s < 50):
                validator_score_dict["45-50"] += 1
            elif(s < 55):
                validator_score_dict["50-55"] += 1
            elif(s < 60):
                validator_score_dict["55-60"] += 1
            elif(s < 65):
                validator_score_dict["60-65"] += 1
            elif(s<70):
                validator_score_dict["65-70"] +=1
            elif(s < 75):
                validator_score_dict["70-75"] += 1
            elif(s<80):
                validator_score_dict["75-80"] += 1
            elif(s < 85):
                validator_score_dict["80-85"] += 1
            elif(s < 90):
                validator_score_dict["85-90"] += 1
            elif(s < 95):
                validator_score_dict["90-95"] += 1
            elif(s>=95):
                validator_score_dict["95-100"] += 1

    fig3.suptitle("Validator scores (T=" + str(total_validator_count) + ")")
    plotter.bar(validator_score_dict.keys(),validator_score_dict.values())
    


#Main
validatorList = []

with open("indorse-prod.validatorsv6.json") as f:
    data = json.loads(f.read())
    for idx, validators in enumerate(data):
        validator = Validator(data[idx])
        validatorList.append(validator)

fig, ax = plt.subplots()
ax.set_xlabel("Data point")
ax.set_ylabel("Validator Reputation")

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)


sorted_list = sorted(validatorList,reverse=True)
legend  =[]
for validator in sorted_list[:5]:
    legend.append(validator.get_user_id())

#Plot 
for validator in validatorList:
    validator.plot_validator(plt,legend)

plot_validator_metrics(validatorList,plt)
plot_validator_score_bar(validatorList,plt)

plt.show()
