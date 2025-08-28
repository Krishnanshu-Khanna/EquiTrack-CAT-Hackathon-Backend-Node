// src/routes/operatorRoutes.js
const express = require("express");
const router = express.Router();
const {
	getOperators,
	createOperator,
} = require("../controllers/operatorController");
const { protect } = require("../middleware/authMiddleware");

router.route("/").get(getOperators);
router.route("/").post(createOperator);

module.exports = router;
