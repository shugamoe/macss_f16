
library(foreign)
vpoints <- read.dbf("abandoned15_9_pts_1.dbf")
head(vpoints)

pcounts <- table(vpoints$Commu_Area)
pcounts

pcframe <- as.data.frame(pcounts)
head(pcframe)

dim(pcframe)

is.factor(pcframe$Var1)

nnf <- pcframe$Var1
levels(nnf)

nnn <- as.numeric(levels(nnf))
nnn

is.factor(nnn)

narea <- max(vpoints$Commu_Area)
vc <- vector(mode="numeric",length=narea)
vc

length(vc)

vc[nnn] <- pcframe$Freq
vc

nid <- (1:narea)
vcframe <- data.frame(as.integer(nid),as.integer(vc))
vcframe

names(vcframe) <- c("AREAID","Vehicles")

write.csv(vcframe,"vehicle_counts.csv",row.names=FALSE)


