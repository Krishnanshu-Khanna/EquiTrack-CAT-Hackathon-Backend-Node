// src/controllers/operatorController.js
const asyncHandler = require("express-async-handler");
const Operator = require("../models/Operator");
const Equipment = require("../models/Equipment"); // Assuming this model exists
const staticData = [
	{ ActiveEngineHours: 620, IdleTime: 180, FuelUsage: 4200, LoadUsage: 850, TypeOfProject: 'Roadwork', WeatherSeason: 'Summer', MachineType: 'Excavator', SiteDemographic: 'Urban', ContractValue: "120,000", PromisedTime: 3, ClientEfficiency: 0.21 },
	{ ActiveEngineHours: 310, IdleTime: 90, FuelUsage: 2100, LoadUsage: 400, TypeOfProject: 'Housing Build', WeatherSeason: 'Winter', MachineType: 'Crane', SiteDemographic: 'Suburban', ContractValue: "85,000", PromisedTime: 2, ClientEfficiency: 0.92 },
	{ ActiveEngineHours: 450, IdleTime: 120, FuelUsage: 3100, LoadUsage: 600, TypeOfProject: 'Mining', WeatherSeason: 'Monsoon', MachineType: 'Loader', SiteDemographic: 'Rural', ContractValue: "150,000", PromisedTime: 5,  ClientEfficiency: 0.55 },
	{ ActiveEngineHours: 250, IdleTime: 60, FuelUsage: 1500, LoadUsage: 280, TypeOfProject: 'Warehouse', WeatherSeason: 'Spring', MachineType: 'Forklift', SiteDemographic: 'Industrial Zone', ContractValue: "40,000", PromisedTime: 1,  ClientEfficiency: 0.89 },
	{ ActiveEngineHours: 540, IdleTime: 200, FuelUsage: 3700, LoadUsage: 720, TypeOfProject: 'Highway Bridge', WeatherSeason: 'Monsoon', MachineType: 'Excavator', SiteDemographic: 'Semi-urban', ContractValue: "180,000", PromisedTime: 4,  ClientEfficiency: 0.18 },
	{ ActiveEngineHours: 400, IdleTime: 100, FuelUsage: 2800, LoadUsage: 500, TypeOfProject: 'Railwork', WeatherSeason: 'Autumn', MachineType: 'Bulldozer', SiteDemographic: 'Rural', ContractValue: "130,000", PromisedTime: 3,  ClientEfficiency: 0.95 },
	{ ActiveEngineHours: 300, IdleTime: 80, FuelUsage: 2100, LoadUsage: 350, TypeOfProject: 'Factory Build', WeatherSeason: 'Summer', MachineType: 'Crane', SiteDemographic: 'Industrial Zone', ContractValue: "95,000", PromisedTime: 2, ClientEfficiency: 0.85 },
	{ ActiveEngineHours: 700, IdleTime: 240, FuelUsage: 4900, LoadUsage: 950, TypeOfProject: 'Dam Construction', WeatherSeason: 'Monsoon', MachineType: 'Excavator', SiteDemographic: 'Rural', ContractValue: "250,000", PromisedTime: 6,  ClientEfficiency: 0.48 },
  ];
  function createExtendedArray(data, size) {
	const extendedArray = [];
	for (let i = 0; i < size; i++) {
	  extendedArray.push(data[i % data.length]);
	}
	return extendedArray;
  }
  function mapOperatorsWithData(operators, dataArray) {
	return operators.map((operator, index) => {
	  return {
		operator,
		...dataArray[index]  // Spread corresponding data object
	  };
	});
  }
  // Example usage to get 12 items
// @desc    Get all operators
// @route   GET /api/operators
// @access  Private
const getOperators = asyncHandler(async (req, res) => {
	console.log("Fetching operators...");
    const operators = await Operator.find({}).populate('assignedEquipment', 'name'); // Populate equipment name
	const extendedDataArray = createExtendedArray(staticData, operators.length);
	const ExtentedOperators =  mapOperatorsWithData(operators, extendedDataArray);
    res.status(200).json(ExtentedOperators);
});

// @desc    Create a new operator
// @route   POST /api/operators
// @access  Private
const createOperator = async (req, res) => {
	try {
	  const {
		name,
		status,
		certification,
		assignedEquipment,
		safeZone,
		initialTrackerPosition,
	  } = req.body;
  
    // Fix safeZone structure if it exists
    let processedSafeZone = null;
      // Check if coordinates are in the wrong format (array of arrays with single points)
  
        
        // Flatten the coordinates - extract the single point from each sub-array
        const flattenedCoordinates = safeZone.coordinates.map(coordArray => coordArray[0]);
        
        processedSafeZone = {
          type: safeZone.type || "Polygon",
          coordinates: [[flattenedCoordinates]] // Wrap in single array for GeoJSON Polygon format
        };
  
    
	console.log("Processed Safe Zone:", processedSafeZone);
	  const operator = await Operator.create({
		name,
		status,
		certification,
		assignedEquipment,
		safeZone,
		initialTrackerPosition,
	  });
  
	  res.status(201).json(operator);
	} catch (error) {
	  console.error('Error creating operator:', error);
	  res.status(500).json({ message: 'Failed to create operator', error: error.message });
	}
  };
  
module.exports = { getOperators, createOperator };
