##
## Seaflow assignment

## UW Data Science Series Assignment 5

## Practical Predictive Analytics Assignment 1

library(caret)
library(rpart)
library(tree)
library(randomForest)
library(e1071)
library(ggplot2)

## Step 1: Read and summarize the data

sf<-read.csv("seaflow_21min.csv")
str(sf)
summary(sf)

# Q2 How many particles labeled "synecho" are in the file provided?

nrow(sf[ sf$pop=="synecho", ])
table(sf$pop)


# Q3 What is the 3rd Quantile of the field fsc_small?
summary(sf)


## Step 2: Split the data into test and training sets

# Divide the data into two equal subsets, one for training and one for
# testing. Make sure to divide the data in an unbiased manner.

# You might consider using either the createDataPartition function or
# the sample function, although there are many ways to achieve the goal.

library(caTools)
set.seed(1000)
spl = sample.split(sf$time, SplitRatio = 0.5)
train = subset(sf, spl==TRUE)
test = subset(sf, spl==FALSE)

#Q4 What is the mean of the variable "time" for your training set?
mean(train$time)

## Step 3: Plot the data

# Plot pe against chl_small and color by pop
plot1<-ggplot(data=sf,aes(x=chl_small,y=pe,col=pop))+geom_point()
plot1

# Q5 In the plot of pe vs. chl_small, the particles labeled ultra
# should appear to be somewhat "mixed" with two other populations 
# of particles. Which two populations?

## Step 4: Train a decision tree.

library(rpart)
library(rpart)
library(rpart.plot)

# construct formula object
fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
CARTmodel <- rpart(fol, method="class", data=train)
print(CARTmodel)

# same thing, using AE terminology
CARTmodel = rpart(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small, data=train, method="class")
prp(CARTb)

## Step 5: Evaluate the decision tree on the test data.

#accuracy of CART model on test set
PredictCARTmodel = predict(CARTmodel, newdata = test, type = "class")
ct<-table(test$pop, PredictCARTmodel)
ct
sum(diag(ct))/sum(ct)

sum(PredictCARTmodel==test$pop)/nrow(test)

## Step 6: Build and evaluate a random forest.

# Install randomForest package
#install.packages("randomForest")
library(randomForest)
fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
forestmodel<-randomForest(fol, data=train)

PredictForest = predict(forestmodel, newdata = test)
sum(PredictForest==test$pop)/nrow(test)
importance(forestmodel)

## Step 7: Train a support vector machine model and compare results.

# Use the e1071 library and call model <- svm(fol, data=trainingdata).
library(e1071)
fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
SVMmodel <- svm(fol, data=train)
PredictSVM = predict(SVMmodel, newdata = test)
sum(PredictSVM==test$pop)/nrow(test)

## Step 8: Construct confusion matrices

# CART
table(pred = PredictCARTmodel, true = test$pop)

#randomForest
table(pred = PredictForest, true = test$pop)

# SVM model
table(pred = PredictSVM, true = test$pop)

## Step 8: Sanity check the data
plot(sf$time,sf$fsc_small)
plot(sf$time,sf$fsc_perp)
plot(sf$time,sf$fsc_big)
plot(sf$time,sf$pe)
plot(sf$time,sf$chl_small)
plot(sf$time,sf$chl_big)


## filter out data connected with file_id 208
sfclean<-sf[ sf$file_id!=208, ]
table(sfclean$file_id) # check that all file_id 208 removed

# repeat analysis

library(caTools)
set.seed(1000)
spl = sample.split(sfclean$time, SplitRatio = 0.5)
train = subset(sfclean, spl==TRUE)
test = subset(sfclean, spl==FALSE)

# Decision tree (CART model)
library(rpart)
library(rpart)
library(rpart.plot)

fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
CARTmodel <- rpart(fol, method="class", data=train)
print(CARTmodel)

PredictCARTmodel = predict(CARTmodel, newdata = test, type = "class")
sum(PredictCARTmodel==test$pop)/nrow(test)


# Random Forest model
library(randomForest)
fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
forestmodel<-randomForest(fol, data=train)

PredictForest = predict(forestmodel, newdata = test)
sum(PredictForest==test$pop)/nrow(test)
importance(forestmodel)

# SVM model
library(e1071)
fol<-formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
SVMmodel <- svm(fol, data=train)
PredictSVM = predict(SVMmodel, newdata = test)
sum(PredictSVM==test$pop)/nrow(test)
