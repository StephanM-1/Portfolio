library(readxl)
library(caTools)
library(randomForest)
library(caret)
library(tidyr)
library(ggplot2)
library(rpart)
library(GGally)

#This data shows factors that affect wine then assigns a score accordingly as a quality feature
#Import the data from excel(Files should be extracted first)
wine <- data.frame(read_excel("Wine.xlsx"))
head(wine)

#Transform the quality into 2 classes
wine$quality<-ifelse(wine$quality>6,'Good','Bad')

#Explore the data
head(wine)
str(wine)
summary(wine)

#The data showed a high imbalance between the good and bad classes which resulted into a bad model and inaccurate predictions
#There was a 0.5 error rate in the prediction of good wine
with(wine, print(table(quality)))
barplot(table(wine$quality))

#Added after analysis!
#I used the up-sampling technique to increase the good observations in the data
good = which(wine$quality == "Good")
bad = which(wine$quality == "Bad")

Good_upsample = sample(good,length(bad)/2,replace = TRUE)
length(Good_upsample)
wine = wine[c(Good_upsample,bad),]
barplot(table(wine$quality))
#!

#Check for missing data
sum(is.na(wine))

#Plot the data
wine%>%
  gather(-quality, key = "var", value = "value") %>% 
  ggplot(aes(x = quality, y = value, color = quality)) +
  geom_boxplot(aes(fill = quality)) +
  facet_wrap(~ var, scales = "free", ncol = 3)+
  theme(legend.position="right")


#Start the classification
set.seed(123)

#Split the data into training and testing
split = sample.split(wine,SplitRatio = 0.8)
train_data = subset(wine,split == TRUE)
test_data = subset(wine,split == FALSE)

#Random forest classification and prediction
rand.forest <- randomForest(as.factor(quality)~. ,data=train_data, importance=TRUE, ntree = 400)
print(rand.forest)

#Check the importance of each feature according to see how high it affects the quality --> the alcohol affects the quality the most
importance(rand.forest)
#Plot the importance
varImpPlot(rand.forest)

#Plot the error and how many trees it takes to stabilize
plot(rand.forest)
#The error stabilizes around 250 trees so we reduce the trees needed for the test from 1000 to 400
Confusion_matrix = rand.forest$confusion
print(Confusion_matrix)

#The prediction model and its accuracy
prediction_model <- predict(rand.forest, test_data)
Pred_Confusion_Matrix <- table(actual = test_data$quality,predicted = prediction_model)
print(Pred_Confusion_Matrix)

accuracy <- sum(diag(Pred_Confusion_Matrix))/sum(Pred_Confusion_Matrix)
paste('The accuracy is',accuracy)

