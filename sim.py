import numpy as np
import matplotlib.pyplot as plt
class SimpleNN:
    def __init__(self):
        self.W1 = np.random.randn(10,20)*0.1
        self.b1 = np.zeros((1,20))
        self.W2 = np.random.randn(20,2)*0.1
        self.b2 = np.zeros((1,2))
    def forward(self,X):
        return np.tanh(X@self.W1+self.b1)@self.W2+self.b2
    def get_params(self):
        return np.concatenate([self.W1.flatten(),self.b1.flatten(),self.W2.flatten(),self.b2.flatten()])
    def set_params(self,flat):
        idx=0
        self.W1=flat[idx:idx+200].reshape(10,20); idx+=200
        self.b1=flat[idx:idx+20].reshape(1,20); idx+=20
        self.W2=flat[idx:idx+40].reshape(20,2); idx+=40
        self.b2=flat[idx:idx+2].reshape(1,2)
def fitness(m,X,y):
    return np.mean(np.argmax(m.forward(X),1)==y)
def digest(p,prey):
    pp = p.get_params()
    lp = prey.get_params()
    mask = np.abs(lp)>np.percentile(np.abs(lp),35)
    d = 0.82*pp + 0.18*lp*mask + np.random.normal(0,0.015,len(pp))
    d[len(d)//2:]*=1.05
    n=SimpleNN()
    n.set_params(d)
    return n
POP=50
GEN=200
X=np.random.randn(500,10)
y=(np.sum(X[:,:5],1)>0).astype(int)
pop=[SimpleNN() for _ in range(POP)]
hist=[]
for g in range(GEN):
    fits=[fitness(m,X,y) for m in pop]
    pop=[pop[i] for i in np.argsort(fits)[::-1]]
    for i in range(int(0.3*POP)):
        pop[-1-i]=digest(pop[i%int(0.3*POP)],pop[-1-i])
    hist.append(max(fits))
    if g%50==0: print(f"Gen {g} best {max(fits):.3f}")
plt.plot(hist)
plt.title("ESP Fitness")
plt.savefig("esp_results.png")
plt.show()
print("done - plot saved")
