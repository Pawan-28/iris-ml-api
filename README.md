# Iris Flower Classification API

## Project Overview

This project will build a machine learning REST API that predicts the species of an Iris flower based on its physical measurements. The API will accept four input features: sepal length, sepal width, petal length, and petal width. A machine learning classification model will process these inputs and return the predicted Iris species.

The main goal of this project is to learn how to serve a machine learning model through a REST API and gradually make the API production-ready with validation, error handling, testing, logging, monitoring, and deployment.

## Dataset

The project will use the Iris dataset provided by scikit-learn.

The dataset contains measurements of Iris flowers and three possible species:

- Setosa
- Versicolor
- Virginica

## API Contract

### Endpoint

`POST /predict`

### Input

The API will accept the following flower measurements:

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

Example request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}