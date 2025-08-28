// src/models/Operator.js
const mongoose = require("mongoose");

// Define a simple Point schema for coordinates
const pointSchema = new mongoose.Schema({
    x: { type: Number, required: true },
    y: { type: Number, required: true }
}, { _id: false }); // _id: false prevents Mongoose from creating an id for each point

const operatorSchema = mongoose.Schema(
    {
        name: { type: String, required: true },
        status: { type: String, enum: ["Active", "Inactive"], default: "Active" },
        certification: { type: String },
        assignedEquipment: { type: mongoose.Schema.Types.ObjectId, ref: "Equipment" },
        hoursWorked: { type: Number, default: 0 },
        
        safeZone: {
            type: {
                type: String,
                enum: ['Polygon'],
                default: 'Polygon'
            },
            coordinates: {
                type: [[pointSchema]], // An array of arrays of points for GeoJSON compatibility
                required: false
            }
        },

        // --- NEWLY ADDED ---
        // Stores the initial {x, y} coordinates for the tracker marker.
        initialTrackerPosition: {
            type: pointSchema,
            required: false // It's optional, as a tracker might not always be set.
        }
    },
    {
        timestamps: true,
    }
);

const Operator = mongoose.model("Operator", operatorSchema);

module.exports = Operator;
