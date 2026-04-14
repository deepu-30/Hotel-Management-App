# Hotel-Management-App
## Project Description
A lightweight serverless email service built using Python and the Serverless Framework, designed to simulate and handle email notifications for backend applications.

This project demonstrates how to create and run a serverless function locally using serverless-offline, exposing an HTTP API endpoint that processes email requests. It is intended to be integrated with a Django-based Hospital Management System to handle actions such as user registration, appointment booking, and system notifications.

## Features
* Serverless architecture using Python
* Local development with serverless-offline
* REST API endpoint for triggering email events
* JSON-based request handling
* Easily integrable with Django or any backend
* Modular and scalable microservice design

## Tech Stack
Python 3.x
Serverless Framework
Node.js (for serverless plugins)
serverless-offline plugin

## API Endpoint
### POST /send

Request Body:
`
{
  "type": "registration",
  "to": "user@example.com"
} `

Response:
`{
  "message": "Email simulated successfully"
}`

## Local Setup
 `npm install
npx serverless offline`

Server will run on:
`http://localhost:3000/send`

## Use Case

This service is designed to be integrated with a Django application to handle:

 * User registration emails
 * Appointment confirmations
 * Notification services

## Architecture
`Django Backend → Serverless API → Email Service`

