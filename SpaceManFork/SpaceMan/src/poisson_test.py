import math
import matplotlib.pyplot as plt
import numpy as np

kmax=50
radius=25000 # meters
lam=1e-8
B=np.pi * radius ** 2   
mu=lam * B

#k=np.arange(0, kmax+1, 1)
#print(k)
p_vals=[]
k_vals=[]
for k in range(kmax+1):
    p = ((mu**k)*np.exp(-mu))/ math.factorial(k)
    k_vals.append(k)
    p_vals.append(p)


p_vals=np.array(p_vals)
print(p_vals)
nb=np.argmax(p_vals)
print(f"NB value: {nb}")
print(f"Probabilidade máxima: {p_vals[nb]:.2f}")
#plt.plot(k_vals, p_vals)
#plt.xlabel("k")
#plt.ylabel("P(k)")
#plt.title("Distribuição de Poisson")
#plt.grid()
#plt.show()



mu = lam * B

# Gerar 100 000 valores aleatórios
X = np.random.poisson(mu, size=100000)

# Criar o histograma
plt.hist(X, bins=np.arange(0, 46) - 0.5,
         density=True, edgecolor="black")

plt.xlabel("Número de eventos (k)")
plt.ylabel("Frequência relativa")
plt.title(f"Distribuição de Poisson (μ = {mu:.3f})")
plt.xticks(range(0, 46, 5))
plt.grid(axis="y", alpha=0.3)
plt.show()