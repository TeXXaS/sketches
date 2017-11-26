class citizen: 
    def __init__(self, opinion, action, pos=(0,0)):
        self.opinion = opinion
        self.action = action
        self.pos = pos
    def __str__(self):
        return(str(self.opinion), str(self.action))
        

def socialremake(g,z,b):
    dice=np.random.uniform()
    neig=g.neighbors(z)
    notneigh=[n for n in g.nodes() if n not in neig]
    if dice<b:
        lmnotneigh=[m for m in notneigh if z.opinion-m.action<=0.5 and z.opinion-m.action>=-0.5]
        for d in lmnotneigh:
            g.add_edge(z,d)
            print("edge added")
            break
    if dice<b:
        diffneig=[l for l in neig if z.opinion-l.opinion>0.5 or z.opinion-l.opinion<-0.5]
        for f in diffneig:
            g.remove_edge(z,f)
            print("edge removed")
            break


def dif_ind_neigh(g,z,a):
    dice=np.random.uniform()
    neigh=g.neighbors(z)
    actionNeigh=[]
    for n in neigh:
        actionNeigh.append(n.action)
    averageActionNeigh = sum(actionNeigh)/len(list(g.neighbors(z)))
    diff = z.action - averageActionNeigh
    if diff <=-1 and dice<=a:
            z.action=z.action+1
            print("action changed + 1")
    elif diff >= 1 and dice<=a:
            z.action = max(1,z.action-1)
            print("action changed - 1")


for timestep in range(100):
    troubled = list(t for t in g.nodes() if t.opinion-t.action>=0.5 or t.opinion-t.action<=-0.5)
    for z in troubled:
        socialremake(g,z,0.7)
        dif_ind_neigh(g,z,0.5)
