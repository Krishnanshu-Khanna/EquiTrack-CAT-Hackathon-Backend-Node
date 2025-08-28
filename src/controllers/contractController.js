// src/controllers/contractController.js
const asyncHandler = require("express-async-handler");
const Contract = require("../models/Contract");

// @desc    Get all contracts
// @route   GET /api/contracts
// @access  Private
const getContracts = asyncHandler(async (req, res) => {
	const contracts = await Contract.find({})
		.populate("equipment")
		.populate("operator");
	res.status(200).json(contracts);
});

// @desc    Create new contract
// @route   POST /api/contracts
// @access  Private
const createContract = asyncHandler(async (req, res) => {
	const { contractID, equipment, operator, startDate, endDate, amount } =
		req.body;

	if (
		!contractID ||
		!equipment ||
		!operator ||
		!startDate ||
		!endDate ||
		!amount
	) {
		res.status(400);
		throw new Error("Please add all required fields");
	}

	const contract = await Contract.create({
		contractID,
		equipment,
		operator,
		startDate,
		endDate,
		amount,
	});
	res.status(201).json(contract);
});

module.exports = { getContracts, createContract };
