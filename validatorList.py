import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)

x = [0,1,4]
y = [0,1,2]
names = np.array(list("ABCDEFGHIJKLMNO"))

x1 = [0,2,6]


#norm = plt.Normalize(1, 4)

fig, ax = plt.subplots()
#print(ax)
line, = plt.plot(x, y, marker="o")
line2, = plt.plot(x1, y, marker="o")

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


def searchAndGenerateAnnotation(event):
    cont, indArr, line = checkIfLineContainsEvent(event)
    if cont:
        # get x,y co-ordinate
        x, y = line.get_data()
        xy = (x[indArr["ind"][0]], y[indArr["ind"][0]])
        text = "{},{}".format("X= ".join([str(
            x[indArr["ind"][0]])]), "Y=".join([str(y[indArr["ind"][0]])]))
        return True, xy, text
    else:
        return False, "", ""


def checkIfLineContainsEvent(event):
    cont, indArr = line.contains(event)
    if cont:
        return cont, indArr, line

    cont, indArr = line2.contains(event)
    if cont:
        return cont, indArr, line2

    return False, [], []



def update_annot(indArr):
    x, y = line.get_data()  
    #print(*ind, sep=", ")

    annot.xy = (x[indArr["ind"][0]], y[indArr["ind"][0]])
    text = "{}, {}".format(" ".join(list(map(str, indArr["ind"]))),
                           " ".join([names[n] for n in indArr["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def update_annotV2(xy,text):
    annot.xy = xy
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)



def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, xy,text = searchAndGenerateAnnotation(event)
        if cont:
            update_annotV2(xy,text)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()


