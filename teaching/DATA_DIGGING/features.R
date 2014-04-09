library(rpart)
library(rattle)
library(rpart.plot)
full <- read.csv("pos.csv")

inspect <- function(model, validation) {
  result <- list()
  result$predictions <- predict(model, validation, type="class")
  result$confusion <- table(validation$tag, result$predictions)
  
  errors <- validation[validation$tag != result$predictions,]$word
  result$errors <- sort(table(errors), decreasing=TRUE)[1:50]
  
  result$acc <- sum(diag(result$confusion)) / sum(result$confusion)
  #result$plot <- fancyRpartPlot(model)
  
  return(result)
}

# Add a feature for how often the word appears
word_count <- table(full$word)
full$count <- word_count[full$word]
full$filter_word <- full$word
full[full$count < 500,]$filter_word <- NA

# Add a feature for whether 

small_train <- full[1:40000,]
train <- full[1:400000,]
dev <- full[400000:440000,]
test <- full[440000:496703,]

model_count <- rpart(tag ~ count, small_train)
model_prefix <- rpart(tag ~ pre + suf, small_train)
model_cap <- rpart(tag ~ cap, small_train)
model_dict <- rpart(tag ~ adj_count + adv_count + v_count + n_count, small_train)
model_comb <- rpart(tag ~ cap + pre + suf + adj_count + adv_count + v_count + n_count, small_train)

res_count <- inspect(model_count, dev)
res_prefix <- inspect(model_prefix, dev)
res_cap <- rpart(model_cap, dev)
res_dict <- inspect(model_dict, dev)
res_comb <- inspect(model_comb, dev)