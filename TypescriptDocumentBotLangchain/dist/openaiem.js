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
exports.chatResponse = exports.extractTextFromPDF = exports.fetchWikiPage = void 0;
const fs = __importStar(require("fs"));
const axios_1 = __importDefault(require("axios"));
const { PDFLoader } = require("langchain/document_loaders/fs/pdf");
const { RecursiveCharacterTextSplitter } = require("langchain/text_splitter");
const { OpenAIEmbeddings } = require("langchain/embeddings/openai");
const { Document } = require("langchain/document");
const openai_1 = require("langchain/llms/openai");
const pinecone_1 = require("langchain/vectorstores/pinecone");
const pinecone_2 = require("@pinecone-database/pinecone");
const dotenv = __importStar(require("dotenv"));
const chains_1 = require("langchain/chains");
const { CheerioWebBaseLoader } = require("langchain/document_loaders/web/cheerio");
const cheerio_1 = __importDefault(require("cheerio"));
dotenv.config();
const pinecone = new pinecone_2.Pinecone();
console.log(process.env.PINECONE_INDEX);
const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX);
function removeHtmlAndCss(content) {
    // Remove HTML tags and CSS styles
    return content.replace(/<style([\s\S]*?)<\/style>/gi, '')
        .replace(/<script([\s\S]*?)<\/script>/gi, '')
        .replace(/<\/div>/ig, '\n')
        .replace(/<\/li>/ig, '\n')
        .replace(/<li>/ig, '  *  ')
        .replace(/<\/ul>/ig, '\n')
        .replace(/<\/p>/ig, '\n')
        .replace(/<br\s*[\/]?>/gi, '\n')
        .replace(/<[^>]+>/ig, '');
}
function createChunks(content, chunkSize) {
    // Split content into chunks of specified size
    const regex = new RegExp(`.{1,${chunkSize}}`, 'g');
    return content.match(regex) || [];
}
function fetchWikiPage(url) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield axios_1.default.get(url);
            const $ = cheerio_1.default.load(response.data);
            let content = $('#bodyContent').text();
            let cn = removeHtmlAndCss(content.trim());
            const tempdocs = createChunks(cn, 1000);
            const chunk_text = yield splitDocsWiki(tempdocs);
            const vectorStore = yield pinecone_1.PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
                pineconeIndex
            });
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                resolve("sucesss");
            }));
        }
        catch (error) {
            console.error('Error fetching Wikipedia page:', error);
            return null;
        }
        // const vectorStore =  await PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
        //   pineconeIndex
        // });
    });
}
exports.fetchWikiPage = fetchWikiPage;
function splitDocs(docs) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log(docs);
        const splitter = RecursiveCharacterTextSplitter.fromLanguage("js", {
            chunkSize: 500,
            chunkOverlap: 50
        });
        //  let spliter_text = ''
        //  for(let i=0;i<docs.length;i++){
        //   spliter_text+=docs[i].pageContent
        //  }
        let docOutput = [];
        for (let i = 0; i < docs.length; i++) {
            yield splitter.splitDocuments([
                docOutput.push(new Document({ pageContent: docs[i].pageContent.replace('\t', '') }))
            ]);
        }
        console.log("test");
        return docOutput;
    });
}
function splitDocsWiki(docs) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log(docs);
        const splitter = new RecursiveCharacterTextSplitter({
            chunkSize: 500,
            chunkOverlap: 50
        });
        //  let spliter_text = ''
        //  for(let i=0;i<docs.length;i++){
        //   spliter_text+=docs[i].pageContent
        //  }
        let docOutput = [];
        for (let i = 0; i < docs.length; i++) {
            yield splitter.splitDocuments([
                docOutput.push(new Document({ pageContent: docs[i] }))
            ]);
        }
        console.log("test");
        return docOutput;
    });
}
function extractTextFromPDF(pdfPath) {
    return __awaiter(this, void 0, void 0, function* () {
        const pdfBuffer = fs.readFileSync(pdfPath);
        const dataBuffer = Buffer.from(pdfBuffer);
        const loader = new PDFLoader(pdfPath);
        const doc = yield loader.load(pdfPath);
        const chunk_text = yield splitDocs(doc);
        const vectorStore = yield pinecone_1.PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
            pineconeIndex
        });
        return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
            resolve("sucesss");
        }));
    });
}
exports.extractTextFromPDF = extractTextFromPDF;
function chatResponse(text) {
    return __awaiter(this, void 0, void 0, function* () {
        const pinecone = new pinecone_2.Pinecone();
        let chatResponse = '';
        const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX);
        const vectorStore = yield pinecone_1.PineconeStore.fromExistingIndex(new OpenAIEmbeddings(), { pineconeIndex });
        const model = new openai_1.OpenAI();
        const chain = chains_1.VectorDBQAChain.fromLLM(model, vectorStore, {
            k: 1,
            returnSourceDocuments: true,
        });
        const instructions = `
  You are a Expert Developer and Data Analyst. 
  you have German Data and Script tutorial in the Storage.  
  Analysize the question and give the perfact answer based on the question,
  if question related to German History give answer from German History Data and if the question is asking for any script or code with relation to german history data then  your response should have the code with German history data`;
        const response = yield chain.call({ query: instructions + "\nQuestion: '" + text, top_k: 5000 });
        if (response.text) {
            chatResponse = response.text;
        }
        return new Promise((resolve) => {
            resolve(chatResponse);
        });
    });
}
exports.chatResponse = chatResponse;
//'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'
//pdtest5455
