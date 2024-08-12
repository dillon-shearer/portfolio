# Load necessary libraries
library(dplyr)
library(ggplot2)

# Download the dataset
url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
heart_data <- read.csv(url, header = FALSE)

# Assign column names based on the dataset description
colnames(heart_data) <- c("age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                          "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num")

# Replace missing values (denoted by '?') with NA
heart_data[heart_data == "?"] <- NA

# Convert relevant columns to numeric
heart_data <- heart_data %>%
  mutate(across(c(ca, thal), as.numeric))

# Drop rows with missing values
heart_data <- na.omit(heart_data)

# Summary of the cleaned dataset
summary(heart_data)

# Create the directory if it doesn't exist
if (!dir.exists("heart_Disease_Analysis/data")) {
  dir.create("data")
}

# Save the cleaned dataset to a CSV file
write.csv(heart_data, "heart_Disease_Analysis/data/heart_disease_cleaned.csv", row.names = FALSE)