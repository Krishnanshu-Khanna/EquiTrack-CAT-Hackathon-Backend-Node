// src/controllers/equipmentController.js
const asyncHandler = require("express-async-handler");
const Equipment = require("../models/Equipment");

// @desc    Get all equipment
// @route   GET /api/equipment
// @access  Private
const getEquipment = asyncHandler(async (req, res) => {
	const equipment = await Equipment.find({});
	res.status(200).json(equipment);
});

// @desc    Create new equipment
// @route   POST /api/equipment
// @access  Private
const createEquipment = asyncHandler(async (req, res) => {
	const { name, type, location } = req.body;

	if (!name || !type) {
		res.status(400);
		throw new Error("Please add all required fields");
	}

	const equipment = await Equipment.create({ name, type, location });
	res.status(201).json(equipment);
});

module.exports = { getEquipment, createEquipment };
