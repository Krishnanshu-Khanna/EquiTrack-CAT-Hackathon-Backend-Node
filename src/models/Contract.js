// src/models/Contract.js
const mongoose = require("mongoose");

const contractSchema = mongoose.Schema(
	{
		contractID: { type: String, required: true, unique: true },
		equipment: {
			type: mongoose.Schema.Types.ObjectId,
			ref: "Equipment",
			required: true,
		},
		operator: {
			type: mongoose.Schema.Types.ObjectId,
			ref: "Operator",
			required: true,
		},
		startDate: { type: Date, required: true },
		endDate: { type: Date, required: true },
		status: {
			type: String,
			enum: ["Active", "Completed", "Overdue"],
			default: "Active",
		},
		amount: { type: Number, required: true },
	},
	{
		timestamps: true,
	}
);

const Contract = mongoose.model("Contract", contractSchema);

module.exports = Contract;
