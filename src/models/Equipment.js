// src/models/Equipment.js
const mongoose = require("mongoose");

const equipmentSchema = mongoose.Schema(
	{
		name: { type: String, required: true },
		type: { type: String, required: true },
		status: {
			type: String,
			enum: ["Operational", "Idle", "Maintenance"],
			default: "Idle",
		},
		location: { type: String },
		engineHours: { type: Number, default: 0 },
	},
	{
		timestamps: true,
	}
);

const Equipment = mongoose.model("Equipment", equipmentSchema);

module.exports = Equipment;
