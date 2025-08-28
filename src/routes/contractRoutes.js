// src/routes/contractRoutes.js
const express = require("express");
const router = express.Router();
const {
	getContracts,
	createContract,
} = require("../controllers/contractController");
const { protect } = require("../middleware/authMiddleware");

router.get("/",getContracts);
router.post("/", createContract);

module.exports = router;
