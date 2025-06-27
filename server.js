import express from 'express';
import { PrismaClient } from '@prisma/client';
import cors from 'cors';
import bodyParser from 'body-parser';
import axios from 'axios';
import session from 'express-session';
import 'dotenv/config';
import path from 'path';
import querystring from 'querystring';
import { v4 as uuidv4 } from 'uuid';
import { Client } from '@line/bot-sdk';
import rateLimit from 'express-rate-limit';
import { z } from 'zod';
import pLimit from 'p-limit';

const PORT = process.env.PORT || 3001;
const app = express();

app.set('trust proxy', 1);

const prisma = new PrismaClient();

const limit = pLimit(5);

global.verifiedBooks = {};
global.lastActivityTime = {};

const lineClient = new Client({
    channelAccessToken: process.env.LINE_ACCESS_TOKEN
});

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(process.cwd(), 'public')));
app.use(express.static(path.join(process.cwd(), 'templates')));

// Session config
app.use(session({
    secret: 'supersecretkey',
    resave: false,
    saveUninitialized: true,
    cookie: {
        secure: false,
        maxAge: 30 * 60 * 1000 // 30 นาที
    }
}));

// API rate limit
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many requests, please try again later.'
});
app.use('/api/', apiLimiter);

// === Sample validation with Zod ===
const SyncBooksSchema = z.object({
    userId: z.string().min(1),
    books: z.array(z.object({
        query_id: z.string(),
        title: z.string(),
        author: z.string(),
        isbn: z.string().optional()
    })),
    userQueries: z.array(z.object({
        query_id: z.string(),
        user_line_id: z.string(),
        user_query: z.string(),
        time_stamp: z.number().optional()
    }))
});

app.get('/auth/microsoft', (req, res) => {
    const lineUserId = req.query.lineUserId;
    if (!lineUserId) {
        console.error("No LINE User ID provided");
        return res.redirect('/login.html?error=true');
    }
    
    req.session.lineUserId = lineUserId;
    console.log(`Initiating Microsoft OAuth login for LINE User ID: ${lineUserId}`);

    const params = {
        client_id: process.env.MICROSOFT_CLIENT_ID,
        response_type: 'code',
        redirect_uri: process.env.MICROSOFT_REDIRECT_URI,
        scope: 'https://graph.microsoft.com/User.Read openid profile email',
        response_mode: 'query',
        prompt: 'select_account',
        domain_hint: 'kmutt.ac.th'
    };
    const authUrl = `https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize?${querystring.stringify(params)}`;
    res.redirect(authUrl);
});

app.get('/auth/microsoft/callback', async (req, res) => {
    const code = req.query.code;
    const lineUserId = req.session.lineUserId;

    if (!code || !lineUserId) {
        console.error("Missing code or LINE User ID");
        return res.redirect('/login.html?error=true');
    }

    try {
        const tokenResponse = await axios.post('https://login.microsoftonline.com/organizations/oauth2/v2.0/token', 
            querystring.stringify({
                client_id: process.env.MICROSOFT_CLIENT_ID,
                client_secret: process.env.MICROSOFT_CLIENT_SECRET,
                redirect_uri: process.env.MICROSOFT_REDIRECT_URI,
                grant_type: 'authorization_code',
                code: code
            }), 
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        );

        const accessToken = tokenResponse.data.access_token;
        const userResponse = await axios.get('https://graph.microsoft.com/v1.0/me', {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        const { displayName, mail } = userResponse.data;

        if (!mail.endsWith('@kmutt.ac.th')) {
            console.error(`Invalid email domain for LINE User ID ${lineUserId}: ${mail}`);
            return res.redirect('/login.html?error=invalid_domain');
        }

        console.log('User logged in successfully:', {
            lineUserId: lineUserId,
            displayName: displayName,
            email: mail,
            loginTime: new Date().toISOString()
        });

        let user;
        const existingUserByLine = await prisma.user.findUnique({
            where: { user_line_id: lineUserId }
        });

        if (existingUserByLine) {
            user = await prisma.user.update({
                where: { user_line_id: lineUserId },
                data: {
                    name: displayName.split(' ')[0],
                    surname: displayName.split(' ')[1] || '',
                    email: mail
                }
            });
            console.log(`Updated existing user: ${lineUserId}`, user);
        } else {
            user = await prisma.user.create({
                data: {
                    user_line_id: lineUserId,
                    name: displayName.split(' ')[0],
                    surname: displayName.split(' ')[1] || '',
                    email: mail
                }
            });
            console.log(`Created new user: ${lineUserId}`, user);
        }

        res.redirect(`/purchase.html?userId=${encodeURIComponent(lineUserId)}`);
    } catch (error) {
        console.error(`Login failed for LINE User ID ${lineUserId}:`, error.message);
        res.redirect('/login.html?error=true');
    }
});

app.get('/', (req, res) => {
    if (req.session.user) {
        return res.redirect(`/login.html?success=true&name=${encodeURIComponent(req.session.user.name)}&email=${encodeURIComponent(req.session.user.email)}`);
    }
    res.sendFile(path.join(process.cwd(), 'templates', 'login.html'));
});

const cleanupInactiveUsers = () => {
    const now = Date.now();
    const INACTIVE_THRESHOLD = 30 * 60 * 1000;

    for (const userId in global.verifiedBooks) {
        if (now - (global.lastActivityTime[userId] || 0) > INACTIVE_THRESHOLD) {
            delete global.verifiedBooks[userId];
            delete global.lastActivityTime[userId];
            console.log(`Cleaned up inactive user: ${userId}`);
        }
    }
};

setInterval(cleanupInactiveUsers, 15 * 60 * 1000);

app.get('/api/recommended-books/:userId', async (req, res) => {
    try {
        const userId = req.params.userId;
        
        global.lastActivityTime[userId] = Date.now();

        const userQueries = await prisma.userQuery.findMany({
            where: {
                user_line_id: userId,
                response_success: 'true',
                purchases: { none: {} }
            },
            orderBy: {
                time_stamp: 'desc'
            },
            select: { query_id: true }
        });

        const validQueryIds = new Set(userQueries.map(query => query.query_id));

        const booksForUser = global.verifiedBooks[userId] || [];
        const recommendedBooks = [];
        const seenBooks = new Set();

        for (const book of booksForUser) {
            if (validQueryIds.has(book.query_id)) {
                const bookUniqueKey = `${book.title.toLowerCase()}|${book.author.toLowerCase()}`;
                
                if (!seenBooks.has(bookUniqueKey)) {
                    recommendedBooks.push(book);
                    seenBooks.add(bookUniqueKey);
                }
            }
        }

        console.log(`Returning all ${recommendedBooks.length} unique recommended books from ${userQueries.length} queries for user ${userId}`);
        res.json(recommendedBooks);
    } catch (error) {
        console.error('Error fetching recommended books:', error);
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/cancel-recommendations', async (req, res) => {
    const { userId } = req.body;

    if (!userId) {
        return res.status(400).json({ error: 'userId is required' });
    }

    try {
        if (global.verifiedBooks[userId]) {
            delete global.verifiedBooks[userId];
            console.log(`Cleared recommendations for userId: ${userId}`);
        }
        res.json({ success: true, message: 'Recommendations cleared' });
    } catch (error) {
        console.error('Error clearing recommendations:', error);
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/purchase', async (req, res) => {
    const { queryIds, userId } = req.body;

    if (!queryIds || !Array.isArray(queryIds) || !userId) {
        return res.status(400).json({ error: 'queryIds and userId are required' });
    }

    try {
        const purchases = await Promise.all(queryIds.map(query =>
            prisma.purchase.create({
                data: {
                    purchase_id: uuidv4(),
                    query_id: query.query_id,
                    user_line_id: userId,
                    response_pick: query.title
                }
            })
        ));

        if (global.verifiedBooks[userId] && queryIds.length > 0) {
            const selectedBooksSet = new Set(queryIds.map(query => `${query.query_id}|${query.title}`));
            global.verifiedBooks[userId] = global.verifiedBooks[userId].filter(book =>
                selectedBooksSet.has(`${book.query_id}|${book.title}`)
            );
        }

        const bookList = queryIds.map(query => `- ${query.title}`).join('\n');
        const date = new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' });
        const message = `🎉 Request completed! (${date})\nYou requested ${queryIds.length} books in total.:\n${bookList}\nThank you for using our service!`;
        
        await lineClient.pushMessage(userId, {
            type: 'text',
            text: message
        });

        console.log(`Sent LINE notification to user ${userId} for ${queryIds.length} books`);

        res.json({ success: true, purchases });
    } catch (error) {
        console.error('Error saving purchase:', error);
        res.status(500).json({ error: error.message });
    }
});

const formatDateThai = (date) => {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Asia/Bangkok',
    };
    return new Intl.DateTimeFormat('th-TH', options).format(new Date(date));
};

app.post('/api/sync-books', async (req, res) => {
    const startTime = Date.now();
    try {
        const { userId, books, userQueries } = req.body;

        console.log('Received data from Python:', { userId, booksCount: books?.length, queriesCount: userQueries?.length });

        if (!userId || !Array.isArray(books) || !Array.isArray(userQueries)) {
            throw new Error('Invalid request: userId, books, and userQueries are required as arrays');
        }

        // Check or create user
        const userCheckStart = Date.now();
        let user = await prisma.user.findUnique({ where: { user_line_id: userId } });
        if (!user) {
            user = await prisma.user.create({
                data: {
                    user_line_id: userId,
                    name: 'Unknown',
                    surname: 'User',
                    email: `logged_out_${userId}@example.com`
                }
            });
            console.log(`Created new user with user_line_id: ${userId}`);
        }
        console.log(`User check/creation took ${Date.now() - userCheckStart}ms`);

        // Batch insert user queries
        const queryInsertStart = Date.now();
        const queryData = userQueries
            .filter(query => query.query_id && query.user_line_id && query.user_query)
            .map(query => ({
                query_id: query.query_id,
                user_line_id: query.user_line_id,
                user_query: query.user_query,
                response_success: 'false',
                time_stamp: typeof query.time_stamp === 'number' ? new Date(query.time_stamp * 1000) : new Date()
            }));

        if (queryData.length > 0) {
            await prisma.userQuery.createMany({
                data: queryData,
                skipDuplicates: true
            });
            console.log(`Synced ${queryData.length} new user queries`);
        }
        console.log(`Query insert took ${Date.now() - queryInsertStart}ms`);

        if (!books || books.length === 0) {
            return res.json({
                status: 'success',
                message: 'No book recommendations available, but user query has been saved',
                data: []
            });
        }

        // Filter new books
        const bookFilterStart = Date.now();
        const existingBooks = await prisma.bookList.findMany({ select: { title: true, author: true } });
        const existingBookSet = new Set(existingBooks.map(book => 
            `${book.title?.trim().toLowerCase() || ''}|${book.author?.trim().toLowerCase() || ''}`
        ));

        const newBooks = books.filter(book => {
            const key = `${book.title?.trim().toLowerCase() || ''}|${book.author?.trim().toLowerCase() || ''}`;
            return !existingBookSet.has(key);
        });
        console.log(`Filtered ${newBooks.length} new books in ${Date.now() - bookFilterStart}ms`);

        // Parallel Google Books API calls
        const googleApiStart = Date.now();
        const bookPromises = newBooks.map(async (book) => {
            if (!book.title || !book.author || !book.query_id) {
                console.error(`Skipping book due to missing fields: ${JSON.stringify(book)}`);
                return null;
            }

            let verifiedBook = {
                query_id: book.query_id,
                title: book.title,
                author: book.author,
                isbn: book.isbn || 'N/A',
                description: 'No description available',
                coverImage: 'https://via.placeholder.com/128x192?text=No+Image'
            };

            try {
                const response = await axios.get('https://www.googleapis.com/books/v1/volumes', {
                    params: {
                        q: `${book.title} ${book.author}`,
                        maxResults: 1,
                        key: process.env.GOOGLE_BOOKS_API_KEY
                    },
                    timeout: 5000 // 5s timeout to prevent hanging
                });

                if (response.data.items && response.data.items.length > 0) {
                    const volumeInfo = response.data.items[0].volumeInfo;
                    verifiedBook = {
                        ...verifiedBook,
                        title: volumeInfo.title || book.title,
                        author: volumeInfo.authors?.join(', ') || book.author,
                        description: volumeInfo.description || 'No description available',
                        coverImage: volumeInfo.imageLinks?.thumbnail || 'https://via.placeholder.com/128x192?text=No+Image'
                    };
                    return { verifiedBook, matched: true };
                }
            } catch (error) {
                console.error(`Error verifying ${book.title} with Google Books API:`, error.message);
            }
            return { verifiedBook, matched: false };
        });

        const results = (await Promise.all(bookPromises)).filter(result => result !== null);
        console.log(`Google Books API calls took ${Date.now() - googleApiStart}ms`);

        // Update query success and store verified books
        const updateStart = Date.now();
        const verifiedBooks = [];
        for (const { verifiedBook, matched } of results) {
            await prisma.userQuery.update({
                where: { query_id: verifiedBook.query_id },
                data: { response_success: matched ? 'true' : 'false' }
            });

            if (matched) {
                if (!global.verifiedBooks[userId]) {
                    global.verifiedBooks[userId] = [];
                }

                const bookKey = `${verifiedBook.query_id}|${verifiedBook.title}`;
                const titleAuthorKey = `${verifiedBook.title.toLowerCase()}|${verifiedBook.author.toLowerCase()}`;
                const bookKeys = new Set(global.verifiedBooks[userId].map(b => `${b.query_id}|${b.title}`));
                const titleAuthorKeys = new Set(global.verifiedBooks[userId].map(b => `${b.title.toLowerCase()}|${b.author.toLowerCase()}`));

                if (!bookKeys.has(bookKey) && !titleAuthorKeys.has(titleAuthorKey)) {
                    global.verifiedBooks[userId].push(verifiedBook);
                    verifiedBooks.push(verifiedBook);
                }
            }
        }
        console.log(`Updates and verification took ${Date.now() - updateStart}ms`);

        res.json({
            status: 'success',
            message: `Synced ${verifiedBooks.length} books`,
            data: verifiedBooks.map(book => ({
                ...book,
                time_stamp: formatDateThai(book.time_stamp || new Date())
            }))
        });
        console.log(`Total /api/sync-books took ${Date.now() - startTime}ms`);
    } catch (error) {
        console.error('Error syncing books:', error);
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
});

// New endpoint to sync books to an external API
app.post('/api/external-sync', async (req, res) => {
    const { queryIds, userId } = req.body;

    // Validate input
    if (!queryIds || !Array.isArray(queryIds) || !userId) {
        return res.status(400).json({ error: 'queryIds and userId are required' });
    }

    try {
        // Prepare data to send to external API
        const booksData = queryIds.map(query => ({
            query_id: query.query_id,
            title: query.title,
            user_line_id: userId,
            purchase_id: uuidv4(),
            timestamp: new Date().toISOString()
        }));

        // Send data to external API
        const externalApiUrl = process.env.EXTERNAL_API_URL; // Define in .env
        const externalApiKey = process.env.EXTERNAL_API_KEY; // Optional: API key for authentication

        const response = await axios.post(externalApiUrl, {
            books: booksData
        }, {
            headers: {
                'Content-Type': 'application/json',
                ...(externalApiKey && { 'Authorization': `Bearer ${externalApiKey}` }) // Add auth if needed
            }
        });

        // Log success
        console.log(`Successfully sent ${booksData.length} books to external API for user ${userId}`, {
            externalApiResponse: response.data
        });

        // Send LINE notification to user
        const bookList = queryIds.map(query => `- ${query.title}`).join('\n');
        const date = new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' });
        const message = `🎉 Books synced to external service! (${date})\nYou selected ${queryIds.length} books:\n${bookList}\nThank you for using our service!`;

        await lineClient.pushMessage(userId, {
            type: 'text',
            text: message
        });

        console.log(`Sent LINE notification to user ${userId} for ${queryIds.length} books`);

        // Return success response
        res.json({
            success: true,
            message: `Successfully synced ${booksData.length} books to external API`,
            externalApiResponse: response.data
        });
    } catch (error) {
        // Log error
        console.error('Error syncing books to external API:', {
            userId,
            error: error.message,
            response: error.response?.data
        });

        // Return error response
        res.status(500).json({
            success: false,
            error: 'Failed to sync books to external API',
            details: error.response?.data || error.message
        });
    }
});

app.post('/webhook', express.json(), (req, res) => {
    console.log('Webhook event:', JSON.stringify(req.body, null, 2));

    const events = req.body.events;
    
    events.forEach(event => {
        console.log('Event Type:', event.type);
        
        if (event.type === 'message') {
            console.log('Message Type:', event.message.type);
            console.log('Message Text:', event.message.text);
            console.log('User ID:', event.source.userId);
            console.log('Timestamp:', new Date(event.timestamp));
        }
    });

    res.sendStatus(200);
});

app.get('/api/check-login', async (req, res) => {
    const lineUserId = req.query.lineUserId;

    if (!lineUserId) {
        return res.status(400).json({ error: 'lineUserId is required' });
    }

    try {
        const user = await prisma.user.findUnique({
            where: { user_line_id: lineUserId }
        });

        if (!user) {
            return res.json({ microsoftLoggedIn: false });
        }

        // ตรวจสอบว่า email ลงท้ายด้วย @kmutt.ac.th และไม่ใช่ email placeholder
        if (user.email && user.email.endsWith('@kmutt.ac.th')) {
            return res.json({ microsoftLoggedIn: true });
        } else {
            return res.json({ microsoftLoggedIn: false });
        }
    } catch (error) {
        console.error('Error checking login status:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.post('/api/logout', async (req, res) => {
    const { userId } = req.body;

    if (!userId) {
        return res.status(400).json({ error: 'userId is required' });
    }

    try {
        // ตรวจสอบว่ามีผู้ใช้ในฐานข้อมูลหรือไม่
        const user = await prisma.user.findUnique({
            where: { user_line_id: userId }
        });

        if (!user) {
            console.warn(`User ${userId} not found in database, proceeding with logout`);
        } else {
            // อัปเดต email เป็น placeholder
            await prisma.user.update({
                where: { user_line_id: userId },
                data: {
                    email: `logged_out_${userId}@example.com`
                }
            });
            console.log(`Updated email to placeholder for user ${userId}`);
        }

        // ลบเซสชัน
        await new Promise((resolve, reject) => {
            req.session.destroy((err) => {
                if (err) {
                    console.error(`Error destroying session for user ${userId}:`, err);
                    reject(err);
                } else {
                    console.log(`Session destroyed for user ${userId}`);
                    resolve();
                }
            });
        });

        // เคลียร์ข้อมูลใน global
        if (global.verifiedBooks[userId]) {
            delete global.verifiedBooks[userId];
        }
        if (global.lastActivityTime[userId]) {
            delete global.lastActivityTime[userId];
        }

        res.json({ success: true, message: 'Logged out successfully' });
    } catch (error) {
        console.error('Error during logout:', error);
        res.status(500).json({ error: `Logout failed: ${error.message}` });
    }
});

app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));