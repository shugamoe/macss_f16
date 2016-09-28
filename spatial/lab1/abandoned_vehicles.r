
vehicall <- read.csv("Abandoned_Vehicles_Map.csv")

names(vehicall)

head(vehicall)

vehicall$credate <- as.Date(vehicall$Creation.Date,"%m/%d/%Y")
head(vehicall$credate)

library(lubridate)

vehicall$year <- year(vehicall$credate)
head(vehicall$year)

vehicall$month <- month(vehicall$credate)
head(vehicall$month)

abandon_15_9 <- vehicall[ (vehicall$year == 2015) & (vehicall$month == 9), ]
head(abandon_15_9)
dim(abandon_15_9)

vehvariables <- c("year","month","credate","Ward","Police.District","Community.Area","Latitude","Longitude")

veh2015_9 <- with(abandon_15_9,abandon_15_9[,vehvariables])

head(veh2015_9)
dim(veh2015_9)

write.csv(veh2015_9,"vehicles2015_9.csv",row.names=FALSE)


