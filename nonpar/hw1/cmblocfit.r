library(locfit)
# to install this, do install.packages("locfit")

wmap = read.table("wmap.dat", header=T)
x = seq(1,700,length=512)
# some normalization of the data
lo = floor(x)
hi = ceiling(x)
y = (x-lo)*wmap$Cl[hi] + (hi-x)*wmap$Cl[lo] + wmap$Cl[lo]*(lo==hi)

out = locfit(y ~ x, alpha=c(0,20), deg=1);
plot(x, y, pch=16,cex=0.8,col=rgb(0.7,0.7,0.9));
lines(x, fitted(out), 'l', col='blue', lwd=3); 

show.smooth = function(x, y, h, degree=0) {
   out = locfit(y ~ x, alpha=c(0,h), deg=degree);
   plot(x, y, pch=16,cex=0.8,col=rgb(0.7,0.7,0.9));
   lines(x, fitted(out), 'l', col='blue', lwd=3);
}

# the diagonal L_ii is gotten from this call to locfit:
# Lii = predict(out, where="data", what="infl")


# the norm || ell_i(x) || is gotten from this call:
# normell = predict(out, where="data", what="vari")
