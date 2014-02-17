
data(mtcars)

# Add two dummy columns full of noise
mtcars <- cbind(runif(nrow(mtcars)), runif(nrow(mtcars)), mtcars)
colnames(mtcars)[1:2] <- c("dummy1", "dummy2")

# Creating a training set

 target <- as.matrix(mtcars$mpg)
features <- as.matrix(subset(mtcars, select=-c(mpg)))

library(glmnet)
reg.l2 <- glmnet(features, target, alpha=0)
reg.l1 <- glmnet(features, target, alpha=1)
models <- data.frame(t(rbind(matrix(reg.l2$lambda, nrow=1), as.matrix(reg.l2$beta))))
colnames(models)[1] <- "lambda"
models <- melt(models, c("lambda"))
ggplot(m) + aes(x=log(lambda), y=value, color=variable) + geom_line()

# Cross validation resampling the training data for L2 regression and L1 regression
cv.l2 <- cv.glmnet(features, target, alpha=0)
cv.l1 <- cv.glmnet(features, target, alpha=1) plot(reglm.l1, main = "L1 n-fold cross validation error")
plot(reglm.l2, main = "L2 n-fold cross validation error") 

