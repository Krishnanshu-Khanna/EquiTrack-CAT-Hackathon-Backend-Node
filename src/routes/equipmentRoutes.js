// src/routes/equipmentRoutes.js
const express = require("express");
const router = express.Router();
const {
	getEquipment,
	createEquipment,
} = require("../controllers/equipmentController");
const { protect } = require("../middleware/authMiddleware");

// The protect middleware is applied to these routes
router.route("/").get(getEquipment)
router.route("/").post( createEquipment);

module.exports = router;
