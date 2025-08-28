// src/models/Operator.js
const mongoose = require("mongoose");

const operatorSchema = mongoose.Schema(
	{
		name: { type: String, required: true },
		status: { type: String, enum: ["Active", "Inactive"], default: "Active" },
		certification: { type: String },
		assignedEquipment: { type: mongoose.Schema.Types.ObjectId, ref: "Equipment" },
		hoursWorked: { type: Number, default: 0 },
	},
	{
		timestamps: true,
	}
);

const Operator = mongoose.model("Operator", operatorSchema);

module.exports = Operator;
