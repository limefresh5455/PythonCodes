"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv = __importStar(require("dotenv"));
const openaiem_1 = require("./openaiem");
const path_1 = __importDefault(require("path"));
dotenv.config();
const app = (0, express_1.default)();
const port = 5050;
app.listen(port, () => {
    console.log(`API listening on http://localhost:${port}`);
});
app.get('/', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const indexPath = path_1.default.join(__dirname, 'index.html');
    var dirname = __dirname.split('/');
    dirname.pop();
    res.sendFile(dirname.join('/') + '/src/index.html');
}));
app.get('/pdftovector', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    console.log("test");
    var dirname = __dirname.split('/');
    dirname.pop();
    console.log(dirname.join('/') + '/src/files/Web_Development_with_Node_Express.pdf');
    const ds = yield (0, openaiem_1.extractTextFromPDF)(dirname.join('/') + '/src/files/Web_Development_with_Node_Express.pdf');
    res.send("Hello");
}));
app.get('/wikitovector', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const wikidocs = yield (0, openaiem_1.fetchWikiPage)('https://en.wikipedia.org/wiki/History_of_Germany');
    // var dirname = __dirname.split('/');
    // dirname.pop();
    // console.log(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
    // const ds:string = await extractTextFromPDF(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
    // res.send("Hello");
    return "Hello";
}));
//https://en.wikipedia.org/wiki/History_of_Germany
app.get('/api/chat', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const messageParam = req.query.message;
        // Check if messageParam is a string or ParsedQs type
        let message = '';
        if (typeof messageParam === 'string') {
            // If it's a string, use it directly
            message = messageParam;
        }
        else if (Array.isArray(messageParam) && messageParam.length > 0 && typeof messageParam[0] === 'string') {
            // If it's an array, use the first element if it's a string
            message = messageParam[0];
        }
        else if (typeof messageParam === 'object' && messageParam !== null) {
            // If it's an object (ParsedQs), extract the first property's value if it's a string
            const keys = Object.keys(messageParam);
            if (keys.length > 0 && typeof messageParam[keys[0]] === 'string') {
                message = messageParam[keys[0]];
            }
        }
        const decodedString = decodeURIComponent(message);
        console.log(decodedString);
        const response = yield (0, openaiem_1.chatResponse)(decodedString);
        res.end(response);
        //res.send(response)
        //res.json({ response });
        //return response
    }
    catch (error) {
        console.error('Error processing message:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}));
