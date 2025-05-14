# 🌿 Light Sensor API (FastAPI + MongoDB)

This project is a simple IoT backend for recording ambient light (lux) data from ESP32 devices, using FastAPI and MongoDB Atlas.

## Features

- REST API to receive lux values via `POST /lux`
- Query stored light data via `GET /lux`
- MongoDB Atlas integration (cloud database)
- Ready for deployment on [Render](https://render.com)

## Example API usage

### POST lux value

```json
POST /lux
Content-Type: application/json

{
  "lux": 153.4
}
