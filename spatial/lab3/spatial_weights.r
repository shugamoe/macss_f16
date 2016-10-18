
library(spdep)

nb1 <- read.gal("natregimes_q.gal")

nb1 <- read.gal("natregimes_q.gal",override.id=TRUE)

nb1

summary(nb1)

class(nb1)

length(nb1)

str(nb1)

nb1[[1]]

nb1$region.id

w1att <- attr(nb1,"region.id")
head(w1att)

w1att[1]
w1att[c(23,31,41)]

attr(nb1,"sym")

is.symmetric.nb(nb1)

library(foreign)
dat2 <- read.dbf("clev_sls_154_core.dbf")
summary(dat2)

nb2 <- read.gwt2nb("clev_sls_154_core_d.gwt",region.id=dat2$unique_id)
nb2

attach(dat2)
nb3 <- read.gwt2nb("clev_sls_154_core_d.gwt",region.id=unique_id)
summary(nb3)

n1 <- nb3[[1]]
n1

w3att <- attr(nb3,"region.id")
head(w3att)

w3att[1]
w3att[n1]

d <- attr(nb3,"GeoDa")$dist[1]
d

coordn <- cbind(x,y)
plot(nb3,coordn,lwd=0.2,col="blue")

nb4 <- read.gwt2nb("clev_sls_154_core_d1500.gwt",region.id=unique_id)
summary(nb4)

plot(nb4,coordn,lwd=0.2,col="blue")

nb5 <- read.gal("clev_sls_154_core_q.gal",region.id=unique_id)
summary(nb5)

plot(nb5,coordn,lwd=0.2,col="blue")

w4 <- nb2listw(nb4)
summary(w4)

w4a <- nb2listw(nb4,zero.policy=TRUE)
summary(w4a,zero.policy=TRUE)

w5 <- nb2listw(nb5)
summary(w5)

w5$weights[1]

w5[[3]][1]

w5a <- nb2listw(nb5,style="B")
summary(w5a)

w5a$weights[1]

plot(w5,coordn)

nd3 <- attr(nb3,"GeoDa")$dist
length(nd3)

nd3[1]

invd3 <- lapply(nd3,function(x) (1/x))

length(invd3)

invd3[1]

invd3a <- lapply(nd3,function(x) (1/(x/100)))
invd3a[1]

w6 <- nb2listw(nb3,glist=invd3a,style="B")

summary(w6)

w6$weights[1]


