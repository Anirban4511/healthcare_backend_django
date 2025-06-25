# Healthcare Backend

This project is a Django-based backend for a healthcare management system. It provides RESTful APIs for managing patients, doctors, and their mappings, with JWT authentication.

## Features

- User registration and JWT-based authentication
- CRUD operations for Patients and Doctors
- Mapping between Patients and Doctors
- Admin interface for managing all models

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)

## Project Structure

```
healthcare_backend/
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── healthcare_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
```

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Create a `.env` file in the root directory with the following variables:
     ```env
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_HOST=localhost
     DB_PORT=5432
     JWT_SECRET=your_jwt_secret
     ALLOWED_HOSTS=127.0.0.1,localhost
     ```
4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (for admin access)**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### 1. Authentication APIs
- `POST /api/auth/register/` — Register a new user with username, email, and password.
- `POST /api/auth/login/` — Log in a user and return a JWT token.

### 2. Patient Management APIs
- `POST /api/patients/` — Add a new patient (Authenticated users only).
- `GET /api/patients/` — Retrieve all patients created by the authenticated user.
- `GET /api/patients/<id>/` — Get details of a specific patient.
- `PUT /api/patients/<id>/` — Update patient details.
- `DELETE /api/patients/<id>/` — Delete a patient record.

### 3. Doctor Management APIs
- `POST /api/doctors/` — Add a new doctor (Authenticated users only).
- `GET /api/doctors/` — Retrieve all doctors.
- `GET /api/doctors/<id>/` — Get details of a specific doctor.
- `PUT /api/doctors/<id>/` — Update doctor details.
- `DELETE /api/doctors/<id>/` — Delete a doctor record.

### 4. Patient-Doctor Mapping APIs
- `POST /api/mappings/` — Assign a doctor to a patient.
- `GET /api/mappings/` — Retrieve all patient-doctor mappings.
- `GET /api/mappings/<patient_id>/` — Get all doctors assigned to a specific patient.
- `DELETE /api/mappings/<id>/` — Remove a doctor from a patient.

## API Usage Examples

### 1. Register a New User

**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### 2. Obtain JWT Token (Login)

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "refresh": "string",
  "access": "string"
}
```

### 3. Create a Patient

**Endpoint:** `POST /api/patients/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "string",
  "age": 25,
  "gender": "string",
  "address": "string"
}
```

### 4. Create a Doctor

**Endpoint:** `POST /api/doctors/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "string",
  "specialization": "string",
  "email": "string",
  "phone": "string (10 digits)"
}
```

> **Note:** All endpoints (except registration and login) require the `Authorization: Bearer <access_token>` header.

## Models

- **Patient**: Linked to a user, stores patient details
- **Doctor**: Stores doctor details
- **PatientDoctorMapping**: Maps patients to doctors (unique per pair)

## Admin

Access the Django admin at `/admin/` with your superuser credentials.