import * as fs from 'fs';
import PDFParser from 'pdf-parse';
import axios from 'axios';
const {PDFLoader}  = require("langchain/document_loaders/fs/pdf");
const {RecursiveCharacterTextSplitter} = require("langchain/text_splitter");
const { OpenAIEmbeddings } =   require("langchain/embeddings/openai");
const  { Document } = require("langchain/document");
import * as path from 'path'; 
import { OpenAI } from "langchain/llms/openai";
import { PineconeStore } from "langchain/vectorstores/pinecone";
import { Pinecone } from "@pinecone-database/pinecone";
import * as dotenv from "dotenv";
import { VectorDBQAChain } from "langchain/chains";
const { CheerioWebBaseLoader }= require("langchain/document_loaders/web/cheerio");
import cheerio from 'cheerio';
dotenv.config();


const pinecone = new Pinecone();
console.log(process.env.PINECONE_INDEX)
const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX);
function removeHtmlAndCss(content: string): string {
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

function createChunks(content: string, chunkSize: number): string[] {
  // Split content into chunks of specified size
  const regex = new RegExp(`.{1,${chunkSize}}`, 'g');
  return content.match(regex) || [];
}

export async function fetchWikiPage(url: string): Promise<string> {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    let content = $('#bodyContent').text(); 
    let cn = removeHtmlAndCss(content.trim())
    const tempdocs  = createChunks(cn,1000)
    const chunk_text =  await splitDocsWiki(tempdocs)
    const vectorStore =  await PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
      pineconeIndex
    });
    return new Promise(async(resolve, reject) => { 
      resolve("sucesss");
      })
  } catch (error) {
    console.error('Error fetching Wikipedia page:', error);
    return null;
  }
  


  // const vectorStore =  await PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
  //   pineconeIndex
  // });

  
}

async function splitDocs(docs){
  console.log(docs)
  const splitter = RecursiveCharacterTextSplitter.fromLanguage("js",{
    chunkSize: 500,
    chunkOverlap:50
  });
  //  let spliter_text = ''
  //  for(let i=0;i<docs.length;i++){
  //   spliter_text+=docs[i].pageContent
    
  //  }
  let docOutput = []
  for(let i=0;i<docs.length;i++){
    await splitter.splitDocuments([
      docOutput.push(new Document({ pageContent:docs[i].pageContent.replace('\t','')  }))
    ]);
  }
  console.log("test")

  return docOutput
}

async function splitDocsWiki(docs){
  console.log(docs)
  
  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 500,
    chunkOverlap:50
  });
  //  let spliter_text = ''
  //  for(let i=0;i<docs.length;i++){
  //   spliter_text+=docs[i].pageContent
    
  //  }
  let docOutput = []
  for(let i=0;i<docs.length;i++){
    await splitter.splitDocuments([
      docOutput.push(new Document({ pageContent:docs[i]  }))
    ]);
  }
  console.log("test")

  return docOutput
}

export async function extractTextFromPDF(pdfPath: string): Promise<string> {
    const pdfBuffer: Buffer = fs.readFileSync(pdfPath);
    const dataBuffer: Buffer = Buffer.from(pdfBuffer);
    const loader = new PDFLoader(pdfPath)
    const doc = await loader.load(pdfPath)
    const chunk_text =  await splitDocs(doc)
    
    const vectorStore =  await PineconeStore.fromDocuments(chunk_text, new OpenAIEmbeddings(), {
          pineconeIndex
      });
   
    return new Promise(async(resolve, reject) => { 
      resolve("sucesss");
    })
}

export async function chatResponse(text:string): Promise<string> {
  const pinecone = new Pinecone();
  let chatResponse:string = ''
  const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX);
  
  const vectorStore = await PineconeStore.fromExistingIndex(
    new OpenAIEmbeddings(),
    { pineconeIndex }
  );
  const model = new OpenAI();
  const chain = VectorDBQAChain.fromLLM(model, vectorStore, {
    k: 1,
  
    returnSourceDocuments: true,
  });
  const instructions = `
  You are a Expert Developer and Data Analyst. 
  you have German Data and Script tutorial in the Storage.  
  Analysize the question and give the perfact answer based on the question,
  if question related to German History give answer from German History Data and if the question is asking for any script or code with relation to german history data then  your response should have the code with German history data`

  const response = await chain.call({ query: instructions+"\nQuestion: '"+text,top_k: 5000 });
  if(response.text){
    chatResponse = response.text
   
  }
  return new Promise<string>((resolve) => { 
      resolve(chatResponse);
  });
}
//'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'

//pdtest5455