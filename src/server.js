// src/server.js
const express = require("express");
const connectDB = require("./config/db");
require("dotenv").config();
const cors = require("cors"); // <--- add this

const asyncHandler = require("express-async-handler");

// Route Imports
const equipmentRoutes = require("./routes/equipmentRoutes");
const operatorRoutes = require("./routes/operatorRoutes");
const contractRoutes = require("./routes/contractRoutes");

// Connect to the database
connectDB();

const app = express();
const PORT = process.env.PORT || 5000;
// Enable CORS for all origins
app.use(cors()); 
// Middleware to parse JSON bodies
app.use(express.json());

// Mount the routes
app.use("/api/equipment", equipmentRoutes);
app.use("/api/operators", operatorRoutes);
app.use("/api/contracts", contractRoutes);
app.use("/api/health", (req, res) => res.send("API is running..."));

// Custom error handling middleware for async functions
app.use((err, req, res, next) => {
	const statusCode = res.statusCode === 200 ? 500 : res.statusCode;
	res.status(statusCode);
	res.json({
		message: err.message,
		stack: process.env.NODE_ENV === "production" ? null : err.stack,
	});
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
