generator1 = function(n=150,d=50,sigma2=1){
 epsilon = rnorm(n,0,sigma2)
 M = matrix(NA,nrow=n,ncol=d)
 x = matrix(runif(d*n,-2.5,2.5),nrow=n,ncol=d)
 for(p in c(1:d)){
   if(p==1){ M[,p] = -sin(2*x[,p])}
   if(p==2){ M[,p] = x[,p]^2 - mean(x[,p]^2)}
   if(p==3){ M[,p] = x[,p]}
   if(p==4){ M[,p] = exp(-x[,p])- mean(exp(-x[,p]))}
   if(p>4 ){ M[,p] = 0}
 }
 for(p in c(1:d)){
    x[,p] = (x[,p]-min(x[,p]))/(max(x[,p])-min(x[,p]))
 }
 M[,1:4]  = scale(M[,1:4])        # rescale the design matrix
 m        = apply(M[,c(1:d)],1,sum)     # mean function
 y        = m +  epsilon
 return(list(y=y,x=x,M=M))
}

kernel.smoothing.matrix = function(h, x) {
  n = length(x)
  S = matrix(0,n,n)
  for (i in 1:n) {
    tmp1  = x - x[i]
    w     = exp(-(tmp1)^2/(2*h^2))
    w     = w/sum(w)
    S[i,] = w
  }
  return(S)
}

local.linear.smoothing.matrix = function(h, x) {
  n = length(x)
  S = matrix(0,n,n)
  
  for (i in 1:n) {
    xdiff = x - x[i]
    w     = exp(-(xdiff)^2/(2*h^2))
    W     = diag(w/sum(w))
    X     = cbind(1,matrix(xdiff,n,1,byrow=TRUE))
    T     = solve(t(X) %*% W %*% X) %*% t(X) %*% W
    S[i,] = T[1,]
  }
  return(S)
}


plotM = function(y,x,Mhat,M){
  d   = ncol(M)
  res = y - apply(Mhat,1,sum)
  par(mfrow=c(1,4))
  for(i in c(1:min(d,10))){
    par(cex=1.0,cex.sub=1.0,cex.lab=1.0)
      ord   = order(x[,i])
      Mhat[,i]= Mhat[,i]- mean(Mhat[,i])
      M[,i] = M[,i]- mean(M[,i])
      l = sum(abs(Mhat[,i]))
      plot(x[,i][ord], Mhat[,i][ord],ylim=c(min(y),max(y)),
           type='l',lwd=2,xlab=paste('x',i,sep=''),
           ylab=paste('m',i,sep=''),col='blue')
      points(x[,i][ord],y[ord]-apply(as.matrix(Mhat[ord,-i]),1,sum),pch=16, cex=.6, col=rgb(0.7,0.7,0.9))
      lines(M[,i][ord]~x[,i][ord],lty=2,lwd=2,col=2)
  }
}

backfit = function(x,y,h,maxStep = 100){
  d  = ncol(x)
  n  = length(y)
  Mhat = matrix(0,n,d)
  alpha = rep(1,d)
  S  = matrix(0,d,n*n)

  cat("constructing smoothing matrices...\n")
  for (i in 1:d) {
    W = kernel.smoothing.matrix(h[i],x[,i])
    #W = local.linear.smoothing.matrix(h[i],x[,i])
    S[i,] = as.vector(W)
  }
  
  order = sample(d,d)  # visit the variables in a random order
  cat("Variable order: ", order[1:min(length(order),8)], "...\n")

  for (iter in c(1:maxStep)){
    curfit    = apply(Mhat %*% diag(alpha), 1, sum)
    
    for(i in order) {
      Z = y - Mhat[,-i] %*% alpha[-i]
      Si = matrix(S[i,],n,n)
      f = as.vector(Si %*% Z)
      norm = sqrt(t(f) %*% f / n)
      Mhat[,i] = f / norm
      Mhat[,i] = Mhat[,i] - mean(Mhat[,i])
      alpha[i] = 1
    }
    newfit    = apply(Mhat %*% diag(alpha),1,sum)
    tmp       = sqrt(sum((curfit-newfit)^2))
    if(tmp<1e-6){ break }
    cat(sprintf("Iteration %d: l2-distance=%f\n", iter, tmp))
    if(iter==maxStep){cat('maximum steps reached!','\n')}
  }
  
  return(list(M=(Mhat %*% diag(alpha)), beta=alpha))
}


example1 = function(n=150,d=50,sigma2=1,h0=.1) {
  out = generator1(n,d,sigma2)
  y = out$y
  x = out$x
  M = out$M
  n = length(y)
  d = ncol(x)

  h = rep(1,d)
  if (h0 != 0) { h = rep(h0,d) }
  else {h =rep(.8*h/(n^0.2),d)}  # the plug-in bandwidths
  cat("bandwidth: ",h[1],"\n")

  tmp = backfit(x,y,h,maxStep=100)
  Mhat = tmp$M
  plotM(y,x,Mhat,M)
}

example1(n=150,d=4,sigma2=.5,h0=.1)

