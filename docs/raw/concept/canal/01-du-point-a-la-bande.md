# Module 1 — Du point à la bande

**Prérequis :** [étape 7](../modele/07-droite-ajustee.md) — la droite ajustée $f(t)$.
**Ce qu'on établit ici :** la définition d'un canal, la propriété de pivot, et ce que le canal ajoute à la seule droite.

---

## 1.1 — Ce que la droite ne dit pas

L'étape 7 livre une droite : $f(t) = E(V) + \phi(V)(2t-n-1)$. Elle résume la
série par deux nombres, un niveau et une pente. C'est peu, et volontairement :
tout le reste a été rejeté dans les résidus $\hat e_i = V_i - f(i)$, dont
l'[étape 4](../modele/04-forme-canonique.md) ne retient que le moment d'ordre 2,
$\operatorname{Var}(\hat e)_{\min}$.

Or c'est ce reste qui porte l'information utile en pratique. Deux séries peuvent
partager exactement la même droite ajustée et n'avoir rien à voir :

| | Série A | Série B |
|---|---|---|
| Pente | $+0{,}15$ €/séance | $+0{,}15$ €/séance |
| $\operatorname{Var}(\hat e)_{\min}$ | $0{,}04$ | $4{,}00$ |
| Écart typique à la droite | $0{,}20$ € | $2{,}00$ € |
| Un écart observé de $1{,}50$ € | **considérable** ($7{,}5\,\sigma$) | banal ($0{,}75\,\sigma$) |

Sans échelle de dispersion, « le cours est au-dessus de sa tendance » ne veut
rien dire. Le canal est cette échelle, tracée.

## 1.2 — Définition

> **Définition.** Un **canal de régression** de demi-largeurs $(a, b)$ est la
> bande du plan comprise entre les deux courbes
> $$\text{support}(t) = f(t) - a(t) \qquad\text{et}\qquad \text{résistance}(t) = f(t) + b(t),$$
> où $f$ est la droite ajustée des moindres carrés sur la fenêtre considérée.

Deux remarques, qui contiennent tout le cours :

1. **$a$ et $b$ sont des fonctions de $t$**, pas nécessairement des constantes.
   Quand elles le sont, les bords sont parallèles à la droite ; c'est le cas le
   plus courant mais pas le seul, ni toujours le bon ([module 3](03-epaisseur-variable-et-levier.md)).
2. **Rien dans la définition ne dit comment choisir $a$ et $b$.** C'est le sujet
   du [module 2](02-les-trois-largeurs.md), et c'est là que se joue le sens de
   l'objet : selon la convention retenue, le même dessin affirme des choses
   entièrement différentes.

## 1.3 — Le canal pivote au point moyen

L'[étape 1](../modele/01-elimination-de-l-ordonnee.md) établit
$v_{0,\min} = E(V) - r_{\min}E(T)$, autrement dit :

$$\boxed{\;f\bigl(E(T)\bigr) = E(V)\;}$$

**La droite ajustée passe toujours par le centre de gravité du nuage.** Pour
$T_i = i$, ce point est $\bigl(\tfrac{n+1}{2},\, E(V)\bigr)$ — le milieu exact de
la fenêtre.

Conséquence directe, et c'est la propriété la plus utile du module : **quand
l'estimation de la pente change, le canal tourne autour de ce point** ; il ne se
translate pas. Si un canal à bords parallèles est tracé sur une fenêtre et que la
pente est révisée de $\Delta r$, le bord se déplace de

$$\Delta f(t) = \Delta r \cdot \bigl(t - E(T)\bigr),$$

c'est-à-dire **de rien au milieu, et du maximum aux deux extrémités**. À $n=20$,
une révision de pente de $0{,}01$ €/séance ne bouge pas le canal à la 10ᵉ séance
et le déplace de $0{,}095$ € à la 20ᵉ.

C'est déjà l'annonce du [module 3](03-epaisseur-variable-et-levier.md) : les
extrémités d'un canal sont sa partie molle, et la séance courante est justement
une extrémité.

## 1.4 — Les résidus ne sont pas libres

Le canal se construit sur les $\hat e_i$, il faut donc savoir ce qu'ils sont. Ce
ne sont **pas** $n$ nombres quelconques : les deux conditions d'optimalité les
contraignent.

$$\sum_i \hat e_i = 0 \qquad\text{([étape 1](../modele/01-elimination-de-l-ordonnee.md))}$$
$$\sum_i \hat e_i\,T_i = 0 \qquad\text{([étape 4](../modele/04-forme-canonique.md), annulation de la dérivée en } r)$$

La seconde s'obtient en écrivant que $r_{\min}$ annule
$\varphi'(r) = -2\operatorname{Cov}(V,T) + 2r\operatorname{Var}(T)$ : au minimum,
la covariance entre résidus et instants est nulle.

Les résidus vivent donc dans un sous-espace de **dimension $n-2$**, orthogonal à
$\mathbf 1$ et à $T$. Trois conséquences pratiques :

- On divise par $n-2$, et non par $n$, pour estimer sans biais la variance du
  bruit — d'où le $s^2$ du [README](README.md#notations).
- Les résidus sont **corrélés entre eux**, même si les erreurs sous-jacentes ne
  le sont pas. Compter les sorties de canal comme des événements indépendants est
  donc une approximation, dont le [module 4](04-sorties-de-canal.md) mesure la
  portée.
- Leurs variances **diffèrent d'un point à l'autre** : c'est l'objet du
  [module 3](03-epaisseur-variable-et-levier.md).

## 1.5 — Ce que le canal ajoute à `VAL_n`

Le script du dépôt calcule `VAL_n` $= f(n)$ : la droite ajustée évaluée à la
séance courante. C'est **un point**, le centre du canal à son bord droit.

Le canal ajoute à ce point l'échelle qui permet de le lire. Comparer `Close` à
`VAL_20` répond à « le cours est-il au-dessus ou en dessous de sa tendance
courte ? » ; comparer $(\texttt{Close} - \texttt{VAL\_20})$ à la demi-largeur du
canal répond à « **de beaucoup ?** » — et c'est la seule des deux questions dont
la réponse soit exploitable.

---

⬅️ [README du cours](README.md) ·
➡️ [Module 2 — Les trois largeurs](02-les-trois-largeurs.md)
