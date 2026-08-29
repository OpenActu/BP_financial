# Module 6c — La loi de Poisson

**Durée : 1 h.** Prérequis : [module 6b](06b-loi-binomiale.md).

> **La question traitée.** Comment compter des événements **rares** dont on ne sait même pas
> combien d'occasions ils avaient de se produire ? La binomiale exige un $n$ ; les krachs, les
> défauts, les pannes n'en ont pas.

**Ce qui est en jeu.** La Poisson est la loi de comptage sans $n$. Elle possède une signature
unique — $E(X)=\operatorname{Var}(X)=\lambda$ — qui en fait un **modèle réfutable** : il suffit de
comparer la moyenne et la variance observées pour savoir si elle tient. Sur les données
financières, elle ne tient presque jamais, et la raison de cet échec est instructive (§ 6c.5).

---

## 6c.1 Définition

> **Définition.** $X$ suit une **loi de Poisson** de paramètre $\lambda>0$, notée
> $X\sim\mathcal P(\lambda)$, si $X$ est à valeurs dans $\mathbb N$ et
> $$P(X=k)=e^{-\lambda}\,\frac{\lambda^k}{k!},\qquad k=0,1,2,\dots$$

**C'est bien une loi de probabilité** : la série exponentielle donne
$\sum_{k\ge0}\lambda^k/k!=e^{\lambda}$, donc $\sum_k P(X=k)=e^{-\lambda}e^{\lambda}=1$.

> 🔑 **La série exponentielle est le seul outil du module.** Tous les calculs qui suivent —
> espérance, variance, fonction caractéristique — consistent à décaler l'indice de sommation d'un
> ou deux crans pour retomber sur $\sum_j \lambda^j/j!=e^\lambda$. Une seule identité, employée
> quatre fois.

**Le contexte de modélisation.** $\mathcal P(\lambda)$ décrit un comptage d'événements sur une
période fixe lorsque trois conditions sont réunies :

| Condition | Formulation | Ce qui la casse en finance |
|---|---|---|
| **Rareté** | À chaque instant, la probabilité d'un événement est infime | — |
| **Homogénéité** | Le taux $\lambda$ ne dépend pas de la date | Les régimes de volatilité |
| **Indépendance** ⭐ | Des périodes disjointes ne s'influencent pas | ⚠️ Le *clustering* de volatilité |

Le § 6c.5 montre que c'est la troisième qui lâche, et comment le détecter en une ligne de calcul.

---

## 6c.2 Espérance et variance, sans transformée

**Espérance.** Le terme $k=0$ est nul ; on part de $k=1$ et on simplifie $k/k!=1/(k-1)!$ :

$$E(X)=\sum_{k\ge 0}k\,e^{-\lambda}\frac{\lambda^k}{k!}
=e^{-\lambda}\sum_{k\ge 1}\frac{\lambda^{k}}{(k-1)!}
\overset{j=k-1}{=}e^{-\lambda}\,\lambda\sum_{j\ge 0}\frac{\lambda^{j}}{j!}
=e^{-\lambda}\lambda\,e^{\lambda}=\boxed{\,\lambda\,}$$

**Moment factoriel d'ordre 2.** Même manœuvre, deux crans au lieu d'un — et c'est pour cela qu'on
calcule $E\bigl(X(X-1)\bigr)$ plutôt que $E(X^2)$ :

$$E\bigl(X(X-1)\bigr)=e^{-\lambda}\sum_{k\ge 2}\frac{\lambda^{k}}{(k-2)!}
\overset{j=k-2}{=}e^{-\lambda}\,\lambda^2\sum_{j\ge 0}\frac{\lambda^{j}}{j!}=\lambda^2$$

**Variance.** On remonte : $E(X^2)=\lambda^2+\lambda$, d'où

$$\operatorname{Var}(X)=\lambda^2+\lambda-\lambda^2=\boxed{\,\lambda\,}\qquad\blacksquare$$

> 🔑 **$E(X)=\operatorname{Var}(X)=\lambda$ : la propriété la plus utile du module.** Aucune autre
> loi usuelle n'impose cette égalité. Elle donne un **test de validité immédiat** : calculez la
> moyenne et la variance de vos comptages ; si elles diffèrent nettement, le modèle de Poisson
> est faux, et il est inutile d'aller plus loin. Ce rapport porte un nom, l'**indice de
> dispersion** $\operatorname{Var}/E$, et vaut 1 sous Poisson.

---

## 6c.3 Espérance et variance, par la fonction caractéristique

### La fonction caractéristique

Toujours la même série, où $\lambda$ est simplement remplacé par $\lambda e^{it}$ :

$$\varphi_X(t)=\sum_{k\ge0}e^{itk}e^{-\lambda}\frac{\lambda^k}{k!}
=e^{-\lambda}\sum_{k\ge0}\frac{\left(\lambda e^{it}\right)^k}{k!}
=e^{-\lambda}\,e^{\lambda e^{it}}
=\boxed{\;e^{\lambda\left(e^{it}-1\right)}\;}$$

(La FGM est $M_X(t)=e^{\lambda(e^{t}-1)}$, finie pour **tout** $t$ réel — la Poisson est l'une des
lois où les deux transformées existent, et où l'on peut vérifier le passage $t\mapsto it$.)

### Les deux dérivations

Le facteur $\varphi_X$ se reproduit à chaque dérivation, ce qui rend le calcul très court. Avec
$\varphi_X'(t)=\varphi_X(t)\times i\lambda e^{it}$ et $\varphi_X(0)=1$ :

$$\varphi_X'(0)=1\times i\lambda=i\lambda
\qquad\Longrightarrow\qquad E(X)=-i\times i\lambda=\boxed{\,\lambda\,}\;\checkmark$$

$$\varphi_X''(t)=\underbrace{\varphi_X'(t)\,i\lambda e^{it}}_{\text{dérivée du premier facteur}}
+\underbrace{\varphi_X(t)\,i^2\lambda e^{it}}_{\text{dérivée du second}}
\qquad\Longrightarrow\qquad
\varphi_X''(0)=(i\lambda)(i\lambda)+(-\lambda)=-\lambda^2-\lambda$$

$$E(X^2)=-\varphi_X''(0)=\lambda^2+\lambda
\qquad\Longrightarrow\qquad
\operatorname{Var}(X)=\lambda\;\checkmark\qquad\blacksquare$$

### Le raccourci décisif : les cumulants

Le logarithme de $\varphi_X$ est ici d'une simplicité rare :

$$K_X(t)=\log\varphi_X(t)=\lambda\left(e^{it}-1\right)
=\lambda\sum_{j\ge1}\frac{(it)^j}{j!}$$

En identifiant avec le développement $K_X(t)=\sum_j \kappa_j\,(it)^j/j!$
([§ 6.4](06-fonction-caracteristique.md)) :

$$\boxed{\;\kappa_j=\lambda\quad\text{pour tout } j\ge1\;}$$

**Tous les cumulants valent $\lambda$.** D'un seul coup :

$$E(X)=\kappa_1=\lambda,\qquad
\operatorname{Var}(X)=\kappa_2=\lambda,\qquad
\gamma_1=\frac{\kappa_3}{\kappa_2^{3/2}}=\frac{1}{\sqrt\lambda},\qquad
\beta_2-3=\frac{\kappa_4}{\kappa_2^{2}}=\frac{1}{\lambda}$$

> 🔑 **Voilà ce que la voie directe ne donnerait jamais en trois lignes.** Sur la Bernoulli, la
> f.c. était un luxe ; ici elle produit *tous* les moments d'un coup, et affiche en clair la
> vitesse de normalisation : $\gamma_1=1/\sqrt\lambda\to0$, donc une Poisson de grand $\lambda$
> ressemble à une gaussienne — c'est la lecture par les cumulants annoncée au § 6.4.

---

## 6c.4 La Poisson comme limite de la binomiale

> **Théorème (loi des événements rares).** Si $X_n\sim\mathcal B(n,p_n)$ avec $np_n\to\lambda$
> quand $n\to\infty$, alors $X_n\xrightarrow{\mathcal L}\mathcal P(\lambda)$.

**Démonstration** — trois lignes, et elle est **entièrement** un exercice du module 6. Avec
$p_n=\lambda/n$ :

$$\varphi_{X_n}(t)=\left(1+p_n\left(e^{it}-1\right)\right)^{n}
\qquad\Longrightarrow\qquad
\log\varphi_{X_n}(t)=n\log\!\left(1+\frac{\lambda\left(e^{it}-1\right)}{n}\right)$$

Comme $\log(1+u)=u+O(u^2)$ pour $u\to0$ et que $u=\lambda(e^{it}-1)/n\to 0$ à $t$ fixé :

$$\log\varphi_{X_n}(t)\;\xrightarrow[n\to\infty]{}\;\lambda\left(e^{it}-1\right)
\qquad\Longrightarrow\qquad
\varphi_{X_n}(t)\to e^{\lambda(e^{it}-1)}$$

La limite est continue en 0 ; le **théorème de Lévy** ([§ 6.3](06-fonction-caracteristique.md))
conclut : $X_n$ converge en loi vers $\mathcal P(\lambda)$. $\blacksquare$

**Les moments se rejoignent, et c'est visible.** $E=np_n\to\lambda$ ;
$\operatorname{Var}=np_n(1-p_n)\to\lambda$ puisque $p_n\to0$. L'égalité moyenne = variance de la
Poisson n'est rien d'autre que « $q\to1$ » dans $npq$.

> 🔑 **Même mécanisme que le TCL, en plus court.** Écrire $\varphi$, prendre le log, développer,
> reconnaître, appliquer Lévy. Le [module 12](12-theoreme-central-limite.md) fera exactement ces
> cinq gestes — avec un développement à l'ordre 2 au lieu de l'ordre 1. **Cette démonstration est
> la meilleure répétition possible avant le TCL.**

> 📐 **Cette limite est chiffrée, contrairement au TCL.** L'inégalité de Le Cam borne l'écart
> entre $\mathcal B(n,p)$ et $\mathcal P(np)$ par $np^2$, et le
> [§ 11bis.6](11bis-convergence-en-loi.md) situe cette convergence face à l'autre — celle vers la
> normale — en disant laquelle des deux utiliser selon le régime.

### Les autres propriétés

| Propriété | Énoncé | Démonstration |
|---|---|---|
| **Additivité** ⭐ | $\mathcal P(\lambda_1)+\mathcal P(\lambda_2)=\mathcal P(\lambda_1+\lambda_2)$ (indépendantes) | $e^{\lambda_1(e^{it}-1)}e^{\lambda_2(e^{it}-1)}$ |
| **Sans contrainte de support** | La somme reste une Poisson, quel que soit $\lambda$ | À comparer au « même $p$ » de la binomiale |
| **Lien exponentiel** ⭐ | Comptage Poisson $\Longleftrightarrow$ attentes exponentielles | [§ 6e.4](06e-loi-exponentielle.md) |
| **Amincissement** | Garder chaque événement avec proba $\pi$ donne $\mathcal P(\pi\lambda)$ | Exercice E6c.4 |

---

## 6c.5 Exemple complet — compter les séances extrêmes, et réfuter le modèle

**Les données.** Sur 5 ans (1 260 séances), une action a connu **21 séances** de variation
absolue supérieure à 4 %, réparties ainsi :

| Année | 1 | 2 | 3 | 4 | 5 | Total |
|---|---|---|---|---|---|---|
| Nombre de séances $\ge4\,\%$ | 1 | 2 | **12** | 3 | 3 | 21 |

**① Le modèle et son estimation.** On pose $N_{\text{année}}\sim\mathcal P(\lambda)$. Comme
$E(N)=\lambda$, l'estimateur naturel est la moyenne :

$$\hat\lambda=\frac{21}{5}=4{,}2\ \text{séances extrêmes par an}$$

Sa précision découle de $\operatorname{Var}(N)=\lambda$ et du [§ 3.3](03-variance-et-moments.md) :

$$\operatorname{se}(\hat\lambda)=\sqrt{\frac{\lambda}{5}}\approx\sqrt{\frac{4{,}2}{5}}=0{,}92
\qquad\Longrightarrow\qquad
\text{IC}_{95\%}=4{,}2\pm1{,}96\times0{,}92=[\,2{,}40\;;\;6{,}00\,]$$

**② Ce que le modèle prédit.** Deux probabilités que le risk manager demandera :

$$P(N=0)=e^{-4{,}2}=0{,}015
\qquad\text{— une année sans aucune secousse : 1 chance sur 67}$$

$$P(N\ge8)=1-\sum_{k=0}^{7}e^{-4{,}2}\frac{4{,}2^k}{k!}=1-0{,}9361=0{,}064
\qquad\text{— 8 secousses ou plus : 1 année sur 16}$$

**③ Le contrôle qui change tout.** Avant d'utiliser ces chiffres, on teste la signature de la
Poisson. Moyenne et variance empiriques des cinq comptages :

$$\bar N=4{,}2,\qquad S^2=\frac{1}{4}\sum_{i=1}^{5}(N_i-\bar N)^2=19{,}7
\qquad\Longrightarrow\qquad
\text{indice de dispersion}=\frac{S^2}{\bar N}=\frac{19{,}7}{4{,}2}=4{,}7$$

Sous $\mathcal P(\lambda)$, cet indice devrait valoir **1**. Il vaut 4,7. La statistique de
dispersion $(n-1)S^2/\bar N=18{,}8$ se compare à une $\chi^2(4)$
([module 15](15-loi-du-chi2.md)), dont le quantile à 95 % est 9,49 :

$$18{,}8>9{,}49\qquad\Longrightarrow\qquad p\text{-valeur}\approx0{,}0009$$

> ⚠️ **Le modèle est rejeté, et l'année 3 explique pourquoi.** 12 séances extrêmes sur une année
> dont le taux moyen est 4,2 : les secousses ne se répartissent pas au hasard dans le temps,
> **elles se regroupent**. C'est le *clustering* de volatilité, le fait stylisé le mieux établi
> des marchés financiers — et il viole frontalement l'hypothèse d'indépendance du § 6c.1.

**④ Ce que le rejet coûte.** Si l'on avait utilisé le modèle sans le tester, on aurait annoncé
$P(N\ge8)=6{,}4\,\%$. Avec une variance réelle 4,7 fois plus grande, la vraie probabilité est
bien supérieure : **le modèle de Poisson sous-estime le risque d'année catastrophique**, et il le
sous-estime précisément dans le scénario qui intéresse le gérant.

**⑤ Ce qu'il faut faire à la place.** Une loi de comptage **surdispersée** (binomiale négative,
ou Poisson à intensité $\lambda$ aléatoire), qui découple moyenne et variance. La logique de
l'échec est celle du [module 14](14-dependance-et-echec-du-tcl.md) : ce n'est pas la forme de la
loi qui est en cause, c'est **la dépendance**.

> 🔑 **La leçon de l'exemple.** La propriété $E=\operatorname{Var}=\lambda$ n'est pas une
> curiosité de cours : c'est **le seul endroit du chapitre où un modèle se réfute en deux
> calculs**. Un modèle qui interdit quelque chose est un modèle qu'on peut prendre en défaut —
> et c'est ce qui en fait un bon modèle.

---

## 6c.6 Simulation

### S6c.1 — Les moments, la limite binomiale, et la surdispersion

```python
import numpy as np

rng = np.random.default_rng(6)
lam, N = 4.2, 500_000
X = rng.poisson(lam, N)

print(f"E(X)   = {X.mean():.4f}   Var(X) = {X.var():.4f}   theorie lambda = {lam}")
print(f"gamma1 = {((X - X.mean())**3).mean() / X.std()**3:.4f}   theorie 1/sqrt(lambda)"
      f" = {1/np.sqrt(lam):.4f}")

# la fonction caracteristique
for t in (0.3, 1.0):
    emp, the = np.mean(np.exp(1j*t*X)), np.exp(lam*(np.exp(1j*t) - 1))
    print(f"t={t}: phi empirique = {emp:+.4f}   theorie = {the:+.4f}")

# la limite du § 6c.4 : B(n, lambda/n) -> P(lambda)
fmt = lambda ech: "  ".join(f"{(ech == k).mean():.4f}" for k in range(5))
print("\nB(n, lambda/n) contre P(lambda), P(X=k) pour k=0..4 :")
for n in (20, 200, 5000):
    print(f"  n={n:5d} : {fmt(rng.binomial(n, lam/n, 200_000))}")
print(f"  Poisson : {fmt(rng.poisson(lam, 200_000))}")

# la surdispersion du § 6c.5 : un lambda qui change d'annee en annee
lam_alea = rng.gamma(shape=4.2/3.7, scale=3.7, size=N)   # E = 4.2 ; indice attendu 1+3.7 = 4.7
Y = rng.poisson(lam_alea)
print(f"\nintensite aleatoire : E(Y) = {Y.mean():.2f}   Var(Y) = {Y.var():.2f}"
      f"   indice = {Y.var()/Y.mean():.2f}")
```

La troisième partie montre la convergence du § 6c.4 se faire sous les yeux ; la quatrième
reproduit la surdispersion observée sur les données réelles : **une intensité qui varie suffit à
détruire $E=\operatorname{Var}$**, sans rien changer à la moyenne.

---

## 6c.7 Exercices

**E6c.1.** Refaire les calculs du § 6c.2 pour $E\bigl(X(X-1)(X-2)\bigr)$. *En déduire $E(X^3)$
puis $\kappa_3$, et vérifier $\kappa_3=\lambda$.*

**E6c.2.** Démontrer
l'additivité$\mathcal P(\lambda_1)+\mathcal P(\lambda_2) =\mathcal P(\lambda_1+\lambda_2)$ par les
fonctions caractéristiques. *Pourquoi cette stabilité
est-elle « plus facile » que celle de la binomiale, qui exigeait le même $p$ ?*

**E6c.3.** Une $\mathcal P(\lambda)$ standardisée est $Z_\lambda=(X-\lambda)/\sqrt\lambda$.
Calculer $\varphi_{Z_\lambda}(t)$ et montrer qu'elle tend vers $e^{-t^2/2}$ quand
$\lambda\to\infty$. *(Piste
:$\log\varphi_{Z_\lambda}(t)=\lambda(e^{it/\sqrt\lambda}-1) -it\sqrt\lambda$, à développer à l'ordre
2.) Quel théorème vient-on de démontrer ?*

**E6c.4.** Chaque séance extrême est signalée par une alerte automatique, mais l'alerte ne part
qu'avec probabilité $\pi=0{,}8$. *Montrer que le nombre d'alertes suit $\mathcal P(\pi\lambda)$.
(Piste : conditionner sur $N$ et calculer $E(e^{itA}\mid N=n)$ avec la f.c. binomiale du
§ 6b.3.)*

**E6c.5.** Sur les données du § 6c.5, calculer $P(N\ge12)$ sous le modèle de Poisson ajusté. *Le
comparer au fait que l'année 3 a bien eu lieu. Combien d'années faudrait-il observer pour voir un
tel comptage une fois, si le modèle était vrai ?*

---

## 6c.8 À retenir

- **$E(X)=\operatorname{Var}(X)=\lambda$** — signature unique, et **test de validité gratuit** :
  l'indice de dispersion $S^2/\bar N$ doit valoir 1.
- **$\varphi_X(t)=e^{\lambda(e^{it}-1)}$**, donc $K_X(t)=\lambda(e^{it}-1)$ et **tous les
  cumulants valent $\lambda$** : moyenne, variance, $\gamma_1=1/\sqrt\lambda$, excès de kurtosis
  $1/\lambda$, d'un seul calcul.
- ⭐ **$\mathcal B(n,\lambda/n)\to\mathcal P(\lambda)$**, démontré en trois lignes avec (P2), un
  développement de $\log(1+u)$ et Lévy — la répétition générale du TCL.
- **Additivité sans condition**
  :$\mathcal P(\lambda_1)+\mathcal P(\lambda_2) =\mathcal P(\lambda_1+\lambda_2)$, là où la binomiale
  imposait un$p$ commun.
- ⚠️ **Sur des données financières, la Poisson est presque toujours rejetée** — non par la forme
  de la loi, mais par le regroupement temporel des événements
  ([module 14](14-dependance-et-echec-du-tcl.md)).

---

⬅️ [Module 6b — La loi binomiale](06b-loi-binomiale.md) ·
➡️ [Module 6d — La loi uniforme](06d-loi-uniforme.md) ·
🏠 [Sommaire](README.md)
