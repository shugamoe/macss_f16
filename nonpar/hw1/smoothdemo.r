library("locfit")
# to install this, do install.packages("locfit")

show.smooth = function(x, y, h, degree=1) {
   out = locfit(y ~ x, alpha=c(0,h), deg=degree);
   plot(x, y, pch=16,cex=0.9,col=rgb(0.7,0.7,0.9));
   lines(x, fitted(out), 'l', col='blue', lwd=3);
   lines(x, myfun(x), 'l', col='red', lwd=3);
}

myfun = function(x) {
  y = x + 5*exp(-4*x^2)
}

sigma = .5
x = seq(-2,2,by=.01)
y = myfun(x)+ sigma*rnorm(length(x))
plot(x,myfun(x),'l',col='red', lwd=3);
points(x,y, pch=16,cex=.8,col=rgb(0.7,0.7,0.7))

out = locfit(y ~ x, alpha=c(0,.08), deg=1)
lines(x, fitted(out), 'l', col='blue', lwd=3)


h = seq(.05,.8,.01); 
alphas = cbind(rep(0,length(h)), h)
gcvs = gcvplot(y ~ x, alpha=alphas, deg=1)
plot(h, gcvs$values, type="l")
points(h, gcvs$values)
hstar = h[which(gcvs$values == min(gcvs$values))]

out = locfit(y ~ x, alpha=c(0,hstar), deg=0)

plot(x,y, pch=16,cex=.8,col=rgb(0.7,0.7,0.9))
lines(x,myfun(x),'l',col='red', lwd=3);
lines(x, fitted(out), 'l', col='blue', lwd=3)

# the diagonal L_ii is gotten from this call to locfit:
# Lii = predict(out, where="data", what="infl")


# the norm || ell_i(x) || is gotten from this call:
normell = predict(out, where="data", what="vari")
n = length(x)
lines(x, fitted(out)+sqrt(n)*2*sigma*normell, 'l', col='gray', lwd=1)
lines(x, fitted(out)-sqrt(n)*2*sigma*normell, 'l', col='gray', lwd=1)



