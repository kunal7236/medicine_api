# 💊 Jan Aushadhi Medicine API

This is a FastAPI-based web API that allows users to search for medicines listed under the Jan Aushadhi scheme and lets the admin update the dataset by uploading a new official PDF.

Hosted at: [`https://medicine-api-m176.onrender.com`](https://medicine-api-m176.onrender.com/docs)

---

## 📌 Features

- 🔍 Search for a medicine by name
- 📆 See the last updated date
- 🔐 Admin can upload new Jan Aushadhi PDF to refresh the database
- 📦 Stores data in MongoDB Atlas

---

## 🚀 Public Routes

### 1. `/search?name=<medicine_name>`

**Description**:  
Returns the matching row for the medicine, if available.

**Method**: `GET`

**Query Parameter**:

- `name` (required): Name of the medicine (partial or full)

**Example**:

```
GET https://medicine-api-m176.onrender.com/search?name=Paracetamol
```

**Response**:

```json
{
  "medicine": {
    "Sr_No": "123",
    "Medicine Name": "Paracetamol 500mg Tablet",
    "Unit Price": "₹2.50"
  },
  "updated_at": "2025-07-28T00:00:00"
}
```

If not found:

```json
{
  "message": "Medicine not found",
  "updated_at": "2025-07-28T00:00:00"
}
```

---

### 2. `/status`

**Description**:  
Check if the API is up and see the last data update timestamp.

**Method**: `GET`

**Example**:

```
GET https://medicine-api-m176.onrender.com/status
```

**Response**:

```json
{
  "status": "API is running",
  "updated_at": "2025-07-28T00:00:00"
}
```

---

## 🔐 Admin Route

### `/upload`

**Description**:  
Allows admin to upload a new PDF file to update the medicines data.

**Method**: `POST`

**Authentication**: Requires an API key in the header:

```
x-api-key: YOUR_SECRET_KEY
```

**Form-Data**:

- `file`: the official Jan Aushadhi PDF file

**Example with `curl`**:

```bash
curl -X POST https://medicine-api-m176.onrender.com/upload \
  -H "x-api-key: YOUR_SECRET_KEY" \
  -F "file=@jan_aushadhi_list.pdf"
```

**Response**:

```json
{
  "message": "Data updated successfully",
  "entries": 2439
}
```

---

## ⚙️ Environment Variables

Create a `.env` file with the following:

```env
API_KEY=your_secret_key
MONGO_URI=your_mongodb_connection_string
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Maintainer

Made with ❤️ by [@kunal7236](https://github.com/kunal7236)
