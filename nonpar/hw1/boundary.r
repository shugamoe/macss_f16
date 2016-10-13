library(locfit)
n = 150
X = rnorm(n,sd=.75); X = sort(X)

Y = 2*(abs(X)^3) + rnorm(length(X))
grid = seq(-3, 3, .01)
m = 2*(abs(grid)^3)
plot(X, Y)
lines(grid, m, 'l')
out0 = locfit(Y ~ lp(X, h=.7, deg=0))
out1 = locfit(Y ~ lp(X, h=.7, deg=1))
lines(X, fitted(out1), 'l', col='blue',lwd=2)
lines(X, fitted(out0), 'l', col='red',lwd=2)

#while(1) { source("boundary.r"); Sys.sleep(1)}
