// src/controllers/operatorController.js
const asyncHandler = require("express-async-handler");
const Operator = require("../models/Operator");
const Equipment = require("../models/Equipment"); // Assuming this model exists

// @desc    Get all operators
// @route   GET /api/operators
// @access  Private
const getOperators = asyncHandler(async (req, res) => {
    const operators = await Operator.find({}).populate('assignedEquipment', 'name'); // Populate equipment name
    res.status(200).json(operators);
});

// @desc    Create a new operator
// @route   POST /api/operators
// @access  Private
const createOperator = asyncHandler(async (req, res) => {
    // 1. Destructure all expected fields, including the new safeZone
    const { name, status, certification, assignedEquipment, safeZone } = req.body;
	console.log(req.body);
    // 2. More robust validation
    if (!name || !certification) {
        res.status(400);
        throw new Error("Please provide all required fields: name and certification.");
    }
    
    // 3. Prepare the data for the new operator
    const operatorData = {
        name,
        status,
        certification,
        assignedEquipment: assignedEquipment, // Default to null
    };

    // --- NEW LOGIC FOR SAFE ZONE ---
    // Check if safeZone data is present and has coordinates
    if (safeZone && safeZone.coordinates && Array.isArray(safeZone.coordinates)) {
        // The frontend sends coordinates as a simple array of points [{x, y}, ...].
        // For GeoJSON Polygon format, it needs to be wrapped in an extra array.
        // e.g., [[ {x,y}, {x,y}, {x,y}, {x,y} ]]
        operatorData.safeZone = {
            type: 'Polygon',
            coordinates: [safeZone.coordinates] // Wrap the coordinates array
        };
    }

    // Note: The logic for finding 'assignedEquipment' by name/ID can be added here if needed.
    // For now, it's kept simple as in your original code.

    // 4. Create the new operator with all the data
    const operator = await Operator.create(operatorData);

    // 5. Send the created operator as a response
    if (operator) {
        res.status(201).json(operator);
    } else {
        res.status(400);
        throw new Error("Invalid operator data.");
    }
});

module.exports = { getOperators, createOperator };
