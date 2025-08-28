// src/controllers/operatorController.js
const asyncHandler = require("express-async-handler");
const Operator = require("../models/Operator");

// @desc    Get all operators
// @route   GET /api/operators
// @access  Private
const getOperators = asyncHandler(async (req, res) => {
	const operators = await Operator.find({});
	res.status(200).json(operators);
});

// @desc    Create new operator
// @route   POST /api/operators
// @access  Private
const createOperator = asyncHandler(async (req, res) => {
	const { name, certification } = req.body;

	if (!name || !certification) {
		res.status(400);
		throw new Error("Please add all required fields");
	}

	const operator = await Operator.create({ name, certification });
	res.status(201).json(operator);
});


module.exports = { getOperators, createOperator };
