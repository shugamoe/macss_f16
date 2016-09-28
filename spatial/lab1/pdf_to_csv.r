
library(pdftools)
dat <- pdf_text("Census_2010_and_2000_CA_Populations.pdf")

dat

length(dat[[1]])

nnlist <- ""
for (i in 1:2) {
  ppage <- strsplit(dat[[i]],split="\n")
  nni <- ppage[[1]]
  nni <- nni[-(1:4)]
  nnu <- unlist(nni)
  nnlist <- c(nnlist,nnu)
}
length(nnlist)

nnlist <- nnlist[2:(length(nnlist)-1)]
length(nnlist)

nnlist[1:3]

nnpop <- vector(mode="numeric",length=length(nnlist))
nnpop

for (i in (1:length(nnlist))) {
     popchar <- substr(nnlist[i],start=27,stop=39)
     popval <- as.numeric(gsub(",","",popchar))
     nnpop[i] <- popval
}
nnpop

nnid <- (1:length(nnlist))
nnid

neighpop <- data.frame(nnid,nnpop)
neighpop

names(neighpop) <- c("NID","POP2010")
neighpop

write.csv(neighpop,"Community_Pop.csv",row.names=FALSE)


