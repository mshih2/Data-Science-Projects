rm(list=ls())
if(!is.null(dev.list())) dev.off()

library('forecast')
library('ggplot2')
library('gridExtra')
library('Metrics')

setwd('/Users/meichengshih/Dropbox/Data Science Note/GrubHub')

set.seed(0)

# This is the minimum of multiplied of 7 greater than 30
frequency<-35

## Step 1, read and combine data
train<-read.csv('train.csv', sep=',')
test<-read.csv('test.csv', sep=',')

test['order_count']<-NA

all<-rbind(train,test)

# change data type of column 'date' and order the data by it
all$date<-as.Date(all$date)
all<-all[order(all$date),]

# box-cox transformation to equalize variances
opt_lambda<-BoxCox.lambda(all$order_count)

## Step 2, detect outliers and replace them
# determine time series data, frequency = 7 based on the assumption that the pattern varies in a week
all$order_count<-ts(all$order_count,  start=c(2016,1,1), frequency=frequency)

# clean the outliers and obtained values 'order_count_clean'
all['order_count_clean']<-tsclean(all$order_count, replace.missing = FALSE, lambda = opt_lambda)

# visdualize and compare the two
p1<-ggplot(all, aes(date, order_count))+geom_line()+scale_x_date('Date')+ylab("Order Count")
p2<-ggplot(all, aes(date, order_count_clean))+geom_line()+scale_x_date('Date')+ylab("Order Count")
grid.arrange(p1, p2, nrow = 1)

## Step 2.1 Did little analysis to event (even though they are not going to be used)
outlier_loc<-which(all$order_count!=all$order_count_clean)
# print out event corresponding to outliers detected
all$event[outlier_loc]

## Cross validation (approximation)
# Originally, each step of rolling forecasting origin needed to be executed
# However, to save time, randomly sample 100 points in 702 days for the purpose of validation
# So for each point, data from first to the location of point will be used to train the model
# and the model will be used to forecast location+1~+30 point
cross_sarima<-function(mini=70, num_sample=100, h=1, p,d,q,P,D,Q){
  # find the list for sample
  k<-which(is.na(all$order_count_clean)==FALSE)
  k<-k[k>=mini]
  
  # sample some data points
  pt<-sample(k,num_sample)
  
  # create lists to store prediction and validation values
  pred<-list()
  true<-list()
  
  # loop over the samepled data to obtain approximate cross validation performance
  for (i in 1:num_sample){
    train_k<-all[1:pt[i],]
    fit<-Arima(ts(train_k$order_count_clean,  start=c(2016,1,1), frequency=frequency),lambda=opt_lambda, order = c(p, d, q), seasonal = c(P, D, Q))
    pred<-append(pred, unlist(as.integer(round(forecast(fit, lambda=opt_lambda, h=h, biasadj=TRUE)$mean,0))))
    true<-append(true, unlist(all$order_count[(pt[i]+1):(pt[i]+h)]))
  }

  pred<-unlist(pred)
  true<-unlist(true)
  
  # delet location with nan true value
  val_loc<-!(is.na(true))
  pred<-pred[val_loc]
  true<-true[val_loc]
  
  return (rmse(pred,true))}

## Step 3, use auto.arima and difference period of data to identify 3 sarmia models
auto.list<-list(c(1,366), c(367,731), c(1,732))
rmses<-rep(0,length(auto.list))
k<-list(0)
k<-rep(k,length(auto.list))

# Step 4, for each period, use auto.arima to find a model
for (i in 1:length(auto.list)){
  train_k<-all[auto.list[[i]][1]:auto.list[[i]][2],]
  fit<-auto.arima(ts(train_k$order_count_clean,  start=c(2016,1,1), frequency=frequency))
  par<-arimaorder(fit)
  k[[i]]<-par
  rmses[i]<-cross_sarima(mini=70, num_sample=100, h=30, p=par[1],d=par[2],q=par[3],P=par[4],D=par[5],Q=par[6])
}

### Step 4.1, find the best one based on recorded rmses
best_par<-k[[which(rmses==min(rmses))]]

### Step 5, make predictions based on the model selected
# Step 5.1, for the missing values part
fit<-Arima(ts(train_k$order_count_clean[1: min(which(is.na(train_k$order_count_clean)))-1],  start=c(2016,1,1), frequency=frequency),lambda=opt_lambda, order = c(p=best_par[1], d=best_par[2], q=best_par[3]), seasonal = c(P=best_par[4], D=best_par[5], Q=best_par[6]))
pred_test<-round(as.numeric(forecast(fit, lambda=opt_lambda, h=30, biasadj=TRUE)$mean),0)
plot(forecast(fit, lambda=opt_lambda, h=30, biasadj=TRUE))

# Step 5.2, for the future forecast (after 01/01/2018)
fit2<-Arima(ts(train_k$order_count_clean,  start=c(2016,1,1), frequency=frequency),lambda=opt_lambda, order = c(p=best_par[1], d=best_par[2], q=best_par[3]), seasonal = c(P=best_par[4], D=best_par[5], Q=best_par[6]))
pred2<-round(as.numeric(forecast(fit, lambda=opt_lambda, h=30, biasadj=TRUE)$mean),0)
plot(forecast(fit2, lambda=opt_lambda, biasadj=TRUE))

# Step 6, plot ACF, PACF, residuals to check if the selected model is reasonable
Acf(fit$residuals)
Pacf(fit$residuals)
plot(fit$residuals)

Acf(fit2$residuals)
Pacf(fit2$residuals)
plot(fit2$residuals)

# write predicted output to test and output it as test_output.csv
test$order_count<-pred_test
test<-test[!(names(test)%in% c('event'))]
write.csv(test, 'test_output.csv', row.names=FALSE)

