import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';

const app = express();
const PORT = 3001; // หรือ port ที่ต้องการ

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.json());

// Test endpoint
app.post('/api/test', (req, res) => {
    console.log('\n=== Received POST Request ===');
    console.log('Time:', new Date().toISOString());
    console.log('\nHeaders:');
    console.log(JSON.stringify(req.headers, null, 2));
    console.log('\nBody:');
    console.log(JSON.stringify(req.body, null, 2));
    console.log('============================\n');
    
    // ส่ง response กลับ
    res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        message: 'Data received successfully',
        receivedData: req.body
    });
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Server is running',
        timestamp: new Date().toISOString()
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({
        status: 'error',
        message: 'Internal server error',
        error: err.message
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`\n=== Test Server Running ===`);
    console.log(`Time: ${new Date().toISOString()}`);
    console.log(`Port: ${PORT}`);
    console.log(`Test URL: http://localhost:${PORT}/api/test`);
    console.log(`Health Check: http://localhost:${PORT}/health`);
    console.log('=========================\n');
});
