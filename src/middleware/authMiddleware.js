// src/middleware/authMiddleware.js
const protect = (req, res, next) => {
	// In a real app, you would check for a token in the request headers
	const token = req.headers.authorization;

	if (token && token.startsWith("Bearer")) {
		// For this example, we'll just log that the token is present
		console.log("User is authenticated.");
		next();
	} else {
		// If no token is found, send a 401 Unauthorized response
		res.status(401).json({ message: "Not authorized, no token" });
	}
};

module.exports = { protect };
