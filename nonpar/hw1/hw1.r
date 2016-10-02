# density plot to illustrate the bias-variance tradeoff

density.movie = function(n=500, h=.1) {
  x = seq(-3, 3, .01)
  f = dnorm(x)
  while(1) {
    plot(x,f,'l',col='red', ylim=c(0,.5))
    X = rnorm(n)
    lines(density(X, bw=h))
    rug(X,quiet=T)
    Sys.sleep(.2)
  }
}

